"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module launches the minion-ci server.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import click
import logging

@click.command()
@click.option("-c", "--config",
              help="Path to configuration file.")
@click.option("-d", "--debug", flag_value=True,
              help="Run server in debug mode.")
@click.version_option()
def main(config, debug):
    """Manage minion-ci server."""
    from .app import create_app, parse_config

    app = create_app("minion")

    if not debug:
        logging.basicConfig(filename=app.config["LOG_FILE_PATH"], level=logging.DEBUG)

    if config:
        app.config.update(parse_config(config))

    app.run(debug=debug)


if __name__ == "__main__":
    main()
