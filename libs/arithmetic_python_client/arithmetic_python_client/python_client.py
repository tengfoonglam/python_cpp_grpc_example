import grpc
import logging

from typing import Callable, Generic, Optional, TypeVar

T = TypeVar('T')


class PythonClient(Generic[T]):
    @staticmethod
    def return_none_if_exception_caught(function: Callable) -> Callable:
        def wrapper() -> Optional[Callable]:
            method_name = getattr(function, '__name__', repr(callable))
            try:
                return function()
            except grpc.RpcError:
                logging.exception(f"RPC error occurred when calling {method_name}")
            except Exception:
                logging.exception(f"Error occurred when calling {method_name}")
            return None

        return wrapper

    def __init__(self) -> None:
        self._channel: Optional[grpc.Channel] = None
        self._stub = None

    @staticmethod
    def _create_stub(channel: grpc.Channel) -> Optional[T]:
        return None

    def is_grpc_active(self) -> bool:
        return self._channel is not None and self._stub is not None

    def open_grpc(self, ip_addr: str = "0.0.0.0", port: str = "50051") -> bool:
        address_with_port = f"{ip_addr}:{port}"
        logging.info(f"Connecting to {address_with_port}")
        self._channel = self._create_connect_channel(address_with_port)
        logging.info(f"gRPC channel creation {'successful' if self._channel else 'unsuccessful'}")
        self._stub = self._create_stub(channel=self._channel) if self._channel else None
        logging.info(f"gRPC stub creation {'successful' if self._channel else 'unsuccessful'}")
        return self.is_grpc_active()

    def _create_connect_channel(self, address_with_port: str) -> Optional[grpc.Channel]:

        try:
            channel = grpc.insecure_channel(target=address_with_port)
        except Exception as e:
            logging.exception(f"Could not create channel: {e}")
            return None

        try:
            grpc.channel_ready_future(channel).result(timeout=5)
        except grpc.FutureTimeoutError:
            logging.error("Connection to gRPC server timed out")
            return None
        except Exception as e:
            logging.error(f"Could not connect to the gRPC-Server. Error: {e}")
            return None

        return channel

    def close_grpc(self) -> bool:

        if self._channel is not None:
            try:
                self._channel.close()
                self._channel = None
            except Exception:
                logging.exception("Error while closing the gRPC-Channel")

        self._stub = None

        grpc_closed = not self.is_grpc_active()
        if grpc_closed:
            logging.info("gRPC channel closed successfully")
        else:
            logging.warn("gRPC channel failed to close")

        return grpc_closed
