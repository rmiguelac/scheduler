import re

from datetime import timedelta


def relative_date_to_timedelta(date: str) -> timedelta:
    """
    handles relative dates and returns the timedelta
    object with current time adding the given relative value
    """
    relative_pattern = re.compile('\d*[hms]{1}', re.IGNORECASE)
    if relative_pattern.match(date):
        delta = int(re.sub('[dhms]', '', date, re.IGNORECASE))
        if 'h' in date or 'H' in date:
            return timedelta(hours=delta)
        elif 'm' in date or 'M' in date:
            return timedelta(minutes=delta)
        elif 'd' in date or 'D' in date:
            return timedelta(days=delta)
        else:
            return timedelta(seconds=delta)