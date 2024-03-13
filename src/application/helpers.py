import math


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
        return "{:.{}f}".format(value, int(n))

    @classmethod
    def number_to_word(cls, number: int) -> str:
        if number == 0:
            return "zero"
        elif number == 1:
            return "one"
        elif number == 2:
            return "two"
        elif number == 3:
            return "three"
        elif number == 4:
            return "four"
        elif number == 5:
            return "five"
        elif number == 6:
            return "six"
        elif number == 7:
            return "seven"
        elif number == 8:
            return "eight"
        elif number == 9:
            return "nine"
        elif number == 10:
            return "ten"
        elif number == 11:
            return "eleven"
        elif number == 12:
            return "twelve"
        elif number == 13:
            return "thirteen"
        elif number == 14:
            return "fourteen"
        elif number == 15:
            return "fifteen"
        elif number == 16:
            return "sixteen"
        elif number == 17:
            return "seventeen"
        elif number == 18:
            return "eighteen"
        elif number == 19:
            return "nineteen"
        elif number == 20:
            return "twenty"
        elif number == 30:
            return "thirty"
        elif number == 40:
            return "forty"
        elif number == 50:
            return "fifty"
        elif number == 60:
            return "sixty"
        elif number == 70:
            return "seventy"
        elif number == 80:
            return "eighty"
        elif number == 90:
            return "ninety"
        elif number <= 99:
            tens = number // 10 * 10
            ones = number % 10
            return (
                cls.number_to_word(tens)
                + cls.number_to_word(ones)[0].upper()
                + cls.number_to_word(ones)[1:]
            )
        else:
            raise RuntimeError("Runtime error.")
