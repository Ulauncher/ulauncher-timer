import os
import subprocess
import gi
import logging

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Notify
from threading import Timer

from ulauncher.extension.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.extension.client.Extension import Extension
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
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.ICON_FILE))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def set_timer(self, delay, text):
        self.timer = Timer(delay, self.show_notification, args=[text])
        self.timer.setDaemon(True)
        self.timer.start()

    def stop_timer(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

    def show_notification(self, text, make_sound=True):
        logger.debug('Show notification: %s' % text)
        Notify.init("TimerExtension")
        Notify.Notification.new("Timer", text, self.icon_path).show()
        if make_sound:
            subprocess.call(("paplay", self.SOUND_FILE))
