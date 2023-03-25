import logging

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

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
from .TimerLoop import TimerLoop

log = logging.getLogger(__name__)


class TimerExtension(Extension):

    def __init__(self):
        super(TimerExtension, self).__init__()
        self.timers = set()
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.get_timers))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(SystemExitEvent, SystemExitEventListener())
        self.loop = TimerLoop()

    def set_timer(self, delay, text):
        log.debug("add timer %s %s", delay, text)
        persistent = self.preferences["persistent"]
        timer = Timer(delay, text, self.on_timer_end, self.loop, persistent)
        timer.start()
        self.timers.add(timer)

    def stop_timer(self, timer_id):
        timer = self.get_timer(timer_id)
        if timer is not None:
            log.debug("stop timer %s", timer.name)
            timer.stop(notify=True)
            self.timers.remove(timer)

    def on_timer_end(self, timer):
        log.debug("end timer %s", timer.name)
        self.timers.discard(timer)

    def get_timers(self):
        return sorted(self.timers, key=lambda t: t.end_time)

    def get_timer(self, timer_id):
        for timer in self.timers:
            if timer.id == timer_id:
                return timer
        log.debug("timer %s not found", timer_id)
        return None

    def quit(self):
        log.debug("quit timer extension")
        self.loop.quit()


class SystemExitEventListener(EventListener):

    def on_event(self, event, extension):
        extension.quit()
