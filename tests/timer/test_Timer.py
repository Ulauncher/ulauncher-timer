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


@using(timer_loop, notify, sound)
def test_persistent_timer(loop, notifications, sounds):
    def callback(timer):
        timers.remove(timer)

    timer = Timer(75, "Time is up!", callback, persistent=True)
    timer.start(loop)
    timers = {timer}
    assert notifications == ["<Timer is set>"]
    assert not sounds
    intervals = [75, 10, 10, 10, 30, 30, 30, 60, 60, 60, 60]
    for i, interval in enumerate(intervals, start=1):
        loop.run(interval)
        assert notifications[-1] == "<Time is up!>"
        assert len(notifications) == i + 1
        assert sum(sounds) == i
    notifications[-1].close()
    loop.run(180)
    assert len(notifications) == len(intervals) + 1
    assert len(sounds) == len(intervals)
