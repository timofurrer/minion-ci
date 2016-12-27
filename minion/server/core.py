"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the core functionality for the minion-ci server.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import shutil
from flask import current_app, request, jsonify
from pymongo import MongoClient, errors
from multiprocessing import Pool, Queue
from subprocess import Popen, PIPE, STDOUT
from functools import wraps

from .models import Job, Result
from ..parser import parse
from ..errors import MinionError, MinionMongoError


class WorkersExtension:
    """A flask extension for the job queue and worker pool."""
    def __init__(self, app=None):
        self._app_cache = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        queue = Queue()
        pool = Pool(1, worker, (queue, app.config))
        self._app_cache[app] = {
            "queue": queue,
            "pool": pool
        }
        
    @property
    def queue(self):
        """Return the job queue used by the workers."""
        return self._app_cache[current_app._get_current_object()]["queue"]

    @property
    def pool(self):
        """Return the worker pool."""
        return self._app_cache[current_app._get_current_object()]["pool"]

workers = WorkersExtension()


def worker(queue, config):
    """Single worker to process jobs from the given queue."""
    while True:
        job_data = queue.get(True)

        # insert job into database
        job = Job()
        job.repository_url = job_data["repository_url"]
        job.commit_hash = job_data["commit_hash"]
        job.branch = job_data["branch"]
        job.attributes = job_data["attributes"]
        job.result = Result()
        job.save()

        process(job, config, job_data["keep_data"])


def process(job, config, keep_data):
    """
        Process the given job.

        The process is composed of the following steps:
            - clone git repository
            - run before run command
            - run command
            - run after run command
    """
    job.result.status = "running"
    job.save()

    local_repo_path = os.path.join(config["JOB_DATAPATH"], str(job.id))

    try:
        # clone the git repository
        git_clone = Popen(["git", "clone", job.repository_url, local_repo_path], stdout=PIPE, stderr=STDOUT)
        tmp_stdout, _ = git_clone.communicate()
        job.result.logs += tmp_stdout.decode("utf-8")
        if git_clone.returncode != 0:
            raise MinionError("Failed to clone git repository from {0} to {1}".format(
                job.repository_url, local_repo_path))

        if job.commit_hash:
            git_reset = Popen(["git", "reset", "--hard", job.commit_hash],
                              cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = git_reset.communicate()
            job.result.logs += tmp_stdout.decode("utf-8")
            job.save()
            if git_reset.returncode != 0:
                raise MinionError("Failed to reset repository to {0}".format(job.commit_hash))
        elif job.branch:
            git_checkout = Popen(["git", "checkout", job.branch],
                                 cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = git_checkout.communicate()
            job.result.logs += tmp_stdout.decode("utf-8")
            job.save()
            if git_checkout.returncode != 0:
                raise MinionError("Failed to checkout branch {0}".format(job.branch))

        # get current git commit hash
        git_rev_parse = Popen(["git", "rev-parse", "HEAD"],
                              cwd=local_repo_path, stdout=PIPE, stderr=PIPE)
        current_commit_hash, _ = git_rev_parse.communicate()
        job.commit_hash = current_commit_hash.decode("utf-8").strip()
        job.save()
        if git_rev_parse.returncode != 0:
            raise MinionError("Failed to parse current git revision")

        config = parse(os.path.join(local_repo_path, job.config_file))

        if "precondition" in config:
            before_run = Popen(config["precondition"], shell=True,
                               cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = before_run.communicate()
            job.result.logs += tmp_stdout.decode("utf-8")
            job.save()
            if before_run.returncode != 0:
                raise MinionError("Failed to run precondition command: '{0}'".format(config["precondition"]))

        if "command" in config:
            command_run = Popen(config["command"], shell=True,
                                cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = command_run.communicate()
            job.result.logs += tmp_stdout.decode("utf-8")
            job.save()
            if command_run.returncode != 0:
                raise MinionError("Failed to run command: '{0}'".format(config["command"]))
    except MinionError as e:
        job.result.error_msg = str(e)
        job.result.status = "failed"
        if True in config and "failure" in config[True]:
            after_run = Popen(config[True]["failure"], shell=True,
                              cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = after_run.communicate()
            job.result.logs += tmp_stdout.decode("utf-8")
            if after_run.returncode != 0:
                job.result.error_msg += "\n{0}".format("Failed to run failure command: '{0}'".format(
                    config[True]["failure"]))
    else:
        job.result.status = "succeded"
        if True in config and "success" in config[True]:
            after_run = Popen(config[True]["success"], shell=True,
                              cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = after_run.communicate()
            job.result.logs += tmp_stdout.decode("utf-8")
            if after_run.returncode != 0:
                job.result.error_msg = "Failed to run failure command: '{0}'".format(
                    config[True]["failure"])
                job.result.status = "failed"
    finally:
        job.save()

        if not keep_data:
            shutil.rmtree(local_repo_path)

def stop_server():
    """
    stop the minion-server.
    
    This command is only used by a post request to /stop
    """
    workers.pool.close()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def ensure_mongo(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        client = MongoClient(serverSelectionTimeoutMS=500, connectTimeoutMS=500)
        try:
             # The ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
        except (errors.ServerSelectionTimeoutError, errors.AutoReconnect):
            raise MinionMongoError("Can't connect to mongodb")
        else:
            return func(*args, **kwargs)
        finally:
            client.close()
    return func_wrapper
