"""Aurorae window decoration + Plasma style, generated from the palette.

Aurorae slices decoration.svg by element id; each id's bounding box defines that
slice, and the ids are read independently, so the nine active slices and the nine
inactive ones can sit anywhere on the canvas. Button SVGs carry five state ids.
Element ids and rc keys were taken from a real installed Aurorae theme, not guessed.
"""
import json


def _plasma_style(DIST, THEME_ID, THEME_NAME, colors_text):
    out = []
    # ══ Plasma style (desktoptheme) ═══════════════════════════════════════════
    # breeze-dark ships only colors + metadata + plasmarc and inherits every SVG
    # from the `default` theme, which recolours them from this colors file. So a
    # colours-only Plasma style is legitimate and is what we do here.
    ds = DIST / 'desktoptheme' / THEME_ID
    ds.mkdir(parents=True, exist_ok=True)
    (ds / 'colors').write_text(colors_text)
    (ds / 'metadata.json').write_text(json.dumps({
        'KPlugin': {
            'Id': THEME_ID, 'Name': THEME_NAME,
            'Description': 'Neon Noir Plasma style',
            'Authors': [{'Name': 'Neon Noir'}],
            'License': 'LGPL', 'Version': '1.0',
            'EnabledByDefault': True,
        },
        'X-Plasma-API': '5.0',
    }, indent=2) + '\n')
    (ds / 'plasmarc').write_text(
        '[Wallpaper]\n'
        f'defaultWallpaperTheme={THEME_ID}\n'
        'defaultFileSuffix=.png\n'
        'defaultWidth=3840\n'
        'defaultHeight=2160\n\n'
        '[ContrastEffect]\n'
        'enabled=true\n'
        'contrast=1.1\n'
        'intensity=0.9\n'
        'saturation=1.3\n\n'
        '[AdaptiveTransparency]\n'
        'enabled=true\n')
    out = [f'desktoptheme/{THEME_ID}/colors',
           f'desktoptheme/{THEME_ID}/metadata.json',
           f'desktoptheme/{THEME_ID}/plasmarc']
    return out



