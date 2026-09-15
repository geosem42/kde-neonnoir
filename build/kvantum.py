"""Kvantum theme: the Qt6 widget style, generated as kvconfig + SVG.

Kvantum keeps the built-in :/Kvantum/default.svg loaded as a per-element
fallback layer, so any id this generator forgets is silently drawn from a grey
Enlightenment skin with purple accents instead of erroring. build() therefore
cross-checks every `*.element` named in the kvconfig against the ids actually
emitted and fails the build if one is missing.

Two more traps, both silent:
  - a theme's general section must be spelled `[%General]` (Qt escaping a group
    literally named General); the SELECTION file kvantum.kvconfig needs plain
    `[General]`. Either one backwards loads the built-in default theme.
  - omitting [GeneralColors] does not mean "inherit the desktop palette" —
    Kvantum still forces Base to #ffffff. Every role is set explicitly here.

Geometry comes from the design: 7px radius, 1px border, 32px primary controls.
"""
import math

R  = 7     # corner radius
BW = 1     # border width

# From the artboard's own spec line: "Primary controls 32 px · compact rows
# 28-30 px · in-titlebar 24 px. 7 px radius, 1 px border throughout."
H_PRIMARY = 32
H_ROW     = 28
V_PRIMARY = 5     # vertical frame slice; see framed() for why it is not R
K  = 24    # nominal length of a stretched edge / interior in the artwork

STATES = ('normal', 'focused', 'pressed', 'toggled', 'disabled')


# ── slice geometry ────────────────────────────────────────────────────────────
# Borders are filled annular wedges rather than strokes: Qt's boundsOnElement
# does not reliably include stroke width, and a slice whose reported bounds are
# half a pixel small is scaled wrong by Kvantum.

def _corner(r, bw, fill, border, flip_x=False, flip_y=False):
    """One rounded corner as filled paths: an annular wedge for the border and a
    wedge for the interior. Degenerates to a square when the radius is at or
    below the border width."""
    if r <= bw:
        w = max(r, bw)
        parts = [f'<rect x="0" y="0" width="{w}" height="{w}" '
                 f'fill="{border or fill or "#000000"}"'
                 + ('' if (border or fill) else ' fill-opacity="0"') + '/>']
        return f'<g>{"".join(parts)}</g>', w
    ring = (f'M 0 {r} A {r} {r} 0 0 1 {r} 0 L {r} {bw} '
            f'A {r - bw} {r - bw} 0 0 0 {bw} {r} Z')
    inner = f'M {bw} {r} A {r - bw} {r - bw} 0 0 1 {r} {bw} L {r} {r} Z'
    parts = []
    if fill:
        parts.append(f'<path d="{inner}" fill="{fill}"/>')
    if border:
        parts.append(f'<path d="{ring}" fill="{border}"/>')
    if not parts:
        parts.append(f'<rect x="0" y="0" width="{r}" height="{r}" '
                     f'fill="#000000" fill-opacity="0"/>')
    t = ''
    if flip_x or flip_y:
        sx, sy = (-1 if flip_x else 1), (-1 if flip_y else 1)
        t = (f' transform="translate({r if flip_x else 0} {r if flip_y else 0}) '
             f'scale({sx} {sy})"')
    return f'<g{t}>{"".join(parts)}</g>', r


def _edge(r, bw, fill, border, side):
    """side: top | bottom | left | right."""
    horiz = side in ('top', 'bottom')
    w, h = (K, r) if horiz else (r, K)
    parts = [f'<rect x="0" y="0" width="{w}" height="{h}" '
             f'fill="#000000" fill-opacity="0"/>']
    if fill:
        parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{fill}"/>')
    if border:
        bx, by, bw_, bh = {
            'top':    (0, 0, w, bw),
            'bottom': (0, h - bw, w, bw),
            'left':   (0, 0, bw, h),
            'right':  (w - bw, 0, bw, h),
        }[side]
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw_}" height="{bh}" fill="{border}"/>')
    return ''.join(parts), (w, h)


