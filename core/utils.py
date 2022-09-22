import datetime

def to_datetime(string):
    return datetime.datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %Z")

