import click

@click.command()
def cli(tracker, activity):
    """Enables entries to be cleared"""
    click.secho('prepared to clear stuff!', color=blue)

