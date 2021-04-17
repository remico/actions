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
import QtQuick.Controls 2.15
import remico.ui 1.0

ApplicationWindow {
    id: root

    property string tab_name: _tab_workflow_runs.name || "@noname"

    width: 640
    height: 480
    visible: true
    title: qsTr("github actions gui - " + tab_name + " [ " + REPO + " ]")

    RunsListView { id: _tab_workflow_runs }

    Shortcut {
        sequence: "Ctrl+Q"
        onActivated: Qt.quit()
    }
}
