minion-ci
=========

**minion-ci** is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

|screenshot_index|

Installation
------------

To persist the job data *minion-ci* uses MongoDB. Make sure you have a MongoDB instance running or install
it with your package manager:

.. code::

    apt-get install mongodb
    yum install mongodb

It's recommended to use pip to install minion-ci:

.. code::

    pip3 install minion-ci

Server API
----------

+----------------+-------------+-----------------+--------------------------+
| Route          | HTTP Method | Parameter       | Description              |
+================+=============+=================+==========================+
| /status        | GET         |                 | Get status of the server |
+----------------+-------------+-----------------+--------------------------+
| /jobs          | GET         | page,           | Get a list of all jobs   |
|                |             | page_size       |                          |
+----------------+-------------+-----------------+--------------------------+
| /jobs          | PUT, POST   | repo_url,       | Create a new job         |
|                |             | commit_hash,    |                          |
|                |             | branch,         |                          |
|                |             | keep_data,      |                          |
|                |             | arbitrary data  |                          |
+----------------+-------------+-----------------+--------------------------+
| /jobs          | DELETE      |                 | Remove all jobs          |
+----------------+-------------+-----------------+--------------------------+
| /jobs/<job_id> | GET         |                 | Get a single job         |
+----------------+-------------+-----------------+--------------------------+
| /jobs/<job_id> | DELETE      |                 | Remove a single job      |
+----------------+-------------+-----------------+--------------------------+


Stack
-----

**minion-ci** is built on top of flask and uses a MongoDB to persist jobs.

.. |screenshot_index| image:: https://raw.githubusercontent.com/timofurrer/minion-ci/master/screenshots/index.jpg
    :alt: Index Page
