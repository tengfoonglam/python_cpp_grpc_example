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

    def _channel_and_stubs_initialized(self) -> bool:
        return self._channel is not None and self._stub is not None

    def open(self, ip_addr: str = "0.0.0.0", port: str = "50051") -> bool:
        address_with_port = f"{ip_addr}:{port}"
        logging.info(f"Connecting to {address_with_port}")
        self._channel = self._create_connect_channel(address_with_port)
        logging.info(f"gRPC channel creation {'successful' if self._channel else 'unsuccessful'}")
        self._stub = self._create_stub(channel=self._channel) if self._channel else None
        logging.info(f"gRPC stub creation {'successful' if self._channel else 'unsuccessful'}")
        return self._channel_and_stubs_initialized()

    @staticmethod
    def _create_connect_channel(address_with_port: str, timeout: float = 5.0) -> Optional[grpc.Channel]:

        try:
            channel = grpc.insecure_channel(target=address_with_port)
        except Exception as e:
            logging.exception(f"Could not create channel: {e}")
            return None

        try:
            future = grpc.channel_ready_future(channel)
            future.result(timeout=timeout)
        except grpc.FutureTimeoutError:
            logging.error("Connection to gRPC server timed out")
        except Exception:
            logging.error("Could not connect to the gRPC-Server.", exc_info=True)

        if future.done():
            return channel
        else:
            future.cancel()
            channel.close()
            logging.error("Failed to create a connected channel")
            return None

    def close(self) -> bool:

        if self._channel is not None:
            try:
                self._channel.close()
                self._channel = None
            except Exception:
                logging.exception("Error while closing the gRPC-Channel")

        self._stub = None

        grpc_closed = not self._channel_and_stubs_initialized()
        if grpc_closed:
            logging.info("gRPC channel closed successfully")
        else:
            logging.warn("gRPC channel failed to close")

        return grpc_closed

    def is_grpc_active(self) -> bool:
        if not self._channel_and_stubs_initialized():
            logging.warning("No active gRPC connection.")
            return False
        active = False
        try:
            future = grpc.channel_ready_future(self._channel)
            future.result(timeout=0.5)
            active = True
        except grpc.FutureTimeoutError:
            future.cancel()
            logging.error("gRPC connection lost. channel_ready_future timed out")
        except Exception:
            logging.exception("gRPC connection lost")

        if not future.done():
            future.cancel()

        return active
