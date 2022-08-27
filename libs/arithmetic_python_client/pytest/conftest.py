import os
import pytest
import subprocess

from dataclasses import dataclass
from threading import Event
from typing import Callable, Generator, List, Optional, Tuple

from arithmetic_python_client import AverageClient, MaxClient, PerformPrimeNumberDecompositionClient, SumClient

ARITHMETIC_EXECUTABLE_NAME = "arithmetic_server"
ARITHMETIC_SERVER_PATH = f"../arithmetic_grpc/build/apps/{ARITHMETIC_EXECUTABLE_NAME}"


@pytest.fixture
def running_arithmetic_server(request: pytest.FixtureRequest) -> subprocess.Popen:

    # We ensure all arithmetic server executables are terminated before/after a test because they could affect current/downstream test results

    def kill_all_arithmetic_servers() -> None:
        os.system(
            f"for pid in $(ps -aux | grep \" + {ARITHMETIC_EXECUTABLE_NAME} \" | awk '{{print $2}}'); do kill -9 $pid; done"
        )

    kill_all_arithmetic_servers()
    process = subprocess.Popen(args=[ARITHMETIC_SERVER_PATH])

    def cleanup() -> None:
        process.terminate()
        kill_all_arithmetic_servers()

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
def configured_prime_client() -> Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]:
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
def open_configured_prime_client(
    request: pytest.FixtureRequest, configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int],
                                                                   Event]
) -> Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]:
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


@pytest.fixture
def configured_max_client() -> Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]], Generator[int, None, None]]]:

    client = MaxClient()

    @dataclass
    class Result:
        current_number: Optional[int] = None

    expect_success_event = Event()
    ready_to_send_next_number_event = Event()
    expect_a_response_event = Event()
    result = Result()

    def input_generator(input_sequence_with_expected_response: List[Tuple[int, bool]]) -> Generator[int, None, None]:
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
def open_configured_max_client(
    request: pytest.FixtureRequest, configured_max_client: Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]],
                                                                                            Generator[int, None, None]]]
) -> Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]], Generator[int, None, None]]]:
    client, expect_success_event, input_generator = configured_max_client
    assert client.open() is True

    def cleanup() -> None:
        assert client.close() is True

    request.addfinalizer(cleanup)
    return client, expect_success_event, input_generator
