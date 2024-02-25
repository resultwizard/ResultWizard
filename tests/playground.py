# TLDR: `pip install -e .` from the root directory of the package
# Then: `python3 ./tests/playground.py`
#
# development mode: "setuptools allows you to install a package without
# copying any files to your interpreter directory
# (e.g. the site-packages directory)."
# From: https://setuptools.pypa.io/en/latest/userguide/quickstart.html#development-mode


import valuewizard as wiz

# TODO: give a warning when a variable is redefined ("shadowed")

#############################
# EXAMPLES
#############################

wiz.res("important", 1.0, r"\mm").print()
# important: 1.0 \mm

wiz.res("important", 1.0, 0.01, r"\mm").print()
# important: (1.0 ± 0.01) \mm

wiz.res("important", 1.0, (0.01, "systematic"), r"\mm").print()
# important: (1.0 ± 0.01 systematic) \mm

wiz.res("important", 1.0, [(0.01, "systematic"), (0.02, "stat")], r"\mm").print()
# important: (1.0 ± 0.01 systematic, 0.02 stat) \mm

# The following wont' work as we can't have positional arguments (here: unit)
# after keyword arguments (here: uncert)
# wiz.res("important", 1.0, uncert=[(0.01, "systematic"), (0.02, "stat")], r"\mm").print()
