from domain.result import _Result
from application.master_stringifier import MasterStringifier


class Stringifier(MasterStringifier):
    def result_to_str(self, result: _Result):
        """
        Returns the result as human-readable string.
        """

        return f"{result.name} = {self.create_str(result.value, result.uncertainties, result.unit)}"

    def _modify_unit(self, unit: str) -> str:
        """
        Returns the modified unit.
        """
        unit = (
            unit.replace(r"\squared", "^2")
            .replace(r"\cubed", "^3")
            .replace(r"\per", "/")
            .replace("\\", "")
        )

        if unit[0] == "/":
            unit = f"1{unit}"

        return unit
