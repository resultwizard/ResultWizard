from domain.result import _Result


class _LaTeXer:
    @classmethod
    def result_to_latex_cmd(cls, result: _Result) -> str:
        """
        Returns the result as LaTeX command to be used in a .tex file.
        """
        return f"\\newcommand*{{\\{result.name}}}{{{cls.result_to_latex_str(result)}}}"

    @classmethod
    def result_to_latex_str(cls, result: _Result) -> str:
        """
        Returns the result as LaTeX string making use of the siunitx package.

        This string does not yet contain "\newcommand*{}".
        """
        # TODO @paul: Implement this method properly
        uncertainties_str = ", ".join([str(u) for u in result.uncertainties])
        return f"\\qty{{{result.value.extract()}}}{{{result.unit}}} and uncertainties: {uncertainties_str}"
