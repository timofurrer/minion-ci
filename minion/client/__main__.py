"""
    `minion-ci` is a minimalist, decentralized, flexible Continuous Integration Server for hackers.

    This module launches the minion client.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import os
import json
import click
import shutil
import subprocess

from .core import Client


@click.group()
@click.pass_context
@click.version_option()
def cli(ctx):
    """Use your minion to test your code."""
    ctx.obj = Client("127.0.0.1", 5000)


@cli.command()
def init():
    """Initialize minion aliases for git repository."""
    # check if git repository
    if subprocess.call(["git", "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
        click.echo("This is not a git repository!")
        return 1

    if os.path.exists("minion.yml"):
        click.echo("This is already a minion repository!")
        return

    if subprocess.call(["git", "config", "alias.minion", "!minion submit ."]) != 0:
        click.echo("Unable to add git minion alias!")
        return 1

    shutil.copyfile(os.path.join(os.path.dirname(__file__), "templates/minion.yml"), "minion.yml")
    click.echo("Added 'git minion' alias")

@cli.command()
@click.pass_context
def stop(ctx):
    """Stop the minion server"""
    ctx.obj.stop_server()

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


@cli.command()
@click.argument("repo_url")
@click.option("-h", "--commit-hash",
              help="The git commit hash to test.")
@click.option("-b", "--branch",
              help="The git branch to test.")
@click.option("-k", "--keep-data", flag_value=True,
              help="If given the result data will not be deleted.")
@click.option("-a", "--attribute", "raw_attributes", multiple=True,
              type=(str, str),
              help="Specify arbitrary attributes.")
@click.pass_context
def submit(ctx, repo_url, commit_hash, branch, keep_data, raw_attributes):
    """Submit a new job."""
    # check if given repo url is path or url
    if os.path.exists(repo_url):  # is local path -> get absolute
        repo_url = os.path.abspath(repo_url)

    attributes = {a[0]: a[1] for a in raw_attributes}
    response = ctx.obj.submit(repo_url, commit_hash, branch, keep_data, attributes)
    if response["status"]:
        click.echo("Submitted new job - Stay tuned for results!")
    else:
        click.echo("Something failed while submitting the job!")


main = cli

if __name__ == "__main__":
    main()
