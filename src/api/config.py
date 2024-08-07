import decimal
from typing import Union, cast
from dataclasses import dataclass
from enum import Enum

from api.res import _res_cache
from application.stringifier import StringifierConfig
from application.rounder import RoundingConfig
from application import error_messages


class ChangeType(Enum):
    NO_CHANGE = 1


@dataclass
# pylint: disable-next=too-many-instance-attributes
class Config:
    """Configuration settings for the application.

    Args:
        sigfigs (int): The number of significant figures to round to.
        decimal_places (int): The number of decimal places to round to.
        print_auto (bool): Whether to print each result directly to the console.
        export_auto_to (str): If not empty, each `res()` call will automatically
            export all results to the file you specify with this keyword. You can
            still use the `export()` method to export results to other files as well.
            This option might be particularly useful when working in a Jupyter
            notebook. This way, you don't have to call `export()` manually each time
            you want to export results.
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
        siunitx_fallback (bool): Whether to use a fallback logic such that LaTeX
            commands still work with an older version of siunitx. See
            the docs for more information: TODO.
        precision (int): The precision to use for the decimal module. Defaults to
            40 in ResultsWizard. You may have to increase this if you get the error
            "Your precision is set too low".
        ignore_result_overwrite (bool): If True, you won't get any warnings if you
            overwrite a result with the same name. Defaults to False. This option
            might be useful for Jupyter notebooks when you want to re-run cells
            without getting any warnings that a result with the same name already
            exists.
    """

    sigfigs: int
    decimal_places: int
    print_auto: bool
    export_auto_to: str
    min_exponent_for_non_scientific_notation: int
    max_exponent_for_non_scientific_notation: int
    identifier: str
    sigfigs_fallback: int
    decimal_places_fallback: int
    siunitx_fallback: bool
    precision: int
    ignore_result_overwrite: bool

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
        raise ValueError(error_messages.SIGFIGS_AND_DECIMAL_PLACES_AT_SAME_TIME)

    if configuration.sigfigs_fallback > -1 and configuration.decimal_places_fallback > -1:
        raise ValueError(error_messages.SIGFIGS_FALLBACK_AND_DECIMAL_PLACES_FALLBACK_AT_SAME_TIME)

    if configuration.sigfigs_fallback <= -1 and configuration.decimal_places_fallback <= -1:
        raise ValueError(
            error_messages.ONE_OF_SIGFIGS_FALLBACK_AND_DECIMAL_PLACES_FALLBACK_MUST_BE_SET
        )

    if configuration.sigfigs == 0:
        raise ValueError(error_messages.CONFIG_SIGFIGS_VALID_RANGE)

    if configuration.sigfigs_fallback == 0:
        raise ValueError(error_messages.CONFIG_SIGFIGS_FALLBACK_VALID_RANGE)


def _set_default_config() -> None:
    global configuration  # pylint: disable=global-statement

    configuration = _default_config


_default_config = Config(
    sigfigs=-1,
    decimal_places=-1,
    print_auto=False,
    export_auto_to="",
    min_exponent_for_non_scientific_notation=-2,
    max_exponent_for_non_scientific_notation=3,
    identifier="result",
    sigfigs_fallback=2,
    decimal_places_fallback=-1,
    siunitx_fallback=False,
    precision=100,
    ignore_result_overwrite=False,
)


