class ExportConfig:
    def __init__(
        self,
        identifier="result",
        error_identifier="error",
        unit_identifier="unit",
        sig_figs_identifier="sigfigs",
        min_exponent_for_non_scientific_notation=-2,
        max_exponent_for_non_scientific_notation=3,
        default_sig_figs=2,
    ) -> None:
        self.identifier = identifier
        self.error_identifier = error_identifier
        self.unit_identifier = unit_identifier
        self.sig_figs_identifier = sig_figs_identifier
        self.min_exponent_for_non_scientific_notation = (
            min_exponent_for_non_scientific_notation
        )
        self.max_exponent_for_non_scientific_notation = (
            max_exponent_for_non_scientific_notation
        )
        self.default_sig_figs = default_sig_figs

    def complete_identifier(self):
        return self.identifier + "_"

    def complete_error_identifier(self):
        return self.identifier + "_" + self.error_identifier + "_"

    def complete_unit_identifier(self):
        return self.identifier + "_" + self.unit_identifier + "_"

    def complete_sig_figs_identifier(self):
        return self.identifier + "_" + self.sig_figs_identifier + "_"
