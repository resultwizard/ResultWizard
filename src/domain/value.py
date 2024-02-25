from dataclasses import dataclass


class _Value:
    """
    A floating-point value represented as string that is either treated as exact
    (does not have any uncertainties) or as inexact (has uncertainties).
    Values that are exact will be exempt from significant figures rounding.

    Note that is_exact signifies if the value is to be taken as a *literal* value,
    i.e. "3.14000" will be output as "3.14000" and not "3.14" if is_exact is True.
    TODO: maybe find a better word for "exact"?
    """

    def __init__(self, value: str, is_exact: bool):
        self.assign(value)
        self._is_exact = is_exact

    def assign(self, value: str):
        self._value_str = value
        self._value_float = float(value)

    def extract(self) -> float:
        return self._value_float

    def extract_exact(self) -> str:
        return self._value_str

    def should_round(self) -> bool:
        return not self._is_exact
