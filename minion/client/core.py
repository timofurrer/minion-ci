"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the core functionality for the minion-ci client.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""


import requests
import subprocess
from time import sleep


def ensure_started_server(func):
    """Ensures that the minion-ci server is started."""
    def _wrapper(self, *args, **kwargs):
        """decorator wrapper"""
        try:
            self.get_status()
        except requests.exceptions.ConnectionError:  # server is not started
            subprocess.Popen(["minion-server"])
            sleep(2)

        return func(self, *args, **kwargs)

    return _wrapper


class Client:
    """Client for the minion-ci server."""
    def __init__(self, host, port, schema="http://"):
        self.host = host
        self.port = port
        self.base_url = "{0}{1}:{2}".format(schema, host, port)

    def _build_url(self, route):
        """Build the API URL of the given route."""
        return "{0}/{1}".format(self.base_url, route)

    def get_status(self):
        """Get status of the minion server."""
        response = requests.get(self._build_url("status"))
        return response.json()

    @ensure_started_server
    def stop_server(self):
        """stop the server by sending a postrequest to /stop"""
        response = requests.post(self._build_url("stop"))
        return response

    @ensure_started_server
    def get_jobs(self):
        """Get all jobs from the minion server."""
        response = requests.get(self._build_url("jobs"))
        return response.json()

    @ensure_started_server
    def get_job(self, job_id):
        """Get a single job from the minion server."""
        response = requests.get(self._build_url("jobs/{0}".format(job_id)))
        return response.json()

    @ensure_started_server
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
        response = requests.post(self._build_url("jobs"), json=data)
        return response.json()
