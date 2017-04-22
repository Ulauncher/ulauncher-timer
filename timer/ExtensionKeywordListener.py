from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CloseAppAction import CloseAppAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from .query_parser import parse_query, ParseQueryError


class ExtensionKeywordListener(EventListener):

    def __init__(self, icon_file):
        self.icon_file = icon_file

    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon=self.icon_file,
                                   on_enter=on_enter or DoNothingAction())

        return RenderResultListAction([item])

    def on_event(self, event, extension):
        query = event.get_argument()
        if query:
            try:
                time_sec, delta, message = parse_query(query)
                return self.get_action_to_render(name="Set timer for %s" % delta,
                                                 description="Message: %s" % message,
                                                 on_enter=ExtensionCustomAction((time_sec, message)))
            except ParseQueryError:
                return self.get_action_to_render(name="Incorrect request",
                                                 description="Example: ti 10m Eggs are ready!")
        else:
            return self.get_action_to_render(name="Type in your query",
                                             description="Example: ti 10m Eggs are ready!")
