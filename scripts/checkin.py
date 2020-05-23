import myfitnesspal as pal
import datetime
import json
<<<<<<< HEAD
from scripts.spreadsheet import *
from scripts.dateUtils import *
=======
from spreadsheet import *
from dateUtils import *
>>>>>>> e0157a949226f00e1860f8988c6c070a4aa26427
import click


# !/usr/bin/env python

def run():
    # init connection to mfp api
<<<<<<< HEAD
    with open('json/creds.json') as src:
=======
    with open('../json/creds.json') as src:
>>>>>>> e0157a949226f00e1860f8988c6c070a4aa26427
        data = json.load(src)
    client = pal.Client(data['email'])

    # query weights
    last_sunday = get_sunday()
    y, m, d = last_sunday.year, last_sunday.month, last_sunday.day
    day = datetime.date(y, m, d)
    weights = client.get_measurements('Weight', day)
    weights = list(weights.items())  # convert ordered dictionary to list

    data_list = []  # container for data row

    for (a, b) in weights:
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
    update_cols(data_list)


@click.command()
@click.option('--clear', '-c', is_flag=True,
              help='''This script clears:
               - Weekly weight and nutrition tracker
               - Athlete daily notes
               - Weekly activity tracker''')
# -m: call multiple times??
# multiple: enable mult calls
# confine first param to be day of week
<<<<<<< HEAD
@click.option('--note', '-n', multiple=True,
              type=(click.Choice(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], case_sensitive=False), str),
=======
@click.option('--note', '-m', multiple=True,
              type=(click.Choice(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']), str),
>>>>>>> e0157a949226f00e1860f8988c6c070a4aa26427
              default='', help='''This script edits the athlete notes table. Takes two parameters:
                @Param 3-letter abbreviation of weekday
                @Param message''')
def cli(clear, note):
    print("Hello! Updating your spreadsheet...")
<<<<<<< HEAD
=======
    run()
>>>>>>> e0157a949226f00e1860f8988c6c070a4aa26427
    if note:
        click.echo('we are in note mode')
        # run edit notes command
    if clear:
        click.echo('we are in clear mode')
<<<<<<< HEAD
    run()

=======
>>>>>>> e0157a949226f00e1860f8988c6c070a4aa26427


if __name__ == "__main__":
    cli()
<<<<<<< HEAD
=======

print("hello!!!")
>>>>>>> e0157a949226f00e1860f8988c6c070a4aa26427
