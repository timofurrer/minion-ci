"""
    `deci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the database configuration.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

from flask.ext.mongoengine import MongoEngine

def get_db():
    return MongoEngine()

# TODO: read from configuration file
settings = {
    "MONGODB_SETTINGS": {"DB": "deci"}
}
