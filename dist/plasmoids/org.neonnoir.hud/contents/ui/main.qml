/*
    Wrapper. No background of its own: the bar is one continuous surface and the
    HUD paints its own segments onto it, so a Plasma applet frame here would
    draw a button around the whole row.

    The Layout hints sit on the PlasmoidItem and the HUD is a direct child of
    it. Declared inside a `fullRepresentation` component instead, the shell
    falls back to the COMPACT representation — which in a panel is the applet's
    own icon, a lone system-monitor glyph where the bar should be. The
    separator applet carries the same note for the same reason.
*/
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore

PlasmoidItem {
    id: root

    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: fullRepresentation

    Layout.fillWidth: true
    Layout.fillHeight: true
    Layout.minimumWidth: 360

    Hud {
        anchors.fill: parent
        // Passed in rather than read inside: screenGeometry and the applet
        // configuration live on the PlasmoidItem, and the HUD is a plain Item
        // so it can be rendered outside a running shell.
        screenGeo: root.screenGeometry
        launchers: Plasmoid.configuration.launchers
        onLaunchersWritten: (list) => Plasmoid.configuration.launchers = list
    }
}
