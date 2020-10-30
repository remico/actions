import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import ui 1.0

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
