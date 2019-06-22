import re
from datetime import datetime


def read_more():
    return '\u200b' * 4000


def is_date_equal_or_bigger(d1, d2):
    # 2 = year; 1 = month; 0 = day
    return (d1[2] > d2[2]) or (d1[2] == d2[2] and d1[1] > d2[1]) or \
           (d1[2] == d2[2] and d1[1] == d2[1] and d1[0] > d2[0]) or \
           (d1[2] == d2[2] and d1[1] == d2[1] and d1[0] == d2[0])


def get_date_from_str(date):
    date_pattern = re.compile('(\d+)-(\d+)-(\d+).+')
    if date_pattern.match(date):
        d = date_pattern.match(date).groups()
        return [int(d[2]), int(d[1]), int(d[0])]
    else:
        return []


def get_datetime_from_format(date):
    if date is None:
        return None
    else:
        date = re.sub('([+-])(\\d{2}):(\\d{2})', r'\1\2\3', date)
        date_format = '%Y-%m-%dT%H:%M:%S%z'
        return datetime.strptime(date, date_format)


def get_date_from_sec(second):
    day_sec = (60 * 60 * 24)
    hour_sec = (60 * 60)
    min_sec = 60

    day = int(second / day_sec)
    hr = int(second % day_sec / hour_sec)
    mn = int(second % day_sec % hour_sec / min_sec)
    data = {'d': day, 'h': hr, 'm': mn}
    s = []
    for k, v in data.items():
        if v != 0 or k == 'm':
            s.append(f'{v}{k}')

    return ' '.join(s)
