import pytest
import subprocess

from threading import Event
from typing import Generator, List, Tuple

from arithmetic_python_client import AverageClient, MaxClient, PerformPrimeNumberDecompositionClient, SumClient


@pytest.fixture
def running_arithmetic_server() -> Generator[subprocess.Popen, None, None]:
    process = subprocess.Popen(args=["../arithmetic_grpc/build/apps/arithmetic_server"])
    yield process
    process.terminate()


@pytest.fixture
def open_average_client() -> AverageClient:
    client = AverageClient()
    assert client.open() is True
    yield client
    assert client.close() is True


@pytest.fixture
def open_max_client() -> MaxClient:
    client = MaxClient()
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
    configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]]
) -> Generator[Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]], None, None]:
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
