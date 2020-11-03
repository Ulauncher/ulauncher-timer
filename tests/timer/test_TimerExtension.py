from threading import Event, Thread

import pytest

from .fixtures import using
from .launcher import TimerLauncher
from .notifications import notify


@using(TimerLauncher)
def test_no_timer_set(launcher):
    assert launcher.query("") == [
        "<Type in your query / Example: ti 10m Eggs are ready!>"
    ]


@using(TimerLauncher)
def test_5m_timer(launcher):
    result = launcher.query("5m")
    assert result == ["<Set timer for 5m / Message: Time is up!>"]


@using(TimerLauncher)
def test_5p_timer(launcher):
    result = launcher.query("5p")
    assert result == ["<Set timer for 5p / Message: Time is up!>"]


@using(notify, TimerLauncher)
def test_review_timers(notifications, launcher):
    launcher.query("3s start")[0].enter()
    launcher.query("5m")[0].enter()
    assert notifications == [
        "<start at 12:00 PM>",
        "<Time is up! at 12:05 PM>",
    ]
    assert launcher.query("") == [
        "<start at 12:00 PM / Select to stop>",
        "<Time is up! at 12:05 PM / Select to stop>",
    ]


@using(notify, TimerLauncher)
def test_stop_timer(notifications, launcher):
    launcher.query("3s start")[0].enter()
    launcher.query("5m")[0].enter()
    stop_query = launcher.query("")
    assert stop_query == [
        "<start at 12:00 PM / Select to stop>",
        "<Time is up! at 12:05 PM / Select to stop>",
    ]
    stop_query[0].enter()
    assert notifications == [
        "<start at 12:00 PM>",
        "<Time is up! at 12:05 PM>",
        "<Timer stopped / start at 12:00 PM>",
    ]
    assert launcher.query("") == ["<Time is up! at 12:05 PM / Select to stop>"]


@using(notify, TimerLauncher(persistent=True))
def test_on_timer_end_race(notifications, launcher):
    # should not error in unlikely event that a on_end() callback is
    # queued just after timer is stopped
    def loop_runner():
        # will block on call_after_delay
        loop.run(4)
        try:
            # should not error, but did before bug was fixed
            loop.run(10)
        except Exception as err:
            errors.append(err)
            raise

    def blocking_call_after_delay(*args, **kw):
        call_event.set()
        if not stop_event.wait(1):
            pytest.fail("unexpected timeout waiting for stop")
        return real_call_after_delay(*args, **kw)

    # start timer before blocking_call_after_delay is installed
    launcher.query("3s race")[0].enter()

    loop = launcher.timer.loop
    real_call_after_delay = loop.call_after_delay
    loop.call_after_delay = blocking_call_after_delay
    call_event = Event()
    stop_event = Event()
    errors = []

    stop_query = launcher.query("")
    assert stop_query == ["<race at 12:00 PM / Select to stop>"]
    thread = Thread(target=loop_runner)
    thread.start()
    if not call_event.wait(1):
        pytest.fail("unexpected timeout waiting for call_after_delay")
    loop.call_after_delay = real_call_after_delay  # restore non-blocking
    stop_query[0].enter()
    stop_event.set()
    thread.join()
    assert not errors
    assert notifications == [
        "<race at 12:00 PM>",
        "<race>",
        "<Timer stopped / race at 12:00 PM>",
        "<race / 10 seconds ago>",  # extra notification after stop
    ]
