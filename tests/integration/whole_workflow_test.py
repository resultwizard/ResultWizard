import re
from pathlib import Path
import pytest

import resultwizard as wiz


def eiffeltower():
    wiz.res("Tour Eiffel Height", 330.362019, 0.5, r"\m")


class TestWholeWorkflow:

    @pytest.fixture
    def output_file(self, tmp_path) -> Path:
        directory = tmp_path / "whole_workflow"
        directory.mkdir()
        return directory / "results.tex"

    @pytest.mark.parametrize("resCallback", [eiffeltower])
    def test_whole_workflow(self, output_file, resCallback):
        resCallback()
        wiz.export(output_file.as_posix())

        # Actual exported text
        actual_text = output_file.read_text()
        pattern = r"\\newcommand\*{.*}"
        matches = re.findall(pattern, actual_text, re.DOTALL)
        assert len(matches) == 1
        newcommand = matches[0]

        # Expected text
        expected_file = Path("tests/integration/fixtures") / f"{resCallback.__name__}.tex"
        expected_text = expected_file.read_text()

        # Compare
        assert newcommand.split() == expected_text.split()
