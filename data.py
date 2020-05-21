import myfitnesspal as pal
import datetime
from datetime import date
import json
from collections import OrderedDict
from spreadsheet import *
from dateUtils import *
import click
#from dateutil.parser import parse


def run():
    # init connection to mfp api
    with open('../json/creds.json') as src:
        data = json.load(src)
    client = pal.Client(data['email'])

    # query weights
    last_sunday = get_sunday()
    y = last_sunday.year
    m = last_sunday.month
    d = last_sunday.day
    # day = parse(last_sunday, dayfirst=False)

    day = datetime.date(y, m, d)
    weights = client.get_measurements('Weight', day)
    # convert ordered dictionary to list
    weights = list(weights.items())
    # container for data row
    data_list = []


    for (a, b) in weights:
        # query nutrition data
        # date = str(a)
        date = a
        y = date.year
        m = date.month
        d = date.day

        # get totals
        day = client.get_date(y, m, d)
        total = day.totals

        # int day totals
        cal, pro, car, fat, fiber = 0, 0, 0, 0, 0

        # check if data exists
        if total:
            total.pop("sodium")  # I am sodium queen DGAF - remove stat from dict
            desired_order = ["calories", "protein", "carbohydrates", "fat", "fiber"]
            # reorder list: {cal, pro, carb, fat, fiber}
            total = {t: total[t] for t in desired_order}
        else:
            total = {"cal": cal, "pro": pro, "car": car, "fat": fat, "fiber": fiber}
        # check values

        weight = str(b)
        # prints most recent --> least recent
        # print((a, b))
        # print("date: " + str(date) + " weight: " + weight)
        data_row = {"weight": weight, "date": date}
        data_row.update(total)
        # prepend
        data_list.insert(0, data_row)

    print(data_list)
    update_col(data_list)


if __name__ == "__main__":
    print("Hello! Updating your spreadsheet...")
    run()