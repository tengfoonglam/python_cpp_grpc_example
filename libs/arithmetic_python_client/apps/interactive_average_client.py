import logging
import os
import sys

from arithmetic_python_client import AverageClient
from arithmetic_python_client.utils import get_terminal_input_generator


def interactive_average() -> None:

    try:
        client = AverageClient()
        success = client.open()

        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Average Client successfully opened")

        while (True):
            numbers_to_average = []
            answer = client.average(input_generator=get_terminal_input_generator(
                new_entry_callback=lambda new_entry: numbers_to_average.append(new_entry)))
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
