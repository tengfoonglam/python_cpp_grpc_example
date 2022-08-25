import math
import pytest
import subprocess
import time

from arithmetic_python_client import PerformPrimeNumberDecompositionClient

from threading import Event
from typing import List, Tuple


@pytest.mark.parametrize("input, answer", [(0, []), (999, [3, 3, 3, 37]), (3125, [5, 5, 5, 5, 5])])
def test_prime_normal_operations(running_arithmetic_server: subprocess.Popen,
                                 open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int],
                                                                     Event], input: int, answer: List[int]) -> None:
    client, output, decomposition_success_event = open_configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=input) is True
    assert client.is_processing() is True
    client.wait_till_completion()
    assert decomposition_success_event.is_set()
    assert output == answer


def test_prime_client_cancels(
        running_arithmetic_server: subprocess.Popen,
        open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]) -> None:
    client, _, decomposition_success_event = open_configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is True
    assert client.is_processing() is True
    time.sleep(0.25)
    client.cancel()
    client.wait_till_completion()
    assert not decomposition_success_event.is_set()


def test_prime_server_cancels(
        running_arithmetic_server: subprocess.Popen,
        open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]) -> None:
    client, _, decomposition_success_event = open_configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is True
    assert client.is_processing() is True
    time.sleep(0.25)
    running_arithmetic_server.terminate()
    client.wait_till_completion()
    assert not decomposition_success_event.is_set()


def test_prime_server_not_running(
        running_arithmetic_server: subprocess.Popen,
        open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]) -> None:
    client, output, decomposition_success_event = open_configured_prime_client
    running_arithmetic_server.terminate()
    time.sleep(0.25)
    assert client.is_grpc_active() is False
    assert client.is_processing() is False
    # Client will attempt to perform service and realise that it is not possible to do so and not complete the task
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is True
    client.wait_till_completion()
    assert len(output) == 0
    assert not decomposition_success_event.is_set()


def test_prime_client_not_open(
        running_arithmetic_server: subprocess.Popen,
        configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], Event]) -> None:
    client, output, decomposition_success_event = configured_prime_client
    assert client.is_grpc_active() is False
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is False
    assert client.is_processing() is False
    assert len(output) == 0
    assert not decomposition_success_event.is_set()
    client.wait_till_completion()
    assert len(output) == 0
    assert not decomposition_success_event.is_set()
