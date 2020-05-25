import click
@click.command()

def cli():
    """Refreshes entries based on latest API data"""
    click.secho('prepared to refresh data!', color=orange)