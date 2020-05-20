import myfitnesspal as pal
import datetime
from datetime import date
import json
from collections import OrderedDict


# TODO create functions to extract m/d/y
def get_year(y):
    return y[:4]


def get_month(m):
    m = str(m)[5:]
    if m[0] == '0':
        m = m[1]
    else:
        m = m[0:2]
    #print(m)
    return m

def get_day(d):
    d = str(d)[5:]
    x = d.find('-')
    d = str(d)[x + 1:]
    if d[0] == '0':
        d = d[1]
    else:
        d = d[0:2]
    # print(d)
    return d

if __name__ == "__main__":
    print("hello")

multiline_str = """Supported operations:
1. To update from custom date, specify start date [m/d]
2. To update current day, press enter key
"""
op = input(multiline_str)

# update using current date
if op == "":
    # get system date in string format YYYYMMDD
    date = date.today()
    date = str(date.strftime("%Y%m%d"))
    # get month, day, year params from system date
    y = date[:4]
    m = date[4:6]
    d = date[6:]
    if m[0] == '0':
        m = m[1]
    if d[0] == '0':
        d = d[1]
# update from custom date m/d mm/d m/dd mm/dd
else:
    # convert custom date to format
    if len(op) == 3:
        m = op[0]
        d = op[2]
    elif len(op) == 4:
        x = op.find('/')
        print(op)
        # print("x index is " + str(x))
        m = op[0:x]
        d = op[x + 1:]
    else:
        m = op[0:2]
        d = op[3:]
    y = input("Enter year:\n")
# print("year: " + str(y) + " month: " + str(m) + " day: " + str(d))

####################################

# init connection to mfp api
with open('../json/creds.json') as src:
    data = json.load(src)
client = pal.Client(data['email'])

# query weights
day = datetime.date(int(y), int(m), int(d))
weights = client.get_measurements('Weight', day)
# convert ordered dictionary to list
weights = list(weights.items())
# container for data row
data_list_list = []

for (a, b) in weights:
    # TODO query nutrition data
    date = str(a)
    y = get_year(date)
    m = get_month(date)
    d = get_day(date)

    # get totals
    day = client.get_date(int(y),int(m), int(d))
    total = day.totals

    # int day totals
    cal, pro, car, fat, fiber = 0, 0, 0, 0, 0

    # check if data exists
    if total:
        cal = total['calories']
        pro = total['protein']
        car = total['carbohydrates']
        fat = total['fat']
        fiber = total['fiber']
    # check values
    print("cal: " + str(cal) + " pro: " + str(pro) + " car: " + str(car) + " fat: " + str(fat) + " fiber " + str(fiber))

    # eat up year
    weight_date = date[5:]
    weight = str(b)
    # prints most recent --> least recent
    print((a, b))
    print("date: " + weight_date + " weight: " + weight)
    data_row = [weight, weight_date, cal, pro, car, fat, fiber]
    print(data_row)
    data_list_list.append(data_row)

print(data_list_list)



