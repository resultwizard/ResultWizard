from typing import Union, cast

from dataclasses import dataclass
from application.stringifier import StringifierConfig
from application.rounder import RoundingConfig


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Config:
    """Configuration settings for the application.

    Args:
        sigfigs (int): The number of significant figures to round to.
        decimal_places (int): The number of decimal places to round to.
        print_auto (bool): Whether to print each result directly to the console.
        min_exponent_for_non_scientific_notation (int): The minimum exponent
            for non-scientific notation.
        max_exponent_for_non_scientific_notation (int): The maximum exponent
            for non-scientific notation.
        identifier (str): The identifier for the result variable in LaTeX. This
            identifier will be prefix each result variable name.
        sigfigs_fallback (int): The number of significant figures to use as a
            fallback if other rounding rules don't apply.
        decimal_places_fallback (int): The number of decimal places to use as
            a fallback if other rounding rules don't apply.
    """

    sigfigs: int
    decimal_places: int
    print_auto: bool
    min_exponent_for_non_scientific_notation: int
    max_exponent_for_non_scientific_notation: int
    identifier: str
    sigfigs_fallback: int
    decimal_places_fallback: int

    def to_stringifier_config(self) -> StringifierConfig:
        return StringifierConfig(
            self.min_exponent_for_non_scientific_notation,
            self.max_exponent_for_non_scientific_notation,
            self.identifier,
        )

    def to_rounding_config(self) -> RoundingConfig:
        return RoundingConfig(
            self.sigfigs,
            self.decimal_places,
            self.sigfigs_fallback,
            self.decimal_places_fallback,
        )


def _check_config() -> None:
    if configuration.sigfigs > -1 and configuration.decimal_places > -1:
        raise ValueError(
            "You can't set both sigfigs and decimal places at the same time. "
            "Please choose one or the other."
        )

    if configuration.sigfigs_fallback > -1 and configuration.decimal_places_fallback > -1:
        raise ValueError(
            "You can't set both sigfigs_fallback and decimal_places_fallback at the same time. "
            "Please choose one or the other."
        )

    if configuration.sigfigs_fallback <= -1 and configuration.decimal_places_fallback <= -1:
        raise ValueError(
            "You need to set either sigfigs_fallback or decimal_places_fallback. "
            "Please choose one."
        )

    if configuration.sigfigs == 0:
        raise ValueError("sigfigs must be greater than 0 (or -1).")

    if configuration.sigfigs_fallback == 0:
        raise ValueError("sigfigs_fallback must be greater than 0 (or -1).")


# pylint: disable-next=too-many-arguments
def config_init(
    sigfigs: int = -1,  # -1: "per default use rounding rules instead"
    decimal_places: int = -1,  # -1: "per default use rounding rules instead"
    print_auto: bool = False,
    min_exponent_for_non_scientific_notation: int = -2,
    max_exponent_for_non_scientific_notation: int = 3,
    identifier: str = "res",
    sigfigs_fallback: int = 2,
    decimal_places_fallback: int = -1,  # -1: "per default use sigfigs as fallback instead"
) -> None:
    global configuration  # pylint: disable=global-statement

    configuration = Config(
        sigfigs,
        decimal_places,
        print_auto,
        min_exponent_for_non_scientific_notation,
        max_exponent_for_non_scientific_notation,
        identifier,
        sigfigs_fallback,
        decimal_places_fallback,
    )

    _check_config()


configuration = cast(Config, None)  # pylint: disable=invalid-name
config_init()


def config(
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
    print_auto: Union[bool, None] = None,
    sigfigs_fallback: Union[int, None] = None,
    decimal_places_fallback: Union[int, None] = None,
):
    if sigfigs is not None and sigfigs > -1 and decimal_places is not None and decimal_places > -1:
        raise ValueError(
            "You can't set both sigfigs and decimal places at the same time. "
            "Please choose one or the other."
        )

    if (
        sigfigs_fallback is not None
        and sigfigs_fallback > -1
        and decimal_places_fallback is not None
        and decimal_places_fallback > -1
    ):
        raise ValueError(
            "You can't set both sigfigs_fallback and decimal_places_fallback at the same time. "
            "Please choose one or the other."
        )

    if sigfigs is not None:
        configuration.sigfigs = sigfigs
        if sigfigs > -1:
            configuration.decimal_places = -1
    if decimal_places is not None:
        configuration.decimal_places = decimal_places
        if decimal_places > -1:
            configuration.sigfigs = -1

    if print_auto is not None:
        configuration.print_auto = print_auto

    if sigfigs_fallback is not None:
        configuration.sigfigs_fallback = sigfigs_fallback
        if sigfigs_fallback > -1:
            configuration.decimal_places_fallback = -1
    if decimal_places_fallback is not None:
        configuration.decimal_places_fallback = decimal_places_fallback
        if decimal_places_fallback > -1:
            configuration.sigfigs_fallback = -1

    _check_config()
