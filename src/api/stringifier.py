import api.config as c
from domain.result import _Result
from application.latexer import _LaTeXer


class Stringifier:
    @classmethod
    def result_to_str(cls, result: _Result):
        """
        Returns the result as human-readable string.
        """

        # Get LaTeX string:
        unit_placeholder = "--" if result.unit != "" else ""
        latex_str = _LaTeXer(c.configuration.to_latex_config()).create_latex_str(
            result.value, result.uncertainties, unit_placeholder
        )

        # Replace placeholder with actual unit:
        if result.unit != "":
            unit = (
                result.unit.replace(r"\per", "/")
                .replace(r"\squared", "^2")
                .replace(r"\cubed", "^3")
                .replace("\\", "")
            )

            if unit[0] == "/":
                unit = f"1{unit}"

            latex_str = latex_str.replace(r"\, \unit{--}", f" {unit}")

        # Remove LaTeX commands:
        latex_str = (
            latex_str.replace(r"\left(", "(")
            .replace(r"\right)", ")")
            .replace(r"\pm", "±")
            .replace(r"_{\text{", " (")
            .replace("}}", ")")
            .replace(r" \cdot 10^{", "e")
            .replace(r"}", "")
        )

        return f"{result.name} = {latex_str}"
