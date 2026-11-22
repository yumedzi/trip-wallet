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
