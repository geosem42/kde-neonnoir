"""The Neon Noir mark, shared by every screen outside the session.

Plymouth, the KSplash stage and the SDDM greeter all show the same lockup — a
pointy-top hexagon with a magenta core, the wordmark under it, one progress
rule — so the handover between boot, login and session start has no visible
seam. Plymouth can only place images, so the same lockup is also baked to PNG.
"""
import io, pathlib

FONT_DIRS = ('/usr/share/fonts/truetype/ibm-plex', '/usr/local/share/fonts',
             str(pathlib.Path.home() / '.local/share/fonts'))
FONT_MEDIUM = 'IBMPlexSans-Medium.ttf'
FONT_BOLD = 'IBMPlexSans-Bold.ttf'


def font_path(name=FONT_MEDIUM):
    for d in FONT_DIRS:
        p = pathlib.Path(d) / name
        if p.exists():
            return p
    return None


def hexagon(cx, cy, r):
    """Pointy-top hexagon: vertices at top and bottom, vertical left/right edges."""
    import math
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
           for a in (-90, -30, 30, 90, 150, 210)]
    return 'M ' + ' L '.join(f'{x:.2f} {y:.2f}' for x, y in pts) + ' Z'


def mark_svg(T, px=256, glow=True):
    """The hexagon mark alone, square, transparent ground."""
    c, r = px / 2, px * 0.34
    sw = max(1.5, px * 0.0145)
    cyan, mag = T['accent.cyan'], T['accent.magenta']
    halo = (f'<defs><radialGradient id="g" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0%" stop-color="{mag}" stop-opacity="0.55"/>'
            f'<stop offset="100%" stop-color="{mag}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{c:.1f}" cy="{c:.1f}" r="{px * 0.15:.1f}" fill="url(#g)"/>') if glow else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" '
            f'viewBox="0 0 {px} {px}">{halo}'
            f'<path d="{hexagon(c, c, r)}" fill="none" stroke="{cyan}" '
            f'stroke-width="{sw:.2f}" stroke-linejoin="round"/>'
            f'<path d="{hexagon(c, c, r * 0.72)}" fill="none" stroke="{cyan}" '
            f'stroke-width="{sw * 0.6:.2f}" stroke-opacity="0.28" stroke-linejoin="round"/>'
            f'<circle cx="{c:.1f}" cy="{c:.1f}" r="{px * 0.042:.1f}" fill="{mag}"/>'
            f'</svg>')


def png(svg, path, w, h):
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path),
                     output_width=w, output_height=h)


