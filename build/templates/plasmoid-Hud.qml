/*
    Neon Noir HUD — the entire contents of the Futuristic bar, in one widget.

    Deliberately NOT assembled out of Plasma's stock applets. A row of stock
    applets in a short panel is just the standard taskbar at a smaller size,
    which is exactly what this variant is not supposed to be. What makes a
    polybar read as a polybar is that every module sits on one grid, in one
    monospaced face, with slanted segment edges and an accent underline
    carrying the state — and none of that is possible while each module is a
    separate applet drawing its own background and picking its own metrics.
    So one item owns the whole row and draws workspaces, tasks, the window
    title, the telemetry and the clock itself.

    Everything here is monospace and mostly uppercase. That is the point: a
    status bar is a readout, and a readout in a proportional face reads as a
    toolbar. The accent is spent only on state — the current desktop, the
    active window, a load above its threshold — so a quiet machine shows a
    quiet bar and a busy one lights up.

    Sensor ids are the ones ksystemstats actually publishes, read off the
    stock System Monitor presets and the plugin binaries rather than guessed.
*/
import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.ksysguard.sensors as Sensors
import org.kde.taskmanager as TaskManager
import org.kde.plasma.plasma5support as P5Support
import QtQuick.Controls as QQC2

Item {
    id: hud

    // Set by the wrapper; the task list is filtered to the screen this panel
    // is on, so a second monitor does not show the first one's windows.
    property var screenGeo

    // Pinned apps. Owned by the applet's configuration, not by this item, so
    // the HUD stays renderable outside a running shell — the wrapper reads the
    // list in and writes back whatever the model ends up with.
    property var launchers: []
    signal launchersWritten(var list)

    readonly property int barH: height
    readonly property int textY: 11

    implicitHeight: 28

    /* ---------------------------------------------------------------- state */

    TaskManager.VirtualDesktopInfo { id: vdi }

    TaskManager.TasksModel {
        id: tasks
        virtualDesktop: vdi.currentDesktop
        screenGeometry: hud.screenGeo
        filterByVirtualDesktop: true
        filterByScreen: true
        // One cell per window, never one per application. A status bar shows
        // what is open, and collapsing two windows into one icon with a badge
        // is a taskbar affordance, not a readout.
        groupMode: TaskManager.TasksModel.GroupDisabled
        // A pinned app and its window are ONE cell: the icon you clicked to
        // start something is where that something stays. With separateLaunchers
        // the launcher keeps its slot and the window opens in a second one.
        separateLaunchers: false
        launchInPlace: true
        // Manual, the same strategy the stock icon task manager uses: pinned
        // apps hold the order they were added and windows append after them.
        // Not SortLastActivated, which reorders the strip every time focus
        // moves, so the icon you are aiming at walks away from the pointer.
        sortMode: TaskManager.TasksModel.SortManual

        // Assigned once rather than bound: requestAddLauncher writes
        // launcherList from inside the model, and a binding here would be
        // clobbered on the first pin and then fight the write-back.
        Component.onCompleted: launcherList = hud.launchers
        onLauncherListChanged: hud.launchersWritten(launcherList)
    }

    // The list can also change from outside the widget — the panel script seeds
    // it at install time. Guarded so the write-back above cannot echo.
    onLaunchersChanged: {
        if (String(launchers) !== String(tasks.launcherList)) {
            tasks.launcherList = launchers;
        }
    }

    property int ctxRow: -1
    property string ctxUrl: ""
    property bool ctxPinned: false
    property bool ctxIsWindow: false
    property string ctxName: ""

    QQC2.Menu {
        id: ctx

        QQC2.MenuItem {
            text: hud.ctxPinned ? "Unpin from taskbar" : "Pin to taskbar"
            enabled: hud.ctxUrl !== ""
            onTriggered: {
                if (hud.ctxPinned) {
                    tasks.requestRemoveLauncher(hud.ctxUrl);
                } else {
                    tasks.requestAddLauncher(hud.ctxUrl);
                }
            }
        }

        QQC2.MenuSeparator { }

        QQC2.MenuItem {
            text: "Close"
            enabled: hud.ctxIsWindow
            onTriggered: tasks.requestClose(tasks.makeModelIndex(hud.ctxRow))
        }
    }

    function launcherUrl(index) {
        return tasks.data(tasks.makeModelIndex(index),
                          TaskManager.AbstractTasksModel.LauncherUrlWithoutIcon);
    }

    Sensors.Sensor { id: cpu;  sensorId: "cpu/all/usage";               updateRateLimit: 1200 }
    Sensors.Sensor { id: mem;  sensorId: "memory/physical/usedPercent"; updateRateLimit: 2500 }
    Sensors.Sensor { id: tmp;  sensorId: "cpu/all/averageTemperature";  updateRateLimit: 3000 }
    Sensors.Sensor { id: dn;   sensorId: "network/all/download";        updateRateLimit: 1200 }
    Sensors.Sensor { id: up;   sensorId: "network/all/upload";          updateRateLimit: 1200 }
    Sensors.Sensor { id: dsk;  sensorId: "disk/all/usedPercent";         updateRateLimit: 30000 }

    readonly property int bars: 22
    property var cpuHist: []
    property var memHist: []

    /* Reassigning the whole array is what notifies the bindings — mutating it
       in place changes nothing QML can see. The Repeater's model is a fixed
       count, so the delegates are not rebuilt, only their heights. */
    function push(a, v) {
        var out = a.slice(Math.max(0, a.length - hud.bars + 1));
        out.push(Math.max(0, Math.min(1, v)));
        return out;
    }

    Connections {
        target: cpu
        function onValueChanged() { hud.cpuHist = hud.push(hud.cpuHist, cpu.value / 100) }
    }
    Connections {
        target: mem
        function onValueChanged() { hud.memHist = hud.push(hud.memHist, mem.value / 100) }
    }

    // Bumped on dataChanged so the title re-reads while the SAME window stays
    // active — a browser switching tabs never emits activeTaskChanged.
    property int titleTick: 0
    Connections {
        target: tasks
        function onDataChanged() { hud.titleTick++ }
        function onActiveTaskChanged() { hud.titleTick++ }
    }

    function activeTitle() {
        void hud.titleTick;
        return tasks.activeTask && tasks.activeTask.valid
             // 0, not Qt.DisplayRole: the Qt namespace exposed to QML does not
             // carry the ItemDataRole enum, so the named form passes undefined
             // and the title comes back empty.
             ? String(tasks.data(tasks.activeTask, 0) || "") : "";
    }

    property date now: new Date()
    Timer { interval: 1000; running: true; repeat: true; onTriggered: hud.now = new Date() }

    /* Straight out of /proc rather than through a sensor. ksystemstats does
       publish an uptime, but only as part of osinfo, and one `cat` on a minute
       timer is less machinery than pulling in a whole provider.

       Read through the DataSource below rather than with an XMLHttpRequest
       against file:///proc/uptime — that request never came back inside the
       shell's engine and the cell simply stayed hidden. */
    property string uptime: ""
    Timer {
        interval: 60000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: shell.exec("cat /proc/uptime")
    }

    /* VirtualDesktopInfo is read-only — it publishes the desktop list and the
       current one but has no way to change it. KWin's own
       org.kde.KWin.VirtualDesktopManager exposes `current` as a WRITABLE
       property, and setting it to a desktop's UUID is the switch. */
    P5Support.DataSource {
        id: shell
        engine: "executable"
        connectedSources: []
        onNewData: (source, data) => {
            if (source.indexOf("/proc/uptime") !== -1) {
                var secs = parseFloat(String(data["stdout"] || "").split(" ")[0]);
                if (isFinite(secs)) {
                    var d = Math.floor(secs / 86400);
                    var h = Math.floor(secs % 86400 / 3600);
                    var m = Math.floor(secs % 3600 / 60);
                    hud.uptime = d > 0 ? d + "d " + String(h).padStart(2, "0") + "h"
                               : h > 0 ? h + "h " + String(m).padStart(2, "0") + "m"
                                       : m + "m";
                }
            }
            disconnectSource(source);
        }
        // Reconnecting an already-connected source is a no-op, so a command
        // that ran once would never run again.
        function exec(cmd) { disconnectSource(cmd); connectSource(cmd) }
    }

    function gotoDesk(id) {
        shell.exec("qdbus6 org.kde.KWin /VirtualDesktopManager " +
                   "org.kde.KWin.VirtualDesktopManager.current " + id);
    }

    /* --------------------------------------------------------------- format */

    // Cyan while there is headroom, amber once the machine is working, magenta
    // when it is not keeping up. Three steps, so a glance is enough.
    function ramp(v) {
        return v > 0.85 ? "@MAGENTA@" : v > 0.60 ? "@AMBER@" : "@CYAN@";
    }

    function pct(s) {
        return s.status === Sensors.Sensor.Ready
             ? String(Math.round(s.value)).padStart(2, "0") + "%" : "--%";
    }

    // No space padding: the cell below reserves a fixed column and right-aligns
    // instead. Padding with spaces kept the figure from reflowing but opened a
    // visible gap inside the reading whenever the rate was small.
    function rate(s) {
        if (s.status !== Sensors.Sensor.Ready) { return "----"; }
        var k = s.value / 1024;
        if (k >= 1024) { return (k / 1024).toFixed(1) + "M"; }
        return Math.round(k) + "K";
    }

    /* ------------------------------------------------------------ primitives */

    // The divider between two cells inside one segment: the same angle as the
    // wedge, one pixel wide, so the slant repeats all the way along.
    component Nick: Canvas {
        property color stroke
        implicitWidth: Math.round(height * 0.34)
        onStrokeChanged: requestPaint()
        onHeightChanged: requestPaint()
        onPaint: {
            var c = getContext("2d");
            c.reset();
            c.strokeStyle = stroke;
            c.lineWidth = 1;
            c.beginPath();
            c.moveTo(width - 0.5, 5);
            c.lineTo(0.5, height - 5);
            c.stroke();
        }
    }

    component Spark: Item {
        id: spark
        property var samples: []
        property color tint: "@CYAN@"
        implicitWidth: hud.bars * 2 + (hud.bars - 1)
        implicitHeight: 11
        Row {
            anchors.fill: parent
            spacing: 1
            Repeater {
                model: hud.bars
                Rectangle {
                    // Right-aligned history: index 0 is the oldest sample and
                    // the row is only full once `bars` readings have arrived.
                    readonly property int slot: index - (hud.bars - spark.samples.length)
                    readonly property real v: slot >= 0 ? spark.samples[slot] : 0
                    width: 2
                    height: Math.max(1, Math.round(spark.height * v))
                    y: spark.height - height
                    color: spark.tint
                    // Older samples recede, so the eye lands on the present.
                    opacity: 0.3 + 0.7 * (index / (hud.bars - 1))
                }
            }
        }
    }

    component Label: Text {
        color: "@CYAN@"
        font.family: "@MONO@"
        font.pixelSize: 10
        font.bold: true
        font.letterSpacing: 1
        renderType: Text.NativeRendering
    }

    component Value: Text {
        color: "@TEXT@"
        font.family: "@MONO@"
        font.pixelSize: hud.textY
        renderType: Text.NativeRendering
    }

    /* ------------------------------------------------------------ the row */

    RowLayout {
        anchors.fill: parent
        spacing: 0

        /* ---- workspaces ------------------------------------------------- */

        Row {
            id: desks
            Layout.fillHeight: true
            spacing: 0

            Repeater {
                model: vdi.numberOfDesktops

                Item {
                    readonly property string did: vdi.desktopIds[index] || ""
                    readonly property bool here: did === vdi.currentDesktop
                    width: 26
                    height: desks.height

                    Text {
                        anchors.centerIn: parent
                        // Zero-padded so the cells never change width when
                        // a tenth desktop appears.
                        text: String(index + 1).padStart(2, "0")
                        color: parent.here ? "@CYAN@" : "@FAINT@"
                        font.family: "@MONO@"
                        font.pixelSize: 10
                        font.bold: parent.here
                        renderType: Text.NativeRendering
                    }

                    // polybar's `line-size`: state lives under the module,
                    // not in a box around it.
                    Rectangle {
                        anchors { left: parent.left; right: parent.right; bottom: parent.bottom }
                        height: 2
                        color: "@CYAN@"
                        visible: parent.here
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: hud.gotoDesk(parent.did)
                    }
                }
            }
        }

        /* ---- open windows ------------------------------------------------ */

        Row {
            id: strip
            Layout.fillHeight: true
            Layout.leftMargin: 8
            spacing: 2

            Repeater {
                model: tasks

                Item {
                    id: cell
                    width: 24
                    height: strip.height

                    // A pinned app with nothing running is a launcher row. It
                    // is dimmed rather than marked, so the strip reads as "what
                    // is here" with the running ones brighter.
                    readonly property bool isLauncher: model.IsLauncher === true
                    readonly property bool pinned: isLauncher || model.HasLauncher === true

                    Kirigami.Icon {
                        anchors.centerIn: parent
                        width: 16
                        height: 16
                        source: model.decoration
                        // A minimized window is still open, so it stays on the
                        // bar — just turned down rather than removed.
                        opacity: cell.isLauncher ? 0.55 : (model.IsMinimized ? 0.35 : 1.0)
                    }

                    Rectangle {
                        anchors { left: parent.left; right: parent.right; bottom: parent.bottom }
                        height: 2
                        color: model.IsDemandingAttention ? "@MAGENTA@" : "@CYAN@"
                        visible: model.IsActive || model.IsDemandingAttention
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
                        onClicked: (m) => {
                            var ix = tasks.makeModelIndex(index);
                            if (m.button === Qt.RightButton) {
                                hud.ctxRow = index;
                                hud.ctxUrl = hud.launcherUrl(index);
                                hud.ctxPinned = cell.pinned;
                                hud.ctxIsWindow = model.IsWindow === true;
                                hud.ctxName = String(model.AppName || model.display || "");
                                ctx.popup();
                            } else if (m.button === Qt.MiddleButton) {
                                if (model.IsWindow) { tasks.requestClose(ix); }
                            } else if (model.IsActive) {
                                tasks.requestToggleMinimized(ix);
                            } else {
                                // Launches a launcher row, raises a window row.
                                tasks.requestActivate(ix);
                            }
                        }
                    }
                }
            }
        }

        /* ---- active window ----------------------------------------------- */

        Text {
            Layout.fillWidth: true
            Layout.leftMargin: 14
            Layout.rightMargin: 14
            // Takes the slack so the bar has no hole in it, and says what has
            // focus without making every task button carry its own title.
            text: tasks.activeTask.valid
                ? "▸ " + tasks.data(tasks.activeTask, Qt.DisplayRole) : ""
            elide: Text.ElideRight
            // Centred in the slack, which is polybar's modules-center: the two
            // dense groups sit at the ends and the focused window names itself
            // between them, so the middle is never a hole.
            horizontalAlignment: Text.AlignHCenter
            color: "@FAINT@"
            font.family: "@MONO@"
            font.pixelSize: 11
            font.letterSpacing: 0.5
            verticalAlignment: Text.AlignVCenter
            height: parent.height
            renderType: Text.NativeRendering
        }

        /* ---- telemetry ---------------------------------------------------- */

        Row {
            id: meters
            Layout.fillHeight: true
            spacing: 0

            Row {
                height: meters.height
                spacing: 6
                leftPadding: 4
                rightPadding: 8
                Label  { anchors.verticalCenter: parent.verticalCenter; text: "CPU" }
                Spark  {
                    anchors.verticalCenter: parent.verticalCenter
                    samples: hud.cpuHist
                    tint: hud.ramp(cpu.value / 100)
                }
                Value  {
                    anchors.verticalCenter: parent.verticalCenter
                    text: hud.pct(cpu)
                    color: hud.ramp(cpu.value / 100)
                }
            }

            Nick { height: meters.height; stroke: "@HAIR2@" }

            Row {
                height: meters.height
                spacing: 6
                leftPadding: 8
                rightPadding: 8
                Label { anchors.verticalCenter: parent.verticalCenter; text: "MEM" }
                Spark {
                    anchors.verticalCenter: parent.verticalCenter
                    samples: hud.memHist
                    tint: hud.ramp(mem.value / 100)
                }
                Value {
                    anchors.verticalCenter: parent.verticalCenter
                    text: hud.pct(mem)
                    color: hud.ramp(mem.value / 100)
                }
            }

            Nick { height: meters.height; stroke: "@HAIR2@"; visible: tmpCell.visible }

            Row {
                id: tmpCell
                height: meters.height
                spacing: 6
                leftPadding: 8
                rightPadding: 8
                // Hidden outright on a machine with no readable core temp,
                // rather than parked on a permanent "--".
                visible: tmp.status === Sensors.Sensor.Ready
                Label { anchors.verticalCenter: parent.verticalCenter; text: "TMP" }
                Value {
                    anchors.verticalCenter: parent.verticalCenter
                    text: Math.round(tmp.value) + "°"
                    // Thresholds are absolute, not a fraction of anything:
                    // 70 is warm for a laptop core and 85 is throttling.
                    color: tmp.value > 85 ? "@MAGENTA@" : tmp.value > 70 ? "@AMBER@" : "@TEXT@"
                }
            }

            Nick { height: meters.height; stroke: "@HAIR2@" }

            Row {
                height: meters.height
                spacing: 6
                leftPadding: 8
                rightPadding: 8
                Label { anchors.verticalCenter: parent.verticalCenter; text: "NET" }
                // A fixed column per direction, right-aligned, so the two
                // figures hold their place as they grow and shrink without
                // spaces opening up inside the reading.
                Value {
                    anchors.verticalCenter: parent.verticalCenter
                    text: "▾" + hud.rate(dn)
                    color: "@DIM@"
                    // Down hugs the label, up hugs the divider, so the
                    // slack the fixed columns reserve falls BETWEEN the two
                    // readings — where it separates them — instead of
                    // opening a gap after the label.
                    width: 34
                    horizontalAlignment: Text.AlignLeft
                }
                Value {
                    anchors.verticalCenter: parent.verticalCenter
                    text: "▴" + hud.rate(up)
                    color: "@DIM@"
                    width: 34
                    horizontalAlignment: Text.AlignRight
                }
            }

            Nick { height: meters.height; stroke: "@HAIR2@"; visible: dskCell.visible }

            Row {
                id: dskCell
                height: meters.height
                spacing: 6
                leftPadding: 8
                rightPadding: 8
                visible: dsk.status === Sensors.Sensor.Ready
                Label { anchors.verticalCenter: parent.verticalCenter; text: "DSK" }
                Value {
                    anchors.verticalCenter: parent.verticalCenter
                    text: hud.pct(dsk)
                    color: hud.ramp(dsk.value / 100)
                }
            }

            Nick { height: meters.height; stroke: "@HAIR2@"; visible: uptCell.visible }

            Row {
                id: uptCell
                height: meters.height
                spacing: 6
                leftPadding: 8
                rightPadding: 6
                visible: hud.uptime !== ""
                Label { anchors.verticalCenter: parent.verticalCenter; text: "UPT" }
                Value {
                    anchors.verticalCenter: parent.verticalCenter
                    text: hud.uptime
                    color: "@DIM@"
                }
            }
        }

        Nick { Layout.fillHeight: true; stroke: "@HAIR2@" }

        /* ---- clock --------------------------------------------------------- */

        Row {
            id: clock
            Layout.fillHeight: true
            spacing: 6
            leftPadding: 6
            rightPadding: 8

            Value {
                anchors.verticalCenter: parent.verticalCenter
                text: Qt.formatDateTime(hud.now, "ddd dd MMM").toUpperCase()
                color: "@DIM@"
                font.pixelSize: 9
                font.letterSpacing: 0.5
            }
            Value {
                anchors.verticalCenter: parent.verticalCenter
                text: Qt.formatTime(hud.now, "HH:mm")
                color: "@CYAN@"
                font.bold: true
            }
            // Seconds kept small and dim: they are movement, not
            // information, and at full weight they pull the eye all day.
            Value {
                anchors.verticalCenter: parent.verticalCenter
                text: Qt.formatTime(hud.now, "ss")
                color: "@FAINT@"
                font.pixelSize: 9
            }
        }
    }
}
