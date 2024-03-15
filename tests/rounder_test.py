# pylint: disable=redefined-outer-name

import pytest

from application.rounder import Rounder, RoundingConfig
from domain.result import Result
from domain.value import Value
from domain.uncertainty import Uncertainty


@pytest.fixture
def config_defaults():
    return RoundingConfig(-1, -1, 2, -1)


class TestRounder:
    def test_hierarchy_1(self, config_defaults):
        res = Result("", Value(1.0000, min_exponent=-4), "", [], 2, 10)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -4

        res = Result("", Value(1.0000, min_exponent=-4), "", [Uncertainty(Value(0.1))], None, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -4
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -4

        res = Result(
            "",
            Value(1.0000, min_exponent=-4),
            "",
            [Uncertainty(Value(0.1, min_exponent=-1))],
            None,
            None,
        )
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -4
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1

    def test_hierarchy_3(self, config_defaults):
        res = Result("", Value(1.0), "", [], 10, 2)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -9

        res = Result("", Value(1.0), "", [Uncertainty(Value(0.1))], 10, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -9
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -9

        res = Result("", Value(1.0), "", [Uncertainty(Value(0.1, min_exponent=-1))], 10, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -9
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1

    def test_hierarchy_4(self, config_defaults):
        res = Result("", Value(1.0), "", [], None, 2)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -2

        res = Result("", Value(1.0), "", [Uncertainty(Value(0.1))], None, 2)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -2

        res = Result("", Value(1.0), "", [Uncertainty(Value(0.1e-5, min_exponent=-6))], None, 2)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -6

    def test_hierarchy_5(self, config_defaults):
        res = Result("", Value(1.0), "", [Uncertainty(Value(0.11))], None, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -2

        res = Result("", Value(1.0), "", [Uncertainty(Value(0.294999))], None, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -2

        res = Result("", Value(1.0), "", [Uncertainty(Value(0.295001))], None, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -1
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1

        res = Result(
            "", Value(1.0), "", [Uncertainty(Value(0.4)), Uncertainty(Value(0.04))], None, None
        )
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1
        assert res.uncertainties[1].uncertainty.get_min_exponent() == -2

    def test_hierarchy_6(self, config_defaults):
        res = Result("", Value(1.0), "", [], None, None)
        Rounder.round_result(res, config_defaults)
        assert res.value.get_min_exponent() == -1
