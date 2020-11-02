from freezegun import freeze_time

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


@freeze_time("12pm")
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


@freeze_time("12pm")
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
