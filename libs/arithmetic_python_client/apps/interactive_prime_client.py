#!/usr/bin/env python

import logging
import os
import sys

from arithmetic_python_client import PerformPrimeNumberDecompositionClient
from arithmetic_python_client.utils import get_int_input_from_terminal


def interactive_prime() -> None:

    try:
        client = PerformPrimeNumberDecompositionClient()

        answer = []

        def on_receive(factor: int) -> None:
            logging.info(f"Received number: {factor}")
            answer.append(factor)

        def on_completion(success: bool) -> None:
            if success:
                logging.info(f"Answer: {answer}")
            else:
                logging.warning("Failed to compute answer")

        client.set_new_response_callback(callback=on_receive)
        client.set_completed_callback(callback=on_completion)

        success = client.open()
        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Prime Client successfully opened")

        while client.is_grpc_active():
            answer.clear()
            number = get_int_input_from_terminal(display_message="Number to perform prime number decomposition: ")

            if number is None:
                logging.warning("Invalid input, please try again")
                continue

            start_success = client.perform_prime_number_decomposition(number=number)
            if start_success:
                client.wait_till_completion()
            else:
                logging.warning("Failed to start prime number decomposition task")

    except KeyboardInterrupt:
        client.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    interactive_prime()
