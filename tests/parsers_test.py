import pytest

from api import parsers


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
            ("ẞ", "Ss"),
            ("äh", "aeh"),
            ("Füße", "Fuesse"),
            ("GIEẞEN", "GIESsEN"),
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
