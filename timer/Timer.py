import logging
from datetime import datetime, timedelta

from gi.repository import Notify

from .media import get_icon_path, play_sound

log = logging.getLogger(__name__)


class Timer:

    def __init__(self, run_seconds, name, callback):
        self.run_seconds = run_seconds
        self.name = name
        self.callback = callback
        self.tag = None
        self.end_time = datetime.now() + timedelta(seconds=run_seconds)
        self.notification = None

    def start(self, loop):
        def on_end():
            self.notify(self.name)
            self.callback(self)
            self.tag = None

        self.tag = loop.call_after_delay(self.run_seconds, on_end)
        self.notify('Timer is set', sound=False)
        log.debug('Timer set for %s', self.end_time)

    def stop(self, loop):
        if self.tag is not None:
            loop.cancel_callback(self.tag)
            self.tag = None

    @property
    def time_remaining(self):
        return self.end_time - datetime.now()

    def notify(self, text, sound=True):
        log.debug('Notify: %s', text)
        self._show_notification("Timer", text)
        if sound:
            play_sound()

    def _show_notification(self, title, body):
        if not Notify.is_initted():
            Notify.init("TimerExtension")
        icon = get_icon_path()
        if self.notification is None:
            self.notification = Notify.Notification.new(title, body, icon)
        else:
            self.notification.update(title, body, icon)
        self.notification.show()
