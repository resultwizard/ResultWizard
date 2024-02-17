# TLDR: `pip install -e .` from the root directory of the package
# Then: `python3 ./tests/playground.py`
#
# development mode: "setuptools allows you to install a package without copying any files to your interpreter directory (e.g. the site-packages directory)." from [1]
# [1] https://setuptools.pypa.io/en/latest/userguide/quickstart.html#development-mode


from valuewizard import res

res(42.31415)
