import math
import pytest
import subprocess
import time

from arithmetic_python_client import AverageClient

from threading import Thread
from typing import List


@pytest.mark.parametrize("numbers_list,answer", [([], 0.0), ([1], 1.0), ([-1, 0, 1], 0.0), ([1, 4], 2.5),
                                                 ([5, 10, 15, 20, 25], 15.0), ([-5, -10, -15, -20, -25], -15.0)])
def test_average_normal_operations(running_arithmetic_server: subprocess.Popen, open_average_client: AverageClient,
                                   numbers_list: List[float], answer: float) -> None:
    output = open_average_client.average(input_iterable=numbers_list)
    assert output is not None
    if output is not None:
        assert math.isclose(output, answer)


def test_average_server_cancels(running_arithmetic_server: subprocess.Popen,
                                open_average_client: AverageClient) -> None:
    def terminate_server_with_delay() -> None:
        time.sleep(0.2)
        running_arithmetic_server.terminate()

    server_termination_thread = Thread(target=terminate_server_with_delay, name="terminate average server with delay")

    server_termination_thread.start()
    output = open_average_client.average(input_iterable=list(range(1000000)))
    server_termination_thread.join()

    assert output is None