class Sheet:
    """Collects elements and lays them out on a grid so the file stays browsable."""

    def __init__(self):
        self.items = []   # (id, body, w, h)
        self.ids = set()

    def add(self, eid, body, w, h):
        if eid in self.ids:
            raise ValueError(f'duplicate Kvantum element id: {eid}')
        self.ids.add(eid)
        self.items.append((eid, body, w, h))

    def frame(self, base, state, fill, border, r=R, bw=BW, interior=True,
              sides=('top', 'bottom', 'left', 'right'), bws=None):
        """The nine ids Kvantum looks up for a framed widget.

        `sides` limits which edges carry the border — an active tab is a frame
        whose only coloured edge is a 2px bottom rule."""
        bws = bws or {}
        pre = f'{base}-{state}' if state else base
        for name, flip, adj in (('topleft', (False, False), ('top', 'left')),
                                ('topright', (True, False), ('top', 'right')),
                                ('bottomleft', (False, True), ('bottom', 'left')),
                                ('bottomright', (True, True), ('bottom', 'right'))):
            b = border if (adj[0] in sides and adj[1] in sides) else None
            body, w = _corner(r, bw, fill, b, *flip)
            self.add(f'{pre}-{name}', body, w, w)
        for side in ('top', 'bottom', 'left', 'right'):
            b = border if side in sides else None
            body, (w, h) = _edge(r, bws.get(side, bw), fill, b, side)
            self.add(f'{pre}-{side}', body, w, h)
        if interior:
            body = (f'<rect x="0" y="0" width="{K}" height="{K}" fill="{fill}"/>'
                    if fill else f'<rect x="0" y="0" width="{K}" height="{K}" fill="none"/>')
            self.add(pre, body, K, K)

    def plain(self, eid, body, w, h):
        self.add(eid, body, w, h)

    def render(self):
        """Lay every element out on a grid. Position is cosmetic — Kvantum
        addresses elements by id and scales each one's own bounding box."""
        pad, x, y, rowh, maxw = 10, 10, 10, 0, 0
        out = []
        for eid, body, w, h in self.items:
            if x + w > 900:
                x, y, rowh = 10, y + rowh + pad, 0
            out.append(f'<g id="{eid}" transform="translate({x} {y})">{body}</g>')
            x += w + pad
            rowh = max(rowh, h)
            maxw = max(maxw, x)
        height = y + rowh + pad
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{maxw}" '
                f'height="{height}" viewBox="0 0 {maxw} {height}">\n'
                + '\n'.join(out) + '\n</svg>\n')


# ── glyphs ────────────────────────────────────────────────────────────────────
# Indicators are single elements, so each one is pinned to a fixed box by a
# zero-opacity FILL rect. `fill="none"` would not do: a none-filled rect can be
# dropped from the bounding-box computation, and the glyph would then be scaled
# up to the whole indicator rect.

def _box(size, body):
    return (f'<rect x="0" y="0" width="{size}" height="{size}" '
            f'fill="#000000" fill-opacity="0"/>{body}')


def chevron(size, colour, direction, w=1.7):
    c, a = size / 2, size * 0.21
    pts = {'down':  [(c - a, c - a / 2), (c, c + a / 2), (c + a, c - a / 2)],
           'up':    [(c - a, c + a / 2), (c, c - a / 2), (c + a, c + a / 2)],
           'left':  [(c + a / 2, c - a), (c - a / 2, c), (c + a / 2, c + a)],
           'right': [(c - a / 2, c - a), (c + a / 2, c), (c - a / 2, c + a)]}[direction]
    d = 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in pts)
    return _box(size, f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w}" '
                      f'stroke-linecap="round" stroke-linejoin="round"/>')


def tick(size, colour, w=2.0):
    s = size
    d = f'M {s*0.24:.2f} {s*0.52:.2f} L {s*0.42:.2f} {s*0.71:.2f} L {s*0.77:.2f} {s*0.30:.2f}'
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{w}" ' \
           f'stroke-linecap="round" stroke-linejoin="round"/>'


def dash(size, colour, w=2.0):
    return (f'<path d="M {size*0.27:.2f} {size/2:.2f} H {size*0.73:.2f}" fill="none" '
            f'stroke="{colour}" stroke-width="{w}" stroke-linecap="round"/>')


def cross(size, colour, w=1.6):
    a, b = size * 0.29, size * 0.71
    return _box(size, f'<path d="M {a:.2f} {a:.2f} L {b:.2f} {b:.2f} M {b:.2f} {a:.2f} '
                      f'L {a:.2f} {b:.2f}" fill="none" stroke="{colour}" '
                      f'stroke-width="{w}" stroke-linecap="round"/>')


