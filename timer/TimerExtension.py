import os
import subprocess
import gi
import logging

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Notify
from threading import Timer

from datetime import timedelta
from datetime import datetime

from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.client.Extension import Extension
from .ExtensionKeywordListener import ExtensionKeywordListener
from .ItemEnterEventListener import ItemEnterEventListener

logger = logging.getLogger(__name__)


class TimerExtension(Extension):

    SOUND_FILE = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    ICON_FILE = 'images/timer.png'

    timer = None

    def __init__(self):
        super(TimerExtension, self).__init__()
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.ICON_FILE)
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.ICON_FILE, lambda : self.get_time_left()))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def set_timer(self, delay, text):
        self.timer = Timer(delay, self.show_notification, args=[text])
        self.timer.setDaemon(True)
        self.timer_start_time = datetime.now()
        self.timer.start()

    def stop_timer(self):
        if self.timer:
            self.timer.stop()
            self.timer_start_time = None
            self.timer = None

    def get_time_left(self):
        if self.timer_start_time and self.timer:
            interval = timedelta(seconds = self.timer.interval)
            end = self.timer_start_time + interval
            return end - datetime.now()
        else:
            return None

    def show_notification(self, text, make_sound=True):
        logger.debug('Show notification: %s' % text)
        Notify.init("TimerExtension")
        Notify.Notification.new("Timer", text, self.icon_path).show()
        if make_sound:
            subprocess.call(("paplay", self.SOUND_FILE))
