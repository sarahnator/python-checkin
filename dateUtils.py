import datetime
from datetime import date
from dateutil import relativedelta

def get_sunday():
    today = datetime.datetime.now()
    start = today - datetime.timedelta((today.weekday() + 1) % 7)
    sun = start + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    sunday_date = '{:%m/%d/%y}'.format(sun)
    return sunday_date

def get_year(y):
    year = '20' + str(y[6:])
    print("year " + year)
    return year

def get_month(m):
    m = str(m)[0:3]
    if m[0] == '0':
        m = m[1]
    return m


def get_day(d):
    d = d[3:5]
    if d[0] == '0':
        d = d[1]
    return d
