import grpc
import logging

from arithmetic_python_client.python_client import PythonClient

from arithmetic_proto import average_pb2_grpc as average_grpc
from arithmetic_proto import average_pb2 as average_proto
from typing import Generator, List


class AverageClient(PythonClient[average_grpc.AverageServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> average_grpc.AverageServiceStub:
        return average_grpc.AverageServiceStub(channel)

    @staticmethod
    def _get_generator(numbers: List[int]) -> Generator[average_proto.AverageRequest, None, None]:
        for number in numbers:
            logging.info(f"Adding {number} into computation")
            request = average_proto.AverageRequest(number=number)
            yield request

    # Note: For synchronous gRPC, client-side streaming gRPC call is blocking
    # So if you want to add numbers over time instead of adding them as an entire list
    # in one go you would need the asynchronous gRPC API,
    # See https://github.com/grpc/grpc/blob/v1.46.3/examples/python/route_guide/asyncio_route_guide_client.py
    def average(self, numbers: List[int]) -> float:
        if not self.is_grpc_active():
            return False

        @PythonClient.return_none_if_exception_caught
        def attempt_average() -> float:
            response = self._stub.Average(self._get_generator(numbers=numbers))
            return response.answer

        return attempt_average()
