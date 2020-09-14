from timer.Timer import Timer

INSTANT = 0.00001


def test_time_is_up():
    def callback(timer):
        calls.append(timer)

    calls = []
    timer = Timer(INSTANT, "Time is up!", callback)
    timer.timer.run()
    assert calls == [timer]
    assert timer.timer is None, timer.timer
