import math
import pytest
import subprocess
import time

from arithmetic_python_client import PerformPrimeNumberDecompositionClient

from typing import List, Tuple


@pytest.mark.parametrize("input, answer", [(0, []), (999, [3, 3, 3, 37]), (3125, [5, 5, 5, 5, 5])])
def test_prime_normal_operations(running_arithmetic_server: subprocess.Popen,
                                 open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int],
                                                                     List[bool]], input: int,
                                 answer: List[int]) -> None:
    client, output, decomposition_completed = open_configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=input) is True
    assert client.is_processing() is True
    client.wait_till_completion()
    assert len(decomposition_completed) == 1 and decomposition_completed[0] is True
    assert output == answer


def test_prime_client_cancels(
        running_arithmetic_server: subprocess.Popen,
        open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]]) -> None:
    client, _, decomposition_completed = open_configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is True
    assert client.is_processing() is True
    time.sleep(0.25)
    client.cancel()
    client.wait_till_completion()
    assert len(decomposition_completed) == 1 and decomposition_completed[0] is False


def test_prime_server_cancels(
        running_arithmetic_server: subprocess.Popen,
        open_configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]]) -> None:
    client, _, decomposition_completed = open_configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is True
    assert client.is_processing() is True
    time.sleep(0.25)
    running_arithmetic_server.terminate()
    client.wait_till_completion()
    assert len(decomposition_completed) == 1 and decomposition_completed[0] is False


def test_prime_server_not_running(
        configured_prime_client: Tuple[PerformPrimeNumberDecompositionClient, List[int], List[bool]]) -> None:
    client, output, decomposition_completed = configured_prime_client
    assert client.is_processing() is False
    assert client.perform_prime_number_decomposition(number=math.factorial(10)) is False
    assert client.is_processing() is False
    assert len(decomposition_completed) == 0
    assert len(output) == 0
    client.wait_till_completion()
    assert len(decomposition_completed) == 0
    assert len(output) == 0
