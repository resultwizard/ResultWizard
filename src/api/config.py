import decimal
from typing import Union, cast
from dataclasses import dataclass

from api.res import _res_cache
from application.stringifier import StringifierConfig
from application.rounder import RoundingConfig
from application import error_messages


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
    table_identifier: str
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
            self.table_identifier,
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


# pylint: disable-next=too-many-arguments
def config_init(
    sigfigs: int = -1,  # -1: "per default use rounding rules instead"
    decimal_places: int = -1,  # -1: "per default use rounding rules instead"
    print_auto: bool = False,
    export_auto_to: str = "",
    min_exponent_for_non_scientific_notation: int = -2,
    max_exponent_for_non_scientific_notation: int = 3,
    identifier: str = "result",
    table_identifier: str = "table",
    sigfigs_fallback: int = 2,
    decimal_places_fallback: int = -1,  # -1: "per default use sigfigs as fallback instead"
    siunitx_fallback: bool = False,
    precision: int = 100,
    ignore_result_overwrite: bool = False,
) -> None:
    global configuration  # pylint: disable=global-statement

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
        table_identifier,
        sigfigs_fallback,
        decimal_places_fallback,
        siunitx_fallback,
        precision,
        ignore_result_overwrite,
    )

    _res_cache.configure(not ignore_result_overwrite)

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
    if sigfigs is not None:
        configuration.sigfigs = sigfigs
        if sigfigs > -1 and decimal_places is None:
            configuration.decimal_places = -1
    if decimal_places is not None:
        configuration.decimal_places = decimal_places
        if decimal_places > -1 and sigfigs is None:
            configuration.sigfigs = -1

    if print_auto is not None:
        configuration.print_auto = print_auto

    if sigfigs_fallback is not None:
        configuration.sigfigs_fallback = sigfigs_fallback
        if sigfigs_fallback > -1 and decimal_places_fallback is None:
            configuration.decimal_places_fallback = -1
    if decimal_places_fallback is not None:
        configuration.decimal_places_fallback = decimal_places_fallback
        if decimal_places_fallback > -1 and sigfigs_fallback is None:
            configuration.sigfigs_fallback = -1

    _check_config()
