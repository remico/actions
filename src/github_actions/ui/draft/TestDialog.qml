import QtQuick 2.15
import QtQuick.Controls 2.15

Dialog {
    objectName: "testdialog"
    width: 300
    height: 200
    x: 150
    y: 150

    title: "Title test dialog"

    modal: true
    closePolicy: Popup.CloseOnEscape

    focus: true
    Component.onCompleted: standardButton(Dialog.Cancel).forceActiveFocus()

    standardButtons: Dialog.Ok | Dialog.Cancel

    onAccepted: console.log("Ok clicked")
    onRejected: console.log("Cancel clicked")
}
