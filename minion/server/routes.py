"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the routes for the minion-ci API.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

from flask import Blueprint, request, jsonify

from .models import Job
from .core import workers

api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def index():
    """Serve index HTML."""
    pass


@api.route("/status", methods=["GET"])
def get_status():
    """Get status of the minion server."""
    status = {
        "queue": {
            "size": workers.queue.qsize()
        },
        "jobs": {

        }
    }
    return jsonify(status)


@api.route("/jobs", methods=["GET"])
def get_jobs():
    """Serve list of jobs."""
    return jsonify({"jobs": Job.objects})


@api.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    """Serve information of specific job."""
    job = Job.objects.get(id=job_id)
    return jsonify({"job": job})


@api.route("/jobs", methods=["PUT"])
def create_job():
    """Create a new job"""
    data = request.json
    job = {
        "repository_url": data.get("repo_url"),
        "commit_hash": data.get("commit_hash"),
        "branch": data.get("branch"),
        "attributes": data.get("attributes")
    }
    workers.queue.put(job)
    return jsonify({"status": True})


@api.route("/jobs/<job_id>", methods=["POST"])
def update_job(job_id):
    """Update a specific job."""
    pass


@api.route("/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    """Delete a specific job."""
    pass