def build(T, DIST, THEME_ID, THEME_NAME, colors_text,
          title_height=40, aurorae_id=None, aurorae_name=None,
          plasma_style=True):
    """Aurorae decoration, and (unless switched off) the Plasma style with it.

    title_height is a parameter rather than a constant because the SVG is DRAWN
    at that height — the corner radius, the accent edge and the button glyphs
    are all laid out against it. A variant that only shrank the rc key would get
    a 40px drawing squeezed into a 26px bar.
    """
    out = []
    AID = aurorae_id or THEME_ID
    ANAME = aurorae_name or THEME_NAME

    if plasma_style:
        out += _plasma_style(DIST, THEME_ID, THEME_NAME, colors_text)

    # ══ Aurorae decoration ════════════════════════════════════════════════════
    au = DIST / 'aurorae' / AID
    au.mkdir(parents=True, exist_ok=True)

    TB      = T['titlebar.active']      # active titlebar fill
    TBI     = T['titlebar.inactive']    # inactive titlebar fill
    BORD    = T['border.hairline']      # 1px window outline
    BORDI   = T['border.hairline']
    CY      = T['accent.cyan']
    MG      = T['accent.magenta']
    WIN     = T['surface.window']

    R   = 10     # top corner radius, px
    TH  = title_height
    EDG = 2      # accent edge thickness, px
    BW  = 4      # side/bottom border slice width in SVG units

    # The window's top hairline is solid cyan across the full width. The
    # artboards fade it to magenta at the right end; that was tried and
    # rejected.
    def titlebar_slice(x, y, w, kind, active):
        """kind: 'left' | 'mid' | 'right'."""
        fill = TB if active else TBI
        edge = CY
        p = []
        if kind == 'left':
            p.append(f'<path d="M{x},{y+TH} L{x},{y+R} Q{x},{y} {x+R},{y} '
                     f'L{x+w},{y} L{x+w},{y+TH} Z" fill="{fill}"/>')
            p.append(f'<path d="M{x},{y+R} Q{x},{y} {x+R},{y} L{x+w},{y} '
                     f'L{x+w},{y+EDG} L{x+R},{y+EDG} '
                     f'Q{x+EDG},{y+EDG} {x+EDG},{y+R} Z" '
                     f'fill="{edge if active else "none"}"/>')
        elif kind == 'right':
            p.append(f'<path d="M{x},{y} L{x+w-R},{y} Q{x+w},{y} {x+w},{y+R} '
                     f'L{x+w},{y+TH} L{x},{y+TH} Z" fill="{fill}"/>')
            p.append(f'<path d="M{x},{y} L{x+w-R},{y} Q{x+w},{y} {x+w},{y+R} '
                     f'L{x+w-EDG},{y+R} '
                     f'Q{x+w-EDG},{y+EDG} {x+w-R},{y+EDG} L{x},{y+EDG} Z" '
                     f'fill="{edge if active else "none"}"/>')
        else:
            p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{TH}" fill="{fill}"/>')
            if active:
                p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{EDG}" '
                         f'fill="{edge}"/>')
        return '\n    '.join(p)

    def decoration_svg():
        W, H = 320, 200
        s = [f'<?xml version="1.0" encoding="UTF-8"?>',
             f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
        for active, oy, pre in ((True, 0, 'decoration'), (False, 100, 'decoration-inactive')):
            fill  = TB if active else TBI
            bord  = BORD if active else BORDI
            # titlebar row
            s.append(f'  <g id="{pre}-topleft">\n    ' + titlebar_slice(0, oy, 24, 'left', active) + '\n  </g>')
            s.append(f'  <g id="{pre}-top">\n    '     + titlebar_slice(30, oy, 40, 'mid', active) + '\n  </g>')
            s.append(f'  <g id="{pre}-topright">\n    '+ titlebar_slice(76, oy, 24, 'right', active) + '\n  </g>')
            # borders
            by = oy + 50
            s.append(f'  <g id="{pre}-left"><rect x="0" y="{by}" width="{BW}" height="20" fill="{bord}"/></g>')
            # OPAQUE, and deliberately flat — this element becomes the entire
            # titlebar when the window is maximized (FrameSvg NoBorder paints
            # only the center), and is stretched over the client area otherwise.
            s.append(f'  <g id="{pre}-center"><rect x="{BW+6}" y="{by}" width="40" height="20" fill="{fill}"/></g>')
            s.append(f'  <g id="{pre}-right"><rect x="{BW+56}" y="{by}" width="{BW}" height="20" fill="{bord}"/></g>')
            byy = oy + 76
            s.append(f'  <g id="{pre}-bottomleft"><rect x="0" y="{byy}" width="{BW}" height="{BW}" fill="{bord}"/></g>')
            s.append(f'  <g id="{pre}-bottom"><rect x="{BW+6}" y="{byy}" width="40" height="{BW}" fill="{bord}"/></g>')
            s.append(f'  <g id="{pre}-bottomright"><rect x="{BW+56}" y="{byy}" width="{BW}" height="{BW}" fill="{bord}"/></g>')
        # Maximized: square corners, no borders. Aurorae needs these explicitly;
        # it does not fall back to the normal slices for the maximized state.
        for active, oy, pre in ((True, 0, 'decoration-maximized'),
                                (False, 100, 'decoration-maximized-inactive')):
            fill = TB if active else TBI
            mx = 120
            for idx, (nm, w) in enumerate((('topleft', 16), ('top', 40), ('topright', 16))):
                x = mx + sum(v for _, v in (('topleft', 16), ('top', 40), ('topright', 16))[:idx]) + idx * 6
                s.append(f'  <g id="{pre}-{nm}">'
                         f'<rect x="{x}" y="{oy}" width="{w}" height="{TH}" fill="{fill}"/>'
                         + (f'<rect x="{x}" y="{oy}" width="{w}" height="{EDG}" fill="{CY}"/>' if active else '')
                         + '</g>')
            by = oy + 50
            for idx, nm in enumerate(('left', 'center', 'right')):
                x = mx + idx * 22
                if nm == 'center':
                    # FLAT, no accent strip. A maximized window is painted with
                    # enabledBorders = NoBorder, so KSvg draws only the center
                    # and stretches it over the WHOLE titlebar — internal detail
                    # scales with it, which turned the 2px edge into a fully
                    # accent-coloured titlebar. The edge lives in -top, which is
                    # only used in the restored state.
                    s.append(f'  <g id="{pre}-{nm}">'
                             f'<rect x="{x}" y="{by}" width="18" height="{TH}" fill="{fill}"/></g>')
                else:
                    s.append(f'  <g id="{pre}-{nm}">'
                             f'<rect x="{x}" y="{by}" width="18" height="18" fill="{fill}"/></g>')
            byy = oy + 76
            for idx, nm in enumerate(('bottomleft', 'bottom', 'bottomright')):
                x = mx + idx * 22
                s.append(f'  <g id="{pre}-{nm}">'
                         f'<rect x="{x}" y="{byy}" width="18" height="4" fill="{fill}"/></g>')
        s.append('</svg>')
        return '\n'.join(s) + '\n'

    (au / 'decoration.svg').write_text(decoration_svg())
    out.append(f'aurorae/{AID}/decoration.svg')

    # ── buttons ───────────────────────────────────────────────────────────────
    # Five states per button, laid out in a row; Aurorae reads them by id.
    BTN, GAP = 24, 8
    STATES = ['active', 'hover', 'pressed', 'inactive', 'deactivated']

    def glyph(kind, x, y, stroke, w=1.6):
        cx, cy = x + BTN / 2, y + BTN / 2
        a = f'stroke="{stroke}" stroke-width="{w}" fill="none" stroke-linecap="round"'
        if kind == 'close':
            return (f'<path d="M{cx-4},{cy-4} L{cx+4},{cy+4}" {a}/>'
                    f'<path d="M{cx+4},{cy-4} L{cx-4},{cy+4}" {a}/>')
        if kind == 'minimize':
            return f'<path d="M{cx-4.5},{cy} L{cx+4.5},{cy}" {a}/>'
        if kind == 'maximize':
            return f'<rect x="{cx-4.5}" y="{cy-4.5}" width="9" height="9" rx="1.5" {a}/>'
        if kind == 'restore':
            return (f'<rect x="{cx-5}" y="{cy-2}" width="7" height="7" rx="1.2" {a}/>'
                    f'<path d="M{cx-2},{cy-2} L{cx-2},{cy-5} L{cx+5},{cy-5} L{cx+5},{cy+2} L{cx+2},{cy+2}" {a}/>')
        if kind == 'alldesktops':
            return f'<circle cx="{cx}" cy="{cy}" r="4.2" {a}/>'
        if kind == 'keepabove':
            return f'<path d="M{cx-4.5},{cy+2.5} L{cx},{cy-3} L{cx+4.5},{cy+2.5}" {a}/>'
        if kind == 'keepbelow':
            return f'<path d="M{cx-4.5},{cy-2.5} L{cx},{cy+3} L{cx+4.5},{cy-2.5}" {a}/>'
        if kind == 'help':
            return (f'<path d="M{cx-3},{cy-2} a3,3 0 1,1 3,3 l0,1.5" {a}/>'
                    f'<circle cx="{cx}" cy="{cy+5}" r="0.9" fill="{stroke}" stroke="none"/>')
        if kind == 'shade':
            return f'<path d="M{cx-4.5},{cy-3} L{cx+4.5},{cy-3}" {a}/><path d="M{cx-4.5},{cy+3} L{cx+4.5},{cy+3}" {a}/>'
        return ''

    def button_svg(kind):
        accent = MG if kind == 'close' else CY
        look = {
            'active':      (T['text.dim'],     None,                   None),
            'hover':       (accent,            T['accent.magenta.ghost'] if kind=='close' else T['accent.cyan.ghost'],
                                               T['accent.magenta.deep'] if kind=='close' else T['accent.cyan.deep']),
            'pressed':     (accent,            T['accent.magenta.dim'] if kind=='close' else T['accent.cyan.dim'],
                                               accent),
            'inactive':    (T['text.disabled'], None,                  None),
            'deactivated': (T['text.faint'],   None,                   None),
        }
        W = len(STATES) * (BTN + GAP)
        s = [f'<?xml version="1.0" encoding="UTF-8"?>',
             f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{BTN}" viewBox="0 0 {W} {BTN}">']
        for i, st in enumerate(STATES):
            x = i * (BTN + GAP)
            fg, bg, ring = look[st]
            s.append(f'  <g id="{st}-center">')
            # pins the bounding box to the full button square for EVERY state
            # zero-opacity FILL, not fill="none" — a fill:none rect can be
            # dropped from bounds computation, which is the bug this fixes.
            s.append(f'    <rect x="{x}" y="0" width="{BTN}" height="{BTN}" '
                     f'fill="#000000" fill-opacity="0"/>')
            if bg:
                s.append(f'    <rect x="{x+1}" y="1" width="{BTN-2}" height="{BTN-2}" rx="5" '
                         f'fill="{bg}" stroke="{ring}" stroke-width="1"/>')
            s.append('    ' + glyph(kind, x, 0, fg, 1.8 if st == 'pressed' else 1.6))
            s.append('  </g>')
        s.append('</svg>')
        return '\n'.join(s) + '\n'

    for k in ('close', 'minimize', 'maximize', 'restore', 'alldesktops',
              'keepabove', 'keepbelow', 'shade', 'help'):
        (au / f'{k}.svg').write_text(button_svg(k))
    out.append(f'aurorae/{AID}/*.svg  (9 buttons)')

    # ── theme rc ──────────────────────────────────────────────────────────────
    def dec(tok): 
        h = T[tok].lstrip('#'); r,g,b = (int(h[i:i+2],16) for i in (0,2,4)); return f'{r},{g},{b}'
    # Animation=0: no cross-fade. Aurorae animates the active/inactive
    # titlebar by blending the two states with opacity, so for the length of
    # the fade the titlebar is partly transparent and the window behind shows
    # through it. Minimising a window hands focus to the one below, whose
    # titlebar then fades — which is how a third window's toolbar icons
    # appeared inside a titlebar two layers up.
    # The buttons scale with the bar, as a PROPORTION of it. 0.6 reproduces the
    # 24px button and 8px margin of the 40px bar exactly, so the classic theme is
    # untouched; subtracting a constant instead would have left a 26px bar with
    # 10px buttons, which is a dot rather than a target.
    BTN = round(TH * 0.6)
    BTN_TOP = (TH - BTN) // 2
    (au / f'{AID}rc').write_text(f'''[General]
ActiveTextColor={dec('text.normal')}
InactiveTextColor={dec('text.title.inactive')}
Animation=0
TitleAlignment=Left
TitleVerticalAlignment=Center

[Layout]
BorderLeft=1
BorderRight=1
BorderBottom=1
TitleEdgeTop=0
TitleEdgeBottom=0
TitleEdgeLeft=8
TitleEdgeRight=8
TitleEdgeTopMaximized=0
TitleEdgeBottomMaximized=0
TitleEdgeLeftMaximized=8
TitleEdgeRightMaximized=8
TitleBorderLeft=6
TitleBorderRight=6
TitleHeight={TH}
ButtonWidth={BTN}
ButtonHeight={BTN}
ButtonSpacing=4
ButtonMarginTop={BTN_TOP}
ButtonMarginTopMaximized={BTN_TOP}
ExplicitButtonSpacer=6
PaddingTop=0
PaddingBottom=0
PaddingLeft=0
PaddingRight=0
''')
    (au / 'metadata.json').write_text(json.dumps({
        'KPackageStructure': 'KWin/Aurorae',
        'KPlugin': {
            'Id': AID, 'Name': ANAME,
            'Description': 'Neon Noir window decoration',
            'Authors': [{'Name': 'Neon Noir'}],
            'Category': 'Plasma 6 Window Decorations',
            'ServiceTypes': ['aurorae'],
            'License': 'LGPL', 'Version': '1.0',
            'EnabledByDefault': True,
            # No blur flag. It tells KWin the decoration is translucent and to
            # blur the backdrop beneath it; this titlebar is fully opaque, so
            # the only thing that produced was a blurred sample of the windows
            # behind showing through during another window's minimise or
            # maximise animation.
        },
    }, indent=2) + '\n')
    (au / 'metadata.desktop').write_text(f'''[Desktop Entry]
Name={ANAME}
X-KDE-PluginInfo-Author=Neon Noir
X-KDE-PluginInfo-EnabledByDefault=true
X-KDE-PluginInfo-License=LGPL
X-KDE-PluginInfo-Name={AID}
X-KDE-PluginInfo-Version=1.0
''')
    out += [f'aurorae/{AID}/{AID}rc',
            f'aurorae/{AID}/metadata.json',
            f'aurorae/{AID}/metadata.desktop']
    return out
