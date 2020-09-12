from dataclasses import dataclass

from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.search.Query import Query

from timer.TimerExtension import TimerExtension


class TimerLauncher:

    def __init__(self):
        self.timer = TimerExtension()
        self.client = self.timer._client = TestClient()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        tx = self.timer
        tx.stop_timer()
        assert not tx.timer, tx.timer

    def query(self, query: str):
        query = Query("ti " + query)
        query_event = KeywordQueryEvent(query)
        self.timer.trigger_event(query_event)
        results = self.client.response.action.result_list
        return [ResultItem(item, query, self) for item in results]


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
