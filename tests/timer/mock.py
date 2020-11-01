import os
import sys
from os.path import abspath, dirname, exists, join

from .notifications import MockNotify

installed = False


def install_mocks():
    global installed
    if installed:
        return
    installed = True
    os.environ.setdefault("ULAUNCHER_WS_API", "n/a")
    sys.modules["gi"] = Gi
    sys.modules["gi.repository"] = GiRepository
    sys.modules["ulauncher.config"] = ulauncher_config
    sys.modules["ulauncher.utils.display"] = ulauncher_utils_display
    sys.modules["ulauncher.utils.image_loader"] = ulauncher_utils_image_loader


def get_ulauncher_path():
    this_dir = dirname(abspath(__file__))
    root_dir = dirname(dirname(this_dir))
    ulauncher_path = join(root_dir, "Ulauncher")
    if not exists(ulauncher_path):
        sys.exit(
            f"Ulauncher not found: {ulauncher_path}\n"
            "Resolution: git clone https://github.com/Ulauncher/Ulauncher"
        )
    return ulauncher_path


class Gi:
    def require_version(what, version):
        pass


class MockGtk:
    def main():
        pass

    def main_quit():
        pass


class MockGLib:

    def timeout_add_seconds(interval, function, *data):
        return -1

    def source_remove(tag):
        pass


class GiRepository:
    Notify = MockNotify
    GLib = MockGLib
    Gtk = MockGtk


class ulauncher_config:
    DATA_DIR = join(get_ulauncher_path(), "data")


class ulauncher_utils_display:
    def get_monitor_scale_factor():
        pass


class ulauncher_utils_image_loader:
    def load_image(path):
        pass
