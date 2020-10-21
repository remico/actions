import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.XmlListModel 2.15
import "utils.js" as Utils

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

        focus: true
        highlight: Rectangle {
            color: _view.activeFocus ? "darkgray" : "lightgray"
            width: 1
            anchors.horizontalCenter: _view.contentItem.horizontalCenter
        }

        delegate: WorkflowRunsDelegate {
            KeyNavigation.right: _buttons
            onChecked: Utils.a_insert2(root.toDelete, model.id, checked)
        }

        model: XmlListModel {
            xml: UiWorkflowRuns.xml
            query: "/all/workflow_runs/item"
            XmlRole { name: 'id'; query: 'id/string()' }
            XmlRole { name: 'created_at'; query: 'created_at/string()' }
            XmlRole { name: 'conclusion'; query: 'conclusion/string()' }
            XmlRole { name: 'event'; query: 'event/string()' }
            XmlRole { name: 'head_branch'; query: 'head_branch/string()' }
            XmlRole { name: 'status'; query: 'status/string()' }
            XmlRole { name: 'html_url'; query: 'html_url/string()' }
        }

        BusyIndicator {
            anchors.centerIn: parent
            running: UiWorkflowRuns.updating
        }
    }

    Column {
        id: _buttons

        anchors.right: parent.right
        spacing: 5

        KeyNavigation.left: _view

        Button {
            width: 140
            text: qsTr("Get Runs")
            onClicked: {
                UiWorkflowRuns.clear_runs()
                UiWorkflowRuns.update_runs()
                root.toDelete = []
            }
        }
        Button {
            width: 140
            text: qsTr("Clear View")
            onClicked: {
                UiWorkflowRuns.clear_runs()
                root.toDelete = []
            }
        }
        Button {
            width: 140
            text: qsTr("Delete Selected")
            onClicked: {
                UiWorkflowRuns.delete_runs(root.toDelete)
                root.toDelete = []
            }
        }
        Button {
            width: 140
            text: qsTr("Start Run")
            onClicked: {
                UiWorkflowRuns.post_workflow_dispatch("develop", settings.workflow_id)
                root.toDelete = []
            }
        }
    }
}
