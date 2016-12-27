"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the exceptions specific to `minion` errors.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

class MinionError(Exception):
    """Exception which is raised for minion specific errors."""
    pass

class MinionMongoError(Exception):
    """Exception raised for minion specific errors related to mongodb"""
    pass