def rounded_box(size, fill, border, r, bw=BW, inset=0.0):
    """A whole small control drawn as one element — checkbox, radio, handle."""
    x = inset
    s = size - 2 * inset
    out = ''
    if border:
        out += (f'<rect x="{x}" y="{x}" width="{s}" height="{s}" rx="{r}" fill="{border}"/>'
                f'<rect x="{x+bw}" y="{x+bw}" width="{s-2*bw}" height="{s-2*bw}" '
                f'rx="{max(0, r-bw)}" fill="{fill or "#000000"}"'
                + ('' if fill else ' fill-opacity="0"') + '/>')
    elif fill:
        out += f'<rect x="{x}" y="{x}" width="{s}" height="{s}" rx="{r}" fill="{fill}"/>'
    return out


def disc(size, fill, border, bw=BW, inset=0.0):
    c, r = size / 2, size / 2 - inset
    out = ''
    if border:
        out += f'<circle cx="{c}" cy="{c}" r="{r:.2f}" fill="{border}"/>'
        out += (f'<circle cx="{c}" cy="{c}" r="{r-bw:.2f}" fill="{fill or "#000000"}"'
                + ('' if fill else ' fill-opacity="0"') + '/>')
    elif fill:
        out += f'<circle cx="{c}" cy="{c}" r="{r:.2f}" fill="{fill}"/>'
    return out


# ── the theme ─────────────────────────────────────────────────────────────────

