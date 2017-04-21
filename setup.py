# -*- coding: utf-8 -*-

"""
    Setup minion-ci package.

    Only support Python versions > 3.4.1
"""

import ast
import re
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 4, 1):
    raise RuntimeError("minion-ci requires Python 3.4.1+")


def get_version():
    """Gets the current version"""
    _version_re = re.compile(r"__VERSION__\s+=\s+(.*)")
    with open("minion/__init__.py", "rb") as init_file:
        version = str(ast.literal_eval(_version_re.search(
            init_file.read().decode("utf-8")).group(1)))
    return version


setup(
    name="minion-ci",
    version=get_version(),
    license="MIT",

    description="minimalist, decentralized, flexible Continuous Integration Server for hackers",
    long_description=open("./README.rst", "r", encoding="utf-8").read(),

    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",

    url="https://github.com/timofurrer/minion-ci",

    packages=find_packages(),
    include_package_data=True,

    install_requires=list(line for line in open("./requirements.txt")),

    entry_points={
        "console_scripts": [
            "minion-server=minion.server.__main__:main",
            "minion=minion.client.__main__:main"
        ]
    },

    keywords=[
        "minion-ci",
        "minimalist", "simple", "flexible", "decentral",
        "ci", "continuous integration", "server",
        "git", "github",
        "source", "code",
        "docker", "container",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
)
