minion-ci
=========

**minion-ci** is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

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

Stack
-----

**minion-ci** is built on top of flask and uses a MongoDB to persist jobs.
