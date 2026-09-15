/*
    Neon Noir SDDM greeter.

    Plain QtQuick only: QtQuick.Controls resolves to the Basic style inside the
    greeter, i18n* is undefined there, Kirigami's palette returns black for
    every role and no icon theme is loaded. Colours are baked in and every
    glyph is an SVG from this directory.
*/
import QtQuick

Item {
    id: root
    width: 1600
    height: 900

    readonly property color cVoid:    "#060B11"
    readonly property color cCard:    "#222B33"
    readonly property color cView:    "#0D131A"
    readonly property color cRaised:  "#2D3640"
    readonly property color cHair:    "#293037"
    readonly property color cFloat:   "#2D3640"
    readonly property color cHover:   "#3A434E"
    readonly property color cText:    "#D9DFE5"
    readonly property color cDim:     "#A1A9B0"
    readonly property color cCyan:    "#36D7D7"
    readonly property color cCyanHi:  "#7AE6E5"
    readonly property color cMagenta: "#F346EB"
    readonly property color cInk:     "#060B11"
    readonly property color cNeg:     "#FE8B83"
    readonly property color cNeutral: "#E1A536"
    readonly property string uiFont:  "IBM Plex Sans"

    property int userIndex: userModel.lastIndex
    property int sessionIndex: sessionModel.lastIndex
    property string userName: ""
    property string userReal: ""
    property url userFace: ""
    property string notice: ""
    property bool busy: false

    function applyUser(n, r, i) { userName = n; userReal = r.length > 0 ? r : n; userFace = i }
    function doLogin() {
        if (busy || userName.length === 0) { return }
        busy = true
        notice = ""
        sddm.login(userName, passwordField.text, sessionIndex)
    }

    // The model is read through delegates rather than by role index: the role
    // ordering is undocumented and shifts between SDDM versions.
    Repeater {
        model: userModel
        delegate: Item {
            required property int index
            required property string name
            required property string realName
            required property url icon
            Component.onCompleted: if (index === root.userIndex) root.applyUser(name, realName, icon)
            Connections {
                target: root
                function onUserIndexChanged() {
                    if (index === root.userIndex) { root.applyUser(name, realName, icon) }
                }
            }
        }
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            root.busy = false
            root.notice = "Wrong password"
            passwordField.text = ""
            passwordField.forceActiveFocus()
            rejectShake.restart()
        }
        function onLoginSucceeded() { root.busy = false }
        function onInformationMessage(message) { root.notice = message }
    }

    // One background per physical screen, positioned by the screen's geometry.
    Repeater {
        model: screenModel
        delegate: Item {
            required property rect geometry
            x: geometry.x; y: geometry.y
            width: geometry.width; height: geometry.height
            clip: true
            Image {
                anchors.fill: parent
                // theme.conf ships the bundled ground; the System Settings
                // KCM can override it via theme.conf.user.
                source: config.background ? config.background : "images/background.png"
                fillMode: Image.PreserveAspectCrop
                asynchronous: false
                cache: true
            }
        }
    }

    // ── top rule ──────────────────────────────────────────────────────────────
    Item {
        id: topBar
        anchors { top: parent.top; left: parent.left; right: parent.right }
        height: 64

        Text {
            anchors { left: parent.left; leftMargin: 32; verticalCenter: parent.verticalCenter }
            text: "UBUNTU 26.04.1 LTS"
            color: root.cCyan
            font.family: root.uiFont
            font.pixelSize: 12
            font.weight: Font.Medium
            font.letterSpacing: 2.2
        }

        Row {
            anchors { right: parent.right; rightMargin: 32; verticalCenter: parent.verticalCenter }
            spacing: 18

            // A MouseArea cannot be a direct child of a Row — positioners
            // reject fill/left/right anchors on their children — so the hit
            // target lives in a wrapping Item.
            Item {
                visible: keyboard.layouts.length > 1
                anchors.verticalCenter: parent.verticalCenter
                width: kbRow.implicitWidth
                height: kbRow.implicitHeight
                Row {
                    id: kbRow
                    spacing: 7
                    Image {
                        source: "images/keyboard.svg"
                        sourceSize: Qt.size(16, 16)
                        anchors.verticalCenter: parent.verticalCenter
                        opacity: 0.8
                    }
                    Text {
                        text: keyboard.layouts.length > 0
                              ? keyboard.layouts[keyboard.currentLayout].shortName : ""
                        color: root.cDim
                        font.family: root.uiFont
                        font.pixelSize: 13
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: keyboard.currentLayout =
                        (keyboard.currentLayout + 1) % keyboard.layouts.length
                }
            }

            Text {
                id: clock
                property date now: new Date()
                text: Qt.formatTime(now, "HH:mm")
                color: root.cText
                font.family: root.uiFont
                font.pixelSize: 15
                font.weight: Font.Medium
                anchors.verticalCenter: parent.verticalCenter
                Timer {
                    interval: 1000; running: true; repeat: true
                    onTriggered: clock.now = new Date()
                }
            }
        }
    }

    // ── login card ────────────────────────────────────────────────────────────
    Rectangle {
        id: card
        anchors.centerIn: parent
        width: 420
        height: cardCol.implicitHeight + 56
        radius: 12
        color: root.cCard
        border.color: root.cHair
        border.width: 1

        SequentialAnimation {
            id: rejectShake
            NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"
                              to: -9; duration: 50 }
            NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"
                              to: 9; duration: 90 }
            NumberAnimation { target: card; property: "anchors.horizontalCenterOffset"
                              to: 0; duration: 60 }
        }

        Column {
            id: cardCol
            anchors { left: parent.left; right: parent.right; verticalCenter: parent.verticalCenter
                      leftMargin: 28; rightMargin: 28 }
            spacing: 14

            Rectangle {
                id: avatar
                anchors.horizontalCenter: parent.horizontalCenter
                width: 78; height: 78; radius: 39
                gradient: Gradient {
                    GradientStop { position: 0.0; color: root.cCyan }
                    GradientStop { position: 1.0; color: root.cMagenta }
                }
                Text {
                    anchors.centerIn: parent
                    visible: face.status !== Image.Ready
                    text: root.userReal.length > 0 ? root.userReal.charAt(0).toUpperCase() : "?"
                    color: root.cInk
                    font.family: root.uiFont
                    font.pixelSize: 34
                    font.weight: Font.DemiBold
                }
                Image {
                    id: face
                    anchors.fill: parent
                    anchors.margins: 2
                    source: root.userFace
                    fillMode: Image.PreserveAspectCrop
                    visible: false
                }
                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 2
                    radius: width / 2
                    visible: face.status === Image.Ready
                    color: "transparent"
                    clip: true
                    Image {
                        anchors.fill: parent
                        source: root.userFace
                        fillMode: Image.PreserveAspectCrop
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    enabled: userModel.count > 1
                    cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onClicked: root.userIndex = (root.userIndex + 1) % userModel.count
                }
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: root.userReal
                color: root.cText
                font.family: root.uiFont
                font.pixelSize: 19
                font.weight: Font.Medium
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: sddm.hostName
                visible: text.length > 0
                color: root.cDim
                font.family: root.uiFont
                font.pixelSize: 13
            }

            Item { width: 1; height: 6 }

            // password
            Rectangle {
                id: pwBox
                anchors { left: parent.left; right: parent.right }
                height: 46
                radius: 8
                color: root.cView
                border.width: passwordField.activeFocus ? 2 : 1
                border.color: root.notice.length > 0 ? root.cNeg
                              : passwordField.activeFocus ? root.cCyan : root.cHair
                Behavior on border.color { ColorAnimation { duration: 120 } }

                Image {
                    id: lockIcon
                    anchors { left: parent.left; leftMargin: 14; verticalCenter: parent.verticalCenter }
                    source: "images/lock.svg"
                    sourceSize: Qt.size(17, 17)
                    opacity: 0.85
                }

                TextInput {
                    id: passwordField
                    anchors { left: lockIcon.right; leftMargin: 12; right: revealButton.left
                              rightMargin: 10; verticalCenter: parent.verticalCenter }
                    color: root.cText
                    font.family: root.uiFont
                    font.pixelSize: 15
                    echoMode: revealButton.revealed ? TextInput.Normal : TextInput.Password
                    passwordCharacter: "•"
                    passwordMaskDelay: 0
                    selectByMouse: true
                    selectionColor: root.cCyan
                    selectedTextColor: root.cInk
                    clip: true
                    focus: true
                    enabled: !root.busy
                    onTextChanged: root.notice = ""
                    Keys.onReturnPressed: root.doLogin()
                    Keys.onEnterPressed: root.doLogin()
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        visible: parent.text.length === 0 && !parent.activeFocus
                        text: "Password"
                        color: root.cDim
                        font: parent.font
                    }
                }

                Item {
                    id: revealButton
                    property bool revealed: false
                    anchors { right: parent.right; rightMargin: 12; verticalCenter: parent.verticalCenter }
                    width: 22; height: 22
                    Image {
                        anchors.centerIn: parent
                        source: revealButton.revealed ? "images/eye-off.svg" : "images/eye.svg"
                        sourceSize: Qt.size(18, 18)
                        opacity: revealArea.containsMouse ? 1.0 : 0.7
                    }
                    MouseArea {
                        id: revealArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: revealButton.revealed = !revealButton.revealed
                    }
                }
            }

            Text {
                anchors { left: parent.left; right: parent.right }
                text: root.notice
                visible: root.notice.length > 0
                color: root.cNeg
                font.family: root.uiFont
                font.pixelSize: 13
                wrapMode: Text.WordWrap
            }

            Text {
                anchors { left: parent.left; right: parent.right }
                text: "Caps Lock is on"
                visible: keyboard.capsLock
                color: root.cNeutral
                font.family: root.uiFont
                font.pixelSize: 13
            }

            // log in
            Rectangle {
                id: loginButton
                anchors { left: parent.left; right: parent.right }
                height: 44
                radius: 8
                color: root.busy ? root.cCyanHi
                       : loginArea.pressed ? root.cCyanHi
                       : loginArea.containsMouse ? root.cCyanHi : root.cCyan
                Behavior on color { ColorAnimation { duration: 120 } }

                Row {
                    anchors.centerIn: parent
                    spacing: 10
                    Text {
                        text: root.busy ? "Signing in" : "Log in"
                        color: root.cInk
                        font.family: root.uiFont
                        font.pixelSize: 15
                        font.weight: Font.DemiBold
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Image {
                        source: "images/arrow.svg"
                        sourceSize: Qt.size(17, 17)
                        visible: !root.busy
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                MouseArea {
                    id: loginArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.doLogin()
                }
            }

            // session
            Item {
                anchors { left: parent.left; right: parent.right }
                height: 26
                visible: sessionModel.count > 0
                Row {
                    id: sessionRow
                    anchors.centerIn: parent
                    spacing: 7
                    Text {
                        id: sessionLabel
                        text: sessionPicker.currentName
                        color: sessionArea.containsMouse ? root.cText : root.cDim
                        font.family: root.uiFont
                        font.pixelSize: 13
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Image {
                        source: "images/chevron.svg"
                        sourceSize: Qt.size(14, 14)
                        opacity: 0.75
                        anchors.verticalCenter: parent.verticalCenter
                        rotation: sessionPicker.open ? 180 : 0
                        Behavior on rotation { NumberAnimation { duration: 120 } }
                    }
                }
                MouseArea {
                    id: sessionArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: sessionPicker.open = !sessionPicker.open
                }
            }
        }
    }

    // ── session menu ──────────────────────────────────────────────────────────
    Rectangle {
        id: sessionPicker
        property bool open: false
        property string currentName: "Session"
        anchors { horizontalCenter: card.horizontalCenter; top: card.bottom; topMargin: 10 }
        width: 260
        height: sessionCol.implicitHeight + 12
        radius: 10
        color: root.cFloat
        border.color: root.cHair
        border.width: 1
        visible: open
        z: 10

        Column {
            id: sessionCol
            anchors { left: parent.left; right: parent.right; top: parent.top
                      margins: 6 }
            Repeater {
                model: sessionModel
                delegate: Rectangle {
                    required property int index
                    required property string name
                    anchors { left: parent.left; right: parent.right }
                    height: 32
                    radius: 6
                    color: rowArea.containsMouse ? root.cHover : "transparent"
                    Text {
                        anchors { left: parent.left; leftMargin: 12
                                  verticalCenter: parent.verticalCenter }
                        text: name
                        color: index === root.sessionIndex ? root.cCyan : root.cText
                        font.family: root.uiFont
                        font.pixelSize: 14
                    }
                    Component.onCompleted: if (index === root.sessionIndex)
                        { sessionPicker.currentName = name }
                    MouseArea {
                        id: rowArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            root.sessionIndex = index
                            sessionPicker.currentName = name
                            sessionPicker.open = false
                        }
                    }
                }
            }
        }
    }

    // ── power row ─────────────────────────────────────────────────────────────
    Row {
        anchors { horizontalCenter: parent.horizontalCenter; bottom: parent.bottom
                  bottomMargin: 48 }
        spacing: 12

        Repeater {
            model: [
                { "label": "Shut down", "glyph": "images/power.svg",   "action": 0 },
                { "label": "Restart",   "glyph": "images/restart.svg", "action": 1 },
                { "label": "Suspend",   "glyph": "images/suspend.svg", "action": 2 }
            ]
            delegate: Rectangle {
                required property var modelData
                visible: modelData.action === 0 ? sddm.canPowerOff
                         : modelData.action === 1 ? sddm.canReboot : sddm.canSuspend
                width: powerRow.implicitWidth + 30
                height: 36
                radius: 8
                color: powerArea.containsMouse ? root.cRaised : "transparent"
                border.color: powerArea.containsMouse ? root.cHover : root.cHair
                border.width: 1
                Behavior on color { ColorAnimation { duration: 120 } }
                Row {
                    id: powerRow
                    anchors.centerIn: parent
                    spacing: 8
                    Image {
                        source: modelData.glyph
                        sourceSize: Qt.size(15, 15)
                        opacity: 0.85
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    Text {
                        text: modelData.label
                        color: root.cText
                        font.family: root.uiFont
                        font.pixelSize: 13
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                MouseArea {
                    id: powerArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        if (modelData.action === 0) { sddm.powerOff() }
                        else if (modelData.action === 1) { sddm.reboot() }
                        else { sddm.suspend() }
                    }
                }
            }
        }
    }

    Component.onCompleted: passwordField.forceActiveFocus()
}
