#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  This file is part of "github actions gui" project
#
#  Author: Roman Gladyshev <remicollab@gmail.com>
#  License: MIT License
#
#  SPDX-License-Identifier: MIT
#  License text is available in the LICENSE file and online:
#  http://www.opensource.org/licenses/MIT
#
#  Copyright (c) 2020 remico

from PySide6.QtCore import Property as PS6Property
from PySide6.QtCore import Signal as PS6Signal
from PySide6.QtCore import Slot as PS6Slot
from PySide6.QtCore import QObject
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtCore import QSettings
from PySide6.QtCore import QMetaObject
from PySide6.QtCore import QSocketNotifier

from PySide6.QtGui import QIcon
from PySide6.QtGui import QGuiApplication

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import QQmlComponent
from PySide6.QtQml import QQmlEngine
from PySide6.QtQml import QQmlContext
from PySide6.QtQml import QQmlProperty

from PySide6.QtQuick import QQuickItem
from PySide6.QtQuick import QQuickView
from PySide6.QtQuick import QQuickWindow


print(f"@@ Importing 'PySide6' module [{__name__}]")
