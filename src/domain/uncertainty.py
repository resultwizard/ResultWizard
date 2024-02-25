from domain.value import _Value


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

    def __init__(self, uncertainty: str, is_exact: bool, name=""):
        if not isinstance(uncertainty, (float, str)):
            raise TypeError(f"`uncertainty` must be a number-string, not {type(uncertainty)}")
        if not isinstance(name, str):
            raise TypeError(f"`name` must be a string, not {type(name)}")

        self.uncertainty = _Value(uncertainty, is_exact)
        self.name = name

    def __str__(self):
        if self.name == "":
            return f"{self.uncertainty.extract()}"
        return f"{self.uncertainty.extract()} {self.name}"
