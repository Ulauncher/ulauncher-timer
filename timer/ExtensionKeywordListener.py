from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from .media import ICON_FILE
from .query_parser import parse_query, ParseQueryError


class ExtensionKeywordListener(EventListener):

    def __init__(self, get_timers):
        self.get_timers = get_timers

    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon=ICON_FILE,
                                   on_enter=on_enter or DoNothingAction())

        return RenderResultListAction([item])

    def get_timer_item(self, timer):
        data = ("stop", timer.id)
        return ExtensionResultItem(name=timer.description,
                                   description="Select to stop",
                                   icon=ICON_FILE,
                                   on_enter=ExtensionCustomAction(data))

    def on_event(self, event, extension):
        query = event.get_argument()
        timers = self.get_timers()
        if query:
            try:
                time_sec, delta, message = parse_query(query)
                data = ("set", (time_sec, message))
                return self.get_action_to_render(name="Set timer for %s" % delta,
                                                 description="Message: %s" % message,
                                                 on_enter=ExtensionCustomAction(data))
            except ParseQueryError:
                return self.get_action_to_render(name="Incorrect request",
                                                 description="Example: ti 10m Eggs are ready!")
        elif timers:
            items = [self.get_timer_item(t) for t in timers]
            return RenderResultListAction(items)
        else:
            return self.get_action_to_render(name="Type in your query",
                                             description="Example: ti 10m Eggs are ready!")
