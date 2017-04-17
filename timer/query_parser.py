import re
from dateutil.relativedelta import relativedelta


TIME_MULT = {
    'h': 60 * 60,
    'm': 60,
    's': 1
}
ATTRS = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']


def parse_query(query, default_text='Time is up!'):
    """
    >>> '5m hello world'
    <<< (300, '5 minutes', 'hello world')
    >>> '3h Go'
    <<< (3*60*60, '3 hours', 'Go')
    >>> '5'
    <<< (300, '5 minutes', 'Time is up!')
    """
    try:
        time_arg = query.split(' ')[0]
        assert time_arg, "Incorrect time"
        m = re.match(r'^(?P<time>\d+)(?P<measure>[mhs])?$', time_arg, re.I)
        time_sec = int(m.group('time')) * TIME_MULT[(m.group('measure') or 'm').lower()]

        message = ' '.join(query.split(' ')[1:]).strip()
        message = message or default_text

        return (time_sec, ' '.join(human_readable(time_sec)), message)
    except Exception as e:
        raise ParseQueryError(e.message)


def human_readable(seconds):
    """
    >>> 125
    <<< ['2 hours', '5 minutes']
    """
    delta = relativedelta(seconds=seconds)
    return ['%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
            for attr in ATTRS if getattr(delta, attr)]


class ParseQueryError(Exception):
    pass
