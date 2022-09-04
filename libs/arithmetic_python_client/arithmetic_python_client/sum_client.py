import grpc

from arithmetic_python_client.python_client import PythonClient
from arithmetic_python_client.future import Future

from arithmetic_proto import sum_pb2_grpc as sum_grpc
from arithmetic_proto import sum_pb2 as sum_proto
from typing import Optional


class SumClient(PythonClient[sum_grpc.SumServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> sum_grpc.SumServiceStub:
        return sum_grpc.SumServiceStub(channel)

    def sum(self, number_1: float, number_2: float) -> Optional[float]:
        if not self._channel_and_stubs_initialized():
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_sum() -> float:
            request = sum_proto.SumRequest(number_1=number_1, number_2=number_2)
            response = self._stub.Sum(request=request)
            return response.answer

        return attempt_sum()

    def sum_non_blocking(self, number_1: float, number_2: float) -> Optional[Future[float]]:
        if not self._channel_and_stubs_initialized():
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_sum_non_blocking() -> Future[float]:
            request = sum_proto.SumRequest(number_1=number_1, number_2=number_2)
            grpc_future = self._stub.Sum.future(request=request)
            return Future[float](grpc_future=grpc_future, conversion_func=lambda response: response.answer)

        return attempt_sum_non_blocking()
