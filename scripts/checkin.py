import myfitnesspal as pal
from scripts.spreadsheet import *
from scripts.dateUtils import *
import click
from scripts.fitbit import *

# !/usr/bin/env python

def query_update():
    print("Querying MyFitnessPal...")
    # init connection to mfp api
    with open('json/creds.json') as src:
        data = json.load(src)
    client = pal.Client(data['email'])

    with click.progressbar(length=4, label='Fetching weight trends') as bar:
        # query weights
        last_sunday = get_sunday()
        bar.update(1)
        y, m, d = last_sunday.year, last_sunday.month, last_sunday.day
        day = datetime.date(y, m, d)
        bar.update(2)
        weights = client.get_measurements('Weight', day)
        bar.update(3)
        weights = list(weights.items())  # convert ordered dictionary to list
        bar.update(4)

    data_list = []  # container for data row

    with click.progressbar(weights, label='Fetching nutrition data', length=len(weights)) as bar:
        for (a, b) in bar:
            # query nutrition data
            date = a
            y, m, d = date.year, date.month, date.day

            # get totals
            day = client.get_date(y, m, d)
            total = day.totals

            # int day totals
            cal, pro, car, fat, fiber = 0, 0, 0, 0, 0

            # check if data exists
            if total:
                total.pop("sodium")  # I am sodium queen DGAF - remove stat from dict
                desired_order = ["calories", "protein", "carbohydrates", "fat", "fiber"]
                total = {t: total[t] for t in desired_order}  # reorder list: {cal, pro, carb, fat, fiber}
            else:
                total = {"cal": cal, "pro": pro, "car": car, "fat": fat, "fiber": fiber}

            weight = str(b)
            # prints most recent --> least recent
            data_row = {"weight": weight, "date": date}
            data_row.update(total)  # append totals
            data_list.insert(0, data_row)  # prepend to front of list of all data

    # print(data_list)
    update_tracker(data_list)

#     click.secho(' All entries updated! ', reverse=True)


@click.group(chain=True)
def cli():
    click.echo('Hello! Making changes to your spreadsheet...')

@cli.command('note', short_help='add note')  # @cli, not @click!
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
        query_update()
    if activity:
        populate_activity(fitbit_query())
    if not tracker and not activity:
        query_update()
        populate_activity(fitbit_query())

if __name__ == "__main__":
    cli()





