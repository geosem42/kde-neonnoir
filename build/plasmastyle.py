"""The Plasma style's artwork — the piece that reshapes the SHELL.

A desktoptheme with no SVGs is not a neutral choice: KSvg falls back to the
`default` theme file by file, so every shell surface keeps Breeze's geometry
and only changes colour. That is what "a new coat of paint" looks like. This
module draws the surfaces from artboard 04 instead.

Fallback is per FILE, not per element, so any file shipped here must carry
every element the shell asks of it — a missing id draws nothing at all.

Colours are baked rather than routed through a `current-color-scheme`
stylesheet: the palette is fixed, and baking removes a whole class of
"why is it tinted wrong" question.
"""

R_BIG, R_MED, R_SMALL, BW = 10, 7, 5, 1


def _corner(r, bw, fill, border, fx, fy):
    """One rounded corner: an annular wedge for the border, a wedge inside."""
    if r <= bw:
        c = border or fill
        body = (f'<rect x="0" y="0" width="{max(r,bw)}" height="{max(r,bw)}" '
                f'fill="{c or "#000"}"{"" if c else " fill-opacity=\"0\""}/>')
        return body, max(r, bw)
    parts = [f'<rect x="0" y="0" width="{r}" height="{r}" fill="#000" fill-opacity="0"/>']
    if fill:
        parts.append(f'<path d="M {bw} {r} A {r-bw} {r-bw} 0 0 1 {r} {bw} L {r} {r} Z" '
                     f'fill="{fill}"/>')
    if border:
        parts.append(f'<path d="M 0 {r} A {r} {r} 0 0 1 {r} 0 L {r} {bw} '
                     f'A {r-bw} {r-bw} 0 0 0 {bw} {r} Z" fill="{border}"/>')
    t = ''
    if fx or fy:
        t = (f' transform="translate({r if fx else 0} {r if fy else 0}) '
             f'scale({-1 if fx else 1} {-1 if fy else 1})"')
    return f'<g{t}>{"".join(parts)}</g>', r


def _edge(r, bw, fill, border, side, K=24):
    w, h = (K, r) if side in ('top', 'bottom') else (r, K)
    parts = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="#000" fill-opacity="0"/>']
    if fill:
        parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{fill}"/>')
    if border:
        bx, by, bw_, bh = {'top': (0, 0, w, bw), 'bottom': (0, h - bw, w, bw),
                           'left': (0, 0, bw, h), 'right': (w - bw, 0, bw, h)}[side]
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw_}" height="{bh}" fill="{border}"/>')
    return ''.join(parts), (w, h)


class Sheet:
    def __init__(self):
        self.items, self.ids = [], set()

    def add(self, eid, body, w, h):
        if eid in self.ids:
            raise ValueError('duplicate id ' + eid)
        self.ids.add(eid)
        self.items.append((eid, body, w, h))

    def frame(self, prefix, fill, border, r=R_MED, bw=BW, margin=None, K=24):
        p = (prefix + '-') if prefix else ''
        for name, (fx, fy) in (('topleft', (0, 0)), ('topright', (1, 0)),
                               ('bottomleft', (0, 1)), ('bottomright', (1, 1))):
            body, s = _corner(r, bw, fill, border, fx, fy)
            self.add(p + name, body, s, s)
        for side in ('top', 'bottom', 'left', 'right'):
            body, (w, h) = _edge(r, bw, fill, border, side, K)
            self.add(p + side, body, w, h)
        self.add(p + 'center',
                 f'<rect x="0" y="0" width="{K}" height="{K}" '
                 f'fill="{fill}"/>' if fill else
                 f'<rect x="0" y="0" width="{K}" height="{K}" fill="#000" fill-opacity="0"/>',
                 K, K)
        if margin is not None:
            # An invisible rect whose SIZE is the content margin on that edge.
            for side in ('top', 'bottom', 'left', 'right'):
                w, h = (margin, margin) if True else (0, 0)
                self.add(f'{p}hint-{side}-margin',
                         f'<rect x="0" y="0" width="{w}" height="{h}" '
                         f'fill="#000" fill-opacity="0"/>', w, h)

    def plain(self, eid, body, w, h):
        self.add(eid, body, w, h)

    def render(self):
        pad, x, y, rowh, maxw = 8, 8, 8, 0, 0
        out = []
        for eid, body, w, h in self.items:
            if x + w > 760:
                x, y, rowh = 8, y + rowh + pad, 0
            out.append(f'<g id="{eid}" transform="translate({x} {y})">{body}</g>')
            x += w + pad
            rowh = max(rowh, h)
            maxw = max(maxw, x)
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{maxw}" '
                f'height="{y + rowh + pad}" viewBox="0 0 {maxw} {y + rowh + pad}">\n'
                + '\n'.join(out) + '\n</svg>\n')


