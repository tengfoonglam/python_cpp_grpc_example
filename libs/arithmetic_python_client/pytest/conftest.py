import pytest
import subprocess

from dataclasses import dataclass
from threading import Event
from typing import Callable, Generator, List, Optional, Tuple

from arithmetic_python_client import AverageClient, MaxClient, PerformPrimeNumberDecompositionClient, SumClient

ARITHMETIC_SERVER_PATH = "../arithmetic_grpc/build/apps/arithmetic_server"


@pytest.fixture
def running_arithmetic_server() -> Generator[subprocess.Popen, None, None]:
    process = subprocess.Popen(args=[ARITHMETIC_SERVER_PATH])
    yield process
    process.terminate()


@pytest.fixture
def open_average_client() -> AverageClient:
    client = AverageClient()
    assert client.open() is True
    yield client
    assert client.close() is True


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
    configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]
) -> Generator[Tuple[PerformPrimeNumberDecompositionClient, List[int], Event], None, None]:
    client, output, decomposition_completed = configured_prime_client
    assert client.open() is True
    yield client, output, decomposition_completed
    assert client.close() is True


@pytest.fixture
def open_sum_client() -> Generator[SumClient, None, None]:
    client = SumClient()
    assert client.open() is True
    yield client
    assert client.close() is True


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
    configured_max_client: Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]], Generator[int, None, None]]]
) -> Generator[Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]], Generator[int, None, None]]], None, None]:
    client, expect_success_event, input_generator = configured_max_client
    assert client.open() is True
    yield client, expect_success_event, input_generator
    assert client.close() is True
