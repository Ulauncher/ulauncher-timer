"""Simple fixture decorators (avoid pytest fixture injection magic)

See also https://github.com/pytest-dev/pytest/issues/3834
"""
from contextlib import contextmanager, ExitStack
from functools import wraps

__all__ = ["fixture", "using"]

fixture = contextmanager


def using(*fixtures):
    """Use fixtures for test function"""
    if not fixtures:
        raise TypeError("at least one fixture is required")

    def apply_fixtures(test):
        @wraps(test)
        def test_func(*args, **kw):
            with ExitStack() as stack:
                fixture_args = [stack.enter_context(f()) for f in fixtures]
                test(*fixture_args, *args, **kw)
        test.nonmagic_fixtures_count = len(fixtures)
        test_func.nonmagic_fixtures_count = len(fixtures)
        return test_func
    return apply_fixtures


def _patch_pytest_num_mock_patch_args():
    # HACK support @pytest.mark.parametrize(...) on @using(...)-wrapped tests
    def num_mock_patch_args(function):
        num = getattr(function, "nonmagic_fixtures_count", 0)
        return num + real_num_mock_patch_args(function)

    import _pytest.compat as compat
    real_num_mock_patch_args = compat.num_mock_patch_args
    compat.num_mock_patch_args = num_mock_patch_args


_patch_pytest_num_mock_patch_args()
