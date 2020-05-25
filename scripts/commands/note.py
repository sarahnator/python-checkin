import click
@click.command()
def cli():
    """Creates a note in the athlete notes table"""
    click.secho('prepared to create a note!', color=purple)