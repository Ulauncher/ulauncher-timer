import pytest

from tests.timer.launcher import TimerLauncher

@pytest.fixture
def launcher():
    with TimerLauncher() as tx:
        yield tx