def artwork(T):
    S = Sheet()
    hair, flt, dis = T['border.hairline'], T['border.float'], T['border.disabled']
    cy, cyd, cyh = T['accent.cyan'], T['accent.cyan.dim'], T['accent.cyan.hover']
    sel, hov = T['selection.bg'], T['surface.hover']
    none = None

    # base -> (radius, {state: (fill, border)}, extra kwargs)
    frames = {
        # No filled-cyan primary button: Kvantum's only hook for a dialog's
        # default button is `<element>-default-indicator`, a small corner mark
        # drawn over the ordinary fill. The artboard's solid accent Apply is
        # not expressible here, so the default button keeps the focus ring and
        # normal_default_pushbutton stays on to suppress the stray marker.
        # A CHECKED button is a quiet teal box with no border, not a solid
        # accent slab: the artboard's toolbar marks its active tool that way,
        # and selection.bg here made every checked button in Gwenview, Dolphin
        # and Kate read as a filled highlight.
        'button':   (R, {'normal':   (T['surface.raised'], hair),
                         'focused':  (hov, T['decoration.hover']),
                         'pressed':  (T['surface.float'], cyd),
                         'toggled':  (T['accent.cyan.ghost'], none),
                         'disabled': (T['surface.disabled'], dis)}, {}),
        # Same states, but flat at rest — a toolbar is a row of glyphs, not a
        # row of raised buttons.
        'toolbtn':  (R, {'normal':   (none, none),
                         'focused':  (T['surface.raised'], hair),
                         'pressed':  (T['surface.float'], cyd),
                         'toggled':  (T['accent.cyan.ghost'], none),
                         'disabled': (none, none)}, {}),
        'combo':    (R, {'normal':   (T['surface.raised'], hair),
                         'focused':  (hov, T['decoration.hover']),
                         'pressed':  (T['surface.float'], cy),
                         'toggled':  (T['surface.float'], cy),
                         'disabled': (T['surface.disabled'], dis)}, {}),
        'lineedit': (R, {'normal':   (T['surface.view'], hair),
                         'focused':  (T['surface.view'], cy),
                         'pressed':  (T['surface.view'], cy),
                         'disabled': (T['surface.disabled'], dis)}, {}),
        'menu':     (R, {'normal':   (T['surface.float'], flt)}, {}),
        'tooltip':  (5, {'normal':   (T['tooltip.bg'], flt)}, {}),
        # The focused frame is the outline around a file view or a scroll area.
        # The artboard draws no ring there at all, so this is the same neutral
        # grey the popup surfaces use rather than any strength of accent — an
        # accent ring around the whole file list reads as an alert.
        'common':   (R, {'normal':   (none, hair),
                         'focused':  (none, flt),
                         'disabled': (none, dis)}, {}),
        'group':    (R, {'normal':   (none, hair)}, {}),
        'dock':     (4, {'normal':   (T['surface.window'], hair)}, {}),
        'tabframe': (R, {'normal':   (T['surface.window'], hair)}, {}),
        'toolbar':  (1, {'normal':   (T['surface.window'], none)}, {}),
        'menubar':  (1, {'normal':   (T['surface.window'], none)}, {}),
        'titlebar': (1, {'normal':   (T['titlebar.active'], none),
                         'focused':  (T['titlebar.active'], none),
                         'disabled': (T['titlebar.inactive'], none)}, {}),
        'header':   (1, {'normal':   (T['surface.alt'], none),
                         'focused':  (T['surface.raised'], none),
                         'pressed':  (hov, none)}, {}),
        'progress': (4, {'normal':   (T['surface.alt'], hair),
                         'disabled': (T['surface.disabled'], dis)}, {}),
        'progress-pattern': (4, {'normal': (cy, none), 'disabled': (dis, none)}, {}),
        'slider':   (2, {'normal':   (T['surface.raised'], none),
                         'toggled':  (cy, none),
                         'disabled': (T['surface.disabled'], none)}, {}),
        'scrollbarslider': (5, {'normal':   (flt, none),
                                'focused':  (cy, none),
                                'pressed':  (cyh, none),
                                'disabled': (T['surface.raised'], none)}, {}),
        'scrollbargroove': (1, {'normal': (none, none)}, {}),
        'menuitem':    (4, {'normal': (none, none), 'focused': (hov, none),
                            'pressed': (hov, none), 'toggled': (hov, none)}, {}),
        'menubaritem': (4, {'normal': (none, none), 'focused': (hov, none),
                            'pressed': (hov, none), 'toggled': (hov, none)}, {}),
    }
    for base, (r, states, kw) in frames.items():
        for state, (fill, border) in states.items():
            S.frame(base, state, fill, border, r=r, **kw)

    # A selected row is a solid deep-cyan fill with a 2px leading edge — legible
    # without a focus outline fighting it.
    for state, fill in (('normal', none), ('focused', hov),
                        ('pressed', sel), ('toggled', sel)):
        S.frame('itemview', state, fill, cy if fill is sel else none, r=4, bw=2,
                sides=('left',), bws={'left': 2})

    # An active tab is accent text plus a 2px rule — no filled pill, no box.
    for state, (fill, under) in (('normal', (none, none)), ('focused', (none, cyd)),
                                 ('pressed', (none, cy)), ('toggled', (none, cy)),
                                 ('disabled', (none, none))):
        S.frame('tab', state, fill, under, r=3, bw=2, sides=('bottom',), bws={'bottom': 2})

    # Window and dialog grounds: interior only, no frame.
    S.plain('window-normal', f'<rect width="{K}" height="{K}" fill="{T["surface.window"]}"/>',
            K, K)

    # The focus ring is stateless — ids are focus-top, focus-topleft, ...
    S.frame('focus', '', none, cy, r=R, interior=False)
    return S


