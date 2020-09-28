import logging

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Notify

from ulauncher.api.shared.event import (
    ItemEnterEvent,
    KeywordQueryEvent,
    SystemExitEvent,
)
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from .ExtensionKeywordListener import ExtensionKeywordListener
from .ItemEnterEventListener import ItemEnterEventListener
from .Timer import Timer

log = logging.getLogger(__name__)


class TimerExtension(Extension):

    def __init__(self):
        super(TimerExtension, self).__init__()
        self.timers = set()
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.get_timers))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(SystemExitEvent, SystemExitEventListener())

    def set_timer(self, delay, text):
        timer = Timer(delay, text, self.on_timer_end)
        timer.start()
        self.timers.add(timer)

    def stop_timer(self, timer):
        timer.stop()
        self.timers.remove(timer)

    def on_timer_end(self, timer):
        self.timers.remove(timer)

    def get_timers(self):
        return sorted(self.timers, key=lambda t: t.end_time)


class SystemExitEventListener(EventListener):

    def on_event(self, event, extension):
        log.debug("Uninitialize notifications")
        Notify.uninit()
