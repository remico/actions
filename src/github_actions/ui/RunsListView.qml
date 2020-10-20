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

        delegate: _d
        model: _m

        BusyIndicator {
            anchors.centerIn: parent
            running: WorkflowRuns.updating
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
                WorkflowRuns.clear_runs()
                WorkflowRuns.update_runs()
                root.toDelete = []
            }
        }
        Button {
            width: 140
            text: qsTr("Clear View")
            onClicked: {
                WorkflowRuns.clear_runs()
                root.toDelete = []
            }
        }
        Button {
            width: 140
            text: qsTr("Delete Selected")
            onClicked: {
                WorkflowRuns.delete_runs(root.toDelete)
                root.toDelete = []
            }
        }
        Button {
            width: 140
            text: qsTr("Start Run")
            onClicked: {
                WorkflowRuns.post_workflow_dispatch("develop", settings.workflow_id)
                root.toDelete = []
            }
        }
    }

    Component {
        id: _d
        Item {
            id: _d_item
            width: _view.contentItem.width
            height: 42

            KeyNavigation.right: _buttons

            // required property string created_at
            // required property string conclusion

            Rectangle {
                id: _led
                height: 0.8 * parent.height
                width: height
                radius: 8
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 5
                color: conclusion == "success" ? "lightgreen" : "pink"
            }

            Column {
                id: _text
                anchors.left: _led.right
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                Text {
                    text: Utils.format_timestamp(created_at)
                    color: _d_item.ListView.isCurrentItem ? "black" : "red"
                }
                Text {
                    text: "[ " + event + " @ " + head_branch + " ]"
                }
            }

            CheckBox {
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                focusPolicy: Qt.NoFocus
                focus: _d_item.ListView.isCurrentItem
                onCheckedChanged: Utils.a_insert2(root.toDelete, model.id, checked)
            }
        }
    }

    XmlListModel {
        id: _m
        xml: WorkflowRuns.xml
        query: "/all/workflow_runs/item"
        XmlRole { name: 'id'; query: 'id/string()' }
        XmlRole { name: 'created_at'; query: 'created_at/string()' }
        XmlRole { name: 'conclusion'; query: 'conclusion/string()' }
        XmlRole { name: 'event'; query: 'event/string()' }
        XmlRole { name: 'head_branch'; query: 'head_branch/string()' }
        XmlRole { name: 'status'; query: 'status/string()' }
        XmlRole { name: 'html_url'; query: 'html_url/string()' }
    }
}
