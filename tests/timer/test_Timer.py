import pytest
from threading import Event, Thread

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
    assert notifications == [
        "<Time is up! at 12:00 PM>",
        "<Time is up!>",
    ]
    assert sum(sounds) == 1


@using(timer_loop, notify, sound)
def test_persistent_timer(loop, notifications, sounds):
    def callback(timer):
        timers.remove(timer)

    timer = Timer(75, "Time is up!", callback, persistent=True)
    timer.start(loop)
    timers = {timer}
    assert notifications == ["<Time is up! at 12:01 PM>"]
    assert not sounds
    intervals = [76, 10, 10, 10, 30, 30, 30, 60, 60, 60, 60]
    for i, interval in enumerate(intervals, start=1):
        loop.run(interval)
        assert len(notifications) == i + 1
        assert sum(sounds) == i
    assert notifications[2] == "<Time is up! / 10 seconds ago>"
    assert notifications[-2] == "<Time is up! / 5 minutes ago>"
    assert notifications[-1] == "<Time is up! / 6 minutes ago>"
    notifications[-1].close()
    loop.run(180)
    assert len(notifications) == len(intervals) + 1
    assert len(sounds) == len(intervals)
    assert not timers


@pytest.mark.parametrize("elapsed,msg", [
    (200, "<Time is up! / 3 minutes ago>"),
    (3840, "<Time is up! / 1 hour, 5 minutes ago>"),
    (7440, "<Time is up! / 2 hours ago>"),
])
@using(timer_loop, notify, sound)
def test_long_overdue_persistent_timer(loop, notifications, sounds, elapsed, msg):
    def callback(timer):
        timers.remove(timer)

    timer = Timer(135, "Time is up!", callback, persistent=True)
    timer.start(loop)
    timers = {timer}
    assert notifications == ["<Time is up! at 12:02 PM>"]
    assert not sounds
    loop.run(136 + elapsed)
    assert notifications[-1] == msg
    notifications[-1].close()
    assert not timers


@using(timer_loop, notify, sound)
def test_persistent_timer_notification_race(loop, notifications, sounds):
    # should not continue to alert if timer is stopped while on_end()
    # callback is executing (likely playing notification sound)
    def loop_runner():
        # will block on notify
        loop.run(4)
        # these should not notify, but did before bug was fixed
        loop.run(10)
        loop.run(10)
        loop.run(10)

    def blocking_notify(*args, **kw):
        notify_event.set()
        if not stop_event.wait(1):
            pytest.fail("unexpected timeout waiting for stop")
        real_notify(*args, **kw)

    timer = Timer(3, "Race!", (lambda x: None), persistent=True)
    timer.start(loop)
    assert notifications == ["<Race! at 12:00 PM>"]

    real_notify = timer.notify
    timer.notify = blocking_notify
    notify_event = Event()
    stop_event = Event()

    thread = Thread(target=loop_runner)
    thread.start()
    if not notify_event.wait(1):
        pytest.fail("unexpected timeout waiting for notify")
    timer.stop(loop)
    stop_event.set()
    thread.join()
    assert notifications == ["<Race! at 12:00 PM>", "<Race!>"]
