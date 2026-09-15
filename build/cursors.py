"""Neon Noir cursor theme — XCursor binaries generated from SVG, no external tools.

Every cursor is drawn on a 32-unit design grid, rendered with cairosvg at each
nominal size, and written straight into the XCursor container format. The format
constants below were not taken from documentation: they were read back out of
/usr/share/icons/breeze_cursors/cursors/left_ptr with a decoder, because the
image chunk type is 0xfffd0002 (type | subtype), not the 0xfffd the Xcursor
headers suggest.

Nominal vs pixel size: a "size 24" cursor is a 32px image. That 4:3 ratio is the
convention breeze uses and what the Plasma cursor-size KCM expects, so the art is
drawn to fill 32 units and every nominal size is nominal * 4/3 pixels.
"""
import io, math, struct

# ── XCursor container ─────────────────────────────────────────────────────────
XC_MAGIC        = b'Xcur'
XC_FILE_HEADER  = 16
XC_FILE_VERSION = 0x00010000
XC_CHUNK_IMAGE  = 0xfffd0002   # verified against breeze_cursors/left_ptr
XC_IMAGE_HEADER = 36
XC_IMAGE_VERSION = 1


def write_xcursor(path, frames):
    """frames: [(nominal, px, xhot, yhot, delay_ms, premultiplied_argb_bytes)]

    Frames must already be grouped by nominal size and ordered within a group;
    libXcursor plays an animation by walking table-of-contents order.
    """
    n = len(frames)
    toc, chunks, pos = b'', b'', XC_FILE_HEADER + 12 * n
    for nominal, px, xh, yh, delay, pixels in frames:
        toc += struct.pack('<III', XC_CHUNK_IMAGE, nominal, pos)
        chunks += struct.pack('<9I', XC_IMAGE_HEADER, XC_CHUNK_IMAGE, nominal,
                              XC_IMAGE_VERSION, px, px, xh, yh, delay) + pixels
        pos += XC_IMAGE_HEADER + len(pixels)
    path.write_bytes(struct.pack('<4sIII', XC_MAGIC, XC_FILE_HEADER,
                                 XC_FILE_VERSION, n) + toc + chunks)


def render(svg, px):
    """SVG -> premultiplied ARGB32 little-endian, which is what XCursor stores."""
    import cairosvg, numpy as np
    from PIL import Image
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)
    a = np.asarray(Image.open(io.BytesIO(png)).convert('RGBA'), dtype=np.uint32)
    alpha = a[..., 3]
    # Straight alpha from the PNG; XCursor wants it premultiplied.
    r = (a[..., 0] * alpha + 127) // 255
    g = (a[..., 1] * alpha + 127) // 255
    b = (a[..., 2] * alpha + 127) // 255
    return ((alpha << 24) | (r << 16) | (g << 8) | b).astype('<u4').tobytes()


# ── drawing primitives ────────────────────────────────────────────────────────
# A cursor is a list of closed shapes. They are painted in three passes — halo,
# outline, fill — over the whole shape list rather than per shape, so that
# overlapping parts (fingers on a palm) keep their separating outline without
# the halo of one part dirtying the fill of the next.

def rect(x, y, w, h, rx=0, fill=None):
    return ('rect', f'x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}"', fill)

def path(d, fill=None, evenodd=False):
    return ('path', f'd="{d}"' + (' fill-rule="evenodd"' if evenodd else ''), fill)

def circle(cx, cy, r, fill=None):
    return ('circle', f'cx="{cx:g}" cy="{cy:g}" r="{r:g}"', fill)

def _pt(cx, cy, r, deg):
    a = math.radians(deg)
    return f'{cx + r * math.cos(a):.3f} {cy + r * math.sin(a):.3f}'

