from dataclasses import dataclass


class _Value:
    """
    A floating-point value represented as string that is either treated as exact
    (does not have any uncertainties) or as inexact (has uncertainties).
    Values that are exact will be exempt from significant figures rounding.
    """

    def __init__(self, value: str, is_exact: bool):
        self._value_str = value
        self._value_float = float(value)
        self._is_exact = is_exact

    def extract(self) -> float:
        return self._value_float

    def extract_exact(self) -> str:
        return self._value_str

    def should_round(self) -> bool:
        return not self._is_exact
