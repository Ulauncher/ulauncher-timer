from timer.Timer import Timer

from .fixtures import using
from .loop import timer_loop
from .notifications import notify
from .sounds import sound


@using(timer_loop, notify, sound)
def test_time_is_up(loop, notifications, sounds):
    def callback(timer):
        calls.append(timer)

    timer = Timer(5, "Time is up!", callback)
    timer.start(loop)
    assert timer.tag is not None
    calls = []
    loop.run(5)
    assert calls == [timer]
    assert timer.tag is None, timer.tag
    assert notifications == ["<Timer is set>", "<Time is up!>"]
    assert sum(sounds) == 1
