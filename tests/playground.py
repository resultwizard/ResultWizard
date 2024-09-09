# TLDR: `pip3 install -e .` from the root directory of the package
# Then: `python3 ./tests/playground.py`
#
# development mode: "setuptools allows you to install a package without
# copying any files to your interpreter directory
# (e.g. the site-packages directory)."
# From: https://setuptools.pypa.io/en/latest/userguide/quickstart.html#development-mode

from random import random
from decimal import Decimal
import resultwizard as wiz

print("#############################")
print("### Playground")
print("#############################")
print()

wiz.config_init(
    print_auto=True,
    export_auto_to="results-immediate.tex",
    siunitx_fallback=False,
    ignore_result_overwrite=False,
)
# wiz.config(sigfigs=2)
# wiz.config(decimal_places=2)

#############################
# EXAMPLES
#############################

print("### RESULTS API")

# wiz.res("", 42.0).print()
# -> Error: "name must not be empty"

wiz.res("a911", 1.05, unit=r"\mm\s\per\N\kg")
# wiz.res("a911", "1.052", 0.25, r"\mm\s\per\N\kg")

wiz.res("1 b", 1.0, 0.01, unit=r"\per\mm\cubed")

# wiz.config(decimal_places=-1, sigfigs_fallback=3)

wiz.res("c big", 1.0, (0.01, "systematic"), r"\mm")
wiz.res("d", 1.0e10, [(0.01e10, "sysyeah"), (0.0294999e10, "statyeah")], r"\mm\per\second^2")
# wiz.res("e", "1.0", r"\mm")  # -> except error message that maybe we have forgotten to put `unit=`

wiz.res("f", "1.0e1", 25e-1)
wiz.res("g", 42)
wiz.res("h", 42, sys=13.0, stat=24.0)
wiz.res("h&", 42, sys=13.0, stat=24.0)

wiz.res("i", Decimal("42.0e-30"), Decimal("0.1e-31"), unit=r"\m")
wiz.res(
    "i",
    Decimal("42.0e-30"),
    sys=Decimal("0.1e-31"),
    stat=Decimal("0.05e-31"),
    unit=r"\m\per\s\squared",
)
wiz.res("j", 0.009, None, "", 2)  # really bad, but this is valid
# wiz.res("k", 1.55, 0.0, unit=r"\tesla")  # -> uncertainty must be positive
wiz.res("k", 3, 1, r"\tesla")  # integers work as well, yeah
wiz.res("l", 1.0, sys=0.01, stat=0.02, unit=r"\mm").print()
wiz.res("m", 1.0, uncerts=[(0.01, "systematic"), (0.02, "stat")], unit=r"\mm").print()

wiz.table(
    "name",
    [
        wiz.column("Num.", [f"{i+1}" for i in range(10)]),
        wiz.column(
            "Random 1", [wiz.table_res(random(), random() * 0.1, r"\mm") for i in range(10)]
        ),
        wiz.column(
            "Random 2",
            [wiz.table_res(random(), random() * 0.1, r"\electronvolt") for i in range(10)],
            concentrate_units_if_possible=False,
        ),
        wiz.column(
            "Random 3",
            [
                wiz.table_res(
                    random(), random() * 0.1, r"\electronvolt" if random() > 0.5 else r"\mm"
                )
                for i in range(10)
            ],
        ),
    ],
    "description",
    resize_to_fit_page_=True,
)

wiz.table(
    "name horizontal",
    [
        wiz.column("Num.", [f"{i+1}" for i in range(4)]),
        wiz.column("Random 1", [wiz.table_res(random(), random() * 0.1, r"\mm") for i in range(4)]),
        wiz.column(
            "Random 2",
            [wiz.table_res(random(), random() * 0.1, r"\electronvolt") for i in range(4)],
            concentrate_units_if_possible=False,
        ),
        wiz.column(
            "Random 3",
            [
                wiz.table_res(
                    random(), random() * 0.1, r"\electronvolt" if random() > 0.5 else r"\mm"
                )
                for i in range(4)
            ],
        ),
    ],
    "description",
    horizontal=True,
    resize_to_fit_page_=True,
    label="tab:horizontal",
)

wiz.res("Tour Eiffel Height", "330.3141516", "0.5", r"\m")
wiz.res("g Another Test", 9.81, 0.78, unit=r"\m/\s^2")

#############################
# Export
#############################

print()
print("### EXPORT")
wiz.export("results.tex")
