import datetime

from dateutil.relativedelta import relativedelta


def get_year_and_quarter(date_str):
    year = int(date_str.strftime('%Y'))
    month = int(date_str.strftime('%m'))
    quarter = (month - 1) // 3 + 1
    return year, quarter


def get_recent_n_year(n=1):
    now = datetime.datetime.now()
    start = now - n * relativedelta(months=12)
    return start, now
