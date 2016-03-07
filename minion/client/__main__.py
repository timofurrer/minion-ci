"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module launches the minion client.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import json
import click

from .core import Client


@click.group()
@click.pass_context
@click.version_option()
def cli(ctx):
    """Use your minion to test your code."""
    ctx.obj = Client("127.0.0.1", 5000)


@cli.command()
@click.option("--json", "as_json", flag_value=True,
              help="Output jobs as JSON.")
@click.pass_context
def jobs(ctx, as_json):
    """Get all jobs from the minion server."""
    jobs = ctx.obj.get_jobs()
    if as_json:
        click.echo(json.dumps(jobs, indent=4, sort_keys=True))
    else:
        for job in jobs["jobs"]:
            click.echo("Job {0}:".format(click.style(job["id"], bold=True)))
            click.echo("    Created at: {0}".format(
                click.style(job["created_at"], bold=True)))
            click.echo("    Repository URL: {0}".format(
                click.style(job["repository_url"], bold=True)))
            click.echo("    Commit Hash: {0}".format(
                click.style(job["commit_hash"], bold=True)))
            click.echo("    Branch: {0}".format(
                click.style(job["branch"], bold=True)))
            click.echo("    Status: {0}".format(
                click.style("✓ success" if job["result"]["status"] else "✘ failure", bold=True,
                            fg="green" if job["result"]["status"] else "red")))
            if not job["result"]["status"]:
                click.echo("        Error Message: {0}".format(
                    click.style(job["result"]["error_msg"], fg="red")))

            click.echo()


@cli.command()
@click.argument("job_id")
@click.option("--json", "as_json", flag_value=True,
              help="Output jobs as JSON.")
@click.pass_context
def job(ctx, job_id, as_json):
    """Get information about a single job from the minion server."""
    job = ctx.obj.get_job(job_id)
    if as_json:
        click.echo(json.dumps(job, indent=4, sort_keys=True))
    else:
        job_data = job["job"]
        click.echo("Id: {0}".format(click.style(job_data["id"], bold=True)))
        click.echo("Created at: {0}".format(
            click.style(job_data["created_at"], bold=True)))
        click.echo("Repository URL: {0}".format(
            click.style(job_data["repository_url"], bold=True)))
        click.echo("Commit Hash: {0}".format(
            click.style(job_data["commit_hash"], bold=True)))
        click.echo("Branch: {0}".format(
            click.style(job_data["branch"], bold=True)))
        click.echo("Status: {0}".format(
            click.style("✓ success" if job_data["result"]["status"] else "✘ failure", bold=True,
                        fg="green" if job_data["result"]["status"] else "red")))
        if not job_data["result"]["status"]:
            click.echo("    Error Message: {0}".format(
                click.style(job_data["result"]["error_msg"], fg="red")))


main = cli

if __name__ == "__main__":
    main()
