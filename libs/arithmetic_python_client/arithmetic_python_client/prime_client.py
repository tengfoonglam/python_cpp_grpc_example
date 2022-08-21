import grpc

from arithmetic_python_client.python_client import PythonClient
from arithmetic_python_client.server_stream_handler import ServerStreamHandler

from arithmetic_proto import prime_pb2_grpc as prime_grpc
from arithmetic_proto import prime_pb2 as prime_proto
from typing import Callable


class PerformPrimeNumberDecompositionClient(PythonClient[prime_grpc.PerformPrimeNumberDecompositionServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> prime_grpc.PerformPrimeNumberDecompositionServiceStub:
        return prime_grpc.PerformPrimeNumberDecompositionServiceStub(channel)

    def __init__(self) -> None:
        super().__init__()
        self._stream_handler: ServerStreamHandler = ServerStreamHandler(
            stream_name="Perform prime number decomposition")
        self._stream_handler.set_initialize_stream_function(
            func=lambda request: self._stub.PerformPrimeNumberDecomposition(request=request))

    def set_new_response_callback(self, callback: Callable) -> None:
        self._stream_handler.set_new_response_callback(callback=lambda response: callback(factor=response.factor))

    def set_completed_callback(self, callback: Callable) -> None:
        self._stream_handler.set_completed_callback(callback=callback)

    def perform_prime_number_decomposition(self, number: int) -> bool:
        if not self._channel_and_stubs_initialized():
            return False
        self._stream_handler.set_generate_request_function(
            func=lambda: prime_proto.PerformPrimeNumberDecompositionRequest(number=number))
        return self._stream_handler.start()

    def is_processing(self) -> bool:
        return self._stream_handler.is_processing()

    def cancel(self) -> None:
        self._stream_handler.cancel()

    def wait_till_completion(self) -> None:
        self._stream_handler.wait_till_completion()

    def close(self) -> bool:
        self._stream_handler.close()
        return super().close()
