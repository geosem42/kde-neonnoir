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
    # Browsers. The artboard draws Firefox as a plain globe, which is right when
    # one browser is on the panel and useless when three are: Firefox, Chrome and
    # Chromium became the same button. Function cannot separate them — they do the
    # same job — so these trace each brand's silhouette instead, and the globe
    # stays for browsers we do not single out.
    'browser-flame': '<path d="M12 3.2c2.6 2.4 4.6 5.2 4.6 8.2a4.6 4.6 0 1 1-9.2 0'
                     'c0-1.6.7-3 1.8-4.1 0 1.6.9 2.6 2 2.6 1.3 0 2.1-1 2.1-2.4 '
                     '0-1.5-.6-3-1.3-4.3z"/>',
    'browser-spokes': '<circle cx="12" cy="12" r="8.6"/>'
                      '<circle cx="12" cy="12" r="3.4"/>'
                      '<path d="M12 8.6V3.4M14.94 13.7l4.5 2.6M9.06 13.7l-4.5 2.6"/>',
    'browser-ring': '<circle cx="12" cy="12" r="8.6"/>'
                    '<circle cx="12" cy="12" r="3.4"/>',
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

    'person': '<circle cx="12" cy="8" r="4.2"/>'
              '<path d="M4.4 20.6a7.6 7.6 0 0 1 15.2 0"/>',

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

    # ── UI verbs: menus, toolbars, dialogs ────────────────────────────────────

    'plus':  '<path d="M12 4.8v14.4M4.8 12h14.4"/>',
    'minus': '<path d="M4.8 12h14.4"/>',
    'cross': '<path d="M5.6 5.6l12.8 12.8M18.4 5.6L5.6 18.4"/>',
    'check': '<path d="M4.6 12.8l4.8 4.6L19.4 6.6"/>',

    'arrow-left':  '<path d="M20 12H4.6"/><path d="M10.8 5.8 4.6 12l6.2 6.2"/>',
    'arrow-right': '<path d="M4 12h15.4"/><path d="M13.2 5.8 19.4 12l-6.2 6.2"/>',
    'arrow-up':    '<path d="M12 20V4.6"/><path d="M5.8 10.8 12 4.6l6.2 6.2"/>',
    'arrow-down':  '<path d="M12 4v15.4"/><path d="M5.8 13.2 12 19.4l6.2-6.2"/>',

    'chevron-left':  '<path d="M14.8 5.4 8.2 12l6.6 6.6"/>',
    'chevron-right': '<path d="M9.2 5.4 15.8 12l-6.6 6.6"/>',
    'chevron-up':    '<path d="M5.4 14.8 12 8.2l6.6 6.6"/>',
    'chevron-down':  '<path d="M5.4 9.2 12 15.8l6.6-6.6"/>',

    'refresh': '<path d="M20.4 12a8.4 8.4 0 1 1-2.5-6"/>'
               '<path d="M20.4 4.4V10h-5.6"/>',
    'sync': '<path d="M3.6 10.4a8.4 8.4 0 0 1 14.3-4.4l2.5 2.4"/>'
            '<path d="M20.4 13.6a8.4 8.4 0 0 1-14.3 4.4l-2.5-2.4"/>'
            '<path d="M20.4 3v5.4H15M3.6 21v-5.4H9"/>',

    'search': '<circle cx="10.6" cy="10.6" r="6.8"/><path d="M15.6 15.6 20.6 20.6"/>',
    'zoom-in': '<circle cx="10.6" cy="10.6" r="6.8"/><path d="M15.6 15.6 20.6 20.6"/>'
               '<path d="M10.6 7.8v5.6M7.8 10.6h5.6"/>',
    'zoom-out': '<circle cx="10.6" cy="10.6" r="6.8"/><path d="M15.6 15.6 20.6 20.6"/>'
                '<path d="M7.8 10.6h5.6"/>',
    'zoom-fit': '<path d="M3.6 8.6V4.6a1 1 0 0 1 1-1h4M15.4 3.6h4a1 1 0 0 1 1 1v4'
                'M20.4 15.4v4a1 1 0 0 1-1 1h-4M8.6 20.4h-4a1 1 0 0 1-1-1v-4"/>',

    'undo': '<path d="M3.6 8.4h9.6a6 6 0 0 1 0 12H7.8"/><path d="M7.4 4.6 3.6 8.4l3.8 3.8"/>',
    'redo': '<path d="M20.4 8.4h-9.6a6 6 0 0 0 0 12h5.4"/>'
            '<path d="M16.6 4.6l3.8 3.8-3.8 3.8"/>',

    'copy': '<rect x="8.4" y="8.4" width="12" height="12" rx="2"/>'
            '<path d="M15.6 5.4V5a1.6 1.6 0 0 0-1.6-1.6H5.2A1.6 1.6 0 0 0 3.6 5v8.8'
            'a1.6 1.6 0 0 0 1.6 1.6h.4"/>',
    'scissors': '<circle cx="6" cy="6" r="2.6"/><circle cx="6" cy="18" r="2.6"/>'
                '<path d="M8.2 7.6 20 18.4M20 5.6 8.2 16.4"/>',

    'save': '<path d="M5.2 3.6h11l4.2 4.2v12.6a.8.8 0 0 1-.8.8H5.2a.8.8 0 0 1-.8-.8'
            'V4.4a.8.8 0 0 1 .8-.8z"/>'
            '<path d="M7.8 3.6v6h8.4v-6"/><rect x="7.8" y="13.4" width="8.4" height="7.6"/>',
    'printer': '<path d="M6.6 9V3.6h10.8V9"/>'
               '<path d="M6.6 17.4H4.8a1.8 1.8 0 0 1-1.8-1.8v-4.8A1.8 1.8 0 0 1 4.8 9'
               'h14.4a1.8 1.8 0 0 1 1.8 1.8v4.8a1.8 1.8 0 0 1-1.8 1.8h-1.8"/>'
               '<rect x="6.6" y="14.4" width="10.8" height="6"/>',

    'pencil': '<path d="M16.8 3.4a2.3 2.3 0 0 1 3.3 3.3L8.2 18.6l-4.3 1 1-4.3z"/>'
              '<path d="M14.8 5.4l3.3 3.3"/>',

    'eye': '<path d="M1.8 12S5.6 5.2 12 5.2 22.2 12 22.2 12 18.4 18.8 12 18.8 1.8 12 1.8 12z"/>'
           '<circle cx="12" cy="12" r="3.2"/>',
    'eye-off': '<path d="M9.6 5.6a8.6 8.6 0 0 1 2.4-.4c6.4 0 10.2 6.8 10.2 6.8'
               'a18 18 0 0 1-2.8 3.6M6.2 7.4A17.6 17.6 0 0 0 1.8 12s3.8 6.8 10.2 6.8'
               'a9 9 0 0 0 3.4-.7"/>'
               '<path d="M9.8 9.8a3.2 3.2 0 0 0 4.4 4.4"/><path d="M3.6 3.6l16.8 16.8"/>',

    'funnel': '<path d="M3.4 4.6h17.2l-6.8 8v6.2l-3.6 2.2V12.6z"/>',
    'sort': '<path d="M4.4 7h9M4.4 12h6M4.4 17h3"/>'
            '<path d="M17.4 5.6v12.8M14 15l3.4 3.4L20.8 15"/>',
    'list': '<path d="M8.4 6.4h12M8.4 12h12M8.4 17.6h12"/>'
            '<path d="M4 6.4h.01M4 12h.01M4 17.6h.01"/>',

    'fullscreen': '<path d="M3.6 9V4.6a1 1 0 0 1 1-1H9M15 3.6h4.4a1 1 0 0 1 1 1V9'
                  'M20.4 15v4.4a1 1 0 0 1-1 1H15M9 20.4H4.6a1 1 0 0 1-1-1V15"/>',

    'bold': '<path d="M6.6 3.8h6.6a4.4 4.4 0 0 1 0 8.8H6.6z"/>'
            '<path d="M6.6 12.6h7.6a4.4 4.4 0 0 1 0 8.8H6.6z"/>',
    'italic': '<path d="M15.4 3.8h-5M13.6 20.2h-5M14.4 3.8l-4.8 16.4"/>',
    'underline': '<path d="M6.8 3.8v7.6a5.2 5.2 0 0 0 10.4 0V3.8"/><path d="M5.4 20.2h13.2"/>',

    'align-left':    '<path d="M3.6 5.4h16.8M3.6 10.2h10.8M3.6 15h16.8M3.6 19.8h10.8"/>',
    'align-center':  '<path d="M3.6 5.4h16.8M6.6 10.2h10.8M3.6 15h16.8M6.6 19.8h10.8"/>',
    'align-right':   '<path d="M3.6 5.4h16.8M9.6 10.2h10.8M3.6 15h16.8M9.6 19.8h10.8"/>',
    'align-justify': '<path d="M3.6 5.4h16.8M3.6 10.2h16.8M3.6 15h16.8M3.6 19.8h16.8"/>',
    'indent': '<path d="M9.4 5.4h11M9.4 12h11M9.4 18.6h11"/><path d="M3.6 8.4 6.8 12l-3.2 3.6"/>',
    'bullets': '<path d="M8.6 6.4h11.8M8.6 12h11.8M8.6 17.6h11.8"/>'
               '<circle cx="4.4" cy="6.4" r="1.1"/><circle cx="4.4" cy="12" r="1.1"/>'
               '<circle cx="4.4" cy="17.6" r="1.1"/>',
    'numbers': '<path d="M10.6 6.4h9.8M10.6 12h9.8M10.6 17.6h9.8"/>'
               '<path d="M3.4 4.6 5.2 3.8v4.8M3.6 8.6h3.2"/>'
               '<path d="M3.6 11.2a1.6 1.6 0 1 1 2.8 1.1L3.6 15.4h3.2"/>'
               '<path d="M3.6 17h3.2l-1.7 2a1.5 1.5 0 1 1-1.5 2"/>',

    'play': '<path d="M7.4 4.8 19.6 12 7.4 19.2z"/>',
    'pause': '<path d="M8.8 4.8v14.4M15.2 4.8v14.4"/>',
    'stop': '<rect x="5.4" y="5.4" width="13.2" height="13.2" rx="1.6"/>',
    'skip-forward': '<path d="M5.6 5.2 15 12l-9.4 6.8z"/><path d="M18.4 5.2v13.6"/>',
    'skip-back': '<path d="M18.4 5.2 9 12l9.4 6.8z"/><path d="M5.6 5.2v13.6"/>',
    'record': '<circle cx="12" cy="12" r="6.4"/>',
    'eject': '<path d="M12 4.4 20 14H4z"/><path d="M4.4 18.2h15.2"/>',
    'repeat': '<path d="M4 9.2V8a2.4 2.4 0 0 1 2.4-2.4h13.6"/><path d="M16.6 2.2 20 5.6l-3.4 3.4"/>'
              '<path d="M20 14.8V16a2.4 2.4 0 0 1-2.4 2.4H4"/><path d="M7.4 21.8 4 18.4l3.4-3.4"/>',
    'shuffle': '<path d="M16.6 3.6 20.4 7l-3.8 3.4M16.6 13.6l3.8 3.4-3.8 3.4"/>'
               '<path d="M3.6 7h3.2l9.6 10h3.6M3.6 17h3.2l2.6-2.8M14.4 9.2 16.4 7h3.6"/>',
    'speaker': '<path d="M3.4 9.4h3.3L11.4 5.3a.7.7 0 0 1 1.2.55v12.3'
               'a.7.7 0 0 1-1.2.55L6.7 14.6H3.4a.9.9 0 0 1-.9-.9v-3.4'
               'a.9.9 0 0 1 .9-.9z"/><path d="M15.6 9.6a3.6 3.6 0 0 1 0 4.8"/>',

    'window': '<rect x="2.8" y="4.2" width="18.4" height="15.6" rx="2"/>'
              '<path d="M2.8 8.6h18.4"/><path d="M6 6.4h.01M8.6 6.4h.01"/>',
    'pin': '<path d="M14.6 2.6 21.4 9.4l-3 1.2-1.4 4.6-6.2-6.2 4.6-1.4z"/>'
           '<path d="M10.8 13.2 3.6 20.4"/>',
    'star': '<path d="m12 3.4 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.9l6.1-.9z"/>',

    'warning': '<path d="M10.4 3.9 1.9 18.3a1.8 1.8 0 0 0 1.6 2.7h17a1.8 1.8 0 0 0 1.6-2.7'
               'L13.6 3.9a1.8 1.8 0 0 0-3.2 0z"/><path d="M12 9.4v4.4M12 17.4h.01"/>',
    'error': '<circle cx="12" cy="12" r="9"/><path d="M8.4 8.4l7.2 7.2M15.6 8.4l-7.2 7.2"/>',
    'info': '<circle cx="12" cy="12" r="9"/><path d="M12 16.4v-4.8M12 7.8h.01"/>',

    'power': '<path d="M12 3.4v9.2"/><path d="M17.8 6.6a8.2 8.2 0 1 1-11.6 0"/>',
    'logout': '<path d="M9.4 20.4H5.2a1.8 1.8 0 0 1-1.8-1.8V5.4a1.8 1.8 0 0 1 1.8-1.8h4.2"/>'
              '<path d="M15.6 16.6 20.4 12l-4.8-4.6"/><path d="M20.4 12H9"/>',

    'gear': '<circle cx="12" cy="12" r="3.2"/>'
            '<path d="M19.2 14.6a1.6 1.6 0 0 0 .3 1.8l.1.1a1.9 1.9 0 1 1-2.7 2.7l-.1-.1'
            'a1.6 1.6 0 0 0-1.8-.3 1.6 1.6 0 0 0-1 1.5v.2a1.9 1.9 0 0 1-3.8 0v-.1'
            'a1.6 1.6 0 0 0-1.1-1.5 1.6 1.6 0 0 0-1.8.3l-.1.1a1.9 1.9 0 1 1-2.7-2.7l.1-.1'
            'a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1h-.2a1.9 1.9 0 0 1 0-3.8h.1'
            'a1.6 1.6 0 0 0 1.5-1.1 1.6 1.6 0 0 0-.3-1.8l-.1-.1a1.9 1.9 0 1 1 2.7-2.7l.1.1'
            'a1.6 1.6 0 0 0 1.8.3h.1a1.6 1.6 0 0 0 1-1.5v-.2a1.9 1.9 0 0 1 3.8 0v.1'
            'a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1a1.9 1.9 0 1 1 2.7 2.7l-.1.1'
            'a1.6 1.6 0 0 0-.3 1.8v.1a1.6 1.6 0 0 0 1.5 1h.2a1.9 1.9 0 0 1 0 3.8h-.1'
            'a1.6 1.6 0 0 0-1.5 1z"/>',
    'menu': '<path d="M3.6 6.4h16.8M3.6 12h16.8M3.6 17.6h16.8"/>',
    'dots': '<circle cx="5.2" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/>'
            '<circle cx="18.8" cy="12" r="1.3"/>',

    'link': '<path d="M9.6 13.4a4.4 4.4 0 0 0 6.6.5l2.6-2.6a4.4 4.4 0 0 0-6.2-6.2l-1.5 1.5"/>'
            '<path d="M14.4 10.6a4.4 4.4 0 0 0-6.6-.5l-2.6 2.6a4.4 4.4 0 0 0 6.2 6.2l1.5-1.5"/>',
    'share': '<circle cx="18.2" cy="5.6" r="2.6"/><circle cx="5.8" cy="12" r="2.6"/>'
             '<circle cx="18.2" cy="18.4" r="2.6"/>'
             '<path d="M8.1 10.7 15.9 6.9M8.1 13.3l7.8 3.8"/>',
    'upload': '<path d="M12 20v-9.4"/><path d="M8.2 14.4 12 10.6l3.8 3.8"/>'
              '<path d="M4.5 16.2v2.1a1.7 1.7 0 0 0 1.7 1.7h11.6a1.7 1.7 0 0 0 1.7-1.7v-2.1"/>',

    'rotate': '<path d="M20.4 12a8.4 8.4 0 1 1-2.5-6"/><path d="M20.4 4.4V10h-5.6"/>'
              '<circle cx="12" cy="12" r="2.4"/>',
    'flip': '<path d="M12 3.4v17.2"/><path d="M8.6 7.4 3.6 12l5 4.6z"/>'
            '<path d="M15.4 7.4 20.4 12l-5 4.6z"/>',
    'crop': '<path d="M6.4 2.6v15h15"/><path d="M2.6 6.4h15v15"/>',
    'layers': '<path d="m12 3 9 4.8-9 4.8-9-4.8z"/><path d="m3 12.6 9 4.8 9-4.8"/>'
              '<path d="m3 17.4 9 4.8 9-4.8"/>',
    'droplet': '<path d="M12 2.8s6.4 6.2 6.4 10.4a6.4 6.4 0 0 1-12.8 0C5.6 9 12 2.8 12 2.8z"/>',

    'send': '<path d="M21.4 2.6 10.6 13.4"/><path d="M21.4 2.6 14.6 21.4l-4-8-8-4z"/>',
    'reply': '<path d="M9.4 5.4 3.6 11.2 9.4 17"/>'
             '<path d="M3.6 11.2h9.8a7 7 0 0 1 7 7v1.4"/>',
    'forward': '<path d="M14.6 5.4 20.4 11.2 14.6 17"/>'
               '<path d="M20.4 11.2H10.6a7 7 0 0 0-7 7v1.4"/>',

    'bug': '<rect x="7.4" y="7.4" width="9.2" height="12.2" rx="4.6"/>'
           '<path d="M8.6 7.4a3.4 3.4 0 0 1 6.8 0"/>'
           '<path d="M3.6 11h3.8M16.6 11h3.8M3.6 16h3.8M16.6 16h3.8'
           'M6.6 6 8.8 8.2M17.4 6l-2.2 2.2"/>',
    'tag': '<path d="M2.8 11.6V4.4a1.6 1.6 0 0 1 1.6-1.6h7.2l9.6 9.6a1.6 1.6 0 0 1 0 2.3'
           'l-6.9 6.9a1.6 1.6 0 0 1-2.3 0z"/><circle cx="7.4" cy="7.4" r="1.4"/>',



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
    'firefox': 'browser-flame',           'firefox_firefox': 'browser-flame',
    'firefox-esr': 'browser-flame',       'web-browser': 'globe',
    'chromium': 'browser-ring',           'chromium-browser': 'browser-ring',
    'google-chrome': 'browser-spokes',    'internet-web-browser': 'globe',
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


