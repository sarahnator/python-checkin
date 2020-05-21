import myfitnesspal as pal
import datetime
from datetime import date
import json
from collections import OrderedDict
from spreadsheet import *
from dateUtils import *
import click
#from dateutil.parser import parse

def weight_year(y):
    return y[:4]

def weight_month(m):
    m = str(m)[5:]
    if m[0] == '0':
        m = m[1]
    else:
        m = m[0:2]
    #print(m)
    return m

def weight_day(d):
    d = str(d)[5:]
    x = d.find('-')
    d = str(d)[x + 1:]
    if d[0] == '0':
        d = d[1]
    else:
        d = d[0:2]
    # print(d)
    return d


def run():
    # init connection to mfp api
    with open('../json/creds.json') as src:
        data = json.load(src)
    client = pal.Client(data['email'])

    # query weights
    last_sunday = get_sunday()
    # day = parse(last_sunday, dayfirst=False)
    y = get_year(last_sunday)
    m = get_month(last_sunday)
    d = get_day(last_sunday)
    # print("day " + str(day))
    # print("y/m/d: " + str(y), str(m), str(d))

    day = datetime.date(int(y), int(m), int(d))
    weights = client.get_measurements('Weight', day)
    # convert ordered dictionary to list
    weights = list(weights.items())
    # container for data row
    data_list = []


    for (a, b) in weights:
        # query nutrition data
        date = str(a)
        # print(date)
        y = weight_year(date)
        m = weight_month(date)
        d = weight_day(date)

        # get totals
        day = client.get_date(int(y), int(m), int(d))
        total = day.totals

        # int day totals
        cal, pro, car, fat, fiber = 0, 0, 0, 0, 0

        # check if data exists
        if total:
            total.pop("sodium")  # I am sodium queen DGAF
            # cal = total['calories']
            # pro = total['protein']
            # car = total['carbohydrates']
            # fat = total['fat']
            # fiber = total['fiber']
            desired_order = ["calories", "protein", "carbohydrates", "fat", "fiber"]
            # reorder list: cal, pro, carb, fat, fiber
            total = {t: total[t] for t in desired_order}
            #print(total)
        else:
            total = {"cal": cal, "pro": pro, "car": car, "fat": fat, "fiber": fiber}
        # check values
        #print("cal: " + str(cal) + " pro: " + str(pro) + " car: " + str(car) + " fat: " + str(fat) + " fiber " + str(fiber))

        weight = str(b)
        # prints most recent --> least recent
        print((a, b))
        print("date: " + date + " weight: " + weight)
        # data_row = {"weight": weight, "date": date, "cal": cal, "pro": pro, "car": car, "fat": fat, "fiber": fiber}
        data_row = {"weight": weight, "date": date}
        data_row.update(total)
        #print(data_row)
        # prepend
        data_list.insert(0, data_row)

    # print(data_list)
    update_col(data_list)


if __name__ == "__main__":
    print("hello")
    run()