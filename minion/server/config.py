"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the server config for minion-ci.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import click

class DefaultConfig:
    # default configuration settings
    MONGODB_SETTINGS = {
        "db": "minion-ci",
        "connect": False  # lazy connect
    }
    APPLICATION_DATAPATH = click.get_app_dir("minion-ci")
    JOB_DATAPATH = os.path.join(APPLICATION_DATAPATH, "jobs")
    DEFAULT_CONFIGURATION_FILE = os.path.join(APPLICATION_DATAPATH, "server-config.yml")
    LOG_FILE_PATH = os.path.join(APPLICATION_DATAPATH, "server.log")
