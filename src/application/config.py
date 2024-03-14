import json


class Config:
    """Configuration settings for the application."""

    sigfigs_default = 2
    decimal_places_default = 2
    print_always_default = False

    def __init__(
        self,
        sigfigs=sigfigs_default,
        decimal_places=decimal_places_default,
        print_always=print_always_default,
    ):
        self.sigfigs = sigfigs
        self.decimal_places = decimal_places
        self.print_always = print_always

    def to_json_str(self):
        return json.dumps(self.__dict__)
