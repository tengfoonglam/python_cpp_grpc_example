import grpc

from arithmetic_python_client.python_client import PythonClient

from arithmetic_proto import sum_pb2_grpc as sum_grpc
from arithmetic_proto import sum_pb2 as sum_proto
from typing import Optional


class SumClient(PythonClient[sum_grpc.SumServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> sum_grpc.SumServiceStub:
        return sum_grpc.SumServiceStub(channel)

    def sum(self, number_1: float, number_2: float) -> Optional[float]:
        if not self.is_grpc_active():
            return None

        @PythonClient.return_none_if_exception_caught
        def attempt_sum() -> float:
            request = sum_proto.SumRequest(number_1=number_1, number_2=number_2)
            response = self._stub.Sum(request=request)
            return response.answer

        return attempt_sum()
