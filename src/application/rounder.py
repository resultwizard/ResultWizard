from typing import List
from decimal import Decimal

from dataclasses import dataclass
from domain.result import Result
from domain.uncertainty import Uncertainty
from domain.value import Value, DecimalPlacesError
from application.helpers import Helpers
from application import error_messages


@dataclass
class RoundingConfig:
    sigfigs: int
    decimal_places: int
    sigfigs_fallback: int
    decimal_places_fallback: int


class Rounder:

    @classmethod
    def round_result(cls, result: Result, config: RoundingConfig) -> None:
        """
        In-place rounds all numerical fields of a result to the correct
        number of significant figures.

        # Rounding hierarchy:

        1. Is uncertainty exact? Do not round.
        2. Round uncertainty according to the hierarchy below.


        # Rounding hierarchy for inexact uncertainty:

        1. Is result value exact?
           Round uncertainty according to result value.

        2. Is number of sigfigs of result given?
           Round value according to number of sigfigs.
           Round uncertainties according to value.

        3. Is number of decimal places of result given?
           Round value according to number of decimal places.
           Round uncertainties according to value.

        4. Is default for sigfigs given (not -1) (see config)?
           Round value according to number of sigfigs.
           Round uncertainties according to value.

        5. Is default for decimal places given (not -1) (see config)?
           Round value according to number of decimal places.
           Round uncertainties according to value.

        6. Is at least one uncertainty given?
           Round each uncertainty according to standard rules.
           Round value according to uncertainty with lowest min exponent.

        7. Is fallback for sigfigs given (not -1) (see config)?
           Round value according to number of sigfigs.

        8. Is fallback for decimal places given (not -1) (see config)?
           Round value according to number of decimal places.
        """

        print_decimal_places_error = cls._round_result(result, config)

        short = result.get_short_result()
        if short:
            print_decimal_places_error = (
                cls._round_result(short, config) or print_decimal_places_error
            )

        if print_decimal_places_error:
            print(error_messages.NUM_OF_DECIMAL_PLACES_TOO_LOW)

    @classmethod
    # pylint: disable-next=too-many-branches
    def _round_result(cls, result: Result, config: RoundingConfig) -> bool:
        """See the docstring of the public `round_result` for details."""

        value = result.value
        uncertainties = result.uncertainties

        print_decimal_places_error = False

        # Rounding hierarchy 1:
        if value.is_exact():
            print_decimal_places_error = cls._uncertainties_set_min_exponents(
                uncertainties, value.get_min_exponent()
            )

        # Rounding hierarchy 2:
        elif result.sigfigs is not None:
            value.set_sigfigs(result.sigfigs)
            print_decimal_places_error = cls._uncertainties_set_min_exponents(
                uncertainties, value.get_min_exponent()
            )

        # Rounding hierarchy 3:
        elif result.decimal_places is not None:
            print_decimal_places_error = cls._value_set_min_exponent(value, -result.decimal_places)
            print_decimal_places_error = cls._uncertainties_set_min_exponents(
                uncertainties, value.get_min_exponent()
            )

        # Rounding hierarchy 4:
        elif config.sigfigs > -1:
            value.set_sigfigs(config.sigfigs)
            print_decimal_places_error = cls._uncertainties_set_min_exponents(
                uncertainties, value.get_min_exponent()
            )

        # Rounding hierarchy 5:
        elif config.decimal_places > -1:
            min_exponent = -config.decimal_places
            print_decimal_places_error = cls._value_set_min_exponent(value, min_exponent)
            print_decimal_places_error = cls._uncertainties_set_min_exponents(
                uncertainties, min_exponent
            )

        # Rounding hierarchy 6:
        elif len(uncertainties) > 0:
            for u in uncertainties:
                if u.uncertainty.is_exact():
                    continue

                shift = Decimal(f"1e{-Helpers.get_exponent(u.uncertainty.get())}")
                normalized_value = abs(u.uncertainty.get()) * shift

                if round(normalized_value, 1) >= 3.0:
                    u.uncertainty.set_sigfigs(1)
                else:
                    u.uncertainty.set_sigfigs(2)

            min_exponent = min(u.uncertainty.get_min_exponent() for u in uncertainties)
            print_decimal_places_error = cls._value_set_min_exponent(value, min_exponent)

        # Rounding hierarchy 7:
        elif config.sigfigs_fallback > -1:
            value.set_sigfigs(config.sigfigs_fallback)

        # Rounding hierarchy 8:
        elif config.decimal_places_fallback > -1:
            min_exponent = -config.decimal_places_fallback
            print_decimal_places_error = cls._value_set_min_exponent(value, min_exponent)

        else:
            # This branch cannot be reached, because the config makes sure that
            # either`sigfigs_fallback` or `decimal_places_fallback` is set.
            raise RuntimeError(error_messages.INTERNAL_ROUNDER_HIERARCHY_ERROR)

        return print_decimal_places_error

    @classmethod
    def _value_set_min_exponent(cls, value: Value, min_exponent: int) -> bool:
        try:
            value.set_min_exponent(min_exponent)
            return False
        except DecimalPlacesError as _:
            return True

    @classmethod
    def _uncertainties_set_min_exponents(
        cls, uncertainties: List[Uncertainty], min_exponent: int
    ) -> bool:
        print_decimal_places_error = False

        for u in uncertainties:
            if not u.uncertainty.is_exact():
                try:
                    u.uncertainty.set_min_exponent(min_exponent)
                except DecimalPlacesError as _:
                    print_decimal_places_error = True

        return print_decimal_places_error
