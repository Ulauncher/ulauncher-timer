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
        item = self.get_item_to_render(description, name, on_enter)

        return RenderResultListAction([item])

    def get_item_to_render(self, description, name, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon=self.icon_file,
                                   on_enter=on_enter or DoNothingAction())
        return item

    def on_event(self, event, extension):
        query = event.get_argument()
        time_lefts = self.get_timers()
        if query:
            try:
                time_sec, delta, message = parse_query(query)
                return self.get_action_to_render(name="Set timer for %s" % delta,
                                                 description="Message: %s" % message,
                                                 on_enter=ExtensionCustomAction((time_sec, message)))
            except ParseQueryError:
                return self.get_action_to_render(name="Incorrect request",
                                                 description="Example: ti 10m Eggs are ready!")
        elif time_lefts is not None and len(time_lefts) > 0:
            items = [self.get_item_to_render(name=timer_name,
                                             description="Time left: %s" % format_timediff(timediff_str))
                     for timer_name, timediff_str in time_lefts]
            return RenderResultListAction(items)
        else:
            return self.get_action_to_render(name="Type in your query",
                                             description="Example: ti 10m Eggs are ready!")
