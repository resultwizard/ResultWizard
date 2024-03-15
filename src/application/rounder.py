from typing import List

from domain.result import _Result
from domain.uncertainty import _Uncertainty
from application.helpers import _Helpers


class _Rounder:

    @classmethod
    def round_result(cls, result: _Result, sigfigs_default: int, decimal_places: int) -> None:
        """
        In-place rounds all numerical fields of a result to the correct
        number of significant figures.

        # Rounding hierarchy:

        1. Is uncertainty exact? Do not round.
        2. Round uncertainty according to the hierarchy below.


        # Rounding hierarchy for inexact uncertainty:

        1. Is result value exact?
           Round uncertainty according to result value.

        2. Is default for decimal places given (not -1) (see method param)?
           Round value according to number of decimal places.
           Round uncertainties according to value.

        3. Is number of sigfigs of result given?
           Round value according to number of sigfigs.
           Round uncertainties according to value.

        4. Is number of decimal places of result given?
           Round value according to number of decimal places.
           Round uncertainties according to value.

        5. Is at least one uncertainty given?
           Round each uncertainty according to standard rules.
           Round value according to uncertainty with lowest min exponent.

        6. Round value to the default for the sigfigs (see method param).

        TODO: Warning message if user specifies exact value and sigfigs etc.
        """
        cls._round_result(result, sigfigs_default, decimal_places)

        short = result.get_short_result()
        if short:
            cls._round_result(short, sigfigs_default, decimal_places)

    @classmethod
    def _round_result(cls, result: _Result, sigfigs_default: int, decimal_places: int) -> None:
        """See the docstring of the public `round_result` for details."""

        value = result.value
        uncertainties = result.uncertainties

        # Rounding hierarchy 1:
        if value.is_exact():
            cls._uncertainties_set_min_exponents(uncertainties, value.get_min_exponent())

        # Rounding hierarchy 2:
        elif decimal_places > -1:
            min_exponent = -decimal_places
            value.set_min_exponent(min_exponent)
            cls._uncertainties_set_min_exponents(uncertainties, min_exponent)

        # Rounding hierarchy 3:
        elif result.sigfigs is not None:
            value.set_sigfigs(result.sigfigs)
            cls._uncertainties_set_min_exponents(uncertainties, value.get_min_exponent())

        # Rounding hierarchy 4:
        elif result.decimal_places is not None:
            value.set_min_exponent(-result.decimal_places)
            cls._uncertainties_set_min_exponents(uncertainties, value.get_min_exponent())

        # Rounding hierarchy 5:
        elif len(uncertainties) > 0:
            for u in uncertainties:
                if u.uncertainty.is_exact():
                    continue

                normalized_value = abs(u.uncertainty.get()) * 10 ** (
                    -_Helpers.get_exponent(u.uncertainty.get())
                )

                if round(normalized_value, 1) >= 3.0:
                    u.uncertainty.set_sigfigs(1)
                else:
                    u.uncertainty.set_sigfigs(2)

            min_exponent = min([u.uncertainty.get_min_exponent() for u in uncertainties])
            value.set_min_exponent(min_exponent)

        # Rounding hierarchy 6:
        else:
            value.set_sigfigs(sigfigs_default)
            cls._uncertainties_set_min_exponents(uncertainties, value.get_min_exponent())

    @classmethod
    def _uncertainties_set_min_exponents(
        cls, uncertainties: List[_Uncertainty], min_exponent: int
    ) -> None:
        for u in uncertainties:
            if not u.uncertainty.is_exact():
                u.uncertainty.set_min_exponent(min_exponent)
