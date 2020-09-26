"""Simple fixture decorators (avoid pytest fixture injection magic)

See also https://github.com/pytest-dev/pytest/issues/3834
"""
from contextlib import contextmanager, ExitStack

__all__ = ["fixture", "using"]

fixture = contextmanager


def using(*fixtures):
    """Use fixtures for test function"""
    if not fixtures:
        raise TypeError("at least one fixture is required")

    def apply_fixtures(test):
        def test_func():
            with ExitStack() as stack:
                args = [stack.enter_context(f()) for f in fixtures]
                test(*args)
        test_func.__doc__ = test.__doc__
        test_func.__module__ = test.__module__
        test_func.__name__ = test.__name__
        test_func.__qualname__ = test.__qualname__
        return test_func
    return apply_fixtures
