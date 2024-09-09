from domain.uncertainty import Uncertainty
from api.console_stringifier import ConsoleStringifier
import api.config as c


class PrintableUncertainty:
    def __init__(self, uncert: Uncertainty, unit: str):
        self._uncert = uncert
        self._unit = unit

        stringifier = ConsoleStringifier(c.configuration.to_stringifier_config())

        self.name = uncert.name
        self.string = stringifier.create_str_uncert(uncert, unit)
        self.value = uncert.uncertainty.get()
