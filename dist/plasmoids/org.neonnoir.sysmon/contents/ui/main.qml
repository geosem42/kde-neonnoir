/*
    Neon Noir system widget. The card draws its own background, so the stock
    Plasma widget frame is switched off.
*/
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore

PlasmoidItem {
    id: root

    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: fullRepresentation

    fullRepresentation: SystemCard {
        Layout.minimumWidth: 240
        Layout.minimumHeight: implicitHeight
        Layout.preferredWidth: 300
        Layout.preferredHeight: implicitHeight
    }
}
