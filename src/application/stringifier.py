from dataclasses import dataclass
from typing import List, Tuple
from typing import Protocol, ClassVar
from decimal import Decimal

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

    # pylint: disable=duplicate-code
    plus_minus: ClassVar[str]
    negative_sign: ClassVar[str]
    positive_sign: ClassVar[str]

    left_parenthesis: ClassVar[str]
    right_parenthesis: ClassVar[str]

    value_prefix: ClassVar[str]
    value_suffix: ClassVar[str]

    uncertainty_name_prefix: ClassVar[str]
    uncertainty_name_suffix: ClassVar[str]

    scientific_notation_prefix: ClassVar[str]
    scientific_notation_suffix: ClassVar[str]

    unit_prefix: ClassVar[str]
    unit_suffix: ClassVar[str]
    # pylint: enable=duplicate-code

    def __init__(self, config: StringifierConfig):
        self.config = config

    def create_str(self, value: Value, uncertainties: List[Uncertainty], unit: str) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.

        This string does not yet contain "\newcommand*{}".
        """
        use_scientific_notation = self._should_use_scientific_notation(value, uncertainties)
        should_use_parentheses = len(uncertainties) > 0 and (use_scientific_notation or unit != "")

        sign = self._value_to_sign_str(value)
        value_rounded, exponent, factor = self._value_to_str(value, use_scientific_notation)

        uncertainties_rounded = []
        for u in uncertainties:
            u_rounded = self._uncertainty_to_str(u, use_scientific_notation, exponent, factor)
            u_rounded = f" {self.plus_minus} {self.value_prefix}{u_rounded}{self.value_suffix}"
            if u.name != "":
                u_rounded += self.uncertainty_name_prefix
                u_rounded += self._modify_uncertainty_name(u.name)
                u_rounded += self.uncertainty_name_suffix
            uncertainties_rounded.append(u_rounded)

        # Assemble everything together
        return self._assemble_str_parts(
            sign,
            value_rounded,
            uncertainties,
            uncertainties_rounded,
            should_use_parentheses,
            use_scientific_notation,
            exponent,
            unit,
        )

    # pylint: disable-next=too-many-arguments
    def _assemble_str_parts(
        self,
        sign: str,
        value_rounded: str,
        uncertainties: List[Uncertainty],
        uncertainties_rounded: List[str],
        should_use_parentheses: bool,
        use_scientific_notation: bool,
        exponent: int,
        unit: str,
    ):
        string = f"{sign}{value_rounded}{''.join(uncertainties_rounded)}"

        if should_use_parentheses:
            string = f"{self.left_parenthesis}{string}{self.right_parenthesis}"

        if use_scientific_notation:
            e = f"{self.scientific_notation_prefix}{str(exponent)}{self.scientific_notation_suffix}"
            string += e

        if unit != "":
            string += f"{self.unit_prefix}{self._modify_unit(unit)}{self.unit_suffix}"

        return string

    def _value_to_sign_str(self, value: Value) -> str:
        return self.negative_sign if value.get() < 0 else self.positive_sign

    def _value_to_str(
        self, value: Value, use_scientific_notation: bool
    ) -> Tuple[str, int, Decimal]:
        exponent = value.get_exponent()
        factor = Decimal(f"1e{-exponent}") if use_scientific_notation else Decimal("1.0")

        value_normalized = value.get_abs() * factor
        decimal_places = (
            value.get_sig_figs() - 1 if use_scientific_notation else value.get_decimal_place()
        )

        return Helpers.round_to_n_decimal_places(value_normalized, decimal_places), exponent, factor

    def _uncertainty_to_str(
        self, u: Uncertainty, use_scientific_notation: bool, exponent: int, factor: Decimal
    ) -> str:
        uncertainty_normalized = u.uncertainty.get_abs() * factor
        decimal_places = (
            exponent - u.uncertainty.get_min_exponent()
            if use_scientific_notation
            else u.uncertainty.get_decimal_place()
        )
        return Helpers.round_to_n_decimal_places(uncertainty_normalized, decimal_places)

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

    def _modify_uncertainty_name(self, name: str) -> str:
        """
        Returns the modified value (as string).
        """
        return name
