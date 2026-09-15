/*
    A hairline rule for the panel.

    Plasma ships no separator applet — marginsseparator only adds space, and
    only in edit mode — but the design puts a rule after the launcher and
    before the clock.

    The Layout hints live on the PlasmoidItem itself and the rule is a direct
    child of it. Putting them on a `fullRepresentation` component instead makes
    the shell fall back to the compact representation, which in a panel is the
    applet's icon: a stray page glyph where the rule should be.
*/
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore

PlasmoidItem {
    id: root

    readonly property bool isVertical: Plasmoid.formFactor === PlasmaCore.Types.Vertical

    // The gutter the rule sits in, measured off the artboard.
    readonly property int gutter: 18

    Layout.minimumWidth:    isVertical ? 1 : gutter
    Layout.preferredWidth:  Layout.minimumWidth
    Layout.maximumWidth:    Layout.minimumWidth
    Layout.minimumHeight:   isVertical ? gutter : 1
    Layout.preferredHeight: Layout.minimumHeight
    Layout.maximumHeight:   isVertical ? Layout.minimumHeight : -1
    Layout.fillHeight:      !isVertical
    Layout.fillWidth:       isVertical

    Plasmoid.backgroundHints: PlasmaCore.Types.NoBackground
    preferredRepresentation: fullRepresentation

    Rectangle {
        anchors.centerIn: parent
        // 44% of the panel, matching the artboard's short rule.
        width:  root.isVertical ? Math.round(parent.width * 0.44) : 1
        height: root.isVertical ? 1 : Math.round(parent.height * 0.44)
        color: "#454F58"
    }
}
