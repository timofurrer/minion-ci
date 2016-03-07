"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module launches the minion-ci server.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import click

@click.command()
@click.option("-c", "--config",
              help="Path to configuration file.")
@click.version_option()
def main(config):
    """Manage minion-ci server."""
    from .app import app, parse_config

    if config:
        app.config.update(parse_config(config))

    app.run(debug=True)


if __name__ == "__main__":
    main()