def indicators(S, T):
    cy, dis = T['accent.cyan'], T['text.disabled']
    ink = T['surface.void']
    tone = {'normal': T['text.dim'], 'focused': T['text.normal'],
            'pressed': T['text.normal'], 'toggled': cy, 'disabled': dis}
    box_tone = {
        'normal':   (T['surface.view'], T['border.strong']),
        'focused':  (T['surface.view'], cy),
        'pressed':  (T['surface.raised'], cy),
        'toggled':  (T['surface.view'], cy),
        'disabled': (T['surface.disabled'], T['border.disabled']),
    }
    checked_fill = {'normal': cy, 'focused': T['accent.cyan.hover'], 'pressed': T['accent.cyan.dim'],
                    'toggled': cy, 'disabled': T['border.disabled']}
    A, C = 16, 18

    for st in STATES:
        col = tone[st]
        for d in ('up', 'down', 'left', 'right'):
            S.plain(f'arrow-{d}-{st}', chevron(A, col, d), A, A)
            S.plain(f'spin-{d}-{st}', chevron(A, col, d), A, A)
        S.plain(f'spin-plus-{st}', _box(A, tick(A, col, 1.7)), A, A)
        S.plain(f'spin-minus-{st}', _box(A, dash(A, col, 1.7)), A, A)
        S.plain(f'tree-plus-{st}', chevron(A, col, 'right'), A, A)
        S.plain(f'tree-minus-{st}', chevron(A, col, 'down'), A, A)
        S.plain(f'tab-close-{st}', cross(A, col), A, A)
        S.plain(f'mdi-close-{st}', cross(A, T['status.negative'] if st in
                ('focused', 'pressed') else col), A, A)
        S.plain(f'mdi-minimize-{st}', _box(A, dash(A, col, 1.6)), A, A)
        S.plain(f'mdi-maximize-{st}', _box(A,
                f'<rect x="{A*0.24:.2f}" y="{A*0.24:.2f}" width="{A*0.52:.2f}" '
                f'height="{A*0.52:.2f}" rx="1.2" fill="none" stroke="{col}" '
                f'stroke-width="1.3"/>'), A, A)
        S.plain(f'mdi-restore-{st}', _box(A,
                f'<rect x="{A*0.32:.2f}" y="{A*0.18:.2f}" width="{A*0.46:.2f}" '
                f'height="{A*0.46:.2f}" rx="1.2" fill="none" stroke="{col}" '
                f'stroke-width="1.2"/>'
                f'<rect x="{A*0.20:.2f}" y="{A*0.34:.2f}" width="{A*0.46:.2f}" '
                f'height="{A*0.46:.2f}" rx="1.2" fill="{T["surface.window"]}" '
                f'stroke="{col}" stroke-width="1.2"/>'), A, A)
        S.plain(f'mdi-shade-{st}', chevron(A, col, 'up'), A, A)
        S.plain(f'mdi-menu-{st}', _box(A, f'<path d="M {A*0.25:.1f} {A*0.36:.1f} H {A*0.75:.1f} '
                f'M {A*0.25:.1f} {A*0.5:.1f} H {A*0.75:.1f} M {A*0.25:.1f} {A*0.64:.1f} '
                f'H {A*0.75:.1f}" stroke="{col}" stroke-width="1.3" stroke-linecap="round"/>'),
                A, A)

        fill, border = box_tone[st]
        S.plain(f'checkbox-{st}', _box(C, rounded_box(C, fill, border, 4, inset=1)), C, C)
        S.plain(f'radio-{st}', _box(C, disc(C, fill, border, inset=1)), C, C)
        cf = checked_fill[st]
        S.plain(f'checkbox-checked-{st}',
                _box(C, rounded_box(C, cf, cf, 4, inset=1) + tick(C, ink)), C, C)
        S.plain(f'checkbox-tristate-{st}',
                _box(C, rounded_box(C, cf, cf, 4, inset=1) + dash(C, ink)), C, C)
        S.plain(f'radio-checked-{st}',
                _box(C, disc(C, None, cf, bw=2, inset=1)
                     + f'<circle cx="{C/2}" cy="{C/2}" r="{C*0.22:.2f}" fill="{cf}"/>'), C, C)
        S.plain(f'slidercursor-{st}', _box(C, disc(C, cf, ink, bw=1.5, inset=1)), C, C)

        # Grips: three dots, the only ornament the theme allows itself.
        dots = ''.join(f'<circle cx="{A/2}" cy="{A*y:.2f}" r="1.1" fill="{col}"/>'
                       for y in (0.32, 0.5, 0.68))
        S.plain(f'resize-grip-{st}', _box(A, ''.join(
            f'<circle cx="{A*(0.72-i*0.18):.2f}" cy="{A*(0.72-j*0.18):.2f}" r="1.1" '
            f'fill="{col}"/>' for i in range(3) for j in range(3) if i + j < 3)), A, A)
        S.plain(f'splitter-grip-{st}', _box(A, dots), A, A)
        S.plain(f'toolbar-handle-{st}', _box(A, dots), A, A)
        S.plain(f'grip-{st}', _box(A, ''), A, A)
    return S


