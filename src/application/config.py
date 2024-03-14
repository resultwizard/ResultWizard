from dataclasses import dataclass
from application.latexer import LaTeXConfig
import json


@dataclass
class Config:
    """Configuration settings for the application.

    Args:
        sigfigs (int): The number of significant figures to round to.
        decimal_places (int): The number of decimal places to round to.
        print_always (bool): Whether to print each result directly to the console.
    """

    sigfigs: int
    decimal_places: int
    print_always: bool
    min_exponent_for_non_scientific_notation: int
    max_exponent_for_non_scientific_notation: int
    identifier: str

    def to_json_str(self):
        return json.dumps(self.__dict__)

    def to_latex_config(self) -> LaTeXConfig:
        return LaTeXConfig(
            self.min_exponent_for_non_scientific_notation,
            self.max_exponent_for_non_scientific_notation,
            self.identifier,
        )
