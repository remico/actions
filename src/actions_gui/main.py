#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from .path import path
from .pyside2 import *
from .rest import Rest
from .uifactory import UiFactory
from . import webhooklistener


def main():
    app = QGuiApplication(sys.argv)
    app.setApplicationName("actions gui")
    app_icon = path("assets/icon.svg")
    app.setWindowIcon(QIcon(app_icon))

    settings_file = path.home().join(".actions_gui.conf")
    print(settings_file)
    settings = QSettings(settings_file, QSettings.IniFormat)
    (repo_owner := settings.value("owner")) or settings.setValue("owner", "")
    (repo_name := settings.value("repo")) or settings.setValue("repo", "")

    engine = QQmlApplicationEngine()
    rest = Rest(repo_name, repo_owner)
    uifactory = UiFactory(engine)

    engine.addImportPath(path())  # NOTE: imports from the package root so far

    engine.rootContext().setContextObject(rest)
    engine.rootContext().setContextProperty("APP_CONFIG", settings_file)

    main_ui = uifactory.make_window(path("ui/ApplicationWindow.qml"))

    # test_ui = uifactory.make_window(path("ui/draft/TestWindow.qml"), main_ui)
    # test_ui.show()  # window

    # test_ui2 = uifactory.make_popup(path("ui/draft/TestDialog.qml"), main_ui)
    # test_ui2.open()  # popup, dialog

    # container = uifactory.child(main_ui, "container_runsview", QQuickItem)
    # view_runs = uifactory.make_item(path("ui/RunsListView.qml"),
    #                                 container,
    #                                 # {'parent': container}
    #                                 )


    listener = webhooklistener.run()
    listener.dataReady.connect(lambda: print("### IPC data:", listener.read()))
    listener.dataReady.connect(lambda: QTimer.singleShot(3000, rest.m_workflowruns.update_runs))

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
