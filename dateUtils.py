import datetime
from datetime import date
from dateutil import relativedelta

def get_sunday():
    today = datetime.datetime.now()
    start = today - datetime.timedelta((today.weekday() + 1) % 7)
    sun = start + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    return sun
