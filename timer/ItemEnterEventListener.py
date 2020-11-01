import logging
from ulauncher.api.client.EventListener import EventListener

logger = logging.getLogger(__name__)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        event_type, data = event.get_data()
        if event_type == "set":
            delay, message = data
            extension.set_timer(delay, message)
        elif event_type == "stop":
            extension.stop_timer(timer_id=data)
        else:
            logger.warning("unknown event: %r %r", event_type, data)
