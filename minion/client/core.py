"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the core functionality for the minion-ci client.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""


import requests


class Client:
    """Client for the minion-ci server."""
    def __init__(self, host, port, schema="http://"):
        self.host = host
        self.port = port
        self.base_url = "{0}{1}:{2}".format(schema, host, port)

    def _build_url(self, route):
        """Build the API URL of the given route."""
        return "{0}/{1}".format(self.base_url, route)

    def get_jobs(self):
        """Get all jobs from the minion server."""
        response = requests.get(self._build_url("jobs"))
        return response.json()

    def get_job(self, job_id):
        """Get a single job from the minion server."""
        response = requests.get(self._build_url("jobs/{0}".format(job_id)))
        return response.json()

    def submit(self, repository_url, commit_hash=None, branch=None, keep_data=None, attributes=None):
        """Submit a new job to the minion server."""
        data = {
            "repo_url": repository_url,
            "commit_hash": commit_hash,
            "branch": branch,
            "keep_data": keep_data,
        }
        if attributes:
            data.update(attributes)
        response = requests.put(self._build_url("jobs"), json=data)
        return response.json()
