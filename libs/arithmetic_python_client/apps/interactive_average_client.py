import logging
import os
import sys

from arithmetic_python_client import AverageClient


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

            collecting_input = True
            while (collecting_input):
                input_str = input("Number to average (leave empty to start computation):")
                if len(input_str) == 0:
                    break
                else:
                    numbers_to_average.append(int(input_str))

            answer = client.average(numbers=numbers_to_average)

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
