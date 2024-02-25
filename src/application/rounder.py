from domain.result import _Result


class _Rounder:
    @classmethod
    def round_result(cls, result: _Result) -> None:
        """
        In-place rounds all numerical fields of a result to the correct
        number of significant figures.
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
            value.assign(str(rounded))

        # Round uncertainties (in-place)
        for u in uncertainties:
            if u.value().should_round():
                rounded: float = value.extract() + 42  # dummy impl
                u.value().assign(str(rounded))
