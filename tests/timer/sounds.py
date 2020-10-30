from contextlib import contextmanager
from unittest.mock import patch


@contextmanager
def sound():
    def mock_play_sound():
        sounds.append(1)

    sounds = []
    with patch("timer.Timer.play_sound", mock_play_sound):
        yield sounds
