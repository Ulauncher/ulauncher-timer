from datetime import timedelta

import pytest

from timer.timediff_formatter import round_time_units


@pytest.mark.parametrize("input,output", [
    (timedelta(minutes=151), timedelta(hours=3)),
    (timedelta(minutes=150), timedelta(hours=2)),
    (timedelta(minutes=130), timedelta(hours=2)),
    (timedelta(minutes=125), timedelta(hours=2)),
    (timedelta(minutes=121), timedelta(hours=2)),
    (timedelta(minutes=118), timedelta(hours=2)),
    (timedelta(minutes=117), timedelta(hours=1, minutes=55)),

    (timedelta(minutes=66), timedelta(hours=1, minutes=5)),
    (timedelta(minutes=65), timedelta(hours=1, minutes=5)),
    (timedelta(minutes=64), timedelta(hours=1, minutes=5)),
    (timedelta(minutes=63), timedelta(hours=1, minutes=5)),
    (timedelta(minutes=62), timedelta(hours=1)),
    (timedelta(minutes=61), timedelta(hours=1)),
    (timedelta(minutes=60), timedelta(hours=1)),

    (timedelta(minutes=59), timedelta(minutes=59)),
    (timedelta(seconds=90), timedelta(seconds=120)),
    (timedelta(seconds=89), timedelta(seconds=60)),
    (timedelta(seconds=70), timedelta(seconds=60)),
    (timedelta(seconds=61), timedelta(seconds=60)),
    (timedelta(seconds=59), timedelta(seconds=60)),

    (timedelta(seconds=15), timedelta(seconds=20)),
    (timedelta(seconds=14), timedelta(seconds=10)),
    (timedelta(seconds=13), timedelta(seconds=10)),
    (timedelta(seconds=12), timedelta(seconds=10)),
    (timedelta(seconds=11), timedelta(seconds=10)),
    (timedelta(seconds=10), timedelta(seconds=10)),
    (timedelta(seconds=6), timedelta(seconds=10)),
])
def test_round_time_units(input, output):
    assert str(round_time_units(input)) == str(output), f"{input} -> {output}"
