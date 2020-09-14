from threading import Timer as TimerThread

from datetime import timedelta
from datetime import datetime


class Timer:

    def __init__(self, run_seconds, name, callback):
        def on_end():
            self.timer = None
            callback(self)

        self.name = name
        self.timer = TimerThread(run_seconds, on_end)
        self.timer.setDaemon(True)
        self.end_time = datetime.now() + timedelta(seconds=run_seconds)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    @property
    def time_remaining(self):
        return self.end_time - datetime.now()
