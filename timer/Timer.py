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
        self.timer = TimerThread(run_seconds, on_end)
        self.timer.setDaemon(True)
        self.end_time = datetime.now() + timedelta(seconds=run_seconds)

    def start(self):
        self.timer.start()
        self.notify('Timer is set', make_sound=False)
        log.debug('Timer set for %s', self.end_time)

    def stop(self):
        self.timer.cancel()

    @property
    def time_remaining(self):
        return self.end_time - datetime.now()

    def notify(self, text, make_sound=True):
        log.debug('Show notification: %s' % text)
        Notify.init("TimerExtension")
        Notify.Notification.new("Timer", text, get_icon_path()).show()
        if make_sound:
            play_sound()
