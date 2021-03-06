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
import "utils.js" as Utils

FocusScope {
    id: root

    readonly property var list: ListView
    readonly property var view: ListView.view

    signal checked(bool checked)

    width: view.width
    height: 42

    required property string run_id
    required property string created_at
    required property string conclusion
    required property string event
    required property string head_branch
    required property string status
    required property string weblink

    Rectangle {
        id: _led
        height: 0.8 * parent.height
        width: height
        radius: 8
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 5
        color: status == "completed" ? (conclusion == "success" ? "lightgreen" : "pink") : "gold"
        MouseArea {
            id: _ledButton
            anchors.fill: parent
            hoverEnabled: true
            ToolTip.visible: containsMouse
            ToolTip.text: weblink
            onClicked: Qt.openUrlExternally(weblink)
        }
    }

    Column {
        id: _text
        anchors.left: _led.right
        anchors.verticalCenter: parent.verticalCenter
        leftPadding: 5
        Row {
            spacing: 60
            Text {
                text: Utils.format_timestamp(created_at)
                color: list.isCurrentItem ? "black" : "red"
            }
            Text {
                text: Utils.time_delta_formatted(created_at)
            }
        }
        Text {
            text: "[ " + event + " @ " + head_branch + " ]"
        }
    }

    MouseArea {
        anchors.fill: parent
        propagateComposedEvents: true
        onClicked: {
            mouse.accepted = false
            var mapped = mapToItem(view, mouse.x, mouse.y)
            view.currentIndex = view.indexAt(mapped.x, mapped.y)
            root.forceActiveFocus()
        }
    }

    CheckBox {
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        focusPolicy: Qt.NoFocus
        focus: true
        onCheckedChanged: root.checked(checked)
    }
}
