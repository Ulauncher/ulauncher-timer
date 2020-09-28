import logging
from datetime import datetime, timedelta
from threading import Timer as TimerThread

from gi.repository import Notify

from .media import get_icon_path, play_sound

log = logging.getLogger(__name__)


class Timer:

    def __init__(self, run_seconds, name, callback):
        def on_end():
            self.notify(name)
            self.timer = None
            callback(self)

        self.name = name
        self.timer = self._get_timer(run_seconds, on_end)
        self.end_time = datetime.now() + timedelta(seconds=run_seconds)
        self.notification = None

    @staticmethod
    def _get_timer(run_seconds, callback):
        timer = TimerThread(run_seconds, callback)
        timer.setDaemon(True)
        return timer

    def start(self):
        self.timer.start()
        self.notify('Timer is set', sound=False)
        log.debug('Timer set for %s', self.end_time)

    def stop(self):
        self.timer.cancel()

    @property
    def time_remaining(self):
        return self.end_time - datetime.now()

    def notify(self, text, sound=True):
        log.debug('Show notification: %s' % text)
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
