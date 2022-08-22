import pytest
import subprocess

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
    client.open()
    yield client
    client.close()


@pytest.fixture
def open_max_client() -> MaxClient:
    client = MaxClient()
    client.open()
    yield client
    client.close()


@pytest.fixture
def configured_prime_client() -> Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]]:
    client = PerformPrimeNumberDecompositionClient()

    decomposition_completed = []
    output = []

    def on_receive(factor: int) -> None:
        output.append(factor)

    def on_completion(success: bool) -> None:
        decomposition_completed.append(success)

    client.set_new_response_callback(callback=on_receive)
    client.set_completed_callback(callback=on_completion)

    return client, output, decomposition_completed


@pytest.fixture
def open_configured_prime_client(
    configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]]
) -> Generator[Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]], None, None]:
    client, output, decomposition_completed = configured_prime_client
    client.open()
    yield client, output, decomposition_completed
    client.close()


@pytest.fixture
def open_sum_client() -> Generator[SumClient, None, None]:
    client = SumClient()
    client.open()
    yield client
    client.close()
