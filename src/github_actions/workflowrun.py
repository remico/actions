#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from pathlib import Path
from tempfile import gettempdir

from json2xml.json2xml import Json2xml
from json2xml.utils import readfromstring

from .pyside2 import *

TEMP_FILE = Path(gettempdir(), "workflow_runs.xml")


def localdata(f):
    @wraps(f)
    def w(*a, **kw):
        if not TEMP_FILE.exists():
            r = f(*a, **kw)
            TEMP_FILE.write_text(r)
        return TEMP_FILE.read_text()
    return w


def json2xml(f):
    @wraps(f)
    def w(*a, **kw):
        text = f(*a, **kw)
        return Json2xml(readfromstring(text)).to_xml()
    return w


class WorkflowRunsModel(QObject):
    api_delete = "actions/runs/{run_id}"  # DELETE run
    api_list = "actions/runs"  # GET list
    api_new_run = "actions/workflows/{workflow_id}/dispatches"  # POST

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.m_data = ""
        self.m_updating = True
        QTimer.singleShot(200, self.update_runs)

    # methods
    def call_api(self, action, url, **kw):
        return self.parent().do_request(action, url, **kw)

    @json2xml
    # @localdata
    def _get_runs(self):
        return self.call_api("GET", WorkflowRunsModel.api_list)

    # signals
    request_action = PS2Signal(str, str)

    # slots
    @PS2Slot()
    def update_runs(self):
        self.updating = True
        self.xml = self._get_runs()

    @PS2Slot()
    def clear_runs(self):
        self.xml = ""

    @PS2Slot(list)
    def delete_runs(self, items):
        if items:
            self.updating = True
            for run in items:
                r = self.call_api("DELETE", WorkflowRunsModel.api_delete.format(run_id=run))
                print("response:", r or "OK")
            QTimer.singleShot(2000, self.update_runs)

    @PS2Slot()
    def post_workflow_dispatch(self, ref, w_id):
        payload = {'ref': ref}
        r = self.call_api("POST", WorkflowRunsModel.api_new_run.format(workflow_id=w_id), params=payload)
        print("response:", r or "OK")
        QTimer.singleShot(2000, self.update_runs)

    # properties
    # =====
    xmlAboutToUpdate = PS2Signal()
    xmlChanged = PS2Signal()

    @PS2Property(str, notify=xmlChanged)
    def xml(self):
        return self.m_data

    @xml.setter
    def setXml(self, xml):
        self.m_data = xml
        self.xmlChanged.emit()
        if xml:
            self.updating = False

    # =====
    updatingChanged = PS2Signal()

    @PS2Property(bool, notify=updatingChanged)
    def updating(self):
        return self.m_updating

    @updating.setter
    def setUpdating(self, val):
        if val:
            self.xmlAboutToUpdate.emit()
        self.m_updating = val
        self.updatingChanged.emit()
