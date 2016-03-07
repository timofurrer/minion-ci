"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the models to persist CI job data.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import datetime
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class Result(db.EmbeddedDocument):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a job test result."""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    status = db.BooleanField(default=False, required=True)
    error_msg = db.StringField()
    logs = db.StringField()


class Job(db.Document):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a single minion-ci job."""
    meta = {
                'ordering': ['-created_at']
    }

    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    repository_url = db.StringField(required=True)
    commit_hash = db.StringField()
    branch = db.StringField()
    attributes = db.DictField()
    result = db.EmbeddedDocumentField(Result)

    config_file = "minion.yml"
