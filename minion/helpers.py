"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains helper functions for the minion-ci server and client

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
from urllib.parse import urlparse

def get_repository_name(repository_url):
    """
        Returns the repository name from the
        given repository_url.
    """
    parts = urlparse(repository_url)
    return os.path.splitext(os.path.basename(parts.path))[0]
