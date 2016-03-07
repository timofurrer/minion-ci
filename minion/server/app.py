"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the server code for `minion-ci`.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import click
import yaml
from flask import Flask
from flask.ext.mongoengine import MongoEngine

from .routes import api
from .models import db
from .core import workers

# default configuration settings
MONGODB_SETTINGS = {"DB": "minion-ci"}
APPLICATION_DATAPATH = click.get_app_dir("minion-ci")
JOB_DATAPATH = os.path.join(APPLICATION_DATAPATH, "jobs")
DEFAULT_CONFIGURATION_FILE = os.path.join(APPLICATION_DATAPATH, "server-config.yml")

def parse_config(path):
    """Parse minion-ci server configuration file."""
    with open(path) as config_file:
        return yaml.load(config_file)

app = Flask(__name__)
app.register_blueprint(api)
app.config.from_object(__name__)

try:
    app.config.update(parse_config(DEFAULT_CONFIGURATION_FILE))
except FileNotFoundError:
    pass

# initialize mongodb engine for use in flask
db.init_app(app)

# initilize worker pool and job queue
workers.init_app(app)
