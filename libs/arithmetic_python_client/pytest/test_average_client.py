import math
import pytest
import time

from .testing_helpers import ArithmeticServerProcess

from arithmetic_python_client import AverageClient

from threading import Thread
from typing import List


@pytest.mark.parametrize("numbers_list,answer", [([], 0.0), ([1], 1.0), ([-1, 0, 1], 0.0), ([1, 4], 2.5),
                                                 ([5, 10, 15, 20, 25], 15.0), ([-5, -10, -15, -20, -25], -15.0)])
def test_average_normal_operations(running_arithmetic_server: ArithmeticServerProcess,
                                   open_average_client: AverageClient, numbers_list: List[float],
                                   answer: float) -> None:
    output = open_average_client.average(input_iterable=numbers_list)
    assert output is not None
    if output is not None:
        assert math.isclose(output, answer)


def test_average_server_cancels(running_arithmetic_server: ArithmeticServerProcess,
                                open_average_client: AverageClient) -> None:
    def terminate_server_with_delay() -> None:
        time.sleep(0.2)
        running_arithmetic_server.kill()

    server_termination_thread = Thread(target=terminate_server_with_delay, name="terminate average server with delay")
    server_termination_thread.start()
    output = open_average_client.average(input_iterable=list(range(1000000)))
    server_termination_thread.join()

    assert output is None


def test_average_server_not_running(running_arithmetic_server: ArithmeticServerProcess,
                                    open_average_client: AverageClient) -> None:
    running_arithmetic_server.kill()
    time.sleep(0.2)
    assert open_average_client.is_grpc_active() is False
    assert open_average_client.average(input_iterable=list(range(1000000))) is None


def test_average_client_not_open(running_arithmetic_server: ArithmeticServerProcess) -> None:
    client = AverageClient()
    assert client.is_grpc_active() is False
    assert client.average(input_iterable=list(range(1000000))) is None
