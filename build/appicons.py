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

    # Kate: a page being written on. The artboard draws it as a screen with a
    # prompt inside, but at panel size that is the terminal glyph with a base
    # rule — the two were indistinguishable. The pencil is what separates an
    # editor from a terminal, and the ruled page from a plain document.
    'editor': '<path d="M16.4 3.4H6.6a1.9 1.9 0 0 0-1.9 1.9v13.4a1.9 1.9 0 0 0 1.9 1.9'
              'h9.2a1.9 1.9 0 0 0 1.9-1.9v-6.1"/>'
              '<path d="M8.4 9h4M8.4 12.6h3M8.4 16.2h4.6"/>'
              '<path d="M19.1 3.6a1.9 1.9 0 0 1 2.7 2.7l-6.2 6.2-3.5.8.8-3.5z"/>',

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

    # ── menu categories ───────────────────────────────────────────────────────

    'grid4': '<rect x="3.4" y="3.4" width="7.2" height="7.2" rx="1.6"/>'
             '<rect x="13.4" y="3.4" width="7.2" height="7.2" rx="1.6"/>'
             '<rect x="3.4" y="13.4" width="7.2" height="7.2" rx="1.6"/>'
             '<rect x="13.4" y="13.4" width="7.2" height="7.2" rx="1.6"/>',

    'wrench': '<path d="M15.6 3.5a4.8 4.8 0 0 0-5.8 6.2l-5.9 5.9a2 2 0 0 0 2.8 2.8l5.9-5.9'
              'a4.8 4.8 0 0 0 6.2-5.8l-3 3-2.5-.7-.7-2.5z"/>',

    'toolbox': '<rect x="2.6" y="8.4" width="18.8" height="11.2" rx="2"/>'
               '<path d="M8.4 8.4V6.6a1.8 1.8 0 0 1 1.8-1.8h3.6a1.8 1.8 0 0 1 1.8 1.8v1.8"/>'
               '<path d="M2.6 13h18.8"/><path d="M10.4 11.6h3.2"/>',

    'paperclip': '<path d="M18.6 11.2 12 17.8a4.2 4.2 0 0 1-5.9-5.9l7.4-7.4a2.8 2.8 0 0 1 4 4'
                 'l-7.4 7.4a1.4 1.4 0 0 1-2-2l6.6-6.6"/>',

    'cap': '<path d="M12 4.2 22 9l-10 4.8L2 9z"/>'
           '<path d="M6 11.2v4.4c0 1.7 2.7 3 6 3s6-1.3 6-3v-4.4"/>',

    'bubble': '<path d="M20.4 14.2a2 2 0 0 1-2 2H7.6l-4 4V5.8a2 2 0 0 1 2-2h12.8'
              'a2 2 0 0 1 2 2z"/>',

    'maths': '<path d="M4.4 7.2h5M6.9 4.7v5"/><path d="M14.6 7.2h5"/>'
             '<path d="M4.9 14.9l4 4M8.9 14.9l-4 4"/>'
             '<path d="M14.6 14.2h5M14.6 17.8h5"/>',

    'atom': '<circle cx="12" cy="12" r="2"/>'
            '<ellipse cx="12" cy="12" rx="9.2" ry="4"/>'
            '<ellipse cx="12" cy="12" rx="9.2" ry="4" transform="rotate(60 12 12)"/>'
            '<ellipse cx="12" cy="12" rx="9.2" ry="4" transform="rotate(120 12 12)"/>',

    'dividers': '<circle cx="12" cy="4.6" r="1.8"/>'
                '<path d="M11.2 6.3 6.4 20.4M12.8 6.3 17.6 20.4"/>'
                '<path d="M9.4 14.6h5.2"/>',

    'gamepad': '<path d="M8.4 9.4h7.2a5.2 5.2 0 0 1 5.1 6.2l-.5 2.4a2.3 2.3 0 0 1-4 1.1'
               'L14.4 17H9.6l-2.2 2.1a2.3 2.3 0 0 1-4-1.1l-.5-2.4a5.2 5.2 0 0 1 5.1-6.2z"/>'
               '<path d="M7.4 12.4v2.2M6.3 13.5h2.2"/>'
               '<circle cx="16.2" cy="12.8" r=".9"/><circle cx="18" cy="15" r=".9"/>',

    'palette': '<path d="M12 3.2a8.8 8.8 0 0 0 0 17.6c1.1 0 1.9-.8 1.9-1.8 0-.5-.2-.9-.5-1.2'
               '-.3-.3-.5-.7-.5-1.2 0-1 .9-1.8 1.9-1.8h2.2a4 4 0 0 0 4-4c0-4.2-4-7.6-9-7.6z"/>'
               '<circle cx="7.4" cy="11.4" r="1.1"/><circle cx="10.6" cy="7.6" r="1.1"/>'
               '<circle cx="15.4" cy="8.4" r="1.1"/>',

    'play': '<rect x="2.8" y="4.8" width="18.4" height="14.4" rx="2.2"/>'
            '<path d="M10 9.6l5 2.8-5 2.8z"/>',

    'nodes': '<circle cx="12" cy="5" r="2.4"/><circle cx="5" cy="18" r="2.4"/>'
             '<circle cx="19" cy="18" r="2.4"/>'
             '<path d="M10.8 7.2 6.2 15.8M13.2 7.2l4.6 8.6M7.4 18h9.2"/>',

    'briefcase': '<rect x="2.6" y="7.2" width="18.8" height="12.4" rx="2.2"/>'
                 '<path d="M8.6 7.2V5.6a1.6 1.6 0 0 1 1.6-1.6h3.6a1.6 1.6 0 0 1 1.6 1.6v1.6"/>'
                 '<path d="M2.6 12.4h18.8"/>',

    'flask': '<path d="M9.6 3.4v5.4l-5.2 9a2 2 0 0 0 1.7 3h11.8a2 2 0 0 0 1.7-3l-5.2-9V3.4"/>'
             '<path d="M8.4 3.4h7.2"/><path d="M7.6 14.6h8.8"/>',

    'chip': '<rect x="6.4" y="6.4" width="11.2" height="11.2" rx="2"/>'
            '<rect x="9.8" y="9.8" width="4.4" height="4.4" rx="1"/>'
            '<path d="M9.6 3.2v3.2M14.4 3.2v3.2M9.6 17.6v3.2M14.4 17.6v3.2'
            'M3.2 9.6h3.2M3.2 14.4h3.2M17.6 9.6h3.2M17.6 14.4h3.2"/>',

    'bookmark': '<path d="M6.4 3.6h11.2a1.2 1.2 0 0 1 1.2 1.2v15.6L12 16.4l-6.8 4V4.8'
                'a1.2 1.2 0 0 1 1.2-1.2z"/>',

    # ── places, and the tray applets that ship a filled Breeze glyph ──────────

    'house': '<path d="M3.4 10.2 12 3.4l8.6 6.8v9a1.8 1.8 0 0 1-1.8 1.8H5.2'
             'a1.8 1.8 0 0 1-1.8-1.8z"/>'
             '<path d="M9.4 21v-7h5.2v7"/>',

    'monitor': '<rect x="2.6" y="4.2" width="18.8" height="12.6" rx="2"/>'
               '<path d="M8 20.4h8M12 16.8v3.6"/>',

    'trash': '<path d="M4.2 6.8h15.6"/>'
             '<path d="M6.4 6.8l.9 12.2a1.8 1.8 0 0 0 1.8 1.6h5.8a1.8 1.8 0 0 0 1.8-1.6'
             'l.9-12.2"/>'
             '<path d="M9.4 6.8V4.8a1.4 1.4 0 0 1 1.4-1.4h2.4a1.4 1.4 0 0 1 1.4 1.4v2"/>'
             '<path d="M10.4 10.4v6.6M13.6 10.4v6.6"/>',

    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 6.6V12l3.6 2.2"/>',

    'drive': '<rect x="2.6" y="4.4" width="18.8" height="15.2" rx="2.2"/>'
             '<path d="M2.6 14h18.8"/><circle cx="17.4" cy="16.8" r="1"/>'
             '<path d="M6.2 8.6h6"/>',

    'clipboard': '<path d="M9 4.2H7a1.8 1.8 0 0 0-1.8 1.8v13a1.8 1.8 0 0 0 1.8 1.8h10'
                 'a1.8 1.8 0 0 0 1.8-1.8V6A1.8 1.8 0 0 0 17 4.2h-2"/>'
                 '<rect x="9" y="2.6" width="6" height="3.6" rx="1.2"/>'
                 '<path d="M8.6 11.6h6.8M8.6 15.2h4.6"/>',

    'lock': '<rect x="4" y="10" width="16" height="10.6" rx="2.2"/>'
            '<path d="M7.8 10V7.4a4.2 4.2 0 0 1 8.4 0V10"/>'
            '<path d="M12 14v2.6"/>',

    'moon': '<path d="M20.4 14.4A8.8 8.8 0 0 1 9.6 3.6a8.8 8.8 0 1 0 10.8 10.8z"/>',

    'usb': '<rect x="8.2" y="8.6" width="7.6" height="12.2" rx="1.6"/>'
           '<path d="M10 8.6V4.4a1.4 1.4 0 0 1 1.4-1.4h1.2a1.4 1.4 0 0 1 1.4 1.4v4.2"/>'
           '<path d="M10.4 12.4h3.2M10.4 15.4h3.2"/>',

    'phone': '<rect x="6.4" y="2.6" width="11.2" height="18.8" rx="2.4"/>'
             '<path d="M10.6 5.4h2.8"/><path d="M12 18.2h.01"/>',

    'keyboard': '<rect x="2.2" y="6" width="19.6" height="12" rx="2"/>'
                '<path d="M6 9.4h.01M9.4 9.4h.01M12.8 9.4h.01M16.2 9.4h.01'
                'M6 12.4h.01M9.4 12.4h.01M12.8 12.4h.01M16.2 12.4h.01'
                'M19 9.4h.01M19 12.4h.01"/>'
                '<path d="M8 15.2h8"/>',

    # Two screens, so it is not the single monitor the Desktop place uses.
    # They sit clear of each other rather than overlapping: an overlap needs a
    # knockout filled with the surface colour, and these glyphs carry no fill
    # so they read correctly on any ground.
    'displays': '<rect x="2.2" y="4.2" width="12" height="9" rx="1.8"/>'
                '<path d="M5.6 16.6h5.2M8.2 13.2v3.4"/>'
                '<rect x="14.2" y="11" width="7.6" height="7.4" rx="1.6"/>'
                '<path d="M16.2 20.8h3.6M18 18.4v2.4"/>',

    # ── file types ────────────────────────────────────────────────────────────

    'note': '<path d="M9.4 18V5.6l9.2-1.8v12.4"/>'
            '<ellipse cx="6.6" cy="18" rx="2.8" ry="2.3"/>'
            '<ellipse cx="15.8" cy="16.2" rx="2.8" ry="2.3"/>',

    # Perforations down both edges, not full-height rules: with rules it read as
    # a 3x2 grid, indistinguishable from the spreadsheet glyph.
    'film': '<rect x="2.6" y="4.6" width="18.8" height="14.8" rx="2.2"/>'
            '<path d="M2.6 8.4h3.6M2.6 12h3.6M2.6 15.6h3.6"/>'
            '<path d="M17.8 8.4h3.6M17.8 12h3.6M17.8 15.6h3.6"/>'
            '<path d="M6.2 4.6v14.8M17.8 4.6v14.8"/>',

    'book': '<path d="M3.4 5a1.6 1.6 0 0 1 1.6-1.6h5.4a1.6 1.6 0 0 1 1.6 1.6v14.8'
            'a1.6 1.6 0 0 0-1.6-1.6H3.4z"/>'
            '<path d="M20.6 5a1.6 1.6 0 0 0-1.6-1.6h-5.4A1.6 1.6 0 0 0 12 5v14.8'
            'a1.6 1.6 0 0 1 1.6-1.6h7z"/>',

    'typeface': '<path d="M5.6 3.4h8.4L19 8.4v12.2H5.6z"/>'
                '<path d="M13.8 3.4v5.2H19"/>'
                '<path d="M8.6 17.4l2.8-6.6 2.8 6.6M9.6 15.2h3.6"/>',

    'table': '<rect x="3" y="4.6" width="18" height="14.8" rx="2"/>'
             '<path d="M3 9.6h18M3 14.4h18M9.4 4.6v14.8"/>',

    'slide': '<rect x="2.6" y="4.6" width="18.8" height="12.4" rx="2"/>'
             '<path d="M6.6 8.8h6.8M6.6 12.6h10.8"/>'
             '<path d="M12 17v3.4M8.6 20.4h6.8"/>',

    'unknown': '<path d="M5.6 3.4h8.4L19 8.4v12.2H5.6z"/>'
               '<path d="M13.8 3.4v5.2H19"/>'
               '<path d="M9.6 12.4a2.4 2.4 0 0 1 4.7.8c0 1.6-2.3 2.4-2.3 2.4"/>'
               '<path d="M12 18.2h.01"/>',


    'question': '<circle cx="12" cy="12" r="9"/>'
                '<path d="M9.4 9.4a2.7 2.7 0 0 1 5.2.9c0 1.8-2.6 2.7-2.6 2.7"/>'
                '<path d="M12 17.2h.01"/>',
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


