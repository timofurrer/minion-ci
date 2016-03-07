minion-ci
=========

**minion-ci** is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

|screenshot_index|


.. contents::

Installation
------------

It's recommended to use pip to install minion-ci:

.. code::

    pip3 install minion-ci


**MongoDB:**
To persist the job data *minion-ci* uses MongoDB.
Make sure you have MongoDB installed ...

.. code::

    apt-get install mongodb
    yum install mongodb

... and an instance is running:

.. code::

    ps -ef | grep mongod

... eventually start one with:

.. code::

    mongod

minion.yml File Format
----------------------

The **minion-ci** server will clone your repository and parse a file called **minion.yml** located
in the root of the cloned repository. The format is really simple:

.. code:: yaml

    # command which is run before the real command
    before_run: "echo 'I was run before the test ...'"
    # the test command
    command: "echo 'This is my test...'"
    # command which is run after the real command
    after_run: "echo 'I was run after the test ...'"


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
