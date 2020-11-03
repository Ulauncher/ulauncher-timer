import logging
from datetime import datetime, timedelta
from itertools import count

from gi.repository import Notify

from .media import get_icon_path, play_sound
from .timediff_formatter import format_timediff, round_time_units

log = logging.getLogger(__name__)
ids = count()


class Timer:
    """Timer

    :param run_seconds: Number of seconds until timer expires.
    :param name: Message to display when timer expires.
    :param callback: Function to be called with the timer object
    as its only argument when the timer is no longer running.
    :param persistent: If set to true, alert periodically until
    the timer notification is closed.
    """

    def __init__(self, run_seconds, name, callback, persistent=False):
        self.id = next(ids)
        self.run_seconds = run_seconds
        self.name = name
        self.callback = callback
        self.persistent = persistent
        self.tag = None
        self.end_time = datetime.now() + timedelta(seconds=run_seconds)
        self.notification = None
        self.intervals = [30, 30, 30, 10, 10, 10]

    def start(self, loop):
        def on_end(on_close=None):
            self.notify(self.name, self.time_since_end, on_close=on_close)
            if self.persistent:
                interval = self.intervals.pop() if self.intervals else 60
                self.tag = loop.call_after_delay(interval, on_end)
            else:
                self.callback(self)
                self.tag = None

        def on_close(arg):
            log.debug("notification closed")
            self.callback(self)
            self.stop(loop)

        self.tag = loop.call_after_delay(self.run_seconds, on_end, on_close)
        self.notify(self.description, sound=False)
        log.debug('Timer set for %s', self.end_time)

    def stop(self, loop, notify=False):
        if self.tag is not None:
            self.persistent = False  # prevent unstoppable on_end() calls
            loop.cancel_callback(self.tag)
            if notify:
                self.notify("Timer stopped", self.description, sound=False)
                loop.call_after_delay(5, self.notification.close)
            self.tag = None

    @property
    def description(self):
        return f"{self.name} at {self.end_time.strftime('%-I:%M %p')}"

    @property
    def time_since_end(self):
        if self.end_time + timedelta(seconds=5) >= datetime.now():
            return ""
        elapsed = round_time_units(datetime.now() - self.end_time)
        return f"{format_timediff(elapsed)} ago"

    def notify(self, title, body="", sound=True, on_close=None):
        log.debug('Notify: %s %s', title, body)
        self._show_notification(title, body, on_close)
        if sound:
            play_sound()

    def _show_notification(self, title, body, on_close):
        if not Notify.is_initted():
            Notify.init("TimerExtension")
        icon = get_icon_path()
        if self.notification is None:
            self.notification = Notify.Notification.new(title, body, icon)
        else:
            self.notification.update(title, body, icon)
        if on_close is not None:
            self.notification.connect("closed", on_close)
        self.notification.show()
