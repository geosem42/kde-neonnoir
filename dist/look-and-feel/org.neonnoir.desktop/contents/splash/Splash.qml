/*
    Neon Noir splash — the same lockup Plymouth draws, so the handover from
    boot to session start has no visible seam.

    ksplashqml drives `stage` from 0 upwards as startup proceeds. Breeze fades
    in at 2 and starts fading out at 5; the progress rule here maps the same
    range so the bar is full exactly as the desktop appears.
*/
import QtQuick

Rectangle {
    id: root
    color: "#060B11"

    property int stage

    readonly property real u: Math.max(8, Math.round(Math.min(width, height) / 90))

    onStageChanged: {
        if (stage >= 2) {
            content.opacity = 1;
        }
        if (stage >= 5) {
            creep.stop();
            fill.width = track.width;
        }
    }

    Image {
        anchors.fill: parent
        source: "images/ground.png"
        fillMode: Image.PreserveAspectCrop
        asynchronous: false
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0
        Behavior on opacity { NumberAnimation { duration: 420; easing.type: Easing.OutCubic } }

        Column {
            anchors.centerIn: parent
            spacing: root.u * 3.0

            Image {
                id: mark
                anchors.horizontalCenter: parent.horizontalCenter
                source: "images/mark.png"
                sourceSize.width: root.u * 19
                sourceSize.height: root.u * 19
                width: root.u * 19
                height: root.u * 19
            }

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "NEON NOIR"
                color: "#D9DFE5"
                font.family: "IBM Plex Sans"
                font.weight: Font.Medium
                font.pixelSize: root.u * 2.5
                font.letterSpacing: root.u * 0.85
                // letterSpacing pads the right of the last glyph too; pull back
                // by half so the word stays optically centred under the mark.
                // An x binding would be ignored here — Column children may use
                // horizontal anchors, and the anchor wins over x.
                anchors.horizontalCenterOffset: -font.letterSpacing / 2
            }

            Item {
                id: track
                anchors.horizontalCenter: parent.horizontalCenter
                width: root.u * 28
                height: 2

                Rectangle {
                    anchors.fill: parent
                    color: "#454F58"
                    opacity: 0.55
                }
                // NOT driven by `stage`. ksplashqml's stage is the count of
                // DISTINCT stage names it has been sent, and on this session
                // only two ever arrive ('initial' from ksplashqml itself and
                // 'startPlasma' from plasma_session) — a bar keyed to stage/5
                // would stall at 40% and never fill. Time-based with a
                // decelerating curve instead, snapped full on the way out.
                Rectangle {
                    id: fill
                    height: parent.height
                    color: "#36D7D7"
                    width: 0
                    NumberAnimation on width {
                        id: creep
                        from: 0
                        to: track.width
                        duration: 9000
                        easing.type: Easing.OutCubic
                        running: true
                    }
                }
            }
        }
    }
}
