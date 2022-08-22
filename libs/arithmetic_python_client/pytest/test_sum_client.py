import pytest
import subprocess

from arithmetic_python_client import SumClient


@pytest.mark.parametrize("number_1, number_2, answer", [(0, 0, 0), (-1, -2, -3), (1, 2, 3), (1, -2, -1), (-1, 2, 1)])
def test_sum_normal_operations(running_arithmetic_server: subprocess.Popen, open_sum_client: SumClient, number_1: int,
                               number_2: int, answer: int) -> None:
    assert open_sum_client.sum(number_1=number_1, number_2=number_2) == answer


def test_sum_server_not_running() -> None:
    client = SumClient()
    assert client.sum(number_1=0, number_2=0) is None
