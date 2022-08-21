import logging

from typing import Callable, Generator, Optional


def get_int_input_from_terminal() -> Optional[int]:
    input_str = input("Input number (leave empty to start computation):")
    if len(input_str) == 0:
        return None
    else:
        int_input = None
        try:
            int_input = int(input_str)
        except ValueError:
            logging.error(
                f"Could not parse terminal input {input_str} as a number, interpreting this as a signal to start computation"
            )
        return int_input


def get_terminal_input_generator(new_entry_callback: Callable = lambda new_entry: None) -> Generator[int, None, None]:
    input_completed = False
    while (not input_completed):
        number = get_int_input_from_terminal()
        if number is not None:
            logging.info(f"Adding {number} into computation")
            new_entry_callback(new_entry=number)
            yield number
        else:
            input_completed = True
            logging.info("Input completed")
