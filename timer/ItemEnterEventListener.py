import logging
from ulauncher.extension.client.EventListener import EventListener

logger = logging.getLogger(__name__)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        delay, message = event.get_data()
        extension.set_timer(delay, message)
        extension.show_notification('Timer is set', make_sound=False)
        logger.debug('Timer is set. Delay %s' % delay)
