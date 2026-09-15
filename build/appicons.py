"""Line-art application icons for the panel.

The design draws every app in the task bar as a monochrome outline glyph on a
24px grid — a folder for Dolphin, a framed `>_` for Konsole, a globe for the
browser — not as the vendor's colour logo. Breeze's app icons are full-colour,
so leaving them alone is what makes the task bar read as stock Plasma no matter
how the panel behind it is painted.

Only the apps that actually appear in a panel are overridden; anything not
listed here still falls through to breeze-dark via `Inherits`.

Stroke colour is `text.dim`, measured off the artboard (the artboard's glyphs
sample at 147,154,161 against the panel fill, which is #A1A9B0 once the
antialiasing against a dark ground is accounted for).
"""

VIEWBOX = 24
STROKE = 1.7

# name -> SVG body drawn on a 24x24 grid. Stroke colour and width come from the
# parent <g>, so a glyph never repeats them.
GLYPHS = {
    # Dolphin: folder with a raised left tab.
    'folder': '<path d="M3 7.6a1.9 1.9 0 0 1 1.9-1.9h3.4l1.9 2.3h9.9A1.9 1.9 0 0 1 22 9.9'
              'v7.5a1.9 1.9 0 0 1-1.9 1.9H4.9A1.9 1.9 0 0 1 3 17.4z"/>',

    # Konsole: framed prompt.
    'terminal': '<rect x="2.6" y="4.6" width="18.8" height="14.8" rx="2.2"/>'
                '<path d="M7 10l2.6 2.2L7 14.4"/><path d="M12.4 15h4.4"/>',

    # Kate: screen with a prompt and a base rule.
    'editor': '<rect x="3.6" y="4.8" width="16.8" height="11.4" rx="1.6"/>'
              '<path d="M8.3 9.3l2.1 1.8-2.1 1.8"/>'
              '<path d="M3 19.2h18"/>',

    # Browser: globe.
    'globe': '<circle cx="12" cy="12" r="9"/>'
             '<ellipse cx="12" cy="12" rx="3.7" ry="9"/>'
             '<path d="M3.3 9.2h17.4M3.3 14.8h17.4"/>',

    # VS Code and friends: angle brackets.
    'code': '<path d="M8.8 8.2L4.4 12l4.4 3.8"/><path d="M15.2 8.2L19.6 12l-4.4 3.8"/>'
            '<path d="M13.4 5.6l-2.8 12.8"/>',

    # Settings: three sliders.
    'sliders': '<path d="M4 7.5h10M18.5 7.5H20"/><path d="M4 16.5h4.5M13 16.5h7"/>'
               '<circle cx="16.2" cy="7.5" r="2.3"/><circle cx="10.7" cy="16.5" r="2.3"/>',

    # Discover: download into a tray.
    'download': '<path d="M12 4v9.4"/><path d="M8.2 10l3.8 3.8L15.8 10"/>'
                '<path d="M4.5 16.2v2.1a1.7 1.7 0 0 0 1.7 1.7h11.6a1.7 1.7 0 0 0 1.7-1.7v-2.1"/>',

    # Image viewer.
    'image': '<rect x="3" y="5" width="18" height="14" rx="2"/>'
             '<circle cx="8.4" cy="10" r="1.6"/>'
             '<path d="M3.6 17.4l4.9-4.6 3.5 3.2 3.1-2.9 4.3 4"/>',

    # Document viewer.
    'document': '<path d="M6 3.2h7.6L19 8.6v12.2H6z"/><path d="M13.4 3.2v5.6H19"/>'
                '<path d="M9 13h7M9 16.6h7"/>',

    # Screenshot tool.
    'camera': '<rect x="2.8" y="7" width="18.4" height="13" rx="2.2"/>'
              '<path d="M8.6 7l1.5-2.6h3.8L15.4 7"/><circle cx="12" cy="13.4" r="3.4"/>',

    # Archiver.
    'archive': '<path d="M3 7.4h18v11.2a1.8 1.8 0 0 1-1.8 1.8H4.8A1.8 1.8 0 0 1 3 18.6z"/>'
               '<rect x="2.4" y="3.6" width="19.2" height="3.8" rx="1.2"/>'
               '<path d="M10 11.6h4"/>',

    # Calculator.
    'calculator': '<rect x="4.6" y="2.8" width="14.8" height="18.4" rx="2"/>'
                  '<rect x="7.6" y="5.8" width="8.8" height="3.4" rx="1"/>'
                  '<path d="M8.4 13.2h.01M12 13.2h.01M15.6 13.2h.01'
                  'M8.4 17h.01M12 17h.01M15.6 17h.01"/>',

    # Mail.
    'mail': '<rect x="2.6" y="5" width="18.8" height="14" rx="2.2"/>'
            '<path d="M3.4 7.2L12 13.2l8.6-6"/>',

    # Generic fallback: the brand hexagon, so an unknown app still belongs here.
    'hexagon': '<path d="M12 2.9l7.9 4.55v9.1L12 21.1l-7.9-4.55v-9.1z"/>',
}

# Icon name -> glyph. Both spellings are listed for every app: KDE's own
# .desktop files are inconsistent about it — dolphin asks for
# `org.kde.dolphin`, kate for plain `kate`, konsole for `utilities-terminal` —
# so guessing one form leaves half the panel on Breeze's colour logos.
MAP = {
    'org.kde.dolphin': 'folder',          'dolphin': 'folder',
    'system-file-manager': 'folder',
    'org.kde.konsole': 'terminal',        'konsole': 'terminal',
    'utilities-terminal': 'terminal',     'terminal': 'terminal',
    'yakuake': 'terminal',                'org.kde.yakuake': 'terminal',
    'org.kde.kate': 'editor',             'kate': 'editor',
    'org.kde.kwrite': 'editor',           'kwrite': 'editor',
    'accessories-text-editor': 'editor',  'text-editor': 'editor',
    'firefox': 'globe',                   'firefox_firefox': 'globe',
    'firefox-esr': 'globe',               'web-browser': 'globe',
    'chromium': 'globe',                  'chromium-browser': 'globe',
    'google-chrome': 'globe',             'internet-web-browser': 'globe',
    'code': 'code',                       'vscode': 'code',
    'visual-studio-code': 'code',         'code-oss': 'code',
    'systemsettings': 'sliders',          'preferences-system': 'sliders',
    'org.kde.discover': 'download',       'plasmadiscover': 'download',
    'org.kde.gwenview': 'image',          'gwenview': 'image',
    'multimedia-photo-viewer': 'image',
    'org.kde.okular': 'document',         'okular': 'document',
    'org.kde.spectacle': 'camera',        'spectacle': 'camera',
    'accessories-screenshot': 'camera',
    'org.kde.ark': 'archive',             'ark': 'archive',
    'utilities-file-archiver': 'archive',
    'org.kde.kcalc': 'calculator',        'kcalc': 'calculator',
    'accessories-calculator': 'calculator',
    'kmail': 'mail',                      'internet-mail': 'mail',
    'application-x-executable': 'hexagon',
    'applications-other': 'hexagon',
}


def svgs(stroke_hex):
    """Return {icon-name: svg-text} for every mapped application icon."""
    out = {}
    for name, glyph in MAP.items():
        body = GLYPHS[glyph]
        out[name] = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEWBOX}" '
            f'height="{VIEWBOX}" viewBox="0 0 {VIEWBOX} {VIEWBOX}">'
            f'<g fill="none" stroke="{stroke_hex}" stroke-width="{STROKE}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n'
        )
    return out
