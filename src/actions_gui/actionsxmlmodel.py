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
#  Copyright (c) 2021 remico

from xml.etree import ElementTree
from enum import IntEnum

from .pyside6 import *


class WorkflowRun(QObject):
    def __init__(self, et_element, parent: QObject = None) -> None:
        super().__init__(parent)
        self._et_element = et_element

    # - Qt properties

    def get_run_id(self):
        return self._et_element.find("id").text
    run_id = PS6Property(str, get_run_id, constant=True)

    def get_created_at(self):
        return self._et_element.find("created_at").text
    created_at = PS6Property(str, get_created_at, constant=True)

    def get_conclusion(self):
        return self._et_element.find("conclusion").text
    conclusion = PS6Property(str, get_conclusion, constant=True)

    def get_event(self):
        return self._et_element.find("event").text
    event = PS6Property(str, get_event, constant=True)

    def get_head_branch(self):
        return self._et_element.find("head_branch").text
    head_branch = PS6Property(str, get_head_branch, constant=True)

    def get_status(self):
        return self._et_element.find("status").text
    status = PS6Property(str, get_status, constant=True)

    def get_weblink(self):
        return self._et_element.find("html_url").text
    weblink = PS6Property(str, get_weblink, constant=True)


class RoleNames(IntEnum):
    id          = Qt.UserRole + 1
    created_at  = Qt.UserRole + 2
    conclusion  = Qt.UserRole + 3
    event       = Qt.UserRole + 4
    head_branch = Qt.UserRole + 5
    status      = Qt.UserRole + 6
    html_url    = Qt.UserRole + 7


class ActionsXmlModel(QAbstractListModel):
    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self._xml = ""
        self._model = []

    def _translate_role(self, role):
        role_str = self.roleNames().get(role, "").decode()

        if role_str == "run_id":
            role_str = "id"
        elif role_str == "weblink":
            role_str = "html_url"

        return role_str

    # ===================
    # - Qt properties
    # ===================

    # -- xml
    def get_xml(self):
        return self._xml

    def set_xml(self, xml):

        def lastRow():
            return len(self._model) - 1

        # notify views
        self.beginRemoveRows(QModelIndex(), 0, lastRow())
        self.endRemoveRows()

        # replace internal data
        self._xml = xml
        self.xmlChanged.emit()

        try:
            etree = ElementTree.XML(self._xml)
            self._model = [element for element in etree.iter("item")]
        except Exception:
            self._model = []

        # notify views
        self.beginInsertRows(QModelIndex(), 0, lastRow())
        self.endInsertRows()

    xmlChanged = PS6Signal()
    xml = PS6Property(str, get_xml, set_xml, notify=xmlChanged)

    # ===================
    # - methods
    # ===================

    def roleNames(self):
        return {
            RoleNames.id:           b"run_id",
            RoleNames.created_at:   b"created_at",
            RoleNames.conclusion:   b"conclusion",
            RoleNames.event:        b"event",
            RoleNames.head_branch:  b"head_branch",
            RoleNames.status:       b"status",
            RoleNames.html_url:     b"weblink"
        }

    def data(self, index: QModelIndex, role=RoleNames.id):
        if not index.isValid():
            return None

        role_tag = self._translate_role(role)
        row = index.row()

        try:
            et_element = self._model[row]
            return et_element.find(role_tag).text
        except Exception:
            return None

    def rowCount(self, index=QModelIndex()):
        return len(self._model)

    def flags(self, index: QModelIndex):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled

    # def hasChildren(self, parent=QModelIndex()) -> bool:
    #     return super().hasChildren(parent)


def register_xml_model():
    qmlRegisterType(WorkflowRun, "remico.models", 1, 0, "WorkflowRun")
    qmlRegisterType(ActionsXmlModel, "remico.models", 1, 0, "ActionsXmlModel")
