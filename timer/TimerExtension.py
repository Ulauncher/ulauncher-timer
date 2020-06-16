import os
import subprocess
from collections import namedtuple

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

from uuid import uuid4

logger = logging.getLogger(__name__)


TimerDef = namedtuple('TimerDef', ('timer', 'text', 'start_time'))


class TimerExtension(Extension):

    SOUND_FILE = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    ICON_FILE = 'images/timer.png'

    timers = dict()

    def __init__(self):
        super(TimerExtension, self).__init__()
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.ICON_FILE)
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.ICON_FILE, self.get_time_left_all))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def set_timer(self, delay, text):
        timer_id = uuid4()
        timer = Timer(delay, self.on_timer_ended, args=[text, timer_id])
        timer.setDaemon(True)
        timer_start_time = datetime.now()
        self.timers[timer_id] = (TimerDef(timer=timer, text=text, start_time=timer_start_time))
        timer.start()

    def stop_timer(self, timer_id):
        if timer_id not in self.timers:
            return

        self.timers[timer_id].timer.cancel()
        del self.timers[timer_id]

    def get_time_left(self, timer_id):
        if timer_id not in self.timers:
            return None

        timer_def = self.timers[timer_id]
        if timer_def:
            interval = timedelta(seconds = timer_def.timer.interval)
            end = timer_def.start_time + interval
            return end - datetime.now()
        else:
            return None

    def get_time_left_all(self):
        return [(timer_def.text, self.get_time_left(tid)) for tid, timer_def in self.timers.items()]

    def on_timer_ended(self, text, timer_id):
        logger.debug("Timer '%s' ('%s') ended" % (timer_id, text))
        self.show_notification(text)
        self.stop_timer(timer_id)

    def show_notification(self, text, make_sound=True):
        logger.debug('Show notification: %s' % text)
        Notify.init("TimerExtension")
        Notify.Notification.new("Timer", text, self.icon_path).show()
        if make_sound:
            subprocess.call(("paplay", self.SOUND_FILE))
