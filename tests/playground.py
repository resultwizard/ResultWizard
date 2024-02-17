# TLDR: `pip install -e .` from the root directory of the package
# Then: `python3 ./tests/playground.py`
#
# development mode: "setuptools allows you to install a package without
# copying any files to your interpreter directory
# (e.g. the site-packages directory)."
# From: https://setuptools.pypa.io/en/latest/userguide/quickstart.html#development-mode


import valuewizard as wiz

wiz.res("hello", 1.0, 0.42, "m")
wiz.res("abc", 5.01, 0.12, "T")
# shadowing (!)
wiz.res("hello", 3.14, (0.41, "myerror1"), (0.42, "myerror2"), "mm").print()

wiz.export("my/path.tex")