# pylint: disable-next=too-many-arguments
def config(
    sigfigs: Union[
        int, None, ChangeType
    ] = ChangeType.NO_CHANGE,  # -1: "per default use rounding rules instead"
    decimal_places: Union[
        int, None, ChangeType
    ] = ChangeType.NO_CHANGE,  # -1: "per default use rounding rules instead"
    print_auto: Union[bool, None, ChangeType] = ChangeType.NO_CHANGE,
    export_auto_to: Union[str, None, ChangeType] = ChangeType.NO_CHANGE,
    min_exponent_for_non_scientific_notation: Union[int, None, ChangeType] = ChangeType.NO_CHANGE,
    max_exponent_for_non_scientific_notation: Union[int, None, ChangeType] = ChangeType.NO_CHANGE,
    identifier: Union[str, None, ChangeType] = ChangeType.NO_CHANGE,
    sigfigs_fallback: Union[int, None, ChangeType] = ChangeType.NO_CHANGE,
    decimal_places_fallback: Union[
        int, None, ChangeType
    ] = ChangeType.NO_CHANGE,  # -1: "per default use sigfigs as fallback instead"
    siunitx_fallback: Union[bool, None, ChangeType] = ChangeType.NO_CHANGE,
    precision: Union[int, None, ChangeType] = ChangeType.NO_CHANGE,
    ignore_result_overwrite: Union[bool, None, ChangeType] = ChangeType.NO_CHANGE,
) -> None:
    """Set the configuration for the application. Pass in the values you want to change. Pass in None for values that you want to reset."""
    global configuration  # pylint: disable=global-statement

    if sigfigs == ChangeType.NO_CHANGE:
        sigfigs = configuration.sigfigs
    if sigfigs is None:
        sigfigs = _default_config.sigfigs

    if decimal_places == ChangeType.NO_CHANGE:
        decimal_places = configuration.decimal_places
    if decimal_places is None:
        decimal_places = _default_config.decimal_places

    if print_auto == ChangeType.NO_CHANGE:
        print_auto = configuration.print_auto
    if print_auto is None:
        print_auto = _default_config.print_auto

    if export_auto_to == ChangeType.NO_CHANGE:
        export_auto_to = configuration.export_auto_to
    if export_auto_to is None:
        export_auto_to = _default_config.export_auto_to

    if min_exponent_for_non_scientific_notation == ChangeType.NO_CHANGE:
        min_exponent_for_non_scientific_notation = (
            configuration.min_exponent_for_non_scientific_notation
        )
    if min_exponent_for_non_scientific_notation is None:
        min_exponent_for_non_scientific_notation = (
            _default_config.min_exponent_for_non_scientific_notation
        )

    if max_exponent_for_non_scientific_notation == ChangeType.NO_CHANGE:
        max_exponent_for_non_scientific_notation = (
            configuration.max_exponent_for_non_scientific_notation
        )
    if max_exponent_for_non_scientific_notation is None:
        max_exponent_for_non_scientific_notation = (
            _default_config.max_exponent_for_non_scientific_notation
        )

    if identifier == ChangeType.NO_CHANGE:
        identifier = configuration.identifier
    if identifier is None:
        identifier = _default_config.identifier

    if sigfigs_fallback == ChangeType.NO_CHANGE:
        sigfigs_fallback = configuration.sigfigs_fallback
    if sigfigs_fallback is None:
        sigfigs_fallback = _default_config.sigfigs_fallback

    if decimal_places_fallback == ChangeType.NO_CHANGE:
        decimal_places_fallback = configuration.decimal_places_fallback
    if decimal_places_fallback is None:
        decimal_places_fallback = _default_config.decimal_places_fallback

    if siunitx_fallback == ChangeType.NO_CHANGE:
        siunitx_fallback = configuration.siunitx_fallback
    if siunitx_fallback is None:
        siunitx_fallback = _default_config.siunitx_fallback

    if precision == ChangeType.NO_CHANGE:
        precision = configuration.precision
    if precision is None:
        precision = _default_config.precision

    if ignore_result_overwrite == ChangeType.NO_CHANGE:
        ignore_result_overwrite = configuration.ignore_result_overwrite
    if ignore_result_overwrite is None:
        ignore_result_overwrite = _default_config.ignore_result_overwrite

    decimal.DefaultContext.prec = precision
    decimal.setcontext(decimal.DefaultContext)

    configuration = Config(
        sigfigs,
        decimal_places,
        print_auto,
        export_auto_to,
        min_exponent_for_non_scientific_notation,
        max_exponent_for_non_scientific_notation,
        identifier,
        sigfigs_fallback,
        decimal_places_fallback,
        siunitx_fallback,
        precision,
        ignore_result_overwrite,
    )

    _res_cache.configure(not ignore_result_overwrite)

    _check_config()


configuration = cast(Config, None)  # pylint: disable=invalid-name
_set_default_config()
