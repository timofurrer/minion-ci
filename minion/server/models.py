"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the models to persist CI job data.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import datetime

from .database import get_db
from ..parser import parse

db = get_db()


class Result(db.EmbeddedDocument):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a job test result."""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    status = db.BooleanField(default=False, required=True)
    error_msg = db.StringField()
    logs = db.StringField()


class Job(db.Document):  # pylint: disable=no-init,too-few-public-methods
    """Document to store a single minion-ci job."""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    repository_url = db.StringField(required=True)
    commit_hash = db.StringField()
    branch = db.StringField()
    attributes = db.DictField()
    result = db.EmbeddedDocumentField(Result)

    @property
    def local_repo_path(self):
        """Returns the path to the local clone of the repository."""
        return os.path.join("jobs", str(self.id))

    @property
    def config_file(self):
        """Discovers the minion config file."""
        return os.path.join(self.local_repo_path, "minion.yml")

    @property
    def config(self):
        """Returns the parsed minion config."""
        return parse(self.config_file)
