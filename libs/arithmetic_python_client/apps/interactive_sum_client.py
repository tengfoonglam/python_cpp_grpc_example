import logging
import os
import sys

from arithmetic_python_client import SumClient


def interactive_sum() -> None:

    try:
        client = SumClient()
        success = client.open_grpc()
        if not success:
            logging.error("Failed to open gRPC channel")
            raise SystemExit(1)

        logging.info("Sum Client successfully opened")

        while (True):
            number_1 = float(input("First number to sum: "))
            number_2 = float(input("Second number to sum: "))
            answer = client.sum(number_1=number_1, number_2=number_2)

            if answer is not None:
                logging.info(f"Received answer: {number_1} + {number_2} = {answer}")
            else:
                logging.error(f"Failed to obtain answer for sum {number_1} + {number_2}")
    except KeyboardInterrupt:
        client.close_grpc()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    FORMAT = ' (%(filename)s:%(lineno)d): %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    interactive_sum()
