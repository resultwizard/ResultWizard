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
    def test_number_substitution(self, name: str, expected: str):
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
    def test_umlaut_replacement(self, name: str, expected: str):
        assert parsers.parse_name(name) == expected
