import QtQuick 2.15
import QtQuick.Layouts 1.15

FocusScope {
    id: _buttons

    default property alias buttons: _c.children

    focus: true

    ColumnLayout {
        id: _c
        onChildrenChanged: children[0] ? children[0].focus = true : null
    }
}
