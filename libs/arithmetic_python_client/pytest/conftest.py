import docker
import logging
import pytest
import _pytest
import subprocess
import threading
import time

from testing_helpers import ArithmeticServerProcess, ConfiguredMaxClient, ConfiguredPrimeClient, IntGenerator

from arithmetic_python_client import AverageClient, MaxClient, PerformPrimeNumberDecompositionClient, SumClient

from dataclasses import dataclass
from threading import Event
from typing import List, Optional, Tuple

ARITHMETIC_SERVER_IMAGE_NAME = "arithmetic_server"
DEFAULT_LOCAL_ARITHMETIC_SERVER_PATH = "../arithmetic_grpc/build/apps/arithmetic_server"


def pytest_addoption(parser: _pytest.config.argparsing.Parser) -> None:
    parser.addoption("--use-local-server",
                     action="store_true",
                     default=False,
                     help=f"Use local arithmetic server executable located at {DEFAULT_LOCAL_ARITHMETIC_SERVER_PATH}")
    parser.addoption("--server-path",
                     action="store",
                     default="",
                     help="Path of arithmetic server executable to be used for the pytests")


def pytest_configure(config: _pytest.config.Config) -> None:
    original_logging_level = logging.root.level
    logging.getLogger().setLevel(logging.INFO)

    pytest.server_path = ""
    if config.option.use_local_server:
        pytest.server_path = DEFAULT_LOCAL_ARITHMETIC_SERVER_PATH
        logging.info(f"Using default arithmetic server executable for testing: {pytest.server_path}")
    elif len(config.option.server_path) > 0:
        pytest.server_path = config.option.server_path
        logging.info(f"Using specified arithmetic server executable for testing: {pytest.server_path}")
    else:
        logging.info(f"Using dockerized arithmetic server named {ARITHMETIC_SERVER_IMAGE_NAME} for testing")

    logging.getLogger().setLevel(original_logging_level)


@pytest.fixture
def running_arithmetic_server(request: pytest.FixtureRequest) -> ArithmeticServerProcess:

    # We ensure all arithmetic server executables are terminated before/after a test because they could affect current/downstream test results

    if len(pytest.server_path) > 0:
        process = ArithmeticServerProcess(process=subprocess.Popen(args=[pytest.server_path]))
    else:
        process = ArithmeticServerProcess(process=docker.from_env().containers.run(
            image=ARITHMETIC_SERVER_IMAGE_NAME, init=True, detach=True, ports={'50051/tcp': 50051}))

    def cleanup() -> None:
        process.kill()

    request.addfinalizer(cleanup)

    return process


@pytest.fixture
def open_average_client(request: pytest.FixtureRequest) -> AverageClient:
    client = AverageClient()
    assert client.open() is True

    def cleanup() -> None:
        assert client.close() is True

    request.addfinalizer(cleanup)

    return client


@pytest.fixture
def configured_max_client() -> ConfiguredMaxClient:

    client = MaxClient()

    @dataclass
    class Result:
        current_number: Optional[int] = None

    expect_success_event = Event()
    ready_to_send_next_number_event = Event()
    expect_a_response_event = Event()
    result = Result()

    def input_generator(input_sequence_with_expected_response: List[Tuple[int, bool]]) -> IntGenerator:
        TIMEOUT = 0.5
        for number, expect_response in input_sequence_with_expected_response:
            ready_to_send_next_number_event.clear()
            expect_a_response_event.clear()
            result.current_number = number
            yield number
            if expect_response:
                response_received = ready_to_send_next_number_event.wait(TIMEOUT)
                assert response_received, "Waiting to send next max number but timed out while waiting for an expected response"
            assert expect_response == expect_a_response_event.is_set()

    def on_receive(max: int) -> None:
        expect_a_response_event.set()
        assert max == result.current_number
        ready_to_send_next_number_event.set()

    def on_completion(success: bool) -> None:
        if success:
            expect_success_event.set()

    client.set_new_response_callback(callback=on_receive)
    client.set_completed_callback(callback=on_completion)

    return client, expect_success_event, input_generator


@pytest.fixture
def open_configured_max_client(request: pytest.FixtureRequest,
                               configured_max_client: ConfiguredMaxClient) -> ConfiguredMaxClient:
    client, expect_success_event, input_generator = configured_max_client
    assert client.open() is True

    def cleanup() -> None:
        assert client.close() is True

    request.addfinalizer(cleanup)
    return client, expect_success_event, input_generator


@pytest.fixture
def configured_prime_client() -> ConfiguredPrimeClient:
    client = PerformPrimeNumberDecompositionClient()

    decomposition_success_event = Event()
    output = []

    def on_receive(factor: int) -> None:
        output.append(factor)

    def on_completion(success: bool) -> None:
        if success:
            decomposition_success_event.set()

    client.set_new_response_callback(callback=on_receive)
    client.set_completed_callback(callback=on_completion)

    return client, output, decomposition_success_event


@pytest.fixture
def open_configured_prime_client(request: pytest.FixtureRequest,
                                 configured_prime_client: ConfiguredPrimeClient) -> ConfiguredPrimeClient:
    client, output, decomposition_completed = configured_prime_client
    assert client.open() is True

    def cleanup() -> None:
        assert client.close() is True

    request.addfinalizer(cleanup)

    return client, output, decomposition_completed


@pytest.fixture
def open_sum_client(request: pytest.FixtureRequest) -> SumClient:
    client = SumClient()
    assert client.open() is True

    def cleanup() -> None:
        assert client.close() is True

    request.addfinalizer(cleanup)

    return client


@pytest.fixture(autouse=True)
def ensure_no_stray_threads(request: pytest.FixtureRequest) -> None:
    def cleanup() -> None:
        cleanup_success = False
        # It takes a while for channels and corresponding threads to be cleared by the garbage collector
        # This is because channel state is updated/polled every 0.2 seconds
        # Hence we retry a few times to cater for this
        # Refer to _channel.py file in the gRPC source code for more details
        for _ in range(3):
            thread_list = threading.enumerate()
            cleanup_success = (len(thread_list) == 1 and thread_list[0].name == "MainThread")
            time.sleep(0.2)
        assert cleanup_success

    request.addfinalizer(cleanup)
