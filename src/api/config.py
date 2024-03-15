from typing import Union, cast

from dataclasses import dataclass
from application.latexer import LaTeXConfig


@dataclass
class _Config:
    """Configuration settings for the application.

    Args:
        sigfigs (int): The number of significant figures to round to.
        decimal_places (int): The number of decimal places to round to.
        print_auto (bool): Whether to print each result directly to the console.
        min_exponent_for_non_scientific_notation (int): The minimum exponent for non-scientific notation.
        max_exponent_for_non_scientific_notation (int): The maximum exponent for non-scientific notation.
        identifier (str): The identifier for the result variable in LaTeX.
    """

    sigfigs: int
    decimal_places: int
    print_auto: bool
    min_exponent_for_non_scientific_notation: int
    max_exponent_for_non_scientific_notation: int
    identifier: str

    def to_latex_config(self) -> LaTeXConfig:
        return LaTeXConfig(
            self.min_exponent_for_non_scientific_notation,
            self.max_exponent_for_non_scientific_notation,
            self.identifier,
        )


def config_init(
    sigfigs: int = 2,
    decimal_places: int = -1,  # -1: "per default use sigfigs instead"
    print_auto: bool = False,
    min_exponent_for_non_scientific_notation: int = -2,
    max_exponent_for_non_scientific_notation: int = 3,
    identifier: str = "res",
) -> None:
    # pylint: disable-next=global-statement
    global configuration

    configuration = _Config(
        sigfigs,
        decimal_places,
        print_auto,
        min_exponent_for_non_scientific_notation,
        max_exponent_for_non_scientific_notation,
        identifier,
    )


configuration = cast(_Config, None)
config_init()


def config(
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
    print_auto: Union[bool, None] = None,
):
    if sigfigs is not None:
        configuration.sigfigs = sigfigs
    if decimal_places is not None:
        configuration.decimal_places = decimal_places
    if print_auto is not None:
        configuration.print_auto = print_auto
