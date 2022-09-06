import pytest
from _pytest.monkeypatch import MonkeyPatch

from arithmetic_python_client.utils import (get_int_input_from_terminal, get_float_input_from_terminal)


@pytest.mark.parametrize("input_str, expected_result", [("0", 0), ("88", 88), ("-9", -9), ("a", None), ("abc", None),
                                                        ("!", None), ("!@#", None), ("6!a", None), ("-9q", None),
                                                        ("0.0", None), ("-1.", None), ("-.1", None)])
def test_get_int_input_from_terminal(monkeypatch: MonkeyPatch, input_str: str, expected_result: bool) -> None:
    monkeypatch.setattr('builtins.input', lambda _: input_str)
    assert get_int_input_from_terminal() == expected_result


@pytest.mark.parametrize("input_str, expected_result", [("0", 0.0), ("88", 88.0), ("-9", -9.0), ("a", None),
                                                        ("abc", None), ("!", None), ("!@#", None), ("6!a", None),
                                                        ("-9q", None), ("0.0", 0.0), ("8.", 8.0), ("-1.", -1.0),
                                                        ("-.6", -0.6)])
def test_get_float_input_from_terminal(monkeypatch: MonkeyPatch, input_str: str, expected_result: bool) -> None:
    monkeypatch.setattr('builtins.input', lambda _: input_str)
    assert get_float_input_from_terminal() == expected_result
