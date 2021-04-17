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
import QtQuick.Window 2.15

Window {
    objectName: "testwnd"
    width: 300
    height: 200
    x: 200
    y: 200

    color: "lightblue"

    Text {
        anchors.fill: parent
        text: "HELLO TEST WINDOW"
    }

    title: "Title test window"
    // modality: Qt.ApplicationModal
    // visible: true
}