def wordmark_png(path, text, size, colour, tracking=0.34, weight=FONT_MEDIUM):
    """Letterspaced caps baked to PNG.

    Plymouth's script module has no text primitive without plymouth-label, and
    the label plugin needs a font inside the initramfs; a PNG has neither
    problem. Drawn glyph by glyph because Pillow has no letter-spacing.
    """
    from PIL import Image, ImageDraw, ImageFont
    fp = font_path(weight)
    if fp is None:
        return None
    f = ImageFont.truetype(str(fp), size)
    gap = size * tracking
    widths = [f.getlength(ch) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    pad = int(size * 0.5)
    img = Image.new('RGBA', (int(total) + 2 * pad, int(size * 1.7)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = pad
    for ch, w in zip(text, widths):
        d.text((x, size * 1.2), ch, font=f, fill=colour, anchor='ls')
        x += w + gap
    img = img.crop(img.getbbox())
    img.save(path)
    return img.size


# An 8x8 Bayer matrix, not random noise. Both hide the banding equally well,
# but random noise is incompressible: it tripled the PNG sizes here, while an
# ordered pattern is periodic and costs almost nothing.
_BAYER8 = None


def _bayer(n=8):
    import numpy as np
    m = np.array([[0]])
    while m.shape[0] < n:
        k = m.shape[0]
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return m / (n * n)


def dither(path, amount=1.0):
    """Break up banding in a near-black gradient.

    At these lightnesses an 8-bit ramp steps visibly. Adding a sub-LSB ordered
    pattern before the value is stored moves the step boundary around so the
    rings dissolve. Deterministic, so the build stays reproducible.
    """
    import numpy as np
    from PIL import Image
    global _BAYER8
    if _BAYER8 is None:
        _BAYER8 = _bayer(8)
    a = np.asarray(Image.open(path).convert('RGB'), dtype=np.float32)
    h, w, _ = a.shape
    tile = np.tile(_BAYER8, (h // 8 + 1, w // 8 + 1))[:h, :w] - 0.5
    a = np.clip(a + (tile * 2.0 * amount)[..., None], 0, 255)
    Image.fromarray(a.astype('uint8')).save(path, optimize=True)


def launcher_svg(T, size=48):
    """The panel launcher: the hexagon inside its own framed button.

    Kickoff draws nothing behind its icon, so the design's bordered square has
    to be part of the icon itself. Drawn edge-to-edge on the viewBox and sized
    by the panel, which is why there is no padding here.
    """
    s = size
    inset = s * 0.0417          # 2/48 — keeps the 1px frame fully inside the box
    r = s * 0.2083              # 10/48
    cx = cy = s / 2
    R = s * 0.2292              # 11/48, the hexagon's circumradius
    pts = []
    for i in range(6):
        import math
        a = math.radians(60 * i - 90)
        pts.append(f'{cx + R * math.cos(a):.2f} {cy + R * math.sin(a):.2f}')
    hexpath = 'M ' + ' L '.join(pts) + ' Z'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" '
        f'viewBox="0 0 {s} {s}">'
        f'<rect x="{inset:.2f}" y="{inset:.2f}" width="{s - 2 * inset:.2f}" '
        f'height="{s - 2 * inset:.2f}" rx="{r:.2f}" fill="{T["accent.cyan.ghost"]}" '
        f'stroke="{T["accent.cyan.deep"]}" stroke-width="{s / 48:.2f}"/>'
        f'<path d="{hexpath}" fill="none" stroke="{T["accent.cyan"]}" '
        f'stroke-width="{s * 0.0417:.2f}" stroke-linejoin="round"/>'
        f'</svg>\n'
    )


def avatar_png(path, initial, T, size=256):
    """The account picture: a cyan-to-magenta disc with one dark letter.

    One file per letter is written at build time rather than rendering at
    install time, so install.sh needs no Python and the output is the same on
    every machine. 26 discs at this size cost a few KB each.
    """
    from PIL import Image, ImageDraw, ImageFont
    a, b = rgb(T['accent.cyan.deep']), rgb(T['accent.magenta.deep'])
    n = size
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    px = im.load()
    # Diagonal ramp, top-left to bottom-right, as the artboard draws it.
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = (round(a[0] + (b[0] - a[0]) * t),
                        round(a[1] + (b[1] - a[1]) * t),
                        round(a[2] + (b[2] - a[2]) * t), 255)
    # Circular mask, supersampled so the edge is not stepped.
    S = 4
    mask = Image.new('L', (n * S, n * S), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, n * S - 1, n * S - 1), fill=255)
    im.putalpha(mask.resize((n, n), Image.LANCZOS))

    fp = font_path(FONT_BOLD) or font_path()
    if fp:
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(str(fp), round(n * 0.46))
        l, t, r, bm = d.textbbox((0, 0), initial, font=f)
        d.text(((n - (r - l)) / 2 - l, (n - (bm - t)) / 2 - t), initial,
               font=f, fill=rgb(T['surface.void']) + (255,))
    im.save(path, optimize=True)


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def build(T, DIST, THEME_ID, THEME_NAME):
    out = []
    d = DIST / 'brand'
    d.mkdir(parents=True, exist_ok=True)

    (d / 'mark.svg').write_text(mark_svg(T, 256))
    out.append('brand/mark.svg')

    (d / 'launcher.svg').write_text(launcher_svg(T, 48))
    out.append('brand/launcher.svg')

    av = d / 'avatars'
    av.mkdir(exist_ok=True)
    for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        avatar_png(av / f'{ch}.png', ch, T, 256)
    out.append('brand/avatars/A-Z.png  (26 discs)')
    for size in (96, 128, 192, 256, 384):
        png(mark_svg(T, size), d / f'mark-{size}.png', size, size)
    out.append('brand/mark-*.png  (5 sizes)')

    size = wordmark_png(d / 'wordmark.png', 'NEON NOIR', 44, T['text.normal'])
    if size is None:
        out.append('  ! IBM Plex Sans not found — wordmark.png not written')
    else:
        out.append(f'brand/wordmark.png  ({size[0]}x{size[1]})')

    # One-pixel-tall strips the Plymouth script scales to length: a dim rule and
    # the cyan fill that grows along it.
    from PIL import Image
    for name, tok, alpha in (('bar-track', 'border.float', 130), ('bar-fill', 'accent.cyan', 255)):
        c = T[tok].lstrip('#')
        rgb = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
        Image.new('RGBA', (2, 2), rgb + (alpha,)).save(d / f'{name}.png')
    out.append('brand/bar-track.png, brand/bar-fill.png')
    return out
