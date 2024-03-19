from typing import Union, List, Tuple
from decimal import Decimal

from application.helpers import Helpers
import application.error_messages as error_messages
from domain.value import Value
from domain.uncertainty import Uncertainty


def check_if_number_string(value: str) -> None:
    """Raises a ValueError if the string is not a valid number."""
    try:
        float(value)
    except ValueError as exc:
        raise ValueError(error_messages.STRING_MUST_BE_NUMBER.format(value)) from exc


def parse_name(name: str) -> str:
    """Parses the name."""
    if not isinstance(name, str):
        raise TypeError(error_messages.FIELD_MUST_BE_STRING.format(field="`name`", type=type(name)))

    if name == "":
        raise ValueError(error_messages.FIELD_MUST_NOT_BE_EMPTY.format(field="`name`"))

    name = (
        name.replace("ä", "ae")
        .replace("Ä", "Ae")
        .replace("ö", "oe")
        .replace("Ö", "Oe")
        .replace("ü", "ue")
        .replace("Ü", "Ue")
        .replace("ß", "ss")
        # we use "SS" instead of "Ss" as replacement for "ẞ"
        # since "ẞ" is only allowed in uppercase names in German
        .replace("ẞ", "SS")
    )

    parsed_name = ""
    next_char_upper = False
    ignored_chars = set()

    while name != "":
        char = name[0]

        if char.isalpha():
            if next_char_upper:
                parsed_name += char.upper()
                next_char_upper = False
            else:
                parsed_name += char
        elif char.isdigit():
            num_digits = _greedily_count_digits_at_start_of_str(name)
            word = Helpers.number_to_word(int(name[:num_digits]))
            if parsed_name != "":
                word = Helpers.capitalize(word)
            parsed_name += word
            next_char_upper = True
            name = name[num_digits:]  # Skip the parsed digits
            continue
        elif char in [" ", "_", "-"]:
            next_char_upper = True
        else:
            ignored_chars.add(char)

        name = name[1:]

    if len(ignored_chars) > 0:
        print(error_messages.INVALID_CHARS_IGNORED.format(chars=", ".join(ignored_chars)))

    if parsed_name == "":
        raise ValueError(error_messages.STRING_EMPTY_AFTER_IGNORING_INVALID_CHARS)

    return parsed_name


def _greedily_count_digits_at_start_of_str(word: str) -> int:
    """Counts the number of digits at the start of the string."""
    num_digits = 0
    for c in word:
        if c.isdigit():
            num_digits += 1
        else:
            break
    return num_digits


def parse_unit(unit: str) -> str:
    """Parses the unit."""
    if not isinstance(unit, str):
        raise TypeError(error_messages.FIELD_MUST_BE_STRING.format(field="`unit`", type=type(unit)))

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
        raise TypeError(
            error_messages.FIELD_MUST_BE_INT.format(field="`sigfigs`", type=type(sigfigs))
        )

    if sigfigs < 1:
        raise ValueError(error_messages.FIELD_MUST_BE_POSITIVE.format(field="`sigfigs`"))

    return sigfigs


def parse_decimal_places(decimal_places: Union[int, None]) -> Union[int, None]:
    """Parses the number of sigfigs."""
    if decimal_places is None:
        return None

    if not isinstance(decimal_places, int):
        raise TypeError(
            error_messages.FIELD_MUST_BE_INT.format(
                field="`decimal_places`", type=type(decimal_places)
            )
        )

    if decimal_places < 0:
        raise ValueError(error_messages.FIELD_MUST_BE_NON_NEGATIVE.format(field="`decimal_places`"))

    return decimal_places


def parse_value(value: Union[float, int, str, Decimal]) -> Value:
    """Converts the value to a _Value object."""
    if not isinstance(value, (float, int, str, Decimal)):
        raise TypeError(error_messages.VALUE_TYPE.format(field="`value`", type=type(value)))

    if isinstance(value, str):
        check_if_number_string(value)
        return parse_exact_value(value)

    return Value(Decimal(value))


def parse_exact_value(value: str) -> Value:
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

    return Value(Decimal(value), min_exponent)


def parse_uncertainties(
    uncertainties: Union[
        float,
        int,
        str,
        Decimal,
        Tuple[Union[float, int, str, Decimal], str],
        List[Union[float, int, str, Decimal, Tuple[Union[float, int, str, Decimal], str]]],
    ]
) -> List[Uncertainty]:
    """Converts the uncertainties to a list of _Uncertainty objects."""
    uncertainties_res = []

    # no list, but a single value was given
    if isinstance(uncertainties, (float, int, str, Decimal, Tuple)):
        uncertainties = [uncertainties]

    for uncert in uncertainties:
        if isinstance(uncert, (float, int, str, Decimal)):
            uncertainties_res.append(Uncertainty(_parse_uncertainty_value(uncert)))

        elif isinstance(uncert, Tuple):
            if not isinstance(uncert[0], (float, int, str, Decimal)):
                raise TypeError(
                    error_messages.VALUE_TYPE.format(
                        field="First argument of uncertainty-tuple", type=type(uncert[0])
                    )
                )
            uncertainties_res.append(
                Uncertainty(_parse_uncertainty_value(uncert[0]), parse_name(uncert[1]))
            )

        else:
            raise TypeError(
                error_messages.UNCERTAINTIES_MUST_BE_TUPLES_OR.format(type=type(uncert))
            )

    return uncertainties_res


def _parse_uncertainty_value(value: Union[float, int, str, Decimal]) -> Value:
    """Parses the value of an uncertainty."""

    if isinstance(value, str):
        check_if_number_string(value)
        return_value = parse_exact_value(value)
    else:
        return_value = Value(Decimal(value))

    if return_value.get() <= 0:
        raise ValueError(error_messages.FIELD_MUST_BE_POSITIVE.format(field="Uncertainty"))

    return return_value
