from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from .query_parser import parse_query, ParseQueryError
from .timediff_formatter import format_timediff


class ExtensionKeywordListener(EventListener):

    def __init__(self, icon_file, get_timers):
        self.icon_file = icon_file
        self.get_timers = get_timers

    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon=self.icon_file,
                                   on_enter=on_enter or DoNothingAction())

        return RenderResultListAction([item])

    def get_timer_item(self, timer, on_enter=None):
        time_remaining = format_timediff(timer.time_remaining)
        return ExtensionResultItem(name=timer.name,
                                   description=f"Time left: {time_remaining}",
                                   icon=self.icon_file,
                                   on_enter=on_enter or DoNothingAction())

    def on_event(self, event, extension):
        query = event.get_argument()
        timers = self.get_timers()
        if query:
            try:
                time_sec, delta, message = parse_query(query)
                return self.get_action_to_render(name="Set timer for %s" % delta,
                                                 description="Message: %s" % message,
                                                 on_enter=ExtensionCustomAction((time_sec, message)))
            except ParseQueryError:
                return self.get_action_to_render(name="Incorrect request",
                                                 description="Example: ti 10m Eggs are ready!")
        elif timers:
            items = [self.get_timer_item(t) for t in timers]
            return RenderResultListAction(items)
        else:
            return self.get_action_to_render(name="Type in your query",
                                             description="Example: ti 10m Eggs are ready!")