def _wrap(body, stroke_hex):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEWBOX}" '
        f'height="{VIEWBOX}" viewBox="0 0 {VIEWBOX} {VIEWBOX}">'
        f'<g fill="none" stroke="{stroke_hex}" stroke-width="{STROKE}" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n'
    )


def svgs(stroke_hex):
    """Return {icon-name: svg-text} for every mapped application icon."""
    return {name: _wrap(GLYPHS[glyph], stroke_hex) for name, glyph in MAP.items()}


# The application-menu categories down the launcher's left edge. These live in
# the `categories` context, which is separate from `apps` — the same theme has
# to ship both or the launcher list stays on Breeze while the task bar changes.
CATEGORIES = {
    'applications-all': 'grid4',
    'applications-accessories': 'paperclip',
    'applications-development': 'wrench',
    'applications-education': 'cap',
    'applications-education-language': 'bubble',
    'applications-education-mathematics': 'maths',
    'applications-education-science': 'atom',
    'applications-engineering': 'dividers',
    'applications-games': 'gamepad',
    'applications-graphics': 'palette',
    'applications-internet': 'globe',
    'applications-multimedia': 'play',
    'applications-network': 'nodes',
    'applications-office': 'briefcase',
    'applications-other': 'hexagon',
    'applications-science': 'flask',
    'applications-system': 'chip',
    'applications-utilities': 'toolbox',
    # Not an `applications-` name, but they sit in the same list.
    'bookmarks': 'bookmark',
    'favorites': 'bookmark',
    'help-browser': 'question',
    'help-contents': 'question',
    'help-about': 'question',
    'system-help': 'question',
}


