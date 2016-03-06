"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module launches the minion-ci server.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import click

from .app import app


@click.command()
def main():
    """Manage minion-ci server."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
