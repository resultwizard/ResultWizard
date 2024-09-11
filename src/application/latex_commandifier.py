from application.stringifier import Stringifier
from application.helpers import Helpers
from application.latex_ifelse import LatexIfElseBuilder
from application import error_messages
from domain.result import Result


class LatexCommandifier:
    """Makes use of a LaTeX stringifier to embed a result (e.g. \\qty{1.23}{\\m})
    into a LaTeX command (e.g. \\newcommand{\\resultImportant}{\\qty{1.23}{\\m}}).
    """

    def __init__(self, stringifier: Stringifier):
        self.s = stringifier

    def result_to_latex_cmd(self, result: Result) -> str:
        """
        Returns the result as LaTeX command to be used in a .tex file.
        """
        builder = LatexIfElseBuilder()

        cmd_name = f"{self.s.config.identifier}{Helpers.capitalize(result.name)}"
        latex_str = rf"\newcommand*{{\{cmd_name}}}[1][]{{" + "\n"

        # Default case (full result) & value
        builder.add_branch("", self.s.create_str(result))
        builder.add_branch("value", self.s.create_str_value(result))

        # Without uncertainty
        if len(result.uncertainties) > 0:
            builder.add_branch("withoutUncert", self.s.create_str_without_uncert(result))

        # Single uncertainties
        for i, u in enumerate(result.uncertainties):
            if len(result.uncertainties) == 1:
                uncertainty_name = "uncert"
            else:
                uncertainty_name = u.name if u.name != "" else Helpers.number_to_word(i + 1)
                uncertainty_name = f"uncert{Helpers.capitalize(uncertainty_name)}"
            uncertainty_latex_str = self.s.create_str_uncert(u, result.unit)
            builder.add_branch(uncertainty_name, uncertainty_latex_str)

        # Total uncertainty and short result
        if len(result.uncertainties) >= 2:
            short_result = result.get_short_result()
            if short_result is None:
                raise RuntimeError(error_messages.SHORT_RESULT_IS_NONE)
            uncertainty_latex_str = self.s.create_str_uncert(
                short_result.uncertainties[0], result.unit
            )
            builder.add_branch("uncertTotal", uncertainty_latex_str)
            builder.add_branch("short", self.s.create_str(short_result))

        # Unit
        if result.unit != "":
            builder.add_branch("unit", rf"\unit{{{result.unit}}}")
            builder.add_branch("withoutUnit", self.s.create_str_without_unit(result))

        # Error message
        keywords = builder.keywords
        if len(keywords) > 0:
            error_message = "Use one of these keywords (or no keyword at all): "
            error_message += ", ".join([rf"\texttt{{{k}}}" for k in keywords])
        else:
            error_message = "This variable can only be used without keywords."
        builder.add_else(rf"\scriptsize{{\textbf{{{error_message}}}}}")

        latex_str += builder.build()
        latex_str += "\n}"

        return latex_str

    def result_to_latex_str(self, result: Result) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.
        """
        return self.s.create_str(result)
