import math
import pytest
import time

from testing_helpers import ArithmeticServerProcess

from arithmetic_python_client import AverageClient

from threading import Thread
from typing import List


@pytest.mark.parametrize("numbers_list,answer", [([], 0.0), ([1], 1.0), ([-1, 0, 1], 0.0), ([1, 4], 2.5),
                                                 ([5, 10, 15, 20, 25], 15.0), ([-5, -10, -15, -20, -25], -15.0)])
class TestAverageNormalOperations:
    def test_average_normal_operations(self, running_arithmetic_server: ArithmeticServerProcess,
                                       open_average_client: AverageClient, numbers_list: List[float],
                                       answer: float) -> None:
        output = open_average_client.average(input_iterable=numbers_list)
        assert output is not None
        if output is not None:
            assert math.isclose(output, answer)

    def test_average_normal_operations_non_blocking(self, running_arithmetic_server: ArithmeticServerProcess,
                                                    open_average_client: AverageClient, numbers_list: List[float],
                                                    answer: float) -> None:
        future = open_average_client.average_non_blocking(input_iterable=numbers_list)
        assert future is not None
        assert not future.done()
        assert future.wait_for_result() == answer
        assert future.done()
        assert future.wait_for_result() == answer
        assert future.cancel() is False


def test_average_non_blocking_future_timeout(running_arithmetic_server: ArithmeticServerProcess,
                                             open_average_client: AverageClient) -> None:
    numbers_to_average = list(range(1000))
    future = open_average_client.average_non_blocking(input_iterable=numbers_to_average)
    assert future.done() is False
    assert future.wait_for_result(timeout=0.0) is None
    assert future.done() is False
    assert math.isclose(future.wait_for_result(), sum(numbers_to_average) / len(numbers_to_average))
    assert future.done() is True
    assert future.cancel() is False


def test_sum_non_blocking_client_cancel(running_arithmetic_server: ArithmeticServerProcess,
                                        open_average_client: AverageClient) -> None:
    future = open_average_client.average_non_blocking(input_iterable=list(range(1000000)))
    assert future is not None
    assert future.done() is False
    assert future.cancel() is True
    assert future.wait_for_result() is None
    assert future.done() is True
    assert future.cancel() is False


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


def test_average_non_blocking_server_cancels(running_arithmetic_server: ArithmeticServerProcess,
                                             open_average_client: AverageClient) -> None:
    def terminate_server_with_delay() -> None:
        time.sleep(0.2)
        running_arithmetic_server.kill()

    server_termination_thread = Thread(target=terminate_server_with_delay, name="terminate average server with delay")
    server_termination_thread.start()
    future = open_average_client.average_non_blocking(input_iterable=list(range(1000000)))
    server_termination_thread.join()
    assert future is not None
    assert future.done()
    assert future.cancel() is False
    assert future.wait_for_result() is None


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
    assert client.average_non_blocking(input_iterable=list(range(1000000))) is None
