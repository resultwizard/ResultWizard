from typing import Union
from decimal import Decimal

from application.helpers import Helpers


class Value:
    """
    A decimal value.

    It is either exact or inexact. Values that are set as exact
    will be exempt form any rounding. If the value is set as exact, it will be
    treated as a *literal* value, i.e. "3.14000" will be output as "3.14000"
    and not "3.14".
    """

    _value: Decimal
    _is_exact: bool
    _max_exponent: int
    _min_exponent: int

    def __init__(self, value: Decimal, min_exponent: Union[int, None] = None):
        self._value = value

        if min_exponent is not None:
            self._min_exponent = min_exponent
            self._is_exact = True
        else:
            self._is_exact = False

        self._max_exponent = Helpers.get_exponent(self._value)

    def set_min_exponent(self, min_exponent: int):
        self._min_exponent = min_exponent

    def get_min_exponent(self) -> int:
        return self._min_exponent

    def set_sigfigs(self, sigfigs: int):
        self._min_exponent = self._max_exponent - sigfigs + 1

    def is_exact(self) -> bool:
        return self._is_exact

    def get(self) -> Decimal:
        return self._value

    def get_abs(self) -> Decimal:
        return abs(self._value)

    def get_exponent(self) -> int:
        return self._max_exponent

    def get_sig_figs(self) -> int:
        return self._max_exponent - self._min_exponent + 1

    def get_decimal_place(self) -> int:
        if self._min_exponent is None:
            # This should not happen as `_min_exponent` should be set
            # by the time this method is called.
            raise RuntimeError("Internal min_exponent not set error. Please report this bug.")
        return -self._min_exponent
