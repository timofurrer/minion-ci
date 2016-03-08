"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the server code for `minion-ci`.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import re
import click
import yaml
from flask import Flask
from jinja2 import evalcontextfilter, Markup, escape

from .config import DefaultConfig
from .routes import api
from .models import db
from .core import workers


def parse_config(path):
    """Parse minion-ci server configuration file."""
    with open(path) as config_file:
        return yaml.load(config_file)


@evalcontextfilter
def nl2br(eval_ctx, value):
    _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def create_app(name):
    """Create flask app"""
    app = Flask(__name__)
    app.register_blueprint(api)
    app.config.from_object(DefaultConfig)

    try:
        app.config.update(parse_config(app.config["DEFAULT_CONFIGURATION_FILE"]))
    except FileNotFoundError:
        pass

    # add required filters
    app.jinja_env.filters["nl2br"] = nl2br

    # initialize mongodb engine for use in flask
    db.init_app(app)

    # initilize worker pool and job queue
    workers.init_app(app)

    return app
