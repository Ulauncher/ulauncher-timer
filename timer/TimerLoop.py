from threading import Thread

from gi.repository import GLib, Gtk, Notify


class TimerLoop:

    def __init__(self):
        self.thread = Thread(target=Gtk.main)
        self.thread.start()

    def call_after_delay(self, delay_seconds, callback):
        """Call function after delay

        :returns: callback tag, which can be passed to `cancel_callback`.
        """
        def _callback():
            callback()
            return False

        return GLib.timeout_add_seconds(delay_seconds, _callback)

    def cancel_callback(self, tag):
        GLib.source_remove(tag)

    def quit(self):
        Notify.uninit()
        Gtk.main_quit()
        self.thread.join()
