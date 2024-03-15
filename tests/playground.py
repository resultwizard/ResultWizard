# TLDR: `pip3 install -e .` from the root directory of the package
# Then: `python3 ./tests/playground.py`
#
# development mode: "setuptools allows you to install a package without
# copying any files to your interpreter directory
# (e.g. the site-packages directory)."
# From: https://setuptools.pypa.io/en/latest/userguide/quickstart.html#development-mode


import resultwizard as wiz

print("#############################")
print("### Playground")
print("#############################")
print()


wiz.config_init(print_auto=True, decimal_places=3)
# wiz.config(sigfigs=2)
# wiz.config(decimal_places=2)

#############################
# EXAMPLES
#############################

print("### RESULTS API")

# wiz.res("", 42.0).print()
# -> Error: "name must not be empty"

wiz.res("a99", 1.0, r"\mm")
# a: 1.0 \mm

wiz.res("1 b", 1.0, 0.01, r"\per\mm\cubed").print()
# b: (1.0 ± 0.01) \mm

wiz.config(decimal_places=-1, sigfigs_fallback=3)

wiz.res("c big", 1.0, (0.01, "systematic"), r"\mm").print()
# c: (1.0 ± 0.01 systematic) \mm

wiz.res(
    "d", 1.0e10, [(0.01e10, "systematic"), (0.0294999999e10, "stat")], r"\mm\per\second\squared"
).print()
# d: (1.0 ± 0.01 systematic ± 0.02 stat) \mm

wiz.res("e", "1.0", r"\mm").print()
# e: 1.0 \mm

wiz.res("f", "1.0e1", 25e-1).print()
# f: 1.0

wiz.res("g", 42).print()

wiz.res("h", 42, 13)
# TODO: 13 is misinterpreted as number of sigfigs


# wiz.res("g", 1.0, sys=0.01, stat=0.02, unit=r"\mm").print()
# g: (1.0 ± 0.01 sys ± 0.02 stat) \mm
# TODO: Why does this not work?
# -> This fix might help: https://github.com/beartype/plum/issues/40#issuecomment-1836613508

# The following wont' work as we can't have positional arguments (here: unit)
# after keyword arguments (here: uncert)
# wiz.res("d", 1.0, uncert=[(0.01, "systematic"), (0.02, "stat")], r"\mm").print()

# wiz.table(
#     "name",
#     {
#         "Header 1": ["Test", "Test2", ...],
#         "Header 2": [wiz.cell_res(...), wiz.cell_res(...), ...],
#         "Header 3": [wiz.cell_res(values[i], errors[i], r"\mm") for i in range(10)],
#     },
#     "description",
#     horizontal = True,
# )


#############################
# Export
#############################

print()
print("### EXPORT")
wiz.export("results.tex")
