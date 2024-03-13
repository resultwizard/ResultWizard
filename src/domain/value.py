from dataclasses import dataclass
from application.helpers import _Helpers


from typing import Union
from plum import dispatch, overload


class _Value:
    """
    A floating-point value represented as string that is either treated as exact
    (does not have any uncertainties) or as inexact (has uncertainties).
    Values that are exact will be exempt from significant figures rounding.

    Note that is_exact signifies if the value is to be taken as a *literal* value,
    i.e. "3.14000" will be output as "3.14000" and not "3.14" if is_exact is True.
    TODO: maybe find a better word for "exact"?
    """

    _value: float
    _is_exact: bool
    _max_exponent: int
    _min_exponent: Union[int, None]

    def __init__(self, value: Union[float, str]):
        if isinstance(value, str):
            self._value = float(value)
            self._is_exact = True

            # Determine min exponent:
            value_str = value
            exponent_offset = 0
            if "e" in value_str:
                exponent_offset = int(value_str[value_str.index("e") + 1 :])
                value_str = value_str[0 : value_str.index("e")]
            if "." in value_str:
                decimal_places = len(value_str) - value_str.index(".") - 1
                self._min_exponent = -decimal_places + exponent_offset
            else:
                self._min_exponent = exponent_offset
        else:
            self._value = value
            self._is_exact = False
            self._min_exponent = None

        self._max_exponent = _Helpers.get_exponent(self._value)

    def set_min_exponent(self, min_exponent: int):
        self._min_exponent = min_exponent

    def set_sigfigs(self, sigfigs: int):
        self._min_exponent = self._max_exponent - sigfigs

    def extract(self) -> float:
        # TODO
        return self._value

    def should_round(self) -> bool:
        # TODO
        return not self._is_exact
