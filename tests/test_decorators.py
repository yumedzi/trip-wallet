from decorators import log_call, timed


def add(a, b):
    return a + b


def test_log_call_returns_the_result():
    assert log_call(add)(2, 3) == 5


def test_timed_returns_the_result():
    assert timed(add)(2, 3) == 5


def test_decorated_function_still_works_twice():
    logged = log_call(add)
    assert [logged(1, 1), logged(2, 2)] == [2, 4]


def test_log_call_prints_the_call_and_result(capsys):
    log_call(add)(2, 3)
    assert capsys.readouterr().out == 'calling add(2, 3)\nadd returned 5\n'


def test_timed_prints_the_time(capsys):
    timed(add)(2, 3)
    out = capsys.readouterr().out
    assert 'add took' in out
    assert ' s' in out