def kvconfig(T, THEME_NAME):
    """The widget spec. Sections are Kvantum's; values come from the design:
    32px primary controls, 28-30px compact rows, 7px radius, 1px border."""
    def sec(name, **kv):
        body = '\n'.join(f'{k.replace("__", ".")}={v}' for k, v in kv.items())
        return f'[{name}]\n{body}\n'

    F = dict(frame='true', frame__top=R, frame__bottom=R, frame__left=R, frame__right=R)

    def framed(element, r=R, interior=True, v=None, **extra):
        """`v` sets the vertical frame slices independently of the radius.

        A control's height is text height + frame.top + frame.bottom + the text
        margins, with no way to subtract: at a 7px slice top and bottom every
        primary control came out 38-40px against the artboard's 32. Narrowing
        only the vertical slices keeps the 7px horizontal radius and buys back
        the 6px, at the cost of corners that are 7 wide by `v` tall."""
        vv = r if v is None else v
        d = dict(frame='true', frame__element=element,
                 frame__top=vv, frame__bottom=vv, frame__left=r, frame__right=r,
                 interior='true' if interior else 'false')
        if interior:
            d['interior__element'] = element
        d.update(extra)
        return d

    out = [sec('%General',
               author='George',
               comment=f'{THEME_NAME} — cyan and magenta on blue-black, '
                       'accent only on focus, check and selection',
               x11drag='menubar_and_primary_toolbar',
               alt_mnemonic='true',
               left_tabs='true',
               attach_active_tab='false',
               mirror_doc_tabs='true',
               group_toolbar_buttons='false',
               toolbutton_style='0',
               slider_width='4',
               slider_handle_width='18',
               slider_handle_length='18',
               tickless_slider_handle_size='18',
               check_size='18',
               progressbar_thickness='6',
               menubar_mouse_tracking='true',
               toolbar_item_spacing='2',
               toolbar_interior_spacing='4',
               spin_button_width='18',
               inline_spin_indicators='true',
               vertical_spin_indicators='false',
               combo_as_lineedit='false',
               combo_menu='true',
               hide_combo_checkboxes='true',
               groupbox_top_label='true',
               scroll_width='11',
               scroll_arrows='false',
               scroll_min_extent='42',
               transient_scrollbar='false',
               transient_groove='false',
               fill_rubberband='true',
               merge_menubar_with_toolbar='true',
               small_icon_size='16',
               large_icon_size='32',
               button_icon_size='16',
               toolbar_icon_size='22',
               composite='true',
               menu_shadow_depth='0',
               tooltip_shadow_depth='0',
               splitter_width='4',
               layout_spacing='4',
               layout_margin='6',
               submenu_overlap='0',
               tooltip_delay='-1',
               animate_states='true',
               no_window_pattern='true',
               respect_DE='false',
               reduce_window_opacity='0',
               reduce_menu_opacity='0',
               shadowless_popup='true',
               no_inactiveness='false',
               dialog_button_layout='0',
               spread_progressbar='true')]

    C = dict(
        window__color=T['surface.window'],
        inactive__window__color=T['surface.window'],
        base__color=T['surface.view'],
        inactive__base__color=T['surface.view'],
        alt__base__color=T['surface.alt'],
        inactive__alt__base__color=T['surface.alt'],
        button__color=T['surface.raised'],
        light__color=T['surface.float'],
        mid__light__color=T['surface.hover'],
        dark__color=T['surface.void'],
        mid__color=T['border.hairline'],
        highlight__color=T['selection.bg'],
        inactive__highlight__color=T['surface.selected'],
        highlight__text__color=T['selection.fg'],
        inactive__highlight__text__color=T['selection.fg.dim'],
        text__color=T['text.normal'],
        inactive__text__color=T['text.dim'],
        window__text__color=T['text.normal'],
        inactive__window__text__color=T['text.dim'],
        button__text__color=T['text.normal'],
        inactive__button__text__color=T['text.dim'],
        disabled__text__color=T['text.disabled'],
        tooltip__base__color=T['tooltip.bg'],
        tooltip__text__color=T['text.normal'],
        link__color=T['accent.indigo'],
        link__visited__color=T['accent.indigo.visited'],
        progress__indicator__text__color=T['text.oncolor'],
        progress__inactive__indicator__text__color=T['text.dim'],
    )
    out.append(sec('GeneralColors', **C))

    out.append(sec('Hacks',
                   transparent_dolphin_view='false',
                   transparent_pcmanfm_sidepane='false',
                   blur_translucent='false',
                   transparent_menutitle='true',
                   respect_darkness='true',
                   force_size_grip='false',
                   iconless_pushbutton='false',
                   iconless_menu='false',
                   disabled_icon_opacity='50',
                   normal_default_pushbutton='true',
                   single_top_toolbar='true',
                   tint_on_mouseover='0',
                   no_selection_tint='true',
                   ))

    txt = dict(text__normal__color=T['text.normal'],
               text__focus__color=T['text.normal'],
               text__press__color=T['text.normal'],
               text__toggle__color=T['selection.fg'],
               text__normal__inactive__color=T['text.dim'])

    # A checked button's label goes cyan to match its box. Kept off the shared
    # `txt` dict: a toggled MENU item is just a hovered row, where cyan text
    # would be wrong.
    btn_txt = dict(txt, text__toggle__color=T['accent.cyan'])
    out.append(sec('PanelButtonCommand', **framed('button', v=V_PRIMARY),
                   indicator__element='arrow', indicator__size='12',
                   min_height=H_PRIMARY, min_width='+0.8font',
                   text__margin__top='1', text__margin__bottom='1',
                   text__margin__left='12', text__margin__right='12',
                   text__iconspacing='6', **btn_txt))
    out.append(sec('PanelButtonTool', **framed('toolbtn', v=V_PRIMARY),
                   indicator__element='arrow', indicator__size='12',
                   min_height=H_PRIMARY,
                   text__margin__top='1', text__margin__bottom='1',
                   text__margin__left='6', text__margin__right='6',
                   text__iconspacing='6', **btn_txt))
    out.append(sec('ToolbarButton', inherits='PanelButtonTool'))
    out.append(sec('DropDownButton', inherits='PanelButtonCommand',
                   indicator__element='arrow-down'))
    out.append(sec('ComboBox', **framed('combo', v=V_PRIMARY),
                   indicator__element='arrow-down',
                   indicator__size='12', min_height=H_PRIMARY,
                   text__margin__top='1', text__margin__bottom='1',
                   text__margin__left='10', text__margin__right='8', **txt))
    out.append(sec('LineEdit', **framed('lineedit', v=V_PRIMARY),
                   min_height=H_PRIMARY,
                   text__margin__top='1', text__margin__bottom='1',
                   text__margin__left='10', text__margin__right='10', **txt))
    out.append(sec('ToolbarLineEdit', inherits='LineEdit'))
    out.append(sec('ToolbarComboBox', inherits='ComboBox'))
    out.append(sec('IndicatorSpinBox', inherits='LineEdit',
                   indicator__element='spin', indicator__size='10'))
    out.append(sec('IndicatorArrow', indicator__element='arrow', indicator__size='12'))
    out.append(sec('CheckBox', indicator__element='checkbox', indicator__size='18',
                   text__margin__left='6', **txt))
    out.append(sec('RadioButton', indicator__element='radio', indicator__size='18',
                   text__margin__left='6', **txt))
    out.append(sec('Focus', frame='true', frame__element='focus',
                   frame__top=R, frame__bottom=R, frame__left=R, frame__right=R,
                   interior='false'))
    out.append(sec('GenericFrame', **framed('common', interior=False)))
    out.append(sec('Tab', frame='true', frame__element='tab',
                   frame__top='3', frame__bottom='3', frame__left='3', frame__right='3',
                   interior='true', interior__element='tab',
                   min_height=H_PRIMARY,
                   text__margin__top='1', text__margin__bottom='1',
                   text__margin__left='14', text__margin__right='14',
                   text__normal__color=T['text.dim'],
                   text__focus__color=T['text.normal'],
                   text__toggle__color=T['accent.cyan'],
                   text__press__color=T['accent.cyan']))
    out.append(sec('TabFrame', **framed('tabframe')))
    out.append(sec('TreeExpander', indicator__element='tree', indicator__size='12'))
    out.append(sec('HeaderSection', **framed('header', r=1),
                   min_height=H_ROW, text__margin__left='8', text__margin__right='8',
                   text__bold='true',
                   text__normal__color=T['accent.cyan'],
                   text__focus__color=T['accent.cyan'],
                   text__press__color=T['accent.cyan']))
    out.append(sec('SizeGrip', indicator__element='resize-grip', indicator__size='12'))
    out.append(sec('Toolbar', **framed('toolbar', r=1)))
    out.append(sec('MenuBar', **framed('menubar', r=1)))
    out.append(sec('MenuBarItem', **framed('menubaritem', r=4, v=3),
                   min_height=H_ROW, text__margin__top='0', text__margin__bottom='0',
                   text__margin__left='10', text__margin__right='10',
                   **txt))
    out.append(sec('Slider', **framed('slider', r=2)))
    out.append(sec('SliderCursor', frame='false', interior='true',
                   interior__element='slidercursor'))
    out.append(sec('Progressbar', **framed('progress', r=4),
                   min_height='+0.1font',
                   text__normal__color=T['text.normal']))
    out.append(sec('ProgressbarContents', **framed('progress-pattern', r=4)))
    out.append(sec('ItemView', **framed('itemview', r=4, v=2),
                   min_height=H_ROW,
                   text__margin__top='0', text__margin__bottom='0',
                   text__margin__left='6', text__margin__right='6',
                   text__normal__color=T['text.normal'],
                   text__focus__color=T['text.normal'],
                   text__toggle__color=T['selection.fg'],
                   text__press__color=T['selection.fg']))
    out.append(sec('Splitter', indicator__element='splitter-grip', indicator__size='12'))
    out.append(sec('Scrollbar', indicator__element='arrow', indicator__size='10'))
    out.append(sec('ScrollbarGroove', **framed('scrollbargroove', r=1, interior=False)))
    out.append(sec('ScrollbarSlider', **framed('scrollbarslider', r=5),
                   indicator__element='grip', indicator__size='10'))
    out.append(sec('MenuItem', **framed('menuitem', r=4, v=3),
                   indicator__element='arrow', indicator__size='12',
                   min_height=H_ROW,
                   text__margin__top='0', text__margin__bottom='0',
                   text__margin__left='10', text__margin__right='10',
                   text__iconspacing='8', **txt))
    out.append(sec('Menu', **framed('menu'), text__margin='0'))
    out.append(sec('TitleBar', **framed('titlebar', r=1),
                   indicator__element='mdi', indicator__size='16',
                   text__normal__color=T['text.normal'],
                   text__normal__inactive__color=T['text.title.inactive']))
    out.append(sec('GroupBox', **framed('group', interior=False),
                   text__bold='true', **txt))
    out.append(sec('ToolTip', **framed('tooltip', r=5), text__margin='4'))
    out.append(sec('Dock', **framed('dock', r=4)))
    out.append(sec('Window', frame='false', interior='true', interior__element='window'))
    out.append(sec('Dialog', inherits='Window'))
    return '\n'.join(out)


