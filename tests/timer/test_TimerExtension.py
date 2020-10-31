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
@using(TimerLauncher, notify)
def test_review_timers(launcher, notifications):
    launcher.query("3s start")[0].enter()
    launcher.query("5m")[0].enter()
    assert notifications == ["<Timer is set>", "<Timer is set>"]
    assert launcher.query("") == [
        "<start / Time left: 3 seconds>",
        "<Time is up! / Time left: 5 minutes>",
    ]
