/*
 * This file is part of "github actions gui" project
 *
 * Author: Roman Gladyshev <remicollab@gmail.com>
 * License: MIT License
 *
 * SPDX-License-Identifier: MIT
 * License text is available in the LICENSE file and online:
 * http://www.opensource.org/licenses/MIT
 *
 * Copyright (c) 2020 remico
 */
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Button {
    property int containerOrientation: Qt.Vertical

    Layout.fillWidth: containerOrientation == Qt.Vertical
    Layout.fillHeight: containerOrientation == Qt.Horizontal

    KeyNavigation.down: containerOrientation == Qt.Vertical ? nextItemInFocusChain() : null
    KeyNavigation.up: containerOrientation == Qt.Vertical ? nextItemInFocusChain(false) : null
    KeyNavigation.right: containerOrientation == Qt.Horizontal ? nextItemInFocusChain() : null
    KeyNavigation.left: containerOrientation == Qt.Horizontal ? nextItemInFocusChain(false) : null
}
