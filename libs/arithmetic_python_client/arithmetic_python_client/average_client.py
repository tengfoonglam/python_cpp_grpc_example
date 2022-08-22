import grpc
import logging

from arithmetic_python_client.python_client import PythonClient

from arithmetic_proto import average_pb2_grpc as average_grpc
from arithmetic_proto import average_pb2 as average_proto
from threading import Event
from typing import Callable, Generator, List, Optional


class AverageClient(PythonClient[average_grpc.AverageServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> average_grpc.AverageServiceStub:
        return average_grpc.AverageServiceStub(channel)

    def __init__(self) -> None:
        super().__init__()
        self._completion_event: Event = Event()
        self._input_function: Callable = lambda: None

    @staticmethod
    def _get_request_generator(
            input_generator: Generator[int, None, None]) -> Generator[average_proto.AverageRequest, None, None]:
        for number in input_generator:
            logging.info(f"Adding {number} into average computation")
            request = average_proto.AverageRequest(number=number)
            yield request

    def average(self, input_generator: Generator[int, None, None]) -> Optional[float]:
        if not self._channel_and_stubs_initialized():
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_average() -> float:
            response = self._stub.Average(self._get_request_generator(input_generator=input_generator))
            return response.answer

        return attempt_average()

    def average_list_of_numbers(self, numbers: List[int]) -> Optional[float]:
        return self.average(input_generator=(i for i in numbers))