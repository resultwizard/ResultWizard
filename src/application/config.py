from dataclasses import dataclass
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

    def to_json_str(self):
        return json.dumps(self.__dict__)
