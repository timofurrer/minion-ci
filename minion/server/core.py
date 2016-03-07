"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the core functionality for the minion-ci server.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import shutil
from flask import current_app
from multiprocessing import Pool, Queue
from subprocess import Popen, PIPE, STDOUT

from .models import db, Job, Result
from ..parser import parse
from ..errors import MinionError


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
    result = Result()
    logs = ""

    local_repo_path = os.path.join(config["JOB_DATAPATH"], str(job.id))

    try:
        # clone the git repository
        git_clone = Popen(["git", "clone", job.repository_url, local_repo_path], stdout=PIPE, stderr=STDOUT)
        tmp_stdout, _ = git_clone.communicate()
        logs += tmp_stdout.decode("utf-8")
        if git_clone.returncode != 0:
            raise MinionError("Failed to clone git repository from {0} to {1}".format(
                job.repository_url, local_repo_path))

        if job.commit_hash:
            git_reset = Popen(["git", "reset", "--hard", job.commit_hash],
                              cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = git_reset.communicate()
            logs += tmp_stdout.decode("utf-8")
            if git_reset.returncode != 0:
                raise MinionError("Failed to reset repository to {0}".format(job.commit_hash))
        elif job.branch:
            git_checkout = Popen(["git", "checkout", job.branch],
                                 cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = git_checkout.communicate()
            logs += tmp_stdout.decode("utf-8")
            if git_checkout.returncode != 0:
                raise MinionError("Failed to checkout branch {0}".format(job.branch))

        # get current git commit hash
        git_rev_parse = Popen(["git", "rev-parse", "HEAD"],
                              cwd=local_repo_path, stdout=PIPE, stderr=PIPE)
        current_commit_hash, _ = git_rev_parse.communicate()
        job.commit_hash = current_commit_hash.decode("utf-8").strip()
        if git_rev_parse.returncode != 0:
            raise MinionError("Failed to parse current git revision")

        config = parse(os.path.join(local_repo_path, job.config_file))

        if "before_run" in config:
            before_run = Popen(config["before_run"], shell=True,
                               cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = before_run.communicate()
            logs += tmp_stdout.decode("utf-8")
            if before_run.returncode != 0:
                raise MinionError("Failed to run before_run command: '{0}'".format(config["before_run"]))

        if "command" in config:
            command_run = Popen(config["command"], shell=True,
                                cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = command_run.communicate()
            logs += tmp_stdout.decode("utf-8")
            if command_run.returncode != 0:
                raise MinionError("Failed to run command: '{0}'".format(config["command"]))

        if "after_run" in config:
            after_run = Popen(config["after_run"], shell=True,
                              cwd=local_repo_path, stdout=PIPE, stderr=STDOUT)
            tmp_stdout, _ = after_run.communicate()
            logs += tmp_stdout.decode("utf-8")
            if after_run.returncode != 0:
                raise MinionError("Failed to run after_run command: '{0}'".format(config["after_run"]))
    except MinionError as e:
        result.error_msg = str(e)
        result.status = False
    else:
        result.status = True
    finally:
        result.logs = logs

        job.result = result
        job.save()

        if not keep_data:
            shutil.rmtree(local_repo_path)