def category_svgs(stroke_hex):
    """{icon-name: svg} for the launcher's category list.

    Every name is emitted twice, plain and `-symbolic`: the launcher asks for
    whichever the menu file names, and a miss falls back to Breeze.
    """
    out = {}
    for name, glyph in CATEGORIES.items():
        svg = _wrap(GLYPHS[glyph], stroke_hex)
        out[name] = svg
        out[name + '-symbolic'] = svg
    return out


# Sidebar places. Emitted only at the SMALL fixed sizes (see icons.py): Breeze
# itself ships monochrome place icons at 16/22/24 and coloured ones at 32 and
# up, and a file manager uses the small set in its sidebar and the large set in
# the file view. Following the same split is what lets the sidebar be outlines
# while folders in the view stay cyan and filled.
PLACES = {
    'user-home': 'house',            'folder-home': 'house',
    'user-desktop': 'monitor',       'folder-desktop': 'monitor',
    'desktop': 'monitor',
    'folder-documents': 'document',  'folder-text': 'document',
    'folder-downloads': 'download',  'folder-download': 'download',
    'folder-music': 'note',          'folder-sound': 'note',
    'folder-pictures': 'image',      'folder-images': 'image',
    'folder-videos': 'film',         'folder-video': 'film',
    'user-trash': 'trash',           'user-trash-full': 'trash',
    'trash-empty': 'trash',          'trash-full': 'trash',
    'network-workgroup': 'nodes',    'folder-network': 'nodes',
    'folder-remote': 'nodes',
    'document-open-recent': 'clock', 'folder-recent': 'clock',
    'folder-temp': 'clock',
    'folder-root': 'drive',          'drive-harddisk': 'drive',
    'folder-development': 'wrench',  'folder-script': 'wrench',
    'folder-html': 'globe',          'folder-cloud': 'globe',
    'folder-print': 'document',      'folder-publicshare': 'nodes',
    'folder-templates': 'slide',     'folder-games': 'gamepad',
    'folder-mail': 'mail',           'folder-favorites': 'bookmark',
    'favorites': 'bookmark',         'bookmarks': 'bookmark',
    'folder-important': 'bookmark',  'folder-locked': 'lock',
    'folder-encrypted': 'lock',      'folder-tar': 'archive',
    'folder-image-people': 'image',  'folder-camera': 'camera',
}

