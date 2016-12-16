"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the models to persist CI job data.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Result(db.EmbeddedDocument):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a job test result."""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    status = db.StringField(default="submitted")
    error_msg = db.StringField()
    logs = db.StringField(default="")


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


def mongo_to_dict(obj):
    """Turn a mongoengine object into a jsonible python object."""

    return_data = []
    if isinstance(obj, db.Document):
        return_data.append(("id", str(obj.id)))

    for field_name in obj._fields:
        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], db.DateTimeField):
            return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], db.StringField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], db.BooleanField):
            return_data.append((field_name, bool(data)))
        elif isinstance(obj._fields[field_name], db.FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], db.IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], (db.ListField, db.DictField)):
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], db.EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))
        elif isinstance(obj._fields[field_name], db.ObjectIdField):
            return_data.append((field_name, str(data)))

    return dict(return_data)
