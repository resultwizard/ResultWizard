from dataclasses import dataclass
from typing import List
from typing import Protocol, ClassVar

# for why we use a Protocol instead of a ABC class, see
# https://github.com/microsoft/pyright/issues/2601#issuecomment-977053380

from domain.value import Value
from domain.uncertainty import Uncertainty
from application.helpers import Helpers


@dataclass
class StringifierConfig:
    min_exponent_for_non_scientific_notation: int
    max_exponent_for_non_scientific_notation: int
    identifier: str


class Stringifier(Protocol):
    """
    Provides methods to convert results to strings of customizable pattern.

    We assume the result to already be correctly rounded at this point.
    """

    config: StringifierConfig

    plus_minus: ClassVar[str]
    negative_sign: ClassVar[str]
    positive_sign: ClassVar[str]

    left_parenthesis: ClassVar[str]
    right_parenthesis: ClassVar[str]

    value_prefix: ClassVar[str]
    value_suffix: ClassVar[str]

    error_name_prefix: ClassVar[str]
    error_name_suffix: ClassVar[str]

    scientific_notation_prefix: ClassVar[str]
    scientific_notation_suffix: ClassVar[str]

    unit_prefix: ClassVar[str]
    unit_suffix: ClassVar[str]

    def __init__(self, config: StringifierConfig):
        self.config = config

    def create_str(self, value: Value, uncertainties: List[Uncertainty], unit: str) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.

        This string does not yet contain "\newcommand*{}".
        """
        string = ""

        use_scientific_notation = self._should_use_scientific_notation(value, uncertainties)
        has_unit = unit != ""
        should_use_parentheses = len(uncertainties) > 0 and (use_scientific_notation or has_unit)

        sign = self.negative_sign if value.get() < 0 else self.positive_sign
        exponent = value.get_exponent()
        factor = 10 ** (-exponent) if use_scientific_notation else 1.0
        value_normalized = value.get_abs() * factor
        decimal_places = (
            value.get_sig_figs() - 1 if use_scientific_notation else value.get_decimal_place()
        )

        if should_use_parentheses:
            string += self.left_parenthesis
        string += sign
        value_str = Helpers.round_to_n_decimal_places(value_normalized, decimal_places)
        string += self.value_prefix + value_str + self.value_suffix

        for u in uncertainties:
            uncertainty_normalized = u.uncertainty.get_abs() * factor
            decimal_places = (
                exponent - u.uncertainty.get_min_exponent()
                if use_scientific_notation
                else u.uncertainty.get_decimal_place()
            )
            string += self.plus_minus
            uncert_str = Helpers.round_to_n_decimal_places(uncertainty_normalized, decimal_places)
            string += self.value_prefix + uncert_str + self.value_suffix
            if u.name != "":
                string += f"{self.error_name_prefix}{u.name}{self.error_name_suffix}"

        if should_use_parentheses:
            string += self.right_parenthesis
        if use_scientific_notation:
            string += (
                f"{self.scientific_notation_prefix}{str(exponent)}{self.scientific_notation_suffix}"
            )
        if has_unit:
            string += f"{self.unit_prefix}{self._modify_unit(unit)}{self.unit_suffix}"

        return string

    def _should_use_scientific_notation(
        self, value: Value, uncertainties: List[Uncertainty]
    ) -> bool:
        """
        Returns whether scientific notation should be used for the given value and uncertainties.
        """
        exponent = value.get_exponent()
        if (
            exponent < self.config.min_exponent_for_non_scientific_notation
            or exponent > self.config.max_exponent_for_non_scientific_notation
        ):
            return True

        if value.get_min_exponent() > 0:
            return True

        for u in uncertainties:
            if u.uncertainty.get_min_exponent() > 0:
                return True

        return False

    def _modify_unit(self, unit: str) -> str:
        """
        Returns the modified unit.
        """
        return unit

    def _modify_value(self, value: str) -> str:
        """
        Returns the modified value (as string).
        """
        return value
