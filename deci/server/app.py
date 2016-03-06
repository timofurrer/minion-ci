"""
    `deci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the server code for `deci`.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

from flask import Flask, g

from .database import get_db, settings
from .routes import api
from .core import workers

app = Flask(__name__)
app.register_blueprint(api)
app.config.update(settings)

db = get_db()
db.init_app(app)
workers.init_app(app)
