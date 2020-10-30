import logging
from ulauncher.api.client.EventListener import EventListener

logger = logging.getLogger(__name__)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        delay, message = event.get_data()
        extension.set_timer(delay, message)
