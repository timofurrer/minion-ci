deci
====

**deci** is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

Installation
------------

To persist the job data *deci* uses MongoDB. Make sure you have a MongoDB instance running or install
it with your package manager:

.. code::

    apt-get install mongodb
    yum install mongodb

It's recommended to use pip to install deci:

.. code::

    pip3 install deci

Stack
-----

**deci** is built on top of flask and uses a MongoDB to persist jobs.
