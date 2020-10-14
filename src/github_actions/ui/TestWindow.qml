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
