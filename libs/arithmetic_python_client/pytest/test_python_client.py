import time

from arithmetic_python_client.python_client import PythonClient


def test_create_connect_channel_timeout() -> None:
    NON_EXISTING_ADDRESS: str = "[::]:123456"
    TIMEOUT: float = 1.0
    inactive_client: PythonClient = PythonClient()

    start_time = time.time()
    result = inactive_client._create_connect_channel(address_with_port=NON_EXISTING_ADDRESS, timeout=TIMEOUT)
    end_time = time.time()

    assert result is None
    assert (end_time - start_time) > TIMEOUT
