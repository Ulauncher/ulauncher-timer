import pytest
from timer.query_parser import parse_query, ParseQueryError
from util import patch_now


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


def secs(hours, minutes=0):
    return hours * 60 * 60 + minutes * 60


@pytest.mark.parametrize("query,result", [
    ("5p", secs(5)),
    ("5pm", secs(5)),
    ("530pm", secs(5, 30)),
    ("5:30p", secs(5, 30)),
    ("310p", secs(3, 10)),
    ("1010p", secs(10, 10)),
    ("10a", secs(22,)),
    ("1156a", secs(23, 56)),
    ("1203a", secs(0, 3)),
])
@patch_now
def test_parse_query__absolute_time__correct_result_returned(query, result):
    assert parse_query(f'{query} hello') == (result, query, 'hello')


@pytest.mark.parametrize("query,message", [
    ("5px", "Bad time format: 5px"),
    ("13p", "Bad time value: 13p"),
    ("25am", "Bad time value: 25am"),
    ("560p", "Bad time value: 560p")
])
@patch_now
def test_parse_query__absolute_time__error(query, message):
    with pytest.raises(ParseQueryError, match=message):
        value = parse_query(f'{query} hello')
        assert 0, f"unexpected value: {value!r}"
