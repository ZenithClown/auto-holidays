# -*- encoding: utf-8 -*-

"""
A Modern Automatic Optimal Holiday Planner

The modern era calls for a modern optimal holiday planner that can
find the most optimal holidays for you or a group of persons. The
module is designed to be simple and easy to use with simple APIs which
can be extended to create a full-fledged application.

@author: Debmalya Pramanik (ZenithClown)
@copywright: 2021; Debmalya Pramanik (ZenithClown)
"""

import os

# ? package follows https://peps.python.org/pep-0440/
# ? https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html
__version__ = open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read().strip()

# ! let's check for package hard dependencies which must be available
hard_dependencies = [] # all should be available in ../requirements.txt
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(e.name)

# ! raise an error during import if any hard package is missing
if missing_dependencies:
    raise ImportError(f"Missing hard dependencies: {missing_dependencies}")

# init-time Option Registrations
