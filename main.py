from ulauncher.extension.client.Extension import Extension
from ulauncher.extension.client.EventListener import EventListener
from ulauncher.extension.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.extension.shared.result_item.ExtensionResultItem import ExtensionResultItem
from ulauncher.result_list.item_action.RenderResultListAction import RenderResultListAction


class FileFindExtension(Extension):

    def __init__(self, *args, **kw):
        super(FileFindExtension, self).__init__(*args, **kw)
        self.file_db = FileDb()
        dirs = '\n'.split(config.prefs.get('watch_dirs'))
        watcher = FileWatcher(self.file_db)
        watcher.watch(dirs)
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener(self.file_db, config))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener(self.file_db, config))


class ExtensionKeywordListener(EventListener):

    def __init__(self, file_db, config):
        self.file_db = file_db
        super(ExtensionKeywordListener, self).__init__()

    def on_event(self, event):
        query = event.get_query()
        files = self.file_db.find(query, limit=9)
        result_list = []
        for file in files:
            result_list.append(ExtensionResultItem(name=file.get_name(),
                                                   icon=file.get_icon(),
                                                   description=file.get_path(),
                                                   enter_action=ExtensionCustomAction(file, True)))

        return RenderResultListAction(result_list)


class ItemEnterEventListener(EventListener):

    def __init__(self, file_db, config):
        self.file_db = file_db
        super(ItemEnterEventListener, self).__init__()

    def on_event(self, event):
        file = event.get_data()
        OpenAction(file.get_path()).run()  # or return action?


if __name__ == '__main__':
    Extension().run()
