#!/usr/bin/env python

import logging
import os
import sys

from arithmetic_python_client import MaxClient
from arithmetic_python_client.utils import get_terminal_input_generator


def interactive_max() -> None:

    try:
        client = MaxClient()
        answer = 0

        def on_receive(max: int) -> None:
            nonlocal answer
            logging.info(f"Received new max: {max}")
            answer = max

        def on_completion(success: bool) -> None:
            if success:
                logging.info(f"Max: {answer}")
            else:
                logging.warning("Failed to compute max")

        client.set_new_response_callback(callback=on_receive)
        client.set_completed_callback(callback=on_completion)

        success = client.open()

        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Max Client successfully opened")

        while (client.is_grpc_active()):
            numbers_to_max = []
            start_success = client.max(input_iterable=get_terminal_input_generator(
                new_entry_callback=lambda new_entry: numbers_to_max.append(new_entry)))
            if start_success:
                client.wait_till_completion()
            else:
                logging.warning("Failed to start max task")

    except KeyboardInterrupt:
        client.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    interactive_max()
