/*
    The Neon Noir system card: CPU, memory and network in the same measured
    language as the rest of the theme — dim labels, accent only on the values
    and the bars.

    Kept free of the Plasmoid API on purpose so it can be rendered and checked
    outside a running Plasma shell; main.qml is a thin wrapper around it.
*/
import QtQuick
import org.kde.ksysguard.sensors as Sensors

Item {
    id: card

    readonly property color cCard:   "@CARD@"
    readonly property color cHair:   "@HAIR@"
    readonly property color cTrack:  "@TRACK@"
    readonly property color cText:   "@TEXT@"
    readonly property color cDim:    "@DIM@"
    readonly property color cCyan:   "@CYAN@"
    readonly property color cAmber:  "@AMBER@"
    readonly property string uiFont: "@FONT@"
    readonly property string monoFont: "@MONO@"

    implicitWidth: 300
    implicitHeight: body.implicitHeight + 40

    Sensors.Sensor { id: cpu;      sensorId: "cpu/all/usage";        updateRateLimit: 1000 }
    Sensors.Sensor { id: memUsed;  sensorId: "memory/physical/used"; updateRateLimit: 2000 }
    Sensors.Sensor { id: memTotal; sensorId: "memory/physical/total" }
    Sensors.Sensor {
        id: netDown
        sensorId: "network/all/download"
        updateRateLimit: 1000
        onValueChanged: spark.push(value)
    }

    Rectangle {
        anchors.fill: parent
        radius: 10
        color: card.cCard
        border.color: card.cHair
        border.width: 1
    }

    Column {
        id: body
        anchors { left: parent.left; right: parent.right; top: parent.top
                  leftMargin: 17; rightMargin: 17; topMargin: 16 }
        spacing: 13

        Text {
            text: "SYSTEM"
            color: card.cCyan
            font.family: card.uiFont
            font.pixelSize: 11
            font.weight: Font.Medium
            font.letterSpacing: 2
        }

        // CPU
        Column {
            anchors { left: parent.left; right: parent.right }
            spacing: 6
            Item {
                anchors { left: parent.left; right: parent.right }
                height: cpuLabel.implicitHeight
                Text {
                    id: cpuLabel
                    text: "CPU"
                    color: card.cDim
                    font.family: card.uiFont
                    font.pixelSize: 13
                }
                Text {
                    anchors.right: parent.right
                    text: cpu.status === Sensors.Sensor.Ready
                          ? Math.round(cpu.value) + "%" : "—"
                    color: card.cCyan
                    font.family: card.monoFont
                    font.pixelSize: 13
                }
            }
            Rectangle {
                anchors { left: parent.left; right: parent.right }
                height: 4
                radius: 2
                color: card.cTrack
                Rectangle {
                    height: parent.height
                    radius: parent.radius
                    color: card.cCyan
                    width: parent.width * Math.min(1, Math.max(0, cpu.value / 100))
                    Behavior on width { NumberAnimation { duration: 420
                                                          easing.type: Easing.OutCubic } }
                }
            }
        }

        // Memory
        Column {
            anchors { left: parent.left; right: parent.right }
            spacing: 6
            Item {
                anchors { left: parent.left; right: parent.right }
                height: memLabel.implicitHeight
                Text {
                    id: memLabel
                    text: "Memory"
                    color: card.cDim
                    font.family: card.uiFont
                    font.pixelSize: 13
                }
                Text {
                    anchors.right: parent.right
                    text: memTotal.value > 0
                          ? memUsed.formattedValue + " / " + memTotal.formattedValue : "—"
                    color: card.cCyan
                    font.family: card.monoFont
                    font.pixelSize: 13
                }
            }
            Rectangle {
                anchors { left: parent.left; right: parent.right }
                height: 4
                radius: 2
                color: card.cTrack
                Rectangle {
                    height: parent.height
                    radius: parent.radius
                    color: card.cCyan
                    width: memTotal.value > 0
                           ? parent.width * Math.min(1, memUsed.value / memTotal.value) : 0
                    Behavior on width { NumberAnimation { duration: 420
                                                          easing.type: Easing.OutCubic } }
                }
            }
        }

        // Network
        Column {
            anchors { left: parent.left; right: parent.right }
            spacing: 6
            Item {
                anchors { left: parent.left; right: parent.right }
                height: netLabel.implicitHeight
                Text {
                    id: netLabel
                    text: "Network"
                    color: card.cDim
                    font.family: card.uiFont
                    font.pixelSize: 13
                }
                Text {
                    anchors.right: parent.right
                    text: netDown.status === Sensors.Sensor.Ready ? netDown.formattedValue : "—"
                    color: card.cAmber
                    font.family: card.monoFont
                    font.pixelSize: 13
                }
            }
            Canvas {
                id: spark
                anchors { left: parent.left; right: parent.right }
                height: 34
                renderStrategy: Canvas.Cooperative

                property var history: []
                readonly property int slots: 48

                function push(v) {
                    const h = history.slice()
                    h.push(Math.max(0, v || 0))
                    while (h.length > slots) { h.shift() }
                    history = h
                    requestPaint()
                }

                onPaint: {
                    const ctx = getContext("2d")
                    ctx.reset()
                    if (history.length < 2) { return }
                    // Scale to the window's own peak: absolute throughput is
                    // already on the label, so the shape is what matters here.
                    let peak = 1
                    for (let i = 0; i < history.length; i++) {
                        if (history[i] > peak) { peak = history[i] }
                    }
                    const step = width / (slots - 1)
                    const x0 = width - (history.length - 1) * step
                    ctx.beginPath()
                    ctx.moveTo(x0, height)
                    for (let i = 0; i < history.length; i++) {
                        const y = height - (history[i] / peak) * (height - 2) - 1
                        ctx.lineTo(x0 + i * step, y)
                    }
                    ctx.lineTo(x0 + (history.length - 1) * step, height)
                    ctx.closePath()
                    ctx.fillStyle = Qt.rgba(card.cAmber.r, card.cAmber.g, card.cAmber.b, 0.16)
                    ctx.fill()

                    ctx.beginPath()
                    for (let i = 0; i < history.length; i++) {
                        const y = height - (history[i] / peak) * (height - 2) - 1
                        if (i === 0) { ctx.moveTo(x0, y) } else { ctx.lineTo(x0 + i * step, y) }
                    }
                    ctx.strokeStyle = card.cAmber
                    ctx.lineWidth = 1.4
                    ctx.lineJoin = "round"
                    ctx.stroke()
                }
            }
        }
    }
}
