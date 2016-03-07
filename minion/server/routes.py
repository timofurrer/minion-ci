"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the routes for the minion-ci API.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import re
import mongoengine
from flask import Blueprint, request, jsonify, render_template

from .models import Job, mongo_to_dict
from .core import workers

api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def index():
    """Serve index HTML."""
    return render_template("index.html", jobs=Job.objects)


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
    return jsonify({"jobs": [mongo_to_dict(j) for j in Job.objects]})


@api.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    """Serve information of specific job."""
    job = Job.objects.get(id=job_id)
    return jsonify({"job": mongo_to_dict(job)})


@api.route("/jobs", methods=["POST", "PUT"])
def create_job():
    """Create a new job"""
    data = request.json
    job = {
        "repository_url": data.pop("repo_url", None),
        "commit_hash": data.pop("commit_hash", None),
        "branch": data.pop("branch", None),
        "keep_data": data.pop("keep_data", False),
        "attributes": data
    }
    workers.queue.put(job)
    return jsonify({"status": True})


@api.route("/jobs", methods=["DELETE"])
def delete_jobs():
    """Delete all jobs."""
    Job.drop_collection()
    return jsonify({"status": True})


@api.route("/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    """Delete a specific job."""
    try:
        job = Job.objects.get(id=job_id)
    except mongoengine.errors.ValidationError:
        return jsonify({"status": False, "msg": "No such job id found: {0}".format(job_id)})
    else:
        job.delete()
        return jsonify({"status": True})
