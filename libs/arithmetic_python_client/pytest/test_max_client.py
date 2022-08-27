import pytest
import subprocess

from arithmetic_python_client import MaxClient

from threading import Event
from typing import Callable, Generator, List, Tuple


@pytest.mark.parametrize(
    "input_sequence_with_expected_response",
    [[], [(0, True), (0, False),
          (0, False)], [(-1, True), (0, True), (10, True), (10, False), (80, True),
                        (88, True)], [(88, True), (80, False), (10, False), (10, False), (0, False), (-1, False)]])
def test_max_normal_operations(running_arithmetic_server: subprocess.Popen,
                               open_configured_max_client: Tuple[MaxClient, Event, Callable[[List[Tuple[int, bool]]],
                                                                                            Generator[int, None,
                                                                                                      None]]],
                               input_sequence_with_expected_response: List[Tuple[int, bool]]) -> None:
    client, expect_success_event, input_generator = open_configured_max_client
    assert client.max(input_iterable=input_generator(input_sequence_with_expected_response)) is True
    assert client.is_processing() is True
    client.wait_till_completion()
    assert expect_success_event.is_set()


def test_max_server_cancels() -> None:
    pass


def test_max_client_cancels() -> None:
    pass


def test_max_server_not_running() -> None:
    pass


def test_max_client_not_open() -> None:
    pass
