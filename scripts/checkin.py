from scripts.spreadsheet import *
import click
from scripts.query import *
# !/usr/bin/env python

@click.group(chain=True)
def cli():
    click.echo('Hello! Making changes to your spreadsheet...')


@cli.command('note', short_help='add note')
def note():
    """
    \b
    Enables you to add a note to the athlete notes table.
    Once called, the script will prompt for a day of the week and a message to add to that day's note entry.
    """
    day = click.prompt(text='Enter day of week to attach a note entry:', show_choices=True,
                       type=click.Choice(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], case_sensitive=False))
    msg = click.prompt(text='Enter the note you would like to add for %s' % day)

    add_note(msg, day)

    click.secho('The note >> ', nl=False)
    click.secho('%s ' % msg, bold=True, nl=False)
    click.secho('<< has been added to ', nl=False)
    click.secho('%s.' % day, bold=True, )


@click.option('--tracker', '-t', is_flag=True,
              help='''This script enables you to make changes to the weekly weight/nutrition tracker''')
@click.option('--activity', '-a', is_flag=True,
              help='''This script enables you to make changes to the weekly activity tracker''')
@click.option('--notes', '-n', is_flag=True,
              help='''This script enables you to make changes t the athlete notes table''')
@cli.command('clear', short_help='clear stuff')  # @cli, not @click!
def clear(tracker, activity, notes):
    """
    \b
    Enables you to clear entries.
    Clears all entries in the athlete notes table, weight/nutrition tracker, and activity tracker,
    unless given specific sections to clear by option parameters.
    """
    if tracker:
        clear_tracker()
    if activity:
        clear_activity()
    if notes:
        clear_notes()
    if not tracker and not activity and not notes:
        clear_all()


@click.option('--tracker', '-t', is_flag=True,
              help='''This script enables you to make changes to the weekly weight/nutrition tracker''')
@click.option('--activity', '-a', is_flag=True,
              help='''This script enables you to make changes to the weekly activity tracker''')
@cli.command('update', short_help='get le data')
def update(tracker, activity):
    """
    \b
    Updates entries with latest API data.
    Updates both the weight/nutrition tracker and activity tracker, unless given an option parameter.
    """
    if tracker:
        populate_tracker(query_mfp())
    if activity:
        populate_activity(query_fitbit())
    if not tracker and not activity:
        populate_tracker(query_mfp())
        populate_activity(query_fitbit())


if __name__ == "__main__":
    cli()
