from application.rounder import _Rounder
from domain.result import _Result
from domain.value import _Value
from domain.uncertainty import _Uncertainty

class TestRounder:
    def test_hierarchy_1(self):
        res = _Result("", _Value("1.0000"), "", [], 2, 10)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -4

        res = _Result("", _Value("1.0000"), "", [_Uncertainty(0.1)], None, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -4
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -4

        res = _Result("", _Value("1.0000"), "", [_Uncertainty("0.1")], None, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -4
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1

    def test_hierarchy_2(self):
        res = _Result("", _Value(1.0), "", [], 10, 2)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -9

        res = _Result("", _Value(1.0), "", [_Uncertainty(0.1)], 10, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -9
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -9

        res = _Result("", _Value(1.0), "", [_Uncertainty("0.1")], 10, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -9
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1

    def test_hierarchy_3(self):
        res = _Result("", _Value(1.0), "", [], None, 2)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -2

        res = _Result("", _Value(1.0), "", [_Uncertainty(0.1)], None, 2)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -2

        res = _Result("", _Value(1.0), "", [_Uncertainty("0.1e-5")], None, 2)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -6

    def test_hierarchy_4(self):
        res = _Result("", _Value(1.0), "", [_Uncertainty(0.11)], None, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -2

        res = _Result("", _Value(1.0), "", [_Uncertainty(0.294999)], None, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -2

        res = _Result("", _Value(1.0), "", [_Uncertainty(0.295001)], None, None)
        _Rounder.round_result(res)
        print(res.uncertainties[0].uncertainty.get_min_exponent())
        assert res.value.get_min_exponent() == -1
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1

        res = _Result("", _Value(1.0), "", [_Uncertainty(0.4), _Uncertainty(0.04)], None, None)
        _Rounder.round_result(res)
        print(res.uncertainties[0].uncertainty.get_min_exponent())
        assert res.value.get_min_exponent() == -2
        assert res.uncertainties[0].uncertainty.get_min_exponent() == -1
        assert res.uncertainties[1].uncertainty.get_min_exponent() == -2

    def test_hierarchy_5(self):
        res = _Result("", _Value(1.0), "", [], None, None)
        _Rounder.round_result(res)
        assert res.value.get_min_exponent() == -1
