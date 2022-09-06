import logging

from typing import Callable, Generator, Optional, TypeVar

T = TypeVar('T')


def get_int_input_from_terminal(display_message: str = "") -> Optional[int]:
    return get_input_from_terminal(conversion_func=lambda input_str: int(input_str), display_message=display_message)


def get_float_input_from_terminal(display_message: str = "") -> Optional[float]:
    return get_input_from_terminal(conversion_func=lambda input_str: float(input_str), display_message=display_message)


def get_input_from_terminal(conversion_func: Callable[[str], T], display_message: str) -> Optional[T]:
    input_str = input(display_message)
    if len(input_str) == 0:
        return None
    else:
        parsed_input = None
        try:
            parsed_input = conversion_func(input_str)
        except ValueError:
            logging.error(f"Could not parse terminal input {input_str} as a number")
        return parsed_input


def get_terminal_input_generator(new_entry_callback: Callable = lambda new_entry: None) -> Generator[int, None, None]:
    input_completed = False
    while not input_completed:
        number = get_int_input_from_terminal(display_message="Input value (leave empty to start computation):")
        if number is not None:
            logging.info(f"Adding {number} into computation")
            new_entry_callback(new_entry=number)
            yield number
        else:
            input_completed = True
            logging.info("Input completed")
