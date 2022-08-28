import pytest
import time

from testing_helpers import ArithmeticServerProcess, ConfiguredMaxClient

from typing import List, Tuple


def get_long_input_sequence_with_expected_response() -> List[Tuple[int, bool]]:
    return [(i, True) for i in range(100000)]


@pytest.mark.parametrize(
    "input_sequence_with_expected_response",
    [[], [(0, True), (0, False),
          (0, False)], [(-1, True), (0, True), (10, True), (10, False), (80, True),
                        (88, True)], [(88, True), (80, False), (10, False), (10, False), (0, False), (-1, False)]])
def test_max_normal_operations(running_arithmetic_server: ArithmeticServerProcess,
                               open_configured_max_client: ConfiguredMaxClient,
                               input_sequence_with_expected_response: List[Tuple[int, bool]]) -> None:
    client, expect_success_event, input_generator = open_configured_max_client
    assert client.max(input_iterable=input_generator(input_sequence_with_expected_response)) is True
    assert client.is_processing() is True
    client.wait_till_completion()
    assert expect_success_event.is_set()


def test_max_client_cancels(running_arithmetic_server: ArithmeticServerProcess,
                            open_configured_max_client: ConfiguredMaxClient) -> None:
    client, expect_success_event, input_generator = open_configured_max_client
    assert client.max(input_iterable=input_generator(get_long_input_sequence_with_expected_response())) is True
    assert client.is_processing() is True
    time.sleep(0.05)
    client.cancel()
    assert client.is_processing() is False
    client.wait_till_completion()
    assert not expect_success_event.is_set()


def test_max_server_cancels(running_arithmetic_server: ArithmeticServerProcess,
                            open_configured_max_client: ConfiguredMaxClient) -> None:
    client, expect_success_event, input_generator = open_configured_max_client
    assert client.is_processing() is False
    assert client.max(input_iterable=input_generator(get_long_input_sequence_with_expected_response())) is True
    assert client.is_processing() is True
    time.sleep(0.05)
    running_arithmetic_server.kill()
    client.wait_till_completion()
    assert not expect_success_event.is_set()


def test_max_server_not_running(running_arithmetic_server: ArithmeticServerProcess,
                                open_configured_max_client: ConfiguredMaxClient) -> None:
    client, expect_success_event, input_generator = open_configured_max_client
    running_arithmetic_server.kill()
    time.sleep(0.25)
    assert client.is_grpc_active() is False
    assert client.is_processing() is False
    # Client will attempt to perform service and realise that it is not possible to do so but cannot not complete the task
    assert client.max(input_iterable=input_generator(get_long_input_sequence_with_expected_response())) is True
    client.wait_till_completion()
    assert not expect_success_event.is_set()


def test_max_client_not_open(running_arithmetic_server: ArithmeticServerProcess,
                             configured_max_client: ConfiguredMaxClient) -> None:
    client, expect_success_event, input_generator = configured_max_client
    assert client.is_grpc_active() is False
    assert client.is_processing() is False
    assert client.max(input_iterable=input_generator(get_long_input_sequence_with_expected_response())) is False
    assert client.is_processing() is False
    assert not expect_success_event.is_set()
    client.wait_till_completion()
    assert not expect_success_event.is_set()
