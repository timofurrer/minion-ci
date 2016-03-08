minion-ci
=========
|pypi| |license|

**minion-ci** is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

|screenshot_index|


.. contents::

Quickstart
----------

Making your repository *minion compatible* is as easy as running this command in the root of your repository:

.. code::

    minion init

After that you should modify the ``minion.yml`` file in your repository to fit your needs. Make a nice commit and run to start your first job:

.. code::

    git minion

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
    precondition: "echo 'I was run before the test ...'"
    # the test command
    command: "echo 'This is my test...'"
    on:
      # command which is run if the command was successful
      success: "echo 'I was run because the test was successful ...'"
      # command which is run if the command failed
      failure: "echo 'I was run because the test failed ...'"


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


.. |pypi| image:: https://img.shields.io/pypi/v/minion-ci.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/minion-ci
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/timofurrer/minion-ci/master/LICENSE
    :alt: Package license

.. |screenshot_index| image:: https://raw.githubusercontent.com/timofurrer/minion-ci/master/screenshots/index.jpg
    :alt: Index Page
