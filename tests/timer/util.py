from datetime import datetime
from unittest.mock import patch

NOW = datetime(2020, 1, 1, 12)


def patch_now(test):
    return patch("timer.query_parser.datetime", DatetimeFixedNow)(test)


class DatetimeFixedNow(datetime):

    @classmethod
    def now(cls):
        return NOW
