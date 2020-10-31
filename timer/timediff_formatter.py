from datetime import timedelta


def format_timediff(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
                period_value , seconds = divmod(seconds, period_seconds)
                has_s = 's' if period_value > 1 else ''
                strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)


def round_time_units(delta):
    """Round `timedelta` to nearest convenient time unit

    Rounding points:

    - nearest 1h if >= 2 hours
    - nearest 5m if >= 1 hour, 1 minute
    - nearest 1m if >= 1 minute
    - nearest 10s if < 1 minute
    """
    seconds = delta.total_seconds()
    if seconds >= 7200:
        round_to = 3600  # nearest hour
    elif seconds >= 3660:
        round_to = 300  # 5 minutes
    elif seconds >= 60:
        round_to = 60  # one minute
    else:
        round_to = 10
    return timedelta(seconds=round(seconds / round_to) * round_to)
