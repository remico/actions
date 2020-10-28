
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide2.QtCore import Property as PS2Property
from PySide2.QtCore import Signal as PS2Signal
from PySide2.QtCore import Slot as PS2Slot
from PySide2.QtCore import QObject
from PySide2.QtCore import QUrl
from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer
from PySide2.QtCore import QSettings
from PySide2.QtCore import QMetaObject
from PySide2.QtCore import QSocketNotifier

from PySide2.QtGui import QIcon
from PySide2.QtGui import QGuiApplication

from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtQml import QQmlComponent
from PySide2.QtQml import QQmlEngine
from PySide2.QtQml import QQmlContext
from PySide2.QtQml import QQmlProperty
from PySide2.QtQml import QtQml

from PySide2.QtQuick import QQuickItem
from PySide2.QtQuick import QQuickView
from PySide2.QtQuick import QQuickWindow


print(f"@@ Importing 'pyside2' module [{__name__}]")
