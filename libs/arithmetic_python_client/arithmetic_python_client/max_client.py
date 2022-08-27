import grpc

from arithmetic_python_client.prime_client import PythonClient
from arithmetic_python_client.server_stream_handler import ServerStreamHandler

from arithmetic_proto import max_pb2_grpc as max_grpc
from arithmetic_proto import max_pb2 as max_proto
from typing import Callable, Generator, Iterable


class MaxClient(PythonClient[max_grpc.MaxServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> max_grpc.MaxServiceStub:
        return max_grpc.MaxServiceStub(channel)

    def __init__(self) -> None:
        super().__init__()
        self._stream_handler: ServerStreamHandler = ServerStreamHandler(stream_name="Max")
        self._stream_handler.set_initialize_stream_function(func=lambda request: self._stub.Max(request))

    def _get_request_generator(self, input_iterable: Iterable[int]) -> Generator[max_proto.MaxRequest, None, None]:
        for number in input_iterable:
            request = max_proto.MaxRequest(number=number)
            yield request

    def set_new_response_callback(self, callback: Callable) -> None:
        self._stream_handler.set_new_response_callback(callback=lambda response: callback(max=response.max))

    def set_completed_callback(self, callback: Callable) -> None:
        self._stream_handler.set_completed_callback(callback=callback)

    def is_processing(self) -> bool:
        return self._stream_handler.is_processing()

    def cancel(self) -> None:
        self._stream_handler.cancel()

    def wait_till_completion(self) -> None:
        self._stream_handler.wait_till_completion()

    def close(self) -> bool:
        self._stream_handler.close()
        return super().close()

    def max(self, input_iterable: Iterable[int]) -> bool:
        if not self._channel_and_stubs_initialized():
            return False
        self._stream_handler.set_generate_request_function(
            func=lambda: self._get_request_generator(input_iterable=input_iterable))
        return self._stream_handler.start()
