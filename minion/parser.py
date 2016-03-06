"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the parser to parse the `minion.yml` file.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import yaml

from .errors import MinionError


def parse(path):
    """Parse the given minion.yml file"""
    try:
        with open(path) as minion_file:
            config = yaml.load(minion_file)
    except OSError:
        raise MinionError("No minion.yml config file found in repository")
    return config
