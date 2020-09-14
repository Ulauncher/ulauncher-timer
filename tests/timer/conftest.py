import pytest

from tests.timer.launcher import TimerLauncher
from tests.timer.notifications import notify

@pytest.fixture
def launcher():
    with TimerLauncher() as tx:
        yield tx

@pytest.fixture
def notifications():
    with notify() as notifications:
        yield notifications
