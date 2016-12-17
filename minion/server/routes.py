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
from .core import workers, stop_server, ensure_mongo
import pymongo

api = Blueprint("api", __name__)


def get_jobs_page(page=1, page_size=10):
    """Returns all jobs from the given page."""
    return Job.objects.paginate(page=page, per_page=page_size)


@ensure_mongo
@api.route("/", methods=["GET"])
def index():
    """Serve index HTML."""
    page = int(request.args.get("page", 1))
    return render_template("index.html", jobs=get_jobs_page(page=page))


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


@ensure_mongo
@api.route("/jobs", methods=["GET"])
def get_jobs():
    """Serve list of jobs."""
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("pageSize", 10))
    return jsonify({"jobs": [mongo_to_dict(j) for j in get_jobs_page(page, page_size).items]})


@ensure_mongo
@api.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    """Serve information of specific job."""
    job = Job.objects.get(id=job_id)
    return jsonify({"job": mongo_to_dict(job)})


@ensure_mongo
@api.route("/jobs", methods=["POST"])
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


@ensure_mongo
@api.route("/jobs", methods=["DELETE"])
def delete_jobs():
    """Delete all jobs."""
    Job.drop_collection()
    return jsonify({"status": True})


@ensure_mongo
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

@ensure_mongo
@api.route('/stop', methods=['POST'])
def stop():
    stop_server()
    return 'Stopping server'

@api.errorhandler(pymongo.errors.ServerSelectionTimeoutError)
def serverselectiontimeout_pymongo(error):
     """Throw error if we can't connect to mongodb"""
     print("Can't connect or reconnect to mongodb")
     return "Can't connect to mongodb, please make sure mongod is running", 500
