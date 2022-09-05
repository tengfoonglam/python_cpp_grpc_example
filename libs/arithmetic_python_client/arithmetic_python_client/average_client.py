import grpc
import logging

from arithmetic_python_client.future import Future
from arithmetic_python_client.python_client import PythonClient

from arithmetic_proto import average_pb2_grpc as average_grpc
from arithmetic_proto import average_pb2 as average_proto
from threading import Event
from typing import Callable, Generator, Iterable, Optional


class AverageClient(PythonClient[average_grpc.AverageServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> average_grpc.AverageServiceStub:
        return average_grpc.AverageServiceStub(channel)

    def __init__(self) -> None:
        super().__init__()
        self._completion_event: Event = Event()
        self._input_function: Callable = lambda: None

    @staticmethod
    def _get_request_generator(input_iterable: Iterable[int]) -> Generator[average_proto.AverageRequest, None, None]:
        for number in input_iterable:
            logging.info(f"Adding {number} into average computation")
            request = average_proto.AverageRequest(number=number)
            yield request

    def average(self, input_iterable: Iterable[int]) -> Optional[float]:
        if not self._channel_and_stubs_initialized():
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_average() -> float:
            response = self._stub.Average(self._get_request_generator(input_iterable=input_iterable))
            return response.answer

        return attempt_average()

    def average_non_blocking(self, input_iterable: Iterable[int]) -> Optional[Future[float]]:
        if not self._channel_and_stubs_initialized():
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_average_non_blocking() -> Future[float]:
            grpc_future = self._stub.Average.future(self._get_request_generator(input_iterable=input_iterable))
            return Future[float](grpc_future=grpc_future, conversion_func=lambda response: response.answer)

        return attempt_average_non_blocking()
