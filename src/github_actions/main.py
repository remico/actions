#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from .path import path
from .pyside2 import *
from .rest import Rest
from .uifactory import UiFactory


def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("actions gui")
    app_icon = path("assets/icon.svg").str()
    app.setWindowIcon(QIcon(app_icon))

    settings_file = path("config.ini").str()

    settings = QSettings(settings_file, QSettings.IniFormat)
    (repo_owner := settings.value("owner")) or settings.setValue("owner", "")
    (repo_name := settings.value("repo")) or settings.setValue("repo", "")

    engine = QQmlApplicationEngine()
    rest = Rest(repo_name, repo_owner)
    uifactory = UiFactory(engine)

    engine.addImportPath(path().str())  # NOTE: imports from the package root so far

    engine.rootContext().setContextObject(rest)
    engine.rootContext().setContextProperty("APP_CONFIG", settings_file)

    main_ui = uifactory.make_window(path("ui/ApplicationWindow.qml").str())

    # test_ui = uifactory.make_window(path("ui/TestWindow.qml").str(), main_ui)
    # test_ui.show()  # window

    # test_ui2 = uifactory.make_popup(path("ui/TestDialog.qml").str(), main_ui)
    # test_ui2.open()  # popup, dialog

    # container = uifactory.child(main_ui, "container_runsview", QQuickItem)
    # view_runs = uifactory.make_item(path("ui/RunsListView.qml").str(),
    #                                 container,
    #                                 # {'parent': container}
    #                                 )


    # if not engine.rootObjects():
    #     sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


# appengine = QQmlApplicationEngine
# rootContext = appengine.rootContext
# window_context = QQmlContext(rootContext)

# component = QQmlComponent(engine)
# window = component.create(url_to_window_qml, window_context)
# context.setParent(window)

# # ... use window ...
