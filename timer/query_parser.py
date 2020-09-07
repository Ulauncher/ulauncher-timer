import re


time_regex = re.compile(
    r'^((?P<time_hours>\d+)h)?'
    r'((?P<time_minutes>\d+)m)?'
    r'((?P<time_seconds>\d+)s)?'
    r'(?P<time_nounits>\d+)?$',
    re.I
)


def parse_time_str(time_str):
    """
    >>> '5h'
    <<< (5, 0, 0)
    >>> '5m'
    <<< (0, 5, 0)
    >>> '5s'
    <<< (0, 0, 5)
    >>> '1h2m3s'
    <<< (1, 2, 3)
    """
    match = time_regex.match(time_str)
    hours = int(match.group('time_hours') or 0)
    minutes = int(match.group('time_minutes') or 0)
    seconds = int(match.group('time_seconds') or 0)
    no_units = int(match.group('time_nounits') or 0)
    if no_units != 0 and (hours > 0 or minutes > 0 or seconds > 0):
        raise ValueError("Bad format: time value with no unit is not allowed if values with units are present")

    return hours, minutes + no_units, seconds


def parse_query(query, default_text='Time is up!'):
    """
    >>> '5m hello world'
    <<< (300, '5m', 'hello world')
    >>> '3h Go'
    <<< (3*60*60, '3h', 'Go')
    >>> '5'
    <<< (300, '5', 'Time is up!')
    """
    try:
        time_arg = query.split(' ')[0]
        assert time_arg, "Incorrect time"
        hours, minutes, seconds = parse_time_str(time_arg)
        time_sec = hours * 60 * 60 + minutes * 60 + seconds

        message = ' '.join(query.split(' ')[1:]).strip()
        message = message or default_text

        return (time_sec, time_arg, message)
    except Exception as e:
        raise ParseQueryError(str(e))


class ParseQueryError(Exception):
    pass
