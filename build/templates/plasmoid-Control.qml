/*
    Neon Noir options. A cog in the panel; the card is the popup.

    State lives in ~/.config/neonnoirrc, not in the applet's own configuration,
    because install.sh writes it too and two sources of truth for "which variant
    is applied" is one too many. It is read back through kreadconfig6 rather
    than cached, so the popup is right even when the last change came from the
    installer or the command line.

    The apply script is launched DETACHED. Switching the taskbar variant rebuilds
    the panel, which destroys this applet — and with it the DataSource that
    started the script. setsid puts the script in its own session so it survives
    the widget that asked for it.
*/
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami
import org.kde.plasma.plasma5support as P5Support

PlasmoidItem {
    id: root

    readonly property string applyScript: "@APPLY@"

    property string panelVariant: "classic"
    property string windowsProfile: "classic"

    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: compactRepresentation

    toolTipMainText: "Neon Noir"
    toolTipSubText: "Theme options"

    P5Support.DataSource {
        id: shell
        engine: "executable"
        connectedSources: []

        onNewData: (source, data) => {
            disconnectSource(source)
            const out = (data["stdout"] || "").trim()
            if (source.indexOf("--key Variant") !== -1) {
                root.panelVariant = out || "classic"
            } else if (source.indexOf("--key Profile") !== -1) {
                root.windowsProfile = out || "classic"
            }
        }

        function exec(cmd) {
            // Reconnecting a source that is already connected is a no-op, so a
            // command that ran once would never run again.
            disconnectSource(cmd)
            connectSource(cmd)
        }
    }

    function refresh() {
        shell.exec("kreadconfig6 --file neonnoirrc --group Panel --key Variant")
        shell.exec("kreadconfig6 --file neonnoirrc --group Windows --key Profile")
    }

    function apply(axis, variant) {
        // Quoted: applyScript carries the XDG lookup unexpanded, and $HOME may
        // hold a space.
        shell.exec("setsid \"" + applyScript + "\" " + axis + " " + variant
                   + " >/dev/null 2>&1 &")
        // Optimistic, because the panel rebuild may take this applet with it
        // before any reply arrives.
        if (axis === "panel") {
            root.panelVariant = variant
        } else {
            root.windowsProfile = variant
        }
    }

    Component.onCompleted: refresh()

    // root.expanded, not the injected parameter: injecting a signal parameter
    // into a handler is deprecated in Qt 6 and warns on every load.
    onExpandedChanged: {
        if (root.expanded) {
            refresh()
        }
    }

    compactRepresentation: MouseArea {
        id: compact

        Layout.minimumWidth: Kirigami.Units.iconSizes.medium
        Layout.minimumHeight: Kirigami.Units.iconSizes.medium
        Layout.maximumWidth: Layout.minimumWidth
        Layout.maximumHeight: Layout.minimumHeight
        Layout.preferredWidth: Layout.minimumWidth
        Layout.preferredHeight: Layout.minimumHeight

        hoverEnabled: true
        onClicked: root.expanded = !root.expanded

        Kirigami.Icon {
            anchors.fill: parent
            active: compact.containsMouse
            source: "configure"
        }
    }

    fullRepresentation: ControlCard {
        Layout.minimumWidth: 300
        Layout.preferredWidth: 320
        Layout.minimumHeight: implicitHeight
        Layout.preferredHeight: implicitHeight

        panelVariant: root.panelVariant
        windowsProfile: root.windowsProfile

        onChoose: (axis, variant) => root.apply(axis, variant)
    }
}
