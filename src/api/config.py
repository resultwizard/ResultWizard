from typing import Union

from application.config import Config


def config_init(
    sigfigs: int = 2,
    decimal_places: int = 2,
    print_always: bool = False,
):
    c = Config(sigfigs, decimal_places, print_always)
    print(c.to_json_str())
    return c


configuration = config_init()


def config(
    sigfigs: Union[int, None] = None,
    decimal_places: Union[int, None] = None,
    print_always: Union[bool, None] = None,
):
    if sigfigs is not None:
        configuration.sigfigs = sigfigs
    if decimal_places is not None:
        configuration.decimal_places = decimal_places
    if print_always is not None:
        configuration.print_always = print_always

    print(configuration.to_json_str())