def build(T, DIST, THEME_ID, THEME_NAME):
    import re
    out = []
    S = artwork(T)
    indicators(S, T)
    svg = S.render()
    cfg = kvconfig(T, THEME_NAME)

    # Kvantum never reports a missing element — it quietly borrows one from its
    # built-in grey/purple default.svg. Every element the config names is
    # checked against the ids actually emitted, and a miss fails the build.
    missing = []
    for kind, base in re.findall(r'^(frame|interior|indicator)\.element=(.+)$', cfg, re.M):
        base = base.strip()
        if kind == 'frame':
            want = f'{base}-topleft' if base == 'focus' else f'{base}-normal-topleft'
            if want not in S.ids:
                missing.append(f'{kind}.element={base} (no {want})')
        elif kind == 'interior':
            if f'{base}-normal' not in S.ids:
                missing.append(f'{kind}.element={base} (no {base}-normal)')
        else:
            if not any(i == base or i.startswith(base + '-') for i in S.ids):
                missing.append(f'{kind}.element={base} (no {base}-* ids)')
    if missing:
        for m in sorted(set(missing)):
            out.append(f'  ! Kvantum element referenced but not drawn: {m}')

    d = DIST / 'kvantum' / THEME_ID
    d.mkdir(parents=True, exist_ok=True)
    (d / f'{THEME_ID}.kvconfig').write_text(cfg)
    (d / f'{THEME_ID}.svg').write_text(svg)
    out.append(f'kvantum/{THEME_ID}/{THEME_ID}.kvconfig')
    out.append(f'kvantum/{THEME_ID}/{THEME_ID}.svg  ({len(S.ids)} elements, {len(svg)} bytes)')
    return out
