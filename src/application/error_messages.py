# Config and res error messages
SIGFIGS_AND_DECIMAL_PLACES_AT_SAME_TIME = (
    "You can't set both sigfigs and decimal places at the same time. "
    "Please choose one or the other."
)
SIGFIGS_FALLBACK_AND_DECIMAL_PLACES_FALLBACK_AT_SAME_TIME = (
    "You can't set both sigfigs_fallback and decimal_places_fallback at the same time. "
    "Please choose one or the other."
)
ONE_OF_SIGFIGS_FALLBACK_AND_DECIMAL_PLACES_FALLBACK_MUST_BE_SET = (
    "You need to set either sigfigs_fallback or decimal_places_fallback. Please choose one."
)
CONFIG_SIGFIGS_VALID_RANGE = "sigfigs must be greater than 0 (or -1)."
CONFIG_SIGFIGS_FALLBACK_VALID_RANGE = "sigfigs_fallback must be greater than 0 (or -1)."
SIGFIGS_AND_EXACT_VALUE_AT_SAME_TIME = (
    "You can't set sigfigs and supply an exact value. Please do one or the other."
)
DECIMAL_PLACES_AND_EXACT_VALUE_AT_SAME_TIME = (
    "You can't set decimal places and supply an exact value. Please do one or the other."
)
UNCERT_AND_SYS_STAT_AT_SAME_TIME = (
    "You can't set uncertainties and systematic/statistical uncertainties at the same time. "
    "Please provide either the `uncert` param or the `sys`/`stat` params."
)

# Parser error messages (generic)
STRING_MUST_BE_NUMBER = "String value must be a valid number, not {value}"
FIELD_MUST_BE_STRING = "{field} must be a string, not {type}}"
FIELD_MUST_BE_INT = "{field} must be an int, not {type}}"
FIELD_MUST_NOT_BE_EMPTY = "{field} must not be empty"
FIELD_MUST_BE_POSITIVE = "{field} must be positive"
FIELD_MUST_BE_NON_NEGATIVE = "{field} must be non-negative"

# Parser error messages (specific)
STRING_EMPTY_AFTER_IGNORING_INVALID_CHARS = (
    "After ignoring invalid characters, the specified name is empty."
)
VALUE_TYPE = "{field} must be a float, int, Decimal or string, not {type}"
UNCERTAINTIES_MUST_BE_TUPLES_OR = (
    "Each uncertainty must be a tuple or a float/int/Decimal/str, not {type}"
)
UNIT_NOT_PASSED_AS_KEYWORD_ARGUMENT = (
    "Could it be the case you provided a unit but forgot `unit=` in front of it?"
)

# Helpers:
PRECISION_TOO_LOW = (
    "Your precision is set too low to be able to process the given value without any loss of "
    "precision. Set a higher precision via: `wiz.config_init (precision=<a-high-enough-number>)`."
)
NUMBER_TO_WORD_TOO_HIGH = "For variable names, only use numbers between 0 and 999. Got {number}."

# Runtime errors:
SHORT_RESULT_IS_NONE = "Short result is None, but there should be at least two uncertainties."
INTERNAL_ROUNDER_HIERARCHY_ERROR = "Internal rounder hierarchy error. Please report this bug."
INTERNAL_MIN_EXPONENT_ERROR = "Internal min_exponent not set error. Please report this bug."
ROUND_TO_NEGATIVE_DECIMAL_PLACES = (
    "Internal rounding to negative decimal places. Please report this bug."
)

# Warnings:
INVALID_CHARS_IGNORED = "Invalid characters in name were ignored: {chars}"
NUM_OF_DECIMAL_PLACES_TOO_LOW = (
    "Warning: At least one of the specified values is out of range of the specified "
    "number of decimal places. Thus, the exported value will be 0."
)
RESULT_SHADOWED = "Warning: A result with the name '{name}' already exists and will be overwritten."
