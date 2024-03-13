from domain.value import _Value

from typing import Union


class _Uncertainty:
    """
    A named uncertainty value, e.g. a systematic uncertainty of ±0.1cm
    when measuring a length. In this case the uncertainty would be 0.1 and the name
    would be "systematic". As Uncertainties are always directly associated with a
    Result, we don't store the unit of the value here.

    We don't use the word "error" to distinguish between errors in our code,
    and uncertainties in the physical sense. In reality, these words might be used
    interchangeably.
    """

    def __init__(self, uncertainty: Union[float, str], name: str = ""):
        self.uncertainty = _Value(uncertainty)
        self.name = name

    def value(self) -> _Value:
        return self.uncertainty

    def __str__(self):
        # TODO
        return ""
