from tests.timer.notifications import notify
from tests.timer.util import patch_now


def test_no_timer_set(launcher):
    assert launcher.query("") == [
        "<Type in your query / Example: ti 10m Eggs are ready!>"
    ]


def test_5m_timer(launcher):
    result = launcher.query("5m")
    assert result == ["<Set timer for 5m / Message: Time is up!>"]


def test_5p_timer(launcher):
    result = launcher.query("5p")
    assert result == ["<Set timer for 5p / Message: Time is up!>"]


@patch_now
def test_review_timers(launcher, notifications):
    launcher.query("3s start")[0].enter()
    launcher.query("5m")[0].enter()
    assert notifications == ["<Timer is set>", "<Timer is set>"]
    assert launcher.query("") == [
        "<start / Time left: 2 seconds>",
        "<Time is up! / Time left: 4 minutes, 59 seconds>",
    ]
