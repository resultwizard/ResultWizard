import numpy as np


class _Helpers:
    @classmethod
    def get_exponent(cls, value: float) -> int:
        return np.floor(np.log10(value))
