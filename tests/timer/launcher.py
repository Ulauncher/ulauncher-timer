from dataclasses import dataclass
from contextlib import ExitStack

from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.search.Query import Query

from timer.TimerExtension import TimerExtension

from .loop import timer_loop
from .sounds import sound


class TimerLauncher:

    def __init__(self, persistent=False):
        self.timer = TimerExtension()
        self.timer.preferences["persistent"] = persistent
        self.timer.icon_path = "unknown"
        self.timer.loop.quit()
        self.client = self.timer._client = TestClient()
        self.loop_context = timer_loop()
        self.sound_context = sound()
        self.stack = ExitStack()
        self.sounds = None

    def __call__(self):
        return self

    def __enter__(self):
        self.timer.loop = self.stack.enter_context(self.loop_context)
        self.sounds = self.stack.enter_context(self.sound_context)
        return self

    def __exit__(self, *exc_info):
        tx = self.timer
        for timer in tx.get_timers():
            tx.stop_timer(timer.id)
        tx.quit()
        self.stack.close()
        assert not tx.timers, tx.timers

    def query(self, query: str):
        query = Query("ti " + query)
        query_event = KeywordQueryEvent(query)
        self.timer.trigger_event(query_event)
        results = self.client.response.action.result_list
        return [ResultItem(item, query, self) for item in results]

    def enter(self, item: "ResultItem"):
        action = item.item.on_enter(item.query)
        self.timer.trigger_event(ItemEnterEvent(action._data))


class TestClient:
    def send(self, response):
        self.response = response


@dataclass
class ResultItem:
    item: ExtensionResultItem
    query: KeywordQueryEvent
    launcher: TimerLauncher

    def __repr__(self):
        return f"<{self.text} / {self.description}>"

    def __eq__(self, other):
        if isinstance(other, str):
            return repr(self) == other
        return NotImplemented

    @property
    def text(self):
        return self.item.get_name()

    @property
    def description(self):
        return self.item.get_description(self.query)

    def enter(self):
        self.launcher.enter(self)
