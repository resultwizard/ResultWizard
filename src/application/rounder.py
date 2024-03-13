from domain.result import _Result


class _Rounder:
    @classmethod
    def round_result(cls, result: _Result) -> None:
        """
        In-place rounds all numerical fields of a result to the correct
        number of significant figures.

        Rounding hierarchy:

        1. Is value exact? Do not round! Rounding hierarchy of uncertainties:
            1. Is uncertainty exact? Do not round!
            2. Round uncertainty according to value.
        2. Is number of sigfigs given? Round value according to number of sigfigs! Round uncertainties according to value.
        3. Is number of decimal places given? Round value according to number of decimal places! Round uncertainties according to value.
        4. Is at least one uncertainty given? Round each uncertainty according to standard rules! Round value according to uncertainty with lowest min exponent!
        5. Round value to 2 sigfigs.
        """
        value = result.value
        uncertainties = result.uncertainties

        # TODO @paul: round values and uncertainties here according to pre-defined
        # rules. Please do not add an external config yet. Instead, hard-code
        # variables like the number of significant figures in this method or
        # somewhere in this file here. We will outsource this to a config method
        # in a later step.
        # TODO: Maybe extract the following parts into separate methods

        # Round value
        if value.should_round():
            rounded: float = value.extract() + 42  # dummy impl
            # value.assign(str(rounded))

        # Round uncertainties (in-place)
        for u in uncertainties:
            if u.value().should_round():
                rounded: float = value.extract() + 42  # dummy impl
                # u.value().assign(str(rounded))
