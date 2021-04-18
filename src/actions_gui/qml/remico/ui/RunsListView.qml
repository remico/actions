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
import QtQuick
import QtQuick.Controls

import remico.ui 1.0
import remico.models 1.0

Item {
    id: root
    anchors.fill: parent

    property string name: "workflow runs"
    property var toDelete: []

    Settings {
        id: settings
        category: root.name
        property string workflow_id: "python-publish.yml"
    }

    ListView {
        id: _view

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: _buttons.left

        KeyNavigation.right: _buttons
        focus: count > 0

        highlight: Rectangle {
            color: _view.activeFocus ? "darkgray" : "lightgray"
            width: 1
            anchors.horizontalCenter: _view.contentItem.horizontalCenter
        }

        delegate: WorkflowRunsDelegate {
            onChecked: Utils.a_insert2(root.toDelete, run_id, checked)
        }

        model: ActionsXmlModel {
            xml: UiWorkflowRuns.xml
        }

        BusyIndicator {
            anchors.centerIn: parent
            running: UiWorkflowRuns.updating
        }
    }

    ButtonColumn {
        id: _buttons

        anchors.right: parent.right

        width: 130
        height: parent.height

        KeyNavigation.left: _view

        Button2 {
            text: qsTr("Get Runs")
            onClicked: {
                UiWorkflowRuns.clear_runs()
                UiWorkflowRuns.update_runs()
                root.toDelete = []
            }
        }
        Button2 {
            text: qsTr("Clear View")
            onClicked: {
                UiWorkflowRuns.clear_runs()
                root.toDelete = []
            }
        }
        Button2 {
            text: qsTr("Delete Selected")
            onClicked: {
                UiWorkflowRuns.delete_runs(root.toDelete)
                root.toDelete = []
            }
        }
        Button2 {
            text: qsTr("Start Run")
            onClicked: {
                UiWorkflowRuns.post_workflow_dispatch("develop", settings.workflow_id)
                root.toDelete = []
            }
        }
    }
}
