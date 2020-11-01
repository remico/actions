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

from threading import Thread
from .pyside2 import *

__all__ = ['WorkerThread']

class WorkerThread(QObject):
    def __init__(self, jobCollable, parent=None) -> None:
        super().__init__(parent)
        self.delay = 0
        def _job():
            jobCollable()
            QMetaObject.invokeMethod(self, "_on_done")  # QueuedConnection
        Thread(target=_job).start()

    def callback(self, callback, delay_ms=0):
        self.delay = delay_ms
        self._done.connect(callback)

    _done = PS2Signal()

    @PS2Slot()
    def _on_done(self):
        QTimer.singleShot(self.delay, lambda: self._done.emit() and self.deleteLater())
