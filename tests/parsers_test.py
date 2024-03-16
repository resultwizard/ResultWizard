import pytest

from api import parsers
from domain.value import Value


class TestNameParser:

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("a12", "aTwelve"),
            ("a01", "aOne"),
            ("042", "fortyTwo"),
            ("a911bc13", "aNineHundredElevenBcThirteen"),
            ("13_600", "thirteenSixHundred"),
            ("a_5_6b7_$5", "aFiveSixBSevenFive"),
        ],
    )
    def test_substitutes_numbers(self, name: str, expected: str):
        assert parsers.parse_name(name) == expected

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("ä", "ae"),
            ("Ä", "Ae"),
            ("ü", "ue"),
            ("Ü", "Ue"),
            ("ö", "oe"),
            ("Ö", "Oe"),
            ("ß", "ss"),
            ("ẞ", "SS"),
            ("äh", "aeh"),
            ("Füße", "Fuesse"),
            ("GIEẞEN", "GIESSEN"),
        ],
    )
    def test_replaces_umlauts(self, name: str, expected: str):
        assert parsers.parse_name(name) == expected

    @pytest.mark.parametrize(
        "name, expected",
        [
            ("!a$", "a"),
            ("!a$b", "ab"),
            ("!a$b", "ab"),
            ("!%a&/(=*)s.,'@\"§d", "asd"),
        ],
    )
    def test_strips_invalid_chars(self, name: str, expected: str):
        assert parsers.parse_name(name) == expected

    @pytest.mark.parametrize("name", ["", "!", "    ", "_  ", "§ _ '*"])
    def test_empty_name_fails(self, name):
        with pytest.raises(ValueError):
            parsers.parse_name(name)


class TestValueParser:

    @pytest.mark.parametrize(
        "value, expected",
        [
            # plain numbers
            ("012", Value(12.0, min_exponent=0)),
            ("12", Value(12.0, min_exponent=0)),
            ("-42", Value(-42.0, min_exponent=0)),
            ("10050", Value(10050, min_exponent=0)),
            # plain numbers scientific
            ("13e3", Value(13000.0, min_exponent=3)),
            # plain decimal
            ("3.1415", Value(3.1415, min_exponent=-4)),
            ("0.005", Value(0.005, min_exponent=-3)),
            ("0.010", Value(0.01, min_exponent=-3)),
            # decimal & scientific
            ("3.1415e3", Value(3141.5, min_exponent=-1)),
            ("2.71828e2", Value(271.828, min_exponent=-3)),
            ("2.5e-1", Value(0.25, min_exponent=-2)),
            ("0.1e2", Value(10.0, min_exponent=1)),
            ("1.2e5", Value(120000.0, min_exponent=4)),
            ("1.20e5", Value(120000.0, min_exponent=3)),
            ("103.1570e-30", Value(0.0000000000000000000000000001031570, min_exponent=-34)),
        ],
    )
    def test_parse_exact_value(self, value: str, expected: Value):
        v = parsers.parse_exact_value(value)
        # pylint: disable=protected-access
        assert v._value == expected._value
        assert v._min_exponent == expected._min_exponent
        # pylint: enable=protected-access
