from contextlib import contextmanager
from dataclasses import dataclass, field


class MockNotify:
    def init(name):
        pass

    @dataclass
    class Notification:
        name: str
        text: str
        icon_path: str

        @classmethod
        def new(cls, *args, **kw):
            return cls(*args, **kw)

        def __eq__(self, other):
            if isinstance(other, str):
                return repr(self) == other
            return NotImplemented

        def __repr__(self):
            return f"<{self.text}>"

        def show(self):
            assert hasattr(MockNotify, "notifications"), \
                "tests.timer.notifications.notify context is missing"
            MockNotify.notifications.append(self)


@contextmanager
def notify():
    MockNotify.notifications = []
    try:
        yield MockNotify.notifications
    finally:
        del MockNotify.notifications