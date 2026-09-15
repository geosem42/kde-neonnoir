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

    (root / 'metadata.json').write_text(json.dumps({
        'KPackageStructure': 'Plasma/Applet',
        'KPlugin': {
            'Id': PLASMOID_ID,
            'Name': f'{THEME_NAME} System',
            'Description': 'CPU, memory and network in the Neon Noir language',
            'Icon': 'utilities-system-monitor',
            'Category': 'System Information',
            'Authors': [{'Name': 'George', 'Email': 'geosem042@gmail.com'}],
            'License': 'GPL-3.0-or-later',
            'Version': '1.0',
            'EnabledByDefault': True,
            'FormFactors': ['desktop'],
        },
        'X-Plasma-API-Minimum-Version': '6.0',
    }, indent=4) + '\n')
    out.append(f'plasmoids/{PLASMOID_ID}/  (metadata.json, main.qml, SystemCard.qml)')
    return out
