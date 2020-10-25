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
