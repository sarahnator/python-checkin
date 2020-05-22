import myfitnesspal as pal
import datetime
import json
from spreadsheet import *
from dateUtils import *
import click


def run():
    # init connection to mfp api
    with open('../json/creds.json') as src:
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

    # make config helper class to set note flag
    # create notes func in spreadsheet
    # test test test


class Config(object):
    def __init__(self):
        self.note = False


pass_config = click.make_pass_decorator(Config, ensure=True)  # ensure=True: first usage, object will be created


@click.group()
@click.option('--note', is_flag=True,
              help='''This script edits the athlete notes table.''')
@pass_config
def cli(note, day_of_week, notes, config):
    click.echo('Coming soon: entering %s into athlete notes table' % note)
    config.note = note


@click.argument('day_of_week', type=str)
@click.argument('notes', type=str)
@click.command()
@pass_config
# config argument main(config)
def main(config):
    print("Hello! Updating your spreadsheet...")
    run()
    # if config.note:
    #     click.echo('we are in note mode')
    #     # run edit notes command


if __name__ == "__main__":
    main()
    # print("Hello! Updating your spreadsheet...")
    # run()
