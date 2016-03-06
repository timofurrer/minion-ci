"""
    `deci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the models to persist CI job data.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import datetime

from .database import get_db

db = get_db()


class Result(db.Document):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a job test result."""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    status = db.BooleanField(required=True)


class Job(db.Document):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a single deci job."""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    repository_url = db.StringField(required=True)
    commit_hash = db.StringField(required=True)
    branch = db.StringField(required=True)
    attributes = db.DictField()
    result = db.ReferenceField(Result)