# Tray applets whose icon is an application or action name rather than one of
# the status families, so statusicons.py never reaches them. These are the ones
# that were still showing a filled Breeze glyph in the panel.
TRAY = {
    'klipper': 'clipboard',          'edit-paste': 'clipboard',
    'klipper-symbolic': 'clipboard',
    'device-notifier': 'usb',        'drive-removable-media': 'usb',
    'drive-removable-media-usb': 'usb',
    'drive-removable-media-usb-pendrive': 'usb',
    'media-removable': 'usb',        'drive-optical': 'usb',
    'kdeconnect': 'phone',           'kdeconnect-tray': 'phone',
    'smartphone': 'phone',           'phone': 'phone',
    'input-keyboard': 'keyboard',    'input-keyboard-virtual': 'keyboard',
    'input-keyboard-virtual-on': 'keyboard',
    'input-keyboard-virtual-off': 'keyboard',
    'input-keyboard-virtual-hide': 'keyboard',
    'keyboard-layout': 'keyboard',   'input-method': 'keyboard',
    'draw-text': 'keyboard',
    'video-display': 'displays',     'preferences-desktop-display': 'displays',
    'preferences-desktop-display-randr': 'displays',
    'kscreen': 'displays',
    'plasmavault': 'lock',           'wallet-closed': 'lock',
    'wallet-open': 'lock',           'vault-closed': 'lock',
    'vault-open': 'lock',            'plasmavault-symbolic': 'lock',
    'redshift-status-on': 'moon',    'redshift-status-off': 'moon',
    'redshift-status-on-symbolic': 'moon',
    'redshift-status-off-symbolic': 'moon',
    'night-color-on': 'moon',        'night-color-off': 'moon',
}


def place_svgs(stroke_hex):
    """{icon-name: svg} for the file-manager sidebar."""
    out = {}
    for name, glyph in PLACES.items():
        svg = _wrap(GLYPHS[glyph], stroke_hex)
        out[name] = svg
        out[name + '-symbolic'] = svg
    return out


def tray_svgs(stroke_hex):
    """{icon-name: svg} for tray applets outside the status families."""
    return {name: _wrap(GLYPHS[glyph], stroke_hex) for name, glyph in TRAY.items()}
