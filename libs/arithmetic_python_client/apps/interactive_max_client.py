import logging
import os
import sys

from arithmetic_python_client import MaxClient


def interactive_average() -> None:

    try:
        client = MaxClient()
        success = client.open()
        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Max Client successfully opened")

        while (True):
            numbers_to_max = []

            collecting_input = True
            while (collecting_input):
                input_str = input("Number to max (leave empty to start computation):")
                if len(input_str) == 0:
                    break
                else:
                    numbers_to_max.append(int(input_str))

            answer = client.max(numbers=numbers_to_max)

            if answer is not None:
                logging.info(f"Received answer: Max of {numbers_to_max} is {answer}")
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
