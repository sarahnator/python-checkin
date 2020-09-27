import datetime
from datetime import date
from dateutil import relativedelta


def get_sunday():
    """
    Gets the last calendar Sunday.
    :return sun: datetime object for Sunday.
    """
    today = datetime.datetime.now()
    start = today - datetime.timedelta((today.weekday() + 1) % 7)
    sun = start + relativedelta.relativedelta(weekday=relativedelta.SU(-1))
    return sun

def get_base_sunday(t_minus=0):
    """
        Calculates base sunday for API call.
        :param t_minus: takes an integer input corresponding to desired time shift
        Default behavior (0) means today's date.
        Positive values indicate to go forward in time (+1 means tomorrow)
        negative valus indicate to go back in time (-1 means yesterday, -7 is the past week)
        :return date: datetime object for desired date.
    """
    sun = datetime.datetime.today() + datetime.timedelta(days=t_minus)
    return sun

