import myfitnesspal as pal
import datetime
from datetime import date
import json
from collections import OrderedDict
if __name__ == "__main__":
    print("hello")

# extract json information @sheetName
with open('../json/creds.json') as src:
    data = json.load(src)

client = pal.Client(data['email'])

# get system date in string format YYYYMMDD
date = date.today()
date = str(date.strftime("%Y%m%d"))

# get month, day, year params
y = int(date[:4])
m = date[4:6]
d = date[6:]
if m[0] == '0':
    m = m[1]
if d[0] == '0':
    d = d[1]
m = int(m)
d = int(d)

day = client.get_date(int(y), int(m), int(d))

# get pal day totals
total = day.totals
print(total)

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

# get weights since given day
day = datetime.date(int(y), int(m), int(d))
weights = client.get_measurements('Weight', day)
# convert ordered dictionary to list
weights = list(weights.items())
# extract date for 0th item format mm-dd
weight_date = str(weights[0][0])[5:]
print(weight_date)

# extract weight on 0th day
weight_w = weights[0][1]
print(weight_w)


# # behavior for undefined future weights not yet logged
# # returns last logged weight
# d += 1
# day = datetime.date(int(y), int(m), int(d))
# newweight = client.get_measurements('Weight', day)
# print(newweight)
# print(str(d))

# # within range of days
# thiswk = datetime.date(int(y), int(m), int(d))
# lastwk = datetime.date(int(y), int(m), int(d))
# weight = client.get_measurements('Weight', thiswk, lastwk)
