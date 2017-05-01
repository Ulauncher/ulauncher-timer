import re


TIME_MULT = {
    'h': 60 * 60,
    'm': 60,
    's': 1
}


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
        m = re.match(r'^(?P<time>\d+)(?P<measure>[mhs])?$', time_arg, re.I)
        time_sec = int(m.group('time')) * TIME_MULT[(m.group('measure') or 'm').lower()]

        message = ' '.join(query.split(' ')[1:]).strip()
        message = message or default_text

        return (time_sec, time_arg, message)
    except Exception as e:
        raise ParseQueryError(e.message)


class ParseQueryError(Exception):
    pass
