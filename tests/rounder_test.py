# pylint: disable=redefined-outer-name

from typing import List
from decimal import Decimal
import pytest

from application.rounder import Rounder, RoundingConfig
from domain.result import Result
from domain.value import Value
from domain.uncertainty import Uncertainty


@pytest.fixture
def config_defaults():
    return RoundingConfig(-1, -1, 2, -1)


class TestRounder:

    @pytest.mark.parametrize(
        "result, config, expected_value_min_exponent, expected_uncert_min_exponents",
        [
            # Hierarchy 1:
            (
                Result("", Value(Decimal(1.0), -1), "", [], None, None),
                RoundingConfig(-1, -1, 2, -1),
                -1,
                [],
            ),
            (
                Result(
                    "", Value(Decimal(1.0), -1), "", [Uncertainty(Value(Decimal(1.0)))], None, None
                ),
                RoundingConfig(-1, -1, 2, -1),
                -1,
                [-1],
            ),
            (
                Result(
                    "",
                    Value(Decimal(1.0), -1),
                    "",
                    [Uncertainty(Value(Decimal(1.0), -2))],
                    None,
                    None,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -1,
                [-2],
            ),
            # Hierarchy 2:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0)))],
                    3,
                    None,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -2,
                [-2],
            ),
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0), -3))],
                    3,
                    None,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -2,
                [-3],
            ),
            # Hierarchy 3:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0)))],
                    None,
                    2,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -2,
                [-2],
            ),
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0), -3))],
                    None,
                    2,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -2,
                [-3],
            ),
            # Hierarchy 4:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0)))],
                    None,
                    None,
                ),
                RoundingConfig(5, -1, 2, -1),
                -4,
                [-4],
            ),
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0), -3))],
                    None,
                    None,
                ),
                RoundingConfig(5, -1, 2, -1),
                -4,
                [-3],
            ),
            # Hierarchy 5:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0)))],
                    None,
                    None,
                ),
                RoundingConfig(-1, 4, 2, -1),
                -4,
                [-4],
            ),
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [Uncertainty(Value(Decimal(1.0), -3))],
                    None,
                    None,
                ),
                RoundingConfig(-1, 4, 2, -1),
                -4,
                [-3],
            ),
            # Hierarchy 6:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [
                        Uncertainty(Value(Decimal(1.0), -3)),
                        Uncertainty(Value(Decimal(1.0))),
                        Uncertainty(Value(Decimal(2.0))),
                        Uncertainty(Value(Decimal(2.9499))),
                        Uncertainty(Value(Decimal(2.9500))),
                        Uncertainty(Value(Decimal(0.007))),
                    ],
                    None,
                    None,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -3,
                [-3, -1, -1, -1, 0, -3],
            ),
            # Hierarchy 7:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [],
                    None,
                    None,
                ),
                RoundingConfig(-1, -1, 2, -1),
                -1,
                [],
            ),
            # Hierarchy 8:
            (
                Result(
                    "",
                    Value(Decimal(1.0)),
                    "",
                    [],
                    None,
                    None,
                ),
                RoundingConfig(-1, -1, -1, 2),
                -2,
                [],
            ),
        ],
    )
    def test_all_hierarchies(
        self,
        result: Result,
        config: RoundingConfig,
        expected_value_min_exponent: int,
        expected_uncert_min_exponents: List[int],
    ):
        Rounder.round_result(result, config)
        assert result.value.get_min_exponent() == expected_value_min_exponent
        assert [
            u.uncertainty.get_min_exponent() for u in result.uncertainties
        ] == expected_uncert_min_exponents
