#!/usr/bin/env python

import logging
import os
import sys

from arithmetic_python_client import AverageClient
from arithmetic_python_client.utils import get_terminal_input_generator


def interactive_average() -> None:

    USE_BLOCKING_METHOD = False

    try:
        client = AverageClient()
        success = client.open()

        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Average Client successfully opened")

        while client.is_grpc_active():
            numbers_to_average = []

            answer = None
            if USE_BLOCKING_METHOD:
                answer = client.average(input_iterable=get_terminal_input_generator(
                    new_entry_callback=lambda new_entry: numbers_to_average.append(new_entry)))
            else:
                future = client.average_non_blocking(input_iterable=get_terminal_input_generator(
                    new_entry_callback=lambda new_entry: numbers_to_average.append(new_entry)))

                # Just to demonstrate that call is non-blocking
                logging.info("Waiting for computation to complete...")

                if future is not None:
                    answer = future.wait_for_result()

            if answer is not None:
                logging.info(f"Received answer: Average of {numbers_to_average} is {answer}")
            else:
                logging.error("Failed to obtain average")
    except KeyboardInterrupt:
        client.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    interactive_average()
