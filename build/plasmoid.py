"""The Neon Noir system-monitor widget.

A Plasma 6 applet (KPackageStructure Plasma/Applet, X-Plasma-API-Minimum-Version
6.0). The visible half lives in SystemCard.qml with no dependency on the
Plasmoid API, so it can be rendered and eyeballed outside a running shell;
main.qml is the wrapper the shell actually loads.

Readings come from org.kde.ksysguard.sensors — the same source the stock System
Monitor widgets use. The sensor ids were read off those widgets rather than
guessed: cpu/all/usage, memory/physical/{used,total}, network/all/download.
"""
import json

MAIN_QML = '''/*
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
'''


def _metadata(pid, name, desc, icon, category, form_factors):
    return json.dumps({
        'KPackageStructure': 'Plasma/Applet',
        'KPlugin': {
            'Id': pid,
            'Name': name,
            'Description': desc,
            'Icon': icon,
            'Category': category,
            'Authors': [{'Name': 'George', 'Email': 'geosem042@gmail.com'}],
            'License': 'GPL-3.0-or-later',
            'Version': '1.0',
            'EnabledByDefault': True,
            'FormFactors': form_factors,
        },
        'X-Plasma-API-Minimum-Version': '6.0',
    }, indent=4) + '\n'


def build_separator(T, DIST, THEME_NAME, SEPARATOR_ID, template_dir):
    root = DIST / 'plasmoids' / SEPARATOR_ID
    ui = root / 'contents' / 'ui'
    ui.mkdir(parents=True, exist_ok=True)
    qml = (template_dir / 'plasmoid-Separator.qml').read_text()
    (ui / 'main.qml').write_text(qml.replace('@RULE@', T['border.float']))
    (root / 'metadata.json').write_text(_metadata(
        SEPARATOR_ID, f'{THEME_NAME} Separator',
        'A hairline rule between panel sections', 'draw-line',
        'Utilities', ['desktop']))
    return [f'plasmoids/{SEPARATOR_ID}/  (metadata.json, main.qml)']


def build_control(T, DIST, THEME_NAME, CONTROL_ID, template_dir, apply_path):
    """The options widget: a cog in the panel over a popup of theme switches."""
    root = DIST / 'plasmoids' / CONTROL_ID
    ui = root / 'contents' / 'ui'
    ui.mkdir(parents=True, exist_ok=True)

    subs = {
        '@CARD@': T['surface.raised'], '@HAIR@': T['border.hairline'],
        '@VOID@': T['surface.view'],   '@HOVER@': T['surface.hover'],
        '@GHOST@': T['accent.cyan.ghost'], '@CYAN@': T['accent.cyan'],
        '@TEXT@': T['text.normal'],    '@DIM@': T['text.dim'],
        '@FAINT@': T['text.faint'],    '@FONT@': 'IBM Plex Sans',
    }
    card = (template_dir / 'plasmoid-ControlCard.qml').read_text()
    for k, v in subs.items():
        card = card.replace(k, v)
    (ui / 'ControlCard.qml').write_text(card)

    main = (template_dir / 'plasmoid-Control.qml').read_text()
    (ui / 'main.qml').write_text(main.replace('@APPLY@', apply_path))

    (root / 'metadata.json').write_text(_metadata(
        CONTROL_ID, f'{THEME_NAME} Options',
        'Switch between the theme\'s window and taskbar variants',
        'configure', 'Utilities', ['desktop']))
    return [f'plasmoids/{CONTROL_ID}/  (metadata.json, main.qml, ControlCard.qml)']


def build(T, DIST, THEME_ID, THEME_NAME, PLASMOID_ID, template_dir):
    out = []
    root = DIST / 'plasmoids' / PLASMOID_ID
    ui = root / 'contents' / 'ui'
    ui.mkdir(parents=True, exist_ok=True)

    subs = {
        '@CARD@': T['surface.raised'], '@HAIR@': T['border.hairline'],
        '@TRACK@': T['surface.alt'],   '@TEXT@': T['text.normal'],
        '@DIM@': T['text.dim'],        '@CYAN@': T['accent.cyan'],
        '@AMBER@': T['status.neutral'],
        '@FONT@': 'IBM Plex Sans',     '@MONO@': 'JetBrains Mono',
    }
    card = (template_dir / 'plasmoid-SystemCard.qml').read_text()
    for k, v in subs.items():
        card = card.replace(k, v)
    (ui / 'SystemCard.qml').write_text(card)
    (ui / 'main.qml').write_text(MAIN_QML)

    (root / 'metadata.json').write_text(_metadata(
        PLASMOID_ID, f'{THEME_NAME} System',
        'CPU, memory and network in the Neon Noir language',
        'utilities-system-monitor', 'System Information', ['desktop']))
    out.append(f'plasmoids/{PLASMOID_ID}/  (metadata.json, main.qml, SystemCard.qml)')
    return out


def build_hud(T, DIST, THEME_NAME, HUD_ID, template_dir):
    """The Futuristic bar's entire contents as one widget.

    One widget rather than a handful, because the look depends on every module
    sharing a grid, a typeface and a slant — which cannot happen while each one
    is a separate applet with its own background and its own metrics.
    """
    root = DIST / 'plasmoids' / HUD_ID
    ui = root / 'contents' / 'ui'
    ui.mkdir(parents=True, exist_ok=True)

    subs = {
        '@CYAN@': T['accent.cyan'],   '@MAGENTA@': T['accent.magenta'],
        '@AMBER@': T['status.neutral'],
        '@TEXT@': T['text.normal'],   '@DIM@': T['text.dim'],
        '@FAINT@': T['text.faint'],   '@HAIR@': T['border.hairline'],
        # The slanted dividers read as neon rather than as furniture, so they
        # take a cyan rather than a grey.
        '@HAIR2@': T['accent.cyan.deep'],
        # NOT surface.window: that is exactly the panel background, so the
        # segments and their wedges were painting themselves invisible.
        # A step darker reads as a slot cut into the bar.
        '@SEG@': T['surface.sheet'],
        '@MONO@': 'JetBrains Mono',
    }
    # The pinned list has to live in the applet's own configuration: it is the
    # only per-widget store that survives a shell restart, and the panel script
    # seeds it through the same key at install time.
    cfg = root / 'contents' / 'config'
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / 'main.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<kcfg xmlns="http://www.kde.org/standards/kcfg/1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.kde.org/standards/kcfg/1.0
                          http://www.kde.org/standards/kcfg/1.0/kcfg.xsd">
  <kcfgfile name=""/>
  <group name="General">
    <entry name="launchers" type="StringList">
      <default></default>
    </entry>
  </group>
</kcfg>
''')

    body = (template_dir / 'plasmoid-Hud.qml').read_text()
    for k, v in subs.items():
        body = body.replace(k, v)
    (ui / 'Hud.qml').write_text(body)

    (ui / 'main.qml').write_text('''/*
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
''')
    (root / 'metadata.json').write_text(_metadata(
        HUD_ID, f'{THEME_NAME} HUD',
        'Workspaces, windows, telemetry and the clock as one status bar',
        'utilities-system-monitor', 'System Information', ['desktop']))
    return [f'plasmoids/{HUD_ID}/  (metadata.json, main.qml, Hud.qml)']
