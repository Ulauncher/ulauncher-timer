import pytest
from timer.query_parser import parse_query, ParseQueryError


def test_parse_query__5m_hello_world__correct_result_returned():
    assert parse_query('5m hello world') == (5 * 60, '5m', 'hello world')


def test_parse_query__5h_hello_world__correct_result_returned():
    assert parse_query('5h hello world') == (5 * 60 * 60, '5h', 'hello world')


def test_parse_query__5__is_correct_query():
    assert parse_query('5') == (5 * 60, '5', 'Time is up!')


def test_parse_query__5h_37m_hello__correct_result_returned():
    assert parse_query('5h37m hello') == (5 * 60 * 60 + 37 * 60, '5h37m', 'hello')


def test_parse_query__1h_2s_hello__correct_result_returned():
    assert parse_query('1h2s hello') == (1 * 60 * 60 + 2, '1h2s', 'hello')

def test_parse_query__2m_5s__is_correct_query():
    assert parse_query('2m5s') == (2*60 + 5, '2m5s', 'Time is up!')


def test_pasrse_query__is_case_insensitive():
    assert parse_query('1H2M3S') == (1 * 60 * 60 + 2 * 60 + 3, '1H2M3S', 'Time is up!')

def test_parse_query__incorrect_query__ParseQueryError():
    with pytest.raises(ParseQueryError):
        assert parse_query('wfa')

def test_parse_query__incorrect_query_with_no_units__ParseQueryError():
    with pytest.raises(ParseQueryError):
        assert parse_query('1h3')