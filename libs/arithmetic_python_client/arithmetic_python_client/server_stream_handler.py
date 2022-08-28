import grpc
import logging
from threading import Thread, Event
from typing import Callable


class ServerStreamHandler:
    def __init__(self, stream_name: str) -> None:
        self._stream_name = stream_name
        self._processing_thread: Thread = Thread()
        self._completion_event: Event = Event()
        self._responses = None
        self._generate_request_function: Callable = lambda: None
        self._initialize_stream_function: Callable = lambda request: []
        self._new_response_callback: Callable = lambda response: print(
            f"{self._stream_name} stream received response: {response}")
        self._completed_callback: Callable = lambda success: print(
            f"{self._stream_name} stream completed. Success: {success}")

    def set_generate_request_function(self, func: Callable) -> None:
        self._generate_request_function = func

    def set_initialize_stream_function(self, func: Callable) -> None:
        self._initialize_stream_function = func

    def set_new_response_callback(self, callback: Callable) -> None:
        self._new_response_callback = callback

    def set_completed_callback(self, callback: Callable) -> None:
        self._completed_callback = callback

    def is_processing(self) -> bool:
        return self._processing_thread.is_alive()

    def cancel(self) -> None:
        if not self.is_processing():
            logging.warning(f"Cancel called when {self._stream_name} is not in progress, ignoring call")
            return
        if self._responses is not None:
            self._responses.cancel()
        self._processing_thread.join()

    def wait_till_completion(self) -> None:
        if self.is_processing():
            self._completion_event.wait()
            self._processing_thread.join()
        else:
            logging.warning(f"wait_till_completion called when {self._stream_name} is not in progress, ignoring call")

    def start(self) -> bool:
        if self.is_processing():
            logging.warning(f"Unable to start {self._stream_name} when it is already in progress")
            return False

        self._processing_thread = Thread(target=self._runner, name=self._stream_name)
        self._processing_thread.start()
        return True

    def _runner(self) -> None:
        logging.info(f"Start stream {self._stream_name}")
        success = False
        self._completion_event.clear()
        try:
            request = self._generate_request_function()
            self._responses = self._initialize_stream_function(request)
            for response in self._responses:
                self._new_response_callback(response=response)
            success = not self._responses.cancelled()
        except grpc.RpcError:
            logging.exception(
                f"RPC error occurred when performing stream {self._stream_name}, most likely cancelled midway")
        except Exception:
            logging.exception(f"Non-RPC Error occurred when performing stream {self._stream_name}")
        self._completed_callback(success=success)
        self._responses = None
        self._completion_event.set()
        logging.info(f"Completed stream {self._stream_name}")
        return

    def close(self) -> None:
        if self.is_processing():
            self.cancel()
