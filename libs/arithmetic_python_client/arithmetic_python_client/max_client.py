import grpc
import logging

from arithmetic_python_client.prime_client import PythonClient

from arithmetic_proto import max_pb2_grpc as max_grpc
from arithmetic_proto import max_pb2 as max_proto
from typing import Generator, List, Optional


class MaxClient(PythonClient[max_grpc.MaxServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> max_grpc.MaxServiceStub:
        return max_grpc.MaxServiceStub(channel)

    @staticmethod
    def _get_generator(numbers: List[int]) -> Generator[max_proto.MaxRequest, None, None]:
        for number in numbers:
            logging.info(f"Adding {number} into max computation")
            request = max_proto.MaxRequest(number=number)
            yield request

    # Note: For synchronous bi-directional gRPC streaming, similar to client-side streaming,
    # the gRPC call is blocking so if you want to send numbers over time instead of sending them as an entire list
    # while receiving replies in real time you would need the asynchronous gRPC API,
    # See https://github.com/grpc/grpc/blob/v1.46.3/examples/python/route_guide/asyncio_route_guide_client.py
    def max(self, numbers: List[int]) -> Optional[int]:
        if not self.is_grpc_active():
            return None

        if len(numbers) == 0:
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_max() -> int:
            responses = self._stub.Max(self._get_generator(numbers=numbers))
            answer = None
            for response in responses:
                answer = response.max
                logging.info(f"Received max value from client: {answer}")
            if answer is not None:
                logging.info(f"Final max: {answer}")
            else:
                logging.info("Did not receive a max value, service could have been stopped/cancelled mid-way")
            return answer

        return attempt_max()
