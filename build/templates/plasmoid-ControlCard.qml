/*
    The Neon Noir options popup.

    Two axes, each a pair of named variants rather than an on/off switch: a
    switch has to decide which side is "on", and neither "standard" nor "riced"
    is the absence of the other. A variant that has not been built yet is shown
    rather than hidden, and says so on its face — hiding it would leave a
    control that changes shape the first time a second variant lands.

    The selected cell is a cyan border over the ghost fill, which is exactly how
    the pager marks the desktop you are on. Every colour is a palette token
    substituted at build time, so this file holds no hex of its own.
*/
import QtQuick
import QtQuick.Layouts

ColumnLayout {
    id: card

    /* Set by main.qml from neonnoirrc: the variant currently applied. */
    property string panelVariant: "classic"
    property string windowsProfile: "classic"

    /* Emitted when a cell is clicked. main.qml runs the apply script. */
    signal choose(string axis, string variant)

    spacing: 0

    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: body.implicitHeight + 28
        color: "@CARD@"
        border.color: "@HAIR@"
        border.width: 1
        radius: 7

        ColumnLayout {
            id: body
            anchors.fill: parent
            anchors.margins: 14
            spacing: 14

            Text {
                text: "Neon Noir"
                color: "@TEXT@"
                font.family: "@FONT@"
                font.pixelSize: 14
                font.bold: true
            }

            Axis {
                Layout.fillWidth: true
                axis: "windows"
                title: "Windows"
                subtitle: "How windows are framed and managed"
                current: card.windowsProfile
                variants: [
                    { id: "classic", label: "Standard", ready: true },
                    { id: "compact", label: "Compact", ready: true },
                    { id: "tiled", label: "Tiled", ready: true }
                ]
                onPick: (a, v) => card.choose(a, v)
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: "@HAIR@"
            }

            Axis {
                Layout.fillWidth: true
                axis: "panel"
                title: "Taskbar"
                subtitle: "The shape and contents of the panel"
                current: card.panelVariant
                variants: [
                    { id: "classic", label: "Standard", ready: true },
                    { id: "neon", label: "Futuristic", ready: false }
                ]
                onPick: (a, v) => card.choose(a, v)
            }
        }
    }

    component Axis: ColumnLayout {
        id: row

        property string axis
        property string title
        property string subtitle
        property string current
        property var variants: []

        signal pick(string axis, string variant)

        spacing: 8

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 1

            Text {
                text: row.title
                color: "@TEXT@"
                font.family: "@FONT@"
                font.pixelSize: 12
            }

            Text {
                Layout.fillWidth: true
                text: row.subtitle
                color: "@DIM@"
                font.family: "@FONT@"
                font.pixelSize: 10
                elide: Text.ElideRight
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Repeater {
                model: row.variants

                delegate: Rectangle {
                    id: cell

                    required property var modelData

                    readonly property bool selected: modelData.id === row.current
                    readonly property bool ready: modelData.ready === true

                    Layout.fillWidth: true
                    Layout.preferredHeight: 34

                    radius: 5
                    border.width: 1
                    border.color: selected ? "@CYAN@" : "@HAIR@"
                    color: selected ? "@GHOST@"
                                    : (hover.hovered && ready ? "@HOVER@" : "@VOID@")

                    ColumnLayout {
                        anchors.centerIn: parent
                        spacing: 0

                        Text {
                            Layout.alignment: Qt.AlignHCenter
                            text: cell.modelData.label
                            color: !cell.ready ? "@FAINT@"
                                               : (cell.selected ? "@CYAN@" : "@DIM@")
                            font.family: "@FONT@"
                            font.pixelSize: 11
                        }

                        Text {
                            Layout.alignment: Qt.AlignHCenter
                            visible: !cell.ready
                            text: "not built yet"
                            color: "@FAINT@"
                            font.family: "@FONT@"
                            font.pixelSize: 8
                        }
                    }

                    HoverHandler {
                        id: hover
                        enabled: cell.ready
                        cursorShape: Qt.PointingHandCursor
                    }

                    // The SELECTED cell stays clickable on purpose: clicking it
                    // re-applies its variant, which is how you put the panel
                    // back after dragging something out of place. Without that
                    // the widget is inert whenever an axis has only one built
                    // variant, which is every axis today.
                    TapHandler {
                        enabled: cell.ready
                        onTapped: row.pick(row.axis, cell.modelData.id)
                    }
                }
            }
        }
    }
}
