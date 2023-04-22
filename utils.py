import datetime


def get_today_formatted(days=0):
    return (datetime.date.today() -
            datetime.timedelta(days=days)).strftime('%Y-%m-%d')
