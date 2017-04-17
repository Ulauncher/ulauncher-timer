import pytest
from timer.query_parser import parse_query, ParseQueryError


def test_parse_query__5m_hello_world__correct_result_returned():
    assert parse_query('5m hello world') == (5 * 60, '5 minutes', 'hello world')


def test_parse_query__5h_hello_world__correct_result_returned():
    assert parse_query('5h hello world') == (5 * 60 * 60, '5 hours', 'hello world')


def test_parse_query__5__is_correct_query():
    assert parse_query('5') == (5 * 60, '5 minutes', 'Time is up!')


def test_parse_query__incorrect_query__ParseQueryError():
    with pytest.raises(ParseQueryError):
        assert parse_query('wfa')
