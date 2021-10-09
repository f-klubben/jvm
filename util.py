from datetime import datetime


def parse_email_date(datemsg):
    return datetime.strptime(datemsg, '%d/%m/%Y %H:%M:%S:%f')
