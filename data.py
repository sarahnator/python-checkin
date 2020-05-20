import myfitnesspal as pal
import datetime
from datetime import date
import json
from collections import OrderedDict

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

for (x,y) in weights:
    # TODO query nutrition data
    weight_date = str(x)[5:]
    weight_w = str(y)
    # prints most recent --> least recent
    print((x,y))
    print("date: " + weight_date + " weight: "  + weight_w)
    #data_list_list.append(tuple(weight_w, weight_date))
    #data_list_list.extend(tuple())


# TODO create functions to extract m/d/y
# def get_year()
# def get_month()
# def get_day()


# ####################################
# # extract json information @sheetName
# with open('../json/creds.json') as src:
#     data = json.load(src)
#
# client = pal.Client(data['email'])
# day = client.get_date(y, m, d)
#
# # get pal day totals
# total = day.totals
# print(total)
#
# # int day totals
# cal, pro, car, fat, fiber = 0, 0, 0, 0, 0
#
# # check if data exists
# if total:
#     cal = total['calories']
#     pro = total['protein']
#     car = total['carbohydrates']
#     fat = total['fat']
#     fiber = total['fiber']
# # check values
# #print("cal: " + str(cal) + " pro: " + str(pro) + " car: " + str(car) + " fat: " + str(fat) + " fiber " + str(fiber))
#
# ####################################
#
# # get weights since given day
# day = datetime.date(y, m, d)
# weights = client.get_measurements('Weight', day)
# # convert ordered dictionary to list
# weights = list(weights.items())
# # extract date for 0th item format mm-dd
# weight_date = str(weights[0][0])[5:]
# print(weight_date)
#
# # extract weight on 0th day
# weight_w = weights[0][1]
# print(weight_w)
#
#
# # # behavior for undefined future weights not yet logged
# # # returns last logged weight
# # d += 1
# # day = datetime.date(int(y), int(m), int(d))
# # newweight = client.get_measurements('Weight', day)
# # print(newweight)
# # print(str(d))
#
# # # within range of days
# # thiswk = datetime.date(int(y), int(m), int(d))
# # lastwk = datetime.date(int(y), int(m), int(d))
# # weight = client.get_measurements('Weight', thiswk, lastwk)
#
# # TODO: get weight, pair with nutrient data
# # TODO: get date input
#
