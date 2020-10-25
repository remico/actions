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

    done = PS2Signal()

    @PS2Slot()
    def _on_done(self):
        QTimer.singleShot(self.delay, lambda: self.done.emit() and self.deleteLater())

    def callback(self, callback, delay_ms=0):
        self.delay = delay_ms
        self.done.connect(callback)