def _wrap(body, stroke_hex, size=VIEWBOX):
    """`size` is the INTRINSIC size; the viewBox always stays 24.

    A Type=Fixed directory promises icons of the size it declares. Writing a
    24x24 file into places/16 made a 16px request hand back a 24px icon, which
    widened the icon column in every menu that used one.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" '
        f'height="{size}" viewBox="0 0 {VIEWBOX} {VIEWBOX}">'
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


# Tray applets whose icon is an application or action name rather than one of
# the status families, so statusicons.py never reaches them. These are the ones
# that were still showing a filled Breeze glyph in the panel.
TRAY = {
    'klipper': 'clipboard',          'edit-paste': 'clipboard',
    'klipper-symbolic': 'clipboard',
    'dialog-warning': 'warning',     'dialog-error': 'error',
    'dialog-information': 'info',    'dialog-question': 'question',
    'dialog-positive': 'check',      'dialog-password': 'lock',
    'document-open-recent': 'clock',
    'drive-harddisk': 'drive',       'drive-harddisk-root': 'drive',
    'drive-harddisk-usb': 'drive',   'drive-multidisk': 'drive',
    'drive-optical': 'book',         'media-optical': 'book',
    'media-flash': 'usb',            'media-flash-sd-mmc': 'usb',
    'drive-removable-media-usb-pendrive-symbolic': 'usb',
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


def tray_svgs(stroke_hex):
    """{icon-name: svg} for tray applets outside the status families."""
    return {name: _wrap(GLYPHS[glyph], stroke_hex) for name, glyph in TRAY.items()}