def build(T, DIST, THEME_ID):
    import shutil
    out = []
    hair, flt, dis = T['border.hairline'], T['border.float'], T['border.disabled']
    cy, cyd = T['accent.cyan'], T['accent.cyan.dim']
    win, raised, view = T['surface.window'], T['surface.raised'], T['surface.view']
    hov, sel, alt = T['surface.hover'], T['selection.bg'], T['surface.alt']
    N = None

    def mask(s, prefix, r):
        """The blur mask: an opaque copy of the shape. Without it a translucent
        panel or popup gets no blur behind it."""
        s.frame(prefix, '#ffffff', N, r=r)

    files = {}

    # Panel: the floating bar from the design's "Panel variants".
    s = Sheet()
    s.frame('', win, hair, r=R_BIG, margin=4)
    mask(s, 'mask', R_BIG)
    s.frame('thick', win, hair, r=R_BIG, margin=8)
    files['widgets/panel-background.svg'] = s

    # Popups: launcher, clock, notifications.
    for path, fill, border, r in (('dialogs/background.svg', T['surface.float'], hair, R_BIG),
                                  ('widgets/tooltip.svg', T['tooltip.bg'], flt, R_MED)):
        s = Sheet()
        s.frame('', fill, border, r=r, margin=r)
        mask(s, 'mask', r)
        files[path] = s

    # Plasmoid background.
    s = Sheet()
    s.frame('', raised, hair, r=R_MED, margin=R_MED)
    files['widgets/background.svg'] = s

    # List rows — the launcher result row, cyan-filled when selected.
    s = Sheet()
    for p, fill, border in (('normal', N, N), ('hover', hov, N),
                            ('pressed', sel, cy), ('section', N, N)):
        s.frame(p, fill, border, r=R_MED, margin=4)
    s.plain('separator', f'<rect x="0" y="0" width="24" height="1" fill="{hair}"/>', 24, 1)
    files['widgets/listitem.svg'] = s

    s = Sheet()
    for p, fill in (('normal', N), ('hover', hov), ('selected', sel), ('selected+hover', sel)):
        s.frame(p, fill, cy if fill is sel else N, r=R_SMALL)
    files['widgets/viewitem.svg'] = s

    # Text entry: hairline at rest, cyan when focused.
    s = Sheet()
    for p, fill, border in (('base', view, hair), ('hover', view, T['decoration.hover']),
                            ('focus', view, cy), ('focusframe', N, cy)):
        s.frame(p, fill, border, r=R_MED, margin=6)
    files['widgets/lineedit.svg'] = s

    s = Sheet()
    for p, fill, border in (('normal', raised, hair), ('hover', hov, T['decoration.hover']),
                            ('pressed', T['surface.float'], cy), ('focus', N, cy),
                            ('toolbutton-hover', hov, N), ('toolbutton-pressed', sel, N),
                            ('toolbutton-focus', N, cy)):
        s.frame(p, fill, border, r=R_MED, margin=6)
    files['widgets/button.svg'] = s

    # Task manager. The active task is the one place the accent appears here.
    s = Sheet()
    tasks = (('normal', N, N), ('hover', hov, N), ('minimized', N, N),
             ('attention', T['status.neutral.ghost'], T['status.neutral']),
             ('progress', T['accent.cyan.ghost'], N), ('group-expander', N, hair))
    for edge in ('', 'north-', 'east-', 'west-'):
        for p, fill, border in tasks:
            s.frame(edge + p, fill, border, r=R_MED, margin=4)
        s.frame(edge + 'focus', raised, cy, r=R_MED, bw=2, margin=4)
    files['widgets/tasks.svg'] = s

    s = Sheet()
    for p, fill, border in (('plain', N, hair), ('raised', raised, hair), ('sunken', view, hair)):
        s.frame(p, fill, border, r=R_MED, margin=6)
    s.frame('border', N, hair, r=R_MED)
    files['widgets/frame.svg'] = s

    s = Sheet()
    for p in ('background-vertical', 'background-horizontal'):
        s.frame(p, N, N, r=R_SMALL)
    s.frame('slider', flt, N, r=R_SMALL)
    s.frame('mouseover-slider', cy, N, r=R_SMALL)
    s.plain('hint-scrollbar-size',
            '<rect x="0" y="0" width="11" height="11" fill="#000" fill-opacity="0"/>', 11, 11)
    files['widgets/scrollbar.svg'] = s

    # Active tab: accent rule, no filled pill — same rule as the Kvantum tabs.
    s = Sheet()
    for edge in ('north', 'south', 'east', 'west'):
        s.frame(f'{edge}-active-tab', raised, N, r=R_SMALL, margin=6)
    files['widgets/tabbar.svg'] = s

    root = DIST / 'desktoptheme' / THEME_ID
    for rel, sheet in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(sheet.render())
    # Opaque variants, used when compositing or blur is off.
    for src, dsts in (('dialogs/background.svg', ('opaque/dialogs/background.svg',)),
                      ('widgets/panel-background.svg',
                       ('opaque/widgets/panel-background.svg',
                        'solid/widgets/panel-background.svg'))):
        for d in dsts:
            (root / d).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(root / src, root / d)
    n = sum(len(s.ids) for s in files.values())
    out.append(f'desktoptheme/{THEME_ID}/  ({len(files) + 3} SVGs, {n} elements)')
    return out
