import grpc
import logging

from arithmetic_python_client.python_client import PythonClient

from arithmetic_proto import prime_pb2_grpc as prime_grpc
from arithmetic_proto import prime_pb2 as prime_proto
from threading import Thread, Event
from typing import Callable


class PerformPrimeNumberDecompositionClient(PythonClient[prime_grpc.PerformPrimeNumberDecompositionServiceStub]):
    @staticmethod
    def _create_stub(channel: grpc.Channel) -> prime_grpc.PerformPrimeNumberDecompositionServiceStub:
        return prime_grpc.PerformPrimeNumberDecompositionServiceStub(channel)

    def __init__(self) -> None:
        super().__init__()
        self._processing_thread: Thread = Thread()
        self._completion_event: Event = Event()
        self._responses = None
        self._new_response_callback: Callable = lambda factor: print(f"Received factor: {factor}")
        self._completed_callback: Callable = lambda success: print(
            f"Prime number decomposition completed. Success: {success}")

    def set_new_response_callback(self, callback: Callable) -> None:
        self._new_response_callback = callback

    def set_completed_callback(self, callback: Callable) -> None:
        self._completed_callback = callback

    def perform_prime_number_decomposition(self, number: int) -> bool:
        if not self.is_grpc_active():
            return False

        if self.is_processing():
            logging.warning(
                "Unable to start a new prime number decomposition when the client is still processing the previous one")
            return False

        self._processing_thread = Thread(target=self._runner,
                                         name="Prime number decomposition",
                                         kwargs={"number": number})
        self._processing_thread.start()
        return True

    def is_processing(self) -> bool:
        return self._processing_thread.is_alive()

    def cancel(self) -> None:
        if not self.is_processing():
            logging.warning("Cancel called when Prime Number Decomposition is not in progress, ignoring call")
            return
        if self._responses is not None:
            self._responses.cancel()
        self._processing_thread.join()

    def wait_till_completion(self) -> None:
        if self.is_processing():
            self._completion_event.wait()
            self._processing_thread.join()
        else:
            logging.warning(
                "wait_till_completion called when Prime Number Decomposition is not in progress, ignoring call")

    def _runner(self, number: int) -> None:
        logging.info(f"Start performing prime number decomposition for number {number}")
        success = False
        self._completion_event.clear()
        try:
            request = prime_proto.PerformPrimeNumberDecompositionRequest(number=number)
            self._responses = self._stub.PerformPrimeNumberDecomposition(request=request)
            for response in self._responses:
                self._new_response_callback(factor=response.factor)
            success = not self._responses.cancelled()
        except grpc.RpcError:
            logging.exception("RPC error occurred when performing prime number decomposition")
        except Exception:
            logging.exception("Error occurred when performing prime number decomposition")
        self._completed_callback(success=success)
        self._responses = None
        self._completion_event.set()
        logging.info(f"Completed performing prime number decomposition for number {number}")
        return

    def close(self) -> bool:
        if self.is_processing():
            self.cancel()
        return super().close()
