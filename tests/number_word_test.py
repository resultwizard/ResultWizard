from application.helpers import Helpers

import pytest


class TestNumberWord:
    @pytest.mark.parametrize(
        "input, expected",
        [
            (1, "one"),
            (2, "two"),
            (3, "three"),
            (10, "ten"),
            (18, "eighteen"),
            (76, "seventySix"),
            (100, "oneHundred"),
            (101, "oneHundredOne"),
            (123, "oneHundredTwentyThree"),
            (305, "threeHundredFive"),
            (911, "nineHundredEleven"),
            (999, "nineHundredNinetyNine"),
        ],
    )
    def test_number_to_word(self, input, expected):
        assert Helpers.number_to_word(input) == expected

    @pytest.mark.parametrize("input", [1000, 1001, -1, -500])
    def test_number_to_word_raises(self, input):
        with pytest.raises(ValueError, match="numbers between 0 and 999"):
            Helpers.number_to_word(input)
