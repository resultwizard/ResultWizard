from typing import Union

from application.helpers import _Helpers


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
    _min_exponent: int

    # "3400.0" -> 3400, -1, 3
    # "3400"   -> 3400,  0, 3
    # "3.4e3"  -> 3400,  2, 3

    def __init__(self, value: float, min_exponent: Union[int, None] = None):
        self._value = value

        if min_exponent is not None:
            self._min_exponent = min_exponent
            self._is_exact = True
        else:
            self._is_exact = False

        self._max_exponent = _Helpers.get_exponent(self._value)

    def set_min_exponent(self, min_exponent: int):
        self._min_exponent = min_exponent

    def get_min_exponent(self) -> int:
        return self._min_exponent

    def set_sigfigs(self, sigfigs: int):
        self._min_exponent = self._max_exponent - sigfigs + 1

    def is_exact(self) -> bool:
        return self._is_exact

    def get(self) -> float:
        return self._value

    def get_abs(self) -> float:
        return abs(self._value)

    def get_exponent(self) -> int:
        return self._max_exponent

    def get_sig_figs(self) -> int:
        return self._max_exponent - self._min_exponent + 1

    def get_decimal_place(self) -> int:
        # TODO: it can never be None, right? So then we don't need this:
        if self._min_exponent is None:
            raise RuntimeError("An unexpected error occurred. Please report this bug.")
        return -self._min_exponent
