import math
import decimal
from decimal import Decimal

import application.error_messages as error_messages

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


class Helpers:
    @classmethod
    def get_exponent(cls, value: Decimal) -> int:
        return math.floor(math.log10(abs(value)))

    @classmethod
    def get_first_digit(cls, value: Decimal) -> int:
        n = abs(value) * 10 ** (-cls.get_exponent(value))
        return math.floor(n)

    @classmethod
    def round_to_n_decimal_places(cls, value: Decimal, n: int) -> str:
        try:
            decimal_value = value.quantize(Decimal(f"1.{'0' * n}"))
            return f"{decimal_value:.{n}f}"
        except decimal.InvalidOperation as exc:
            raise ValueError(error_messages.PRECISION_TOO_LOW) from exc

    @classmethod
    def number_to_word(cls, number: int) -> str:
        if 0 <= number <= 19:
            return _NUMBER_TO_WORD[number]
        if 0 <= number <= 99:
            tens = number // 10 * 10
            ones = number % 10
            if ones == 0:
                return _NUMBER_TO_WORD[tens]
            return _NUMBER_TO_WORD[tens] + cls.capitalize(_NUMBER_TO_WORD[ones])
        if 0 <= number <= 999:
            hundreds = number // 100
            tens = number % 100
            if tens == 0:
                return _NUMBER_TO_WORD[hundreds] + "Hundred"
            return _NUMBER_TO_WORD[hundreds] + "Hundred" + cls.capitalize(cls.number_to_word(tens))

        raise ValueError(error_messages.NUMBER_TO_WORD_TOO_HIGH.format(number=number))

    @classmethod
    def capitalize(cls, s: str) -> str:
        return s[0].upper() + s[1:]
