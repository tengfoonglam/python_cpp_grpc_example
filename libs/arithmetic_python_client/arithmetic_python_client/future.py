import logging
import grpc

from typing import Callable, Generic, Optional, TypeVar

T = TypeVar('T')


class Future(Generic[T]):
    def __init__(self, grpc_future: grpc.Future, conversion_func: Callable) -> None:
        self._grpc_future = grpc_future
        self._conversion_func = conversion_func

    def cancel(self) -> bool:
        return self._grpc_future.cancel()

    def done(self) -> bool:
        return self._grpc_future.done()

    def wait_till_completion(self, timeout: Optional[float] = None) -> Optional[T]:
        try:
            response = self._grpc_future.result(timeout=timeout)
            return self._conversion_func(response)
        except grpc.FutureTimeoutError:
            logging.error("Timed out while waiting from response")
        except grpc.FutureCancelledError:
            logging.error("Call was cancelled while waiting for response")
        except Exception:
            logging.exception("Non-gRPC exception called while waiting for response")
        return None
