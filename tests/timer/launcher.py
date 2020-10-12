from dataclasses import dataclass

from ulauncher.api.shared.event import ItemEnterEvent, KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.search.Query import Query

from timer.TimerExtension import TimerExtension


class TimerLauncher:

    def __init__(self):
        self.timer = TimerExtension()
        self.timer.preferences["persistent"] = False
        self.timer.icon_path = "unknown"
        self.client = self.timer._client = TestClient()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        tx = self.timer
        for timer in tx.get_timers():
            tx.stop_timer(timer)
        tx.quit()
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
