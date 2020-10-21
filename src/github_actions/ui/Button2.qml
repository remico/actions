import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Button {
    property int orientation: Qt.Vertical

    Layout.fillWidth: orientation == Qt.Vertical
    Layout.fillHeight: orientation == Qt.Horizontal

    KeyNavigation.down: orientation == Qt.Vertical ? nextItemInFocusChain() : null
    KeyNavigation.up: orientation == Qt.Vertical ? nextItemInFocusChain(false) : null
    KeyNavigation.right: orientation == Qt.Horizontal ? nextItemInFocusChain() : null
    KeyNavigation.left: orientation == Qt.Horizontal ? nextItemInFocusChain(false) : null
}
