from contextlib import contextmanager
from datetime import timedelta
from itertools import count
from unittest.mock import patch

from freezegun import freeze_time
from gi.repository import GLib

from timer.TimerLoop import TimerLoop


@contextmanager
def timer_loop():
    """Context manager for running TimerLoop events

    The context object is a `TimerLoop` with a `run` method that can be
    called with a number of seconds to simulate elapsed time. Timeout
    functions will be called if their timeout expires within the elapsed
    time.
    """
    def timeout_add_seconds(interval, function, *data):
        tag = next(tags)
        timeouts[tag] = [interval, function, data]
        return tag

    def source_remove(tag):
        timeouts.pop(tag, None)

    def run(seconds):
        frozen_time.tick(timedelta(seconds=seconds))
        for tag, timeout in list(timeouts.items()):
            timeout[0] -= seconds
            interval, function, data = timeout
            if interval <= 0:
                timeouts.pop(tag)
                repeat = function(*data)
                assert repeat is False

    tags = count()
    timeouts = {}
    loop = TimerLoop()
    assert not hasattr(loop, "run")
    loop.run = run
    try:
        with patch.object(GLib, "timeout_add_seconds", timeout_add_seconds), \
                patch.object(GLib, "source_remove", source_remove), \
                freeze_time("12pm") as frozen_time:
            yield loop
    finally:
        loop.quit()
