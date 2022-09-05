import pytest
import time

from testing_helpers import ArithmeticServerProcess

from arithmetic_python_client import SumClient
from threading import Thread


@pytest.mark.parametrize("number_1, number_2, answer", [(0, 0, 0), (-1, -2, -3), (1, 2, 3), (1, -2, -1), (-1, 2, 1)])
class TestSumNormalOperations:
    def test_sum_normal_operations_blocking(self, running_arithmetic_server: ArithmeticServerProcess,
                                            open_sum_client: SumClient, number_1: int, number_2: int,
                                            answer: int) -> None:
        assert open_sum_client.sum(number_1=number_1, number_2=number_2) == answer

    def test_sum_normal_operations_non_blocking(self, running_arithmetic_server: ArithmeticServerProcess,
                                                open_sum_client: SumClient, number_1: int, number_2: int,
                                                answer: int) -> None:
        future = open_sum_client.sum_non_blocking(number_1=number_1, number_2=number_2)
        assert future is not None
        assert not future.done()
        assert future.wait_till_completion() == answer
        assert future.done()
        assert future.wait_till_completion() == answer
        assert future.cancel() is False


def test_sum_server_cancels(running_arithmetic_server: ArithmeticServerProcess, open_sum_client: SumClient) -> None:
    def terminate_server_with_delay() -> None:
        time.sleep(0.1)
        running_arithmetic_server.kill()

    server_termination_thread = Thread(target=terminate_server_with_delay, name="terminate average server with delay")
    server_termination_thread.start()
    output = open_sum_client.sum(number_1=0, number_2=0)
    server_termination_thread.join()

    assert output is None


def test_sum_non_blocking_server_cancels(running_arithmetic_server: ArithmeticServerProcess,
                                         open_sum_client: SumClient) -> None:
    def terminate_server_with_delay() -> None:
        time.sleep(0.1)
        running_arithmetic_server.kill()

    server_termination_thread = Thread(target=terminate_server_with_delay, name="terminate average server with delay")
    server_termination_thread.start()
    future = open_sum_client.sum_non_blocking(number_1=0, number_2=0)
    server_termination_thread.join()

    assert future.done()
    assert future.cancel() is False
    assert future.wait_till_completion() is None


def test_sum_non_blocking_client_cancel(running_arithmetic_server: ArithmeticServerProcess,
                                        open_sum_client: SumClient) -> None:
    future = open_sum_client.sum_non_blocking(number_1=0, number_2=0)
    assert future is not None
    assert future.done() is False
    assert future.cancel() is True
    assert future.wait_till_completion() is None
    assert future.done() is True
    assert future.cancel() is False


def test_sum_server_not_running(running_arithmetic_server: ArithmeticServerProcess, open_sum_client: SumClient) -> None:
    running_arithmetic_server.kill()
    time.sleep(0.25)
    assert open_sum_client.is_grpc_active() is False
    assert open_sum_client.sum(number_1=0, number_2=0) is None
    future = open_sum_client.sum_non_blocking(number_1=0, number_2=0)
    assert future is not None
    assert future.done() is True
    assert future.wait_till_completion() is None


def test_sum_client_not_open(running_arithmetic_server: ArithmeticServerProcess) -> None:
    client = SumClient()
    assert not client.is_grpc_active()
    assert client.sum(number_1=0, number_2=0) is None
    assert client.sum_non_blocking(number_1=0, number_2=0) is None