def ring(cx, cy, ro, ri, fill=None):
    """Full annulus as one even-odd path, so the hole is a real hole."""
    d = (f'M {cx - ro:g} {cy:g} a {ro:g} {ro:g} 0 1 0 {2 * ro:g} 0 '
         f'a {ro:g} {ro:g} 0 1 0 {-2 * ro:g} 0 Z '
         f'M {cx - ri:g} {cy:g} a {ri:g} {ri:g} 0 1 1 {2 * ri:g} 0 '
         f'a {ri:g} {ri:g} 0 1 1 {-2 * ri:g} 0 Z')
    return path(d, fill, evenodd=True)

def arc_ring(cx, cy, ro, ri, a0, a1, fill=None):
    """Annular sector from a0 to a1 degrees, clockwise, 0 deg = east."""
    large = 1 if (a1 - a0) % 360 > 180 else 0
    d = (f'M {_pt(cx, cy, ro, a0)} A {ro:g} {ro:g} 0 {large} 1 {_pt(cx, cy, ro, a1)} '
         f'L {_pt(cx, cy, ri, a1)} A {ri:g} {ri:g} 0 {large} 0 {_pt(cx, cy, ri, a0)} Z')
    return path(d, fill)

def bar(x1, y1, x2, y2, w, fill=None):
    """A rectangle of width w laid along a segment — used for handles and slashes."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return path(f'M {x1 + nx:.3f} {y1 + ny:.3f} L {x2 + nx:.3f} {y2 + ny:.3f} '
                f'L {x2 - nx:.3f} {y2 - ny:.3f} L {x1 - nx:.3f} {y1 - ny:.3f} Z', fill)

def rot(shapes, deg, cx=16, cy=16):
    return ('group', shapes, f'rotate({deg:g} {cx:g} {cy:g})')

def flipx(shapes, cx=16):
    return ('group', shapes, f'translate({2 * cx:g} 0) scale(-1 1)')


def _walk(shapes, pass_attrs, body):
    out = []
    for s in shapes:
        if s[0] == 'group':
            out.append(f'<g transform="{s[2]}">{_walk(s[1], pass_attrs, body)}</g>')
        else:
            tag, geom, fill = s
            out.append(f'<{tag} {geom} {pass_attrs(fill or body)}/>')
    return ''.join(out)


def svg_document(shapes, overlay, C):
    """Halo, outline, fill — in that order over the whole shape list.

    The halo is a wide low-opacity ink stroke. It is doing the job a drop shadow
    would do, which cairosvg cannot render: it keeps a light cursor readable when
    it crosses a light window, without needing an SVG filter.
    """
    halo = _walk(shapes, lambda f: f'fill="none" stroke="{C["ink"]}" stroke-width="3.1" '
                 'stroke-opacity="0.34" stroke-linejoin="round" stroke-linecap="round"', C['body'])
    line = _walk(shapes, lambda f: f'fill="none" stroke="{C["ink"]}" stroke-width="1.5" '
                 'stroke-linejoin="round" stroke-linecap="round"', C['body'])
    fill = _walk(shapes, lambda f: f'fill="{f}" stroke="none"', C['body'])
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" '
            f'viewBox="0 0 32 32" shape-rendering="geometricPrecision">'
            f'{halo}{line}{fill}{overlay}</svg>')


def badge(cx, cy, r, C, glyph):
    """A dark chip with a cyan rim, carrying a stroked glyph.

    Badged cursors are state cursors — copy, help, alias — so by the theme's own
    rule they are the one place the accent is allowed to appear on a cursor.
    """
    chip = [circle(cx, cy, r, C['chip'])]
    over = (f'<circle cx="{cx:g}" cy="{cy:g}" r="{r - 0.75:g}" fill="none" '
            f'stroke="{C["cyan"]}" stroke-width="1.1"/>'
            f'<g fill="none" stroke="{C["cyan"]}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round">{glyph}</g>')
    return chip, over


def xf(shapes, transform):
    return ('group', shapes, transform)

def scaled(shapes, k, cx=16, cy=16):
    return xf(shapes, f'translate({cx:g} {cy:g}) scale({k:g}) translate({-cx:g} {-cy:g})')


# ── the catalogue ─────────────────────────────────────────────────────────────
# Hotspots follow breeze's, read out of its own cursor files, so muscle memory
# carries over. The exceptions are the window-edge and corner cursors: breeze
# anchors those at the corner of an L-shaped glyph, and these are plain double
# arrows, so they are centred on the pointer instead and symlinked to the
# matching resize arrow.

ARROW = ('M 4 3.5 L 16.14 18.11 L 11.53 19.78 L 13.69 26.65 '
         'L 10.53 27.79 L 8.37 20.92 L 4 22.5 Z')

FLEUR = ('M 16 3 L 21 9 L 18.6 9 L 18.6 13.4 L 23 13.4 L 23 11 L 29 16 L 23 21 '
         'L 23 18.6 L 18.6 18.6 L 18.6 23 L 21 23 L 16 29 L 11 23 L 13.4 23 '
         'L 13.4 18.6 L 9 18.6 L 9 21 L 3 16 L 9 11 L 9 13.4 L 13.4 13.4 '
         'L 13.4 9 L 11 9 Z')

DBL_ARROW = ('M 16 3.5 L 22 12 L 18.4 12 L 18.4 20 L 22 20 L 16 28.5 L 10 20 '
             'L 13.6 20 L 13.6 12 L 10 12 Z')

ONE_ARROW = 'M 16 3.5 L 23.5 13 L 18.8 13 L 18.8 28 L 13.2 28 L 13.2 13 L 8.5 13 Z'

IBEAM = ('M 11 6 L 21 6 L 21 8.4 L 17.3 8.4 L 17.3 23.6 L 21 23.6 L 21 26 '
         'L 11 26 L 11 23.6 L 14.7 23.6 L 14.7 8.4 L 11 8.4 Z')


def catalogue(C):
    cy, neg, ink = C['cyan'], C['negative'], C['ink']
    arrow = [path(ARROW)]

    def forbidden(cx_, cy_, ro, ri, w):
        return [ring(cx_, cy_, ro, ri, neg),
                bar(cx_ - ro * 0.72, cy_ + ro * 0.72, cx_ + ro * 0.72, cy_ - ro * 0.72, w, neg)]

    def spinner(cx_, cy_, ro, ri, deg):
        return [ring(cx_, cy_, ro, ri, C['body']),
                arc_ring(cx_, cy_, ro, ri, deg, deg + 110, cy)]

    def badged(glyph, gw=1.7):
        chip, over = badge(23, 23, 6.6, C, glyph)
        if gw != 1.7:
            over = over.replace('stroke-width="1.7"', f'stroke-width="{gw:g}"')
        return arrow + chip, over

    pencil = [
        path('M 4.42 23.34 L 8.66 27.58 L 10.78 25.46 L 6.54 21.22 Z'),          # collar
        path('M 6.54 21.22 L 10.78 25.46 L 23.50 12.74 L 19.26 8.50 Z'),          # barrel
        path('M 19.26 8.50 L 23.50 12.74 L 26.33 9.91 L 22.09 5.67 Z', C['grip']),
        path('M 3 29 L 4.42 23.34 L 8.66 27.58 Z'),                               # sharpened point
    ]
    graphite = 'M 3 29 L 3.56 26.74 L 5.26 28.44 Z'

    magnifier = [ring(13.5, 13.5, 9.0, 6.4), bar(18.5, 18.5, 28, 28, 4.2)]

    hand_open = [
        rect(9.4, 13.8, 13.2, 12.6, 4.6),
        rect(10.1, 8.0, 3.4, 9.5, 1.7), rect(13.9, 6.2, 3.4, 11.5, 1.7),
        rect(17.7, 7.2, 3.4, 10.5, 1.7), rect(21.2, 10.0, 3.2, 8.0, 1.6),
        xf([rect(5.6, 14.6, 3.4, 8.0, 1.7)], 'rotate(-28 7.3 18.6)'),
    ]
    hand_shut = [
        rect(9.4, 13.0, 13.2, 13.2, 4.6),
        rect(10.2, 10.2, 3.2, 5.4, 1.6), rect(13.8, 9.6, 3.2, 6.0, 1.6),
        rect(17.4, 10.0, 3.2, 5.6, 1.6), rect(20.8, 11.2, 3.0, 4.6, 1.5),
        rect(7.6, 16.6, 7.2, 3.4, 1.7),
    ]
    hand_point = [
        rect(11.3, 13.5, 12.4, 13.5, 4.2), rect(14.2, 3.5, 3.6, 14.5, 1.8),
        rect(17.9, 11.0, 3.3, 6.5, 1.65), rect(20.6, 12.2, 3.2, 5.5, 1.6),
        rect(8.9, 16.2, 4.8, 3.4, 1.7),
    ]
    cross = [rect(15.1, 2.5, 1.8, 9.5), rect(15.1, 20, 1.8, 9.5),
             rect(2.5, 15.1, 9.5, 1.8), rect(20, 15.1, 9.5, 1.8)]
    col = [rect(15.2, 5.5, 1.6, 21, 0.8),
           path('M 2.5 16 L 10 11 L 10 21 Z'), path('M 29.5 16 L 22 11 L 22 21 Z')]
    # Drawn along +x from the tip and rotated into place, which keeps the
    # eyedropper's proportions readable instead of solving them by hand.
    dropper = [xf([path('M 3 28 L 9 25.4 L 9 30.6 Z', cy),
                   rect(9, 25.7, 6.0, 4.6),
                   rect(14.5, 23.9, 3.0, 8.2, 1.0),
                   rect(17.5, 23.4, 11.0, 9.2, 3.4)], 'rotate(-45 3 28)')]
    skull = [circle(16, 12.5, 8.2), rect(11.5, 17, 9, 7.5, 2.2)]
    skull_face = (f'<g fill="{ink}"><circle cx="12.6" cy="12" r="2.5"/>'
                  f'<circle cx="19.4" cy="12" r="2.5"/>'
                  f'<path d="M 16 15.2 L 17.4 18 L 14.6 18 Z"/></g>'
                  f'<g stroke="{ink}" stroke-width="1.1"><path d="M 13.6 19.6 V 23.8 '
                  f'M 16 19.6 V 23.8 M 18.4 19.6 V 23.8"/></g>')

    C_ = {}
    def add(name, shapes, hot, overlay='', frames=None):
        C_[name] = dict(shapes=shapes, hot=hot, overlay=overlay, frames=frames)

    add('default',        arrow,                   (4, 4))
    add('wayland-cursor', arrow,                   (4, 4))
    add('right_ptr',      [flipx(arrow)],          (28, 4))
    add('center_ptr',     [path('M 16 3 L 23.6 24.5 L 16 20.4 L 8.4 24.5 Z')], (16, 4))
    add('pointer',        hand_point,              (16, 4))
    add('openhand',       hand_open,               (16, 16))
    add('dnd-move',       hand_shut,               (16, 16))
    add('text',           [path(IBEAM)],           (16, 16))
    add('vertical-text',  [rot([path(IBEAM)], 90)], (16, 16))
    add('crosshair',      cross,                   (16, 16))
    add('x-cursor',       [rot([rect(15.1, 3, 1.8, 26), rect(3, 15.1, 26, 1.8)], 45)], (16, 16))
    add('cell',           cross + [path('M 10.5 10.5 H 21.5 V 21.5 H 10.5 Z '
                                        'M 13 13 H 19 V 19 H 13 Z', evenodd=True)], (16, 16))
    add('fleur',          [path(FLEUR)],           (16, 16))
    add('all-scroll',     [path(FLEUR)],           (16, 16),
        f'<circle cx="16" cy="16" r="2.3" fill="{ink}"/>')
    add('size_ver',       [path(DBL_ARROW)],       (16, 16))
    add('size_hor',       [rot([path(DBL_ARROW)], 90)], (16, 16))
    add('size_bdiag',     [rot([scaled([path(DBL_ARROW)], 1.18)], 45)],  (16, 16))
    add('size_fdiag',     [rot([scaled([path(DBL_ARROW)], 1.18)], -45)], (16, 16))
    add('col-resize',     col,                     (16, 16))
    add('row-resize',     [rot(col, 90)],          (16, 16))
    add('up-arrow',       [path(ONE_ARROW)],       (16, 4))
    add('down-arrow',     [rot([path(ONE_ARROW)], 180)], (16, 28))
    add('left-arrow',     [rot([path(ONE_ARROW)], -90)], (4, 16))
    add('right-arrow',    [rot([path(ONE_ARROW)], 90)],  (28, 16))
    add('pencil',         pencil, (3, 29), f'<path d="{graphite}" fill="{ink}"/>')
    add('draft',          pencil, (3, 29), f'<path d="{graphite}" fill="{cy}"/>')
    add('color-picker',   dropper,                 (3, 28))
    add('zoom-in',        magnifier, (14, 14),
        f'<g fill="none" stroke="{cy}" stroke-width="1.9" stroke-linecap="round">'
        f'<path d="M 9.9 13.5 H 17.1 M 13.5 9.9 V 17.1"/></g>')
    add('zoom-out',       magnifier, (14, 14),
        f'<g fill="none" stroke="{cy}" stroke-width="1.9" stroke-linecap="round">'
        f'<path d="M 9.9 13.5 H 17.1"/></g>')
    add('not-allowed',    forbidden(16, 16, 10, 6.8, 4.2), (16, 16))
    add('no-drop',        arrow + forbidden(23, 23, 6.6, 4.4, 2.8), (4, 4))
    add('dnd-no-drop',    hand_shut + forbidden(23.5, 23.5, 6.0, 4.0, 2.6), (16, 16))
    add('pirate',         skull, (16, 16), skull_face)

    for name, glyph, gw in (
        ('help',         '<path d="M 20.9 21.5 a 2.2 2.2 0 1 1 2.2 2.5 v 0.8"/>'
                         '<path d="M 23.1 26.3 v 0.01"/>', 1.7),
        ('copy',         '<path d="M 23 19.6 V 26.4 M 19.6 23 H 26.4"/>', 1.7),
        ('alias',        '<path d="M 20.2 25.8 L 25.8 20.2"/>'
                         '<path d="M 21.6 20.2 H 25.8 V 24.4"/>', 1.5),
        ('context-menu', '<path d="M 20.1 20.7 H 25.9 M 20.1 23 H 25.9 M 20.1 25.3 H 25.9"/>', 1.2),
    ):
        s, o = badged(glyph, gw)
        add(name, s, (4, 4), o)

    add('wait',     None, (16, 16), frames=[spinner(16, 16, 10.5, 6.6, i * 30) for i in range(12)])
    add('progress', None, (4, 4),
        frames=[arrow + spinner(23, 23, 6.6, 4.2, i * 30) for i in range(12)])
    return C_


# Every alias breeze ships, so apps that ask for an X11 name, a CSS name or one
# of the MD5-named GTK drag cursors all resolve. Chains are flattened: each link
# points straight at a real file.
LINKS = {
    'arrow': 'default', 'top_left_arrow': 'default', 'left_ptr': 'default',
    'size-bdiag': 'size_bdiag', 'size-fdiag': 'size_fdiag',
    'size-hor': 'size_hor', 'size-ver': 'size_ver',
    'ibeam': 'text', 'xterm': 'text',
    'cross': 'crosshair', 'tcross': 'crosshair', 'plus': 'cell',
    'hand1': 'pointer', 'hand2': 'pointer', 'pointing_hand': 'pointer',
    'grab': 'openhand', 'closedhand': 'dnd-move', 'grabbing': 'dnd-move',
    'move': 'dnd-move', 'dnd-none': 'dnd-move',
    'circle': 'not-allowed', 'crossed_circle': 'not-allowed', 'forbidden': 'no-drop',
    'dnd-copy': 'copy', 'link': 'alias',
    'left_ptr_help': 'help', 'question_arrow': 'help', 'whats_this': 'help',
    'left_ptr_watch': 'progress', 'half-busy': 'progress', 'watch': 'wait',
    'size_all': 'fleur',
    'e-resize': 'size_hor', 'w-resize': 'size_hor', 'ew-resize': 'size_hor',
    'h_double_arrow': 'size_hor', 'sb_h_double_arrow': 'size_hor',
    'left_side': 'size_hor', 'right_side': 'size_hor',
    'n-resize': 'size_ver', 's-resize': 'size_ver', 'ns-resize': 'size_ver',
    'v_double_arrow': 'size_ver', 'sb_v_double_arrow': 'size_ver',
    'top_side': 'size_ver', 'bottom_side': 'size_ver',
    'ne-resize': 'size_bdiag', 'sw-resize': 'size_bdiag', 'nesw-resize': 'size_bdiag',
    'top_right_corner': 'size_bdiag', 'bottom_left_corner': 'size_bdiag',
    'nw-resize': 'size_fdiag', 'se-resize': 'size_fdiag', 'nwse-resize': 'size_fdiag',
    'top_left_corner': 'size_fdiag', 'bottom_right_corner': 'size_fdiag',
    'split_h': 'col-resize', 'split_v': 'row-resize',
    # Names KWin's alternative-name table requests that breeze_cursors does not
    # ship; breeze only gets away with it because an earlier alias in the same
    # group happens to hit first.
    'all_scroll': 'all-scroll', 'all-resize': 'fleur', 'centre_ptr': 'center_ptr',
    'bd_double_arrow': 'size_bdiag', 'fd_double_arrow': 'size_fdiag',
    'dnd-ask': 'context-menu', 'dnd-link': 'alias',
    'cross-reverse': 'crosshair', 'diamond-cross': 'crosshair', 'X_cursor': 'x-cursor',
    'base_arrow_up': 'up-arrow', 'based_arrow_up': 'up-arrow', 'sb_up_arrow': 'up-arrow',
    'base_arrow_down': 'down-arrow', 'based_arrow_down': 'down-arrow',
    'sb_down_arrow': 'down-arrow',
    'op_left_arrow': 'left-arrow', 'sb_left_arrow': 'left-arrow',
    'sb_right_arrow': 'right-arrow',
    # X11 cursor-font hashes used by GTK/Firefox drag and drop.
    '00000000000000020006000e7e9ffc3f': 'progress',
    '08e8e1c95fe2fc01f976f1e063a24ccd': 'progress',
    '3ecb610c1bf2410f44200f48c40d3599': 'progress',
    '00008160000006810000408080010102': 'size_ver',
    '03b6e0fcb3499374a867c041f52298f0': 'not-allowed',
    '1081e37283d90000800003c07f3ef6bf': 'copy',
    '6407b0e94181790501fd1e167b474872': 'copy',
    'b66166c04f8c3109214a4fbd64a50fc8': 'copy',
    '3085a0e285430894940527032f8b26df': 'alias',
    '640fb0e74195791501fd1ed57b41487f': 'alias',
    'a2a266d0498c3104214a47bd64ab0fc8': 'alias',
    '4498f0e0c1937ffe01fd06f973665830': 'dnd-move',
    '9081237383d90e509aa00f00170e968f': 'dnd-move',
    'fcf21c00b30f7e3f83fe0dfd12e71cff': 'dnd-move',
    '5c6cd98b3f3ebcb1f9c7f1c204630408': 'help',
    'd9ce0ab605698f320427677b458ad60b': 'help',
    '9d800788f1b08800ae810202380a0822': 'pointer',
    'e29285e634086352946a0e7090d73106': 'pointer',
}

# Nominal sizes the theme offers in the cursor-size KCM. Breeze ships 12..72 in
# steps of 6; the in-between steps are dropped here because each one costs
# ~1 MB across the theme and no HiDPI scale factor lands on them.
NOMINALS = (12, 18, 24, 30, 36, 48, 60, 72)
# Breeze stamps 50ms on static cursors too, and xcursorgen defaults to 50 when
# the delay column is omitted. A zero delay on an animated cursor is a
# busy-loop hazard, so neither case is left at 0.
STATIC_MS, ANIM_MS = 50, 50


def build(T, DIST, THEME_ID, THEME_NAME):
    out = []
    C = {
        'body':     T['selection.fg'],      # lighter than text.normal: a cursor is
        'ink':      T['surface.void'],      # read against everything, not just chrome
        'cyan':     T['accent.cyan'],
        'negative': T['status.negative'],
        'chip':     T['surface.view'],
        'grip':     T['surface.hover'],
    }
    root = DIST / 'cursors' / f'{THEME_ID}-cursors'
    cdir = root / 'cursors'
    cdir.mkdir(parents=True, exist_ok=True)
    for stale in cdir.iterdir():
        stale.unlink()

    cat = catalogue(C)
    for name, spec in cat.items():
        hx, hy = spec['hot']
        seq = spec['frames'] or [spec['shapes']]
        docs = [svg_document(s, spec['overlay'], C) for s in seq]
        frames = []
        for nominal in NOMINALS:
            px = nominal * 4 // 3
            for doc in docs:
                frames.append((nominal, px, round(hx * px / 32), round(hy * px / 32),
                               ANIM_MS if len(docs) > 1 else STATIC_MS, render(doc, px)))
        write_xcursor(cdir / name, frames)
        expect = 16 + 12 * len(frames) + sum(36 + f[1] * f[1] * 4 for f in frames)
        got = (cdir / name).stat().st_size
        if got != expect:
            out.append(f'  ! {name}: {got} bytes, container arithmetic says {expect}')
    out.append(f'cursors/{THEME_ID}-cursors/cursors/  ({len(cat)} cursors, '
               f'{len(NOMINALS)} sizes)')

    missing = sorted({v for v in LINKS.values()} - set(cat))
    if missing:
        out.append(f'  ! symlink targets that do not exist: {missing}')
    for link, target in LINKS.items():
        (cdir / link).symlink_to(target)
    out.append(f'cursors/{THEME_ID}-cursors/cursors/  ({len(LINKS)} aliases)')

    (root / 'index.theme').write_text(
        f'[Icon Theme]\nName={THEME_NAME}\n'
        f'Comment=Neon noir pointer set — cyan only where something is happening\n'
        f'Inherits=breeze_cursors\n')
    out.append(f'cursors/{THEME_ID}-cursors/index.theme')
    return out


def contact_sheet(T, dest, px=64):
    """Debug aid: every cursor rendered onto one checkerboard PNG."""
    import numpy as np
    from PIL import Image
    C = {'body': T['selection.fg'], 'ink': T['surface.void'], 'cyan': T['accent.cyan'],
         'negative': T['status.negative'], 'chip': T['surface.view'], 'grip': T['surface.hover']}
    cat = catalogue(C)
    cols = 8
    rows = (len(cat) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * px, rows * px))
    for i in range(0, cols * px, px // 2):
        for j in range(0, rows * px, px // 2):
            shade = 90 if ((i // (px // 2)) + (j // (px // 2))) % 2 else 150
            sheet.paste((shade, shade, shade, 255), (i, j, i + px // 2, j + px // 2))
    import cairosvg
    for n, (name, spec) in enumerate(sorted(cat.items())):
        shapes = spec['frames'][3] if spec['frames'] else spec['shapes']
        png = cairosvg.svg2png(bytestring=svg_document(shapes, spec['overlay'], C).encode(),
                               output_width=px, output_height=px)
        img = Image.open(io.BytesIO(png)).convert('RGBA')
        sheet.alpha_composite(img, ((n % cols) * px, (n // cols) * px))
    sheet.save(dest)
    return sorted(cat)
