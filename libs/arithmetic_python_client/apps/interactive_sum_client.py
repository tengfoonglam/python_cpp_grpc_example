#!/usr/bin/env python

import logging
import os
import sys

from arithmetic_python_client import SumClient
from arithmetic_python_client.utils import get_float_input_from_terminal


def interactive_sum() -> None:

    USE_BLOCKING_METHOD = False

    try:
        client = SumClient()
        success = client.open()
        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Sum Client successfully opened")

        while client.is_grpc_active():
            number_1 = get_float_input_from_terminal(display_message="First float to sum: ")
            number_2 = get_float_input_from_terminal(display_message="Second float to sum: ")

            if None not in (number_1, number_2):

                answer = None
                if USE_BLOCKING_METHOD:
                    answer = client.sum(number_1=number_1, number_2=number_2)
                else:
                    future = client.sum_non_blocking(number_1=number_1, number_2=number_2)

                    logging.info("Waiting for computation to complete...")

                    if future is not None:
                        answer = future.wait_till_completion()

                if answer is not None:
                    logging.info(f"Received answer: {number_1} + {number_2} = {answer}")
                else:
                    logging.error(f"Failed to obtain answer for sum {number_1} + {number_2}")
            else:
                logging.warning("Invalid input, please try again")
    except KeyboardInterrupt:
        client.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    interactive_sum()
