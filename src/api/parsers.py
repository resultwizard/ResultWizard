from typing import Union, List, Tuple

from application.helpers import _Helpers
from domain.value import _Value
from domain.uncertainty import _Uncertainty


def check_if_number_string(value: str) -> None:
    """Raises a ValueError if the string is not a valid number."""
    try:
        float(value)
    except ValueError as exc:
        raise ValueError(f"String value must be a valid number, not {value}") from exc


def parse_name(name: str) -> str:
    """Parses the name."""
    if not isinstance(name, str):
        raise TypeError(f"`name` must be a string, not {type(name)}")

    if name == "":
        raise ValueError("`name` must not be empty")

    name = (
        name.replace("ä", "ae")
        .replace("Ä", "Ae")
        .replace("ö", "oe")
        .replace("Ö", "Oe")
        .replace("ü", "ue")
        .replace("Ü", "Ue")
        .replace("ß", "ss")
        .replace("ẞ", "Ss")
    )

    parsed_name = ""
    next_chat_upper = False

    ignored_chars = set()

    for char in name:
        if char.isalpha():
            if next_chat_upper:
                parsed_name += char.upper()
                next_chat_upper = False
            else:
                parsed_name += char
        elif char.isdigit():
            digit = _Helpers.number_to_word(int(char))
            if parsed_name == "":
                parsed_name += digit
            else:
                parsed_name += digit[0].upper() + digit[1:]
            next_chat_upper = True
        elif char in [" ", "_", "-"]:
            next_chat_upper = True
        else:
            ignored_chars.add(char)

    if len(ignored_chars) > 0:
        print(f"Invalid characters in name were ignored: {', '.join(ignored_chars)}")

    if parsed_name == "":
        raise ValueError("After ignoring invalid characters, the specified name is empty.")

    return parsed_name


def parse_unit(unit: str) -> str:
    """Parses the unit."""
    if not isinstance(unit, str):
        raise TypeError(f"`unit` must be a string, not {type(unit)}")

    # TODO: maybe add some basic checks to catch siunitx errors, e.g.
    # unsupported symbols etc. But maybe leave this to LaTeX and just return
    # the LaTeX later on. But catching it here would be more user-friendly,
    # as the user would get immediate feedback and not only once they try to
    # export the results.
    return unit


def parse_sigfigs(sigfigs: Union[int, None]) -> Union[int, None]:
    """Parses the number of sigfigs."""
    if sigfigs is None:
        return None

    if not isinstance(sigfigs, int):
        raise TypeError(f"`sigfigs` must be an int, not {type(sigfigs)}")

    if sigfigs < 1:
        raise ValueError("`sigfigs` must be positive")

    return sigfigs


def parse_decimal_places(decimal_places: Union[int, None]) -> Union[int, None]:
    """Parses the number of sigfigs."""
    if decimal_places is None:
        return None

    if not isinstance(decimal_places, int):
        raise TypeError(f"`decimal_places` must be an int, not {type(decimal_places)}")

    if decimal_places < 0:
        raise ValueError("`decimal_places` must be non-negative")

    return decimal_places


def parse_value(value: Union[float, int, str]) -> _Value:
    """Converts the value to a _Value object."""
    if not isinstance(value, (float, int, str)):
        raise TypeError(f"`value` must be a float, int or string, not {type(value)}")

    if isinstance(value, str):
        check_if_number_string(value)
        return parse_exact_value(value)

    if isinstance(value, int):
        value = float(value)

    return _Value(value)


def parse_exact_value(value: str) -> _Value:
    # Determine min exponent:
    exponent_offset = 0
    value_str = value
    if "e" in value_str:
        exponent_offset = int(value_str[value_str.index("e") + 1 :])
        value_str = value_str[0 : value_str.index("e")]
    if "." in value:
        decimal_places = len(value_str) - value_str.index(".") - 1
        min_exponent = -decimal_places + exponent_offset
    else:
        min_exponent = exponent_offset

    return _Value(float(value), min_exponent)


def parse_uncertainties(
    uncertainties: Union[
        float,
        int,
        str,
        Tuple[Union[float, int, str], str],
        List[Union[float, str, Tuple[Union[float, int, str], str]]],
    ]
) -> List[_Uncertainty]:
    """Converts the uncertainties to a list of _Uncertainty objects."""
    uncertainties_res = []

    # no list, but a single value was given
    if isinstance(uncertainties, (float, int, str, Tuple)):
        uncertainties = [uncertainties]

    assert isinstance(uncertainties, List)

    for uncert in uncertainties:
        if isinstance(uncert, (float, int, str)):
            uncertainties_res.append(_Uncertainty(_parse_uncertainty_value(uncert)))

        elif isinstance(uncert, Tuple):
            if not isinstance(uncert[0], (float, int, str)):
                raise TypeError(
                    "First argument of uncertainty-tuple must be a float,"
                    + f" int or a string, not {type(uncert[0])}"
                )
            uncertainties_res.append(
                _Uncertainty(_parse_uncertainty_value(uncert[0]), parse_name(uncert[1]))
            )

        else:
            raise TypeError(
                f"Each uncertainty must be a tuple or a float/int/str, not {type(uncert)}"
            )

    return uncertainties_res


def _parse_uncertainty_value(value: Union[float, int, str]) -> _Value:
    """Parses the value of an uncertainty."""

    if isinstance(value, str):
        check_if_number_string(value)
        return_value = parse_exact_value(value)
    else:
        if isinstance(value, int):
            value = float(value)
        return_value = _Value(value)

    if return_value.get() <= 0:
        raise ValueError("Uncertainty must be positive.")

    return return_value
