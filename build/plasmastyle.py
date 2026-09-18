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


# The task indicator: 2px thick, held 3px clear of the button edge, exactly as
# the artboard draws it. It lives only in the stretched edge element, never in
# the corners, which is what insets it from the ends of the button.
BAR_T, BAR_GAP = 2, 3


def _edge(r, bw, fill, border, side, K=24, bar=None, gap=None):
    w, h = (K, r) if side in ('top', 'bottom') else (r, K)
    parts = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="#000" fill-opacity="0"/>']
    if fill:
        parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{fill}"/>')
    if border:
        bx, by, bw_, bh = {'top': (0, 0, w, bw), 'bottom': (0, h - bw, w, bw),
                           'left': (0, 0, bw, h), 'right': (w - bw, 0, bw, h)}[side]
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw_}" height="{bh}" fill="{border}"/>')
    if bar:
        g = BAR_GAP if gap is None else gap
        bx, by, bw_, bh = {
            'top':    (0, g, w, BAR_T),
            'bottom': (0, h - g - BAR_T, w, BAR_T),
            'left':   (g, 0, BAR_T, h),
            'right':  (w - g - BAR_T, 0, BAR_T, h),
        }[side]
        parts.append(f'<rect x="{bx}" y="{by}" width="{bw_}" height="{bh}" fill="{bar}"/>')
    return ''.join(parts), (w, h)


