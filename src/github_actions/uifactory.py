#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .pyside2 import *


class UiFactory:
    engine: QQmlEngine

    def __init__(self, engine):
        self.engine =  engine

    @staticmethod
    def _isWindow(o):
        return isinstance(o, QQuickWindow)

    @staticmethod
    def _track(o):
        o.destroyed.connect(lambda o: print(f"$$ destroyed [{o.objectName()}] {o}"))

    @staticmethod
    def child(o, child_name="", child_type=QObject):
        return o.findChild(child_type, child_name)

    @staticmethod
    def property(o, property_name):
        return QQmlProperty(o, property_name)

    def oContext(self, o):
        if UiFactory._isWindow(o):
            o = o.contentItem()
        return self.engine.contextForObject(o) or self.engine.rootContext()

    def make_popup(self, url, parent, initialProperties={}, ownership=QQmlEngine.JavaScriptOwnership):
        context = self.oContext(parent)
        component = QQmlComponent(self.engine, url)

        # make dialog visible
        if 'parent' not in initialProperties:
            initialProperties['parent'] = parent.contentItem()

        item = component.createWithInitialProperties(initialProperties, context)
        item.setParent(parent)  # memory management: if parent => QML ignores JavaScriptOwnership
        self.engine.setObjectOwnership(item, ownership)
        return item

    def make_item(self, url, parent, initialProperties={}, ownership=QQmlEngine.JavaScriptOwnership):
        context = self.oContext(parent)
        component = QQmlComponent(self.engine, url)
        item = component.createWithInitialProperties(initialProperties, context)
        item.setParent(parent)  # memory management: if parent => QML ignores JavaScriptOwnership
        item.setParentItem(parent)  # make item visible
        self.engine.setObjectOwnership(item, ownership)
        return item

    # @staticmethod
    # def make_mainview(url, initialProperties={}, resizeMode=QQuickView.SizeViewToRootObject):
    #     view = QQuickView()
    #     view.setInitialProperties(initialProperties)
    #     view.setResizeMode(resizeMode)
    #     view.setSource(url)
    #     return view

    def make_window(self, url, parent_wnd:QQuickWindow=None, initialProperties={}):
        context = QQmlContext(self.oContext(parent_wnd))
        component = QQmlComponent(self.engine, url)
        window = component.createWithInitialProperties(initialProperties, context)

        # to remove the context when the related window deletion
        context.setParent(window)

        # for top-level window (no parent), pass an object to prevent python GC to kill the window
        # for child window, pass a window to show this window inside the parent window
        window.setParent(parent_wnd.contentItem() if parent_wnd else self.engine)  # memory management
        window.setTransientParent(parent_wnd)  # windows hierarchy

        # # extra flags
        # window.setModality(Qt.WindowModal)
        # window.setFlags(Qt.Dialog)

        return window

    @staticmethod
    def show_inside(parent_wnd: QQuickWindow, item_or_wnd):
        if UiFactory._isWindow(item_or_wnd):
            item_or_wnd.setParent(parent_wnd.contentItem())
        else:
            item_or_wnd.setParentItem(parent_wnd.contentItem())
