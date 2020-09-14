import logging
import os
import subprocess

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Notify

from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.client.Extension import Extension
from .ExtensionKeywordListener import ExtensionKeywordListener
from .ItemEnterEventListener import ItemEnterEventListener
from .Timer import Timer

logger = logging.getLogger(__name__)


class TimerExtension(Extension):

    SOUND_FILE = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    ICON_FILE = 'images/timer.png'

    def __init__(self):
        super(TimerExtension, self).__init__()
        self.timers = set()
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.ICON_FILE)
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.ICON_FILE, self.get_timers))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def set_timer(self, delay, text):
        timer = Timer(delay, text, self.on_timer_end)
        timer.start()
        self.timers.add(timer)

    def stop_timer(self, timer):
        timer.stop()
        self.timers.remove(timer)

    def on_timer_end(self, timer):
        self.timers.remove(timer)
        self.show_notification(timer.name)

    def get_timers(self):
        return sorted(self.timers, key=lambda t: t.end_time)

    def show_notification(self, text, make_sound=True):
        logger.debug('Show notification: %s' % text)
        Notify.init("TimerExtension")
        Notify.Notification.new("Timer", text, self.icon_path).show()
        if make_sound:
            subprocess.call(("paplay", self.SOUND_FILE))
