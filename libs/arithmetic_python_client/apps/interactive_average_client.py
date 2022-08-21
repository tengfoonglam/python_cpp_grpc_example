import logging
import os
import sys

from arithmetic_python_client import AverageClient
from typing import Generator, Optional


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

            def get_int_input_from_terminal() -> Optional[int]:
                input_str = input("Number to average (leave empty to start computation):")
                if len(input_str) == 0:
                    return None
                else:
                    int_input = None
                    try:
                        int_input = int(input_str)
                        numbers_to_average.append(int_input)
                    except ValueError:
                        logging.error(
                            f"Could not parse terminal input {input_str} as a number, interpreting this as a signal to start computation"
                        )
                    return int_input

            def input_generator() -> Generator[int, None, None]:
                input_completed = False
                while (not input_completed):
                    number = get_int_input_from_terminal()
                    if number is not None:
                        logging.info(f"Adding {number} into max computation")
                        yield number
                    else:
                        input_completed = True
                        logging.info("Input for max computation completed")

            answer = client.average(input_generator=input_generator())

            if answer is not None:
                logging.info(f"Received answer: Average of {numbers_to_average} is {answer}")
            else:
                logging.error("Failed to obtain answer")
    except KeyboardInterrupt:
        client.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    interactive_average()