class Sheet:
    def __init__(self):
        self.items, self.ids = [], set()

    def add(self, eid, body, w, h):
        if eid in self.ids:
            raise ValueError('duplicate id ' + eid)
        self.ids.add(eid)
        self.items.append((eid, body, w, h))

    def frame(self, prefix, fill, border, r=R_MED, bw=BW, margin=None, K=24,
              bar=None, bar_side='bottom', bar_gap=None):
        p = (prefix + '-') if prefix else ''
        for name, (fx, fy) in (('topleft', (0, 0)), ('topright', (1, 0)),
                               ('bottomleft', (0, 1)), ('bottomright', (1, 1))):
            body, s = _corner(r, bw, fill, border, fx, fy)
            self.add(p + name, body, s, s)
        for side in ('top', 'bottom', 'left', 'right'):
            body, (w, h) = _edge(r, bw, fill, border, side, K,
                                 bar if side == bar_side else None, bar_gap)
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

    # Popups: launcher, clock, notifications. The window surface, not the
    # floating one: the artboard draws the launcher a step above its near-black
    # ground, but on a real desktop that step reads as a grey slab next to the
    # panel and the window chrome, which are both surface.window. A hairline
    # border carries the elevation instead.
    for path, fill, border, r in (('dialogs/background.svg', T['surface.window'], flt, R_BIG),
                                  ('widgets/tooltip.svg', T['tooltip.bg'], flt, R_MED)):
        s = Sheet()
        s.frame('', fill, border, r=r, margin=r)
        mask(s, 'mask', r)
        files[path] = s

    # Plasmoid background.
    s = Sheet()
    s.frame('', raised, hair, r=R_MED, margin=R_MED)
    files['widgets/background.svg'] = s

    # List rows. The artboard marks the current row with a solid deep-cyan fill
    # and a 2px cyan leading edge — not a grey pill.
    #
    # `hover` carries it too, not a lighter wash: the launcher and KRunner both
    # drive the CURRENT row through hover rather than selected, so a subtler
    # hover state means keyboard navigation shows almost nothing. These two
    # files only reach Plasma's own surfaces — launcher, KRunner, notifications,
    # tray popups — where pointing at a row and landing on it are the same
    # thing. Qt applications take their rows from Kvantum instead.
    s = Sheet()
    for p, fill, bar in (('normal', N, None), ('hover', sel, cy),
                         ('pressed', sel, cy), ('section', N, None)):
        s.frame(p, fill, N, r=R_MED, margin=4, bar=bar, bar_side='left', bar_gap=0)
    s.plain('separator', f'<rect x="0" y="0" width="24" height="1" fill="{hair}"/>', 24, 1)
    files['widgets/listitem.svg'] = s

    s = Sheet()
    for p, fill, bar in (('normal', N, None), ('hover', sel, cy),
                         ('selected', sel, cy), ('selected+hover', sel, cy)):
        s.frame(p, fill, N, r=R_SMALL, bar=bar, bar_side='left', bar_gap=0)
    files['widgets/viewitem.svg'] = s

    # Text entry: hairline at rest, cyan when focused.
    s = Sheet()
    # Only `base` carries the content inset. TextFieldFocus.qml anchors the
    # hover/focus overlay with NEGATIVE margins equal to that prefix's own
    # margins, so a 6px margin on `hover` paints the overlay 6px outside the
    # field on every side — which is the field appearing to swell on hover.
    # Breeze sets these to 0.001: small enough to add nothing, non-zero so the
    # element still has bounds KSvg can measure.
    for p, fill, border, m in (('base', view, hair, 6),
                               ('hover', view, T['decoration.hover'], 0.001),
                               ('focus', view, cy, 0.001),
                               ('focusframe', N, cy, 2)):
        s.frame(p, fill, border, r=R_MED, margin=m)
    # Presence alone is the signal: with this element Plasma paints the focus
    # frame OVER the field, without it the field grows to make room for a ring
    # drawn outside — which is why the search box swelled on hover.
    s.plain('hint-focus-over-base',
            '<rect x="0" y="0" width="2" height="2" fill="#000" fill-opacity="0"/>', 2, 2)
    files['widgets/lineedit.svg'] = s

    s = Sheet()
    for p, fill, border in (('normal', raised, hair), ('hover', hov, T['decoration.hover']),
                            ('pressed', T['surface.float'], cy), ('focus', N, cy),
                            ('toolbutton-hover', hov, N), ('toolbutton-pressed', sel, N),
                            ('toolbutton-focus', N, cy)):
        s.frame(p, fill, border, r=R_MED, margin=6)
    files['widgets/button.svg'] = s

    # Task manager. The artboard marks state with a RULE under the button, not
    # with a border box: the active task gets a raised pill plus a cyan rule, a
    # running task gets the rule alone, and a launcher gets nothing. A 2px
    # accent border here is what made every open window look boxed in.
    #
    # The prefix names the panel edge, so the rule has to move with it: a top
    # panel underlines along its own bottom edge visually, which in FrameSvg
    # terms is the 'top' element for the 'north-' set.
    s = Sheet()
    dim = T['text.disabled']
    tasks = (('normal', N, N, dim), ('hover', hov, N, dim),
             ('minimized', N, N, T['text.faint']),
             ('attention', N, N, T['status.neutral']),
             ('progress', T['accent.cyan.ghost'], N, None),
             ('focus', raised, N, cy))
    for edge, side in (('', 'bottom'), ('north-', 'top'),
                       ('east-', 'right'), ('west-', 'left')):
        for p, fill, border, bar in tasks:
            s.frame(edge + p, fill, border, r=R_MED, margin=4,
                    bar=bar, bar_side=side)
        # The badge Plasma stamps on a task that owns more than one window —
        # the only cue that an app has several instances, since every task
        # draws the same indicator bar whatever its window count. It was an
        # invisible transparent rect, so the cue was simply missing. A solid
        # The badge Plasma stamps on a task that owns more than one window —
        # the only cue that an app has several instances, since every task draws
        # the same bar whatever its window count. Ours was a transparent rect,
        # so the cue was rendered all along and simply invisible.
        #
        # Built slice by slice rather than with frame(): the gap that separates
        # the dot from the bar has to be on the LEFT and RIGHT only. Plasma
        # centres this element on the panel's bottom edge and clips the lower
        # half, so a border along the top would eat most of the few pixels that
        # survive, and a cyan dot on the active task's cyan bar would merge
        # into it again.
        gap, dot = T['surface.void'], cy
        GW, GH, DW = 2, 3, 5      # gap width, slice height, dot width
        for e in ('topleft', 'bottomleft', 'left'):
            s.add(f'{edge}group-expander-{e}',
                  f'<rect x="0" y="0" width="{GW}" height="{GH}" fill="{gap}"/>', GW, GH)
        for e in ('topright', 'bottomright', 'right'):
            s.add(f'{edge}group-expander-{e}',
                  f'<rect x="0" y="0" width="{GW}" height="{GH}" fill="{gap}"/>', GW, GH)
        for e in ('top', 'bottom', 'center'):
            s.add(f'{edge}group-expander-{e}',
                  f'<rect x="0" y="0" width="{DW}" height="{GH}" fill="{dot}"/>', DW, GH)
    files['widgets/tasks.svg'] = s

    # Virtual-desktop pager. One tile per desktop, and unlike every other
    # surface in this theme the tile IS a box: the element stands for a screen,
    # so a rule under it would say nothing. Three states only — Plasma asks
    # `widgets/pager` for `normal`, `hover` and `active`, and a file that ships
    # any of them must ship all three, since KSvg falls back per FILE.
    #
    # R_SMALL, not R_MED: at a 48px panel the tile is roughly 24px tall, and the
    # medium radius eats the straight run of every edge.
    s = Sheet()
    for p_, fill, border in (('normal', view, hair),
                             ('hover', hov, T['decoration.hover']),
                             ('active', T['accent.cyan.ghost'], cy)):
        s.frame(p_, fill, border, r=R_SMALL, margin=2)
    files['widgets/pager.svg'] = s

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
    # It was a filled pill, which the comment already denied, and the fill is
    # opaque: the show-desktop applet draws this element OVER its icon as its
    # "active" marker (it is the last child, so it paints last), so clicking the
    # button covered the icon with a plain raised box and left a blank slot in
    # the panel. As a rule it marks the state and leaves the glyph alone.
    #
    # The rule goes on the edge the prefix names, which for the applet is the
    # panel's outer edge — the same place, and the same 2px, as the underline
    # under a running task.
    s = Sheet()
    for edge, side in (('north', 'top'), ('south', 'bottom'),
                       ('east', 'right'), ('west', 'left')):
        s.frame(f'{edge}-active-tab', N, N, r=R_SMALL, margin=6,
                bar=cy, bar_side=side)
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
