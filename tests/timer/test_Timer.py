from timer.Timer import Timer

from .fixtures import using
from .notifications import notify
from .sounds import sound

INSTANT = 0.00001


@using(notify, sound)
def test_time_is_up(notifications, sounds):
    def callback(timer):
        calls.append(timer)

    calls = []
    timer = Timer(INSTANT, "Time is up!", callback)
    timer.timer.run()
    assert calls == [timer]
    assert timer.timer is None, timer.timer
    assert notifications == ["<Time is up!>"]
    assert sum(sounds) == 1
