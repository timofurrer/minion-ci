"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module contains the core functionality for the minion-ci server.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
from flask import current_app
from multiprocessing import Pool, Queue
from time import sleep

from .database import get_db
from .models import Job

class WorkersExtension:
    """A flask extension for the job queue and worker pool."""
    def __init__(self, app=None):
        self._app_cache = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        queue = Queue()
        pool = Pool(1, worker, (queue,))
        self._app_cache[app] = {
            "queue": queue,
            "pool": pool
        }

    @property
    def queue(self):
        return self._app_cache[current_app._get_current_object()]["queue"]

    @property
    def pool(self):
        return self._app_cache[current_app._get_current_object()]["pool"]

workers = WorkersExtension()


def worker(queue):
    """Single worker to process jobs from the given queue."""
    print("Launched worker:", os.getpid())
    get_db()
    while True:
        job_task = queue.get(True)
        print("Got job task:", job_task)

        # insert job into database
        job = Job(**job_task)
        job.save()

        sleep(1)
        print("Processed job task:", job_task)
