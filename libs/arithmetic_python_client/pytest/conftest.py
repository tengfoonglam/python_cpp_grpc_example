import pytest
import subprocess

from typing import Generator

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
def open_prime_client() -> PerformPrimeNumberDecompositionClient:
    client = PerformPrimeNumberDecompositionClient()
    client.open()
    yield client
    client.close()


@pytest.fixture
def open_sum_client() -> SumClient:
    client = SumClient()
    client.open()
    yield client
    client.close()
