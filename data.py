import myfitnesspal as pal
import datetime
from datetime import date

if __name__ == "__main__":
    print("hello")

client = pal.Client('almundbutter@gmail.com')

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
# int day totals
cal = total['calories']
pro = total['protein']
car = total['carbohydrates']
fat = total['fat']
fiber = total['fiber']

# check values
# print("cal: " + str(cal) + " pro: " + str(pro) + " car: " + str(car) + " fat: " + str(fat) + " fiber " + str(fiber))

# get weights
# since given day
day = datetime.date(int(y), int(m), int(d))
weight = client.get_measurements('Weight', day)
print(weight)

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

# TODO: parse ordered dictionary return param for weight