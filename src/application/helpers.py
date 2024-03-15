import math


_NUMBER_TO_WORD = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
}


class _Helpers:
    @classmethod
    def get_exponent(cls, value: float) -> int:
        return math.floor(math.log10(abs(value)))

    @classmethod
    def get_first_digit(cls, value: float) -> int:
        n = abs(value) * 10 ** (-cls.get_exponent(value))
        return math.floor(n)

    @classmethod
    def round_to_n_decimal_places(cls, value: float, n: int):
        return f"{value:.{int(abs(n))}f}"

    @classmethod
    def number_to_word(cls, number: int) -> str:
        if number >= 0 and number <= 19:
            return _NUMBER_TO_WORD[number]
        elif number >= 0 and number <= 99:
            tens = number // 10 * 10
            ones = number % 10
            if ones == 0:
                return _NUMBER_TO_WORD[tens]
            else:
                return (
                    _NUMBER_TO_WORD[tens]
                    + _NUMBER_TO_WORD[ones][0].upper()
                    + _NUMBER_TO_WORD[ones][1:]
                )
        else:
            raise RuntimeError("Runtime error.")

    @classmethod
    def capitalize(cls, s: str) -> str:
        return s[:1].upper() + s[1:]
