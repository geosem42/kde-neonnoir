"""Icon theme: Breeze's own icons with every blue rotated to the theme's cyan.

Breeze paints its accent in brand blue — #3daee9 in 1,246 files, plus a long
tail of other blues, and every application that ships its own icon picks a
different one again (Dolphin's is #147cdc and #3593e6). A find-and-replace on
one hex therefore recoloured folders and nothing else, which is exactly what it
looked like: cyan folders in the file view, a blue Dolphin in the titlebar.

So the transform is a hue rotation, not a substitution. Any colour whose hue
falls in the blue band is moved to the cyan hue with its lightness and
saturation untouched, so shading, gradients and contrast all survive. Greens,
reds, yellows and greys are left exactly as Breeze drew them — the band stops
short of green at one end and violet at the other, and anything desaturated is
skipped so greys never tint.

Shapes are Breeze's throughout. An earlier version of this theme redrew about
6,150 icons as monochrome outlines; it matched the artboards and was the wrong
call, because an icon is something you recognise before you read it.

Only files that actually change are written. Everything else resolves in
breeze-dark through Inherits, which keeps the theme to the icons it restyles
rather than a copy of the whole set.
"""
import colorsys, re, pathlib

BREEZE = pathlib.Path('/usr/share/icons/breeze-dark')
# Applications install their own icon here, outside any theme. An icon theme is
# searched before hicolor, so a recoloured copy under our name wins — this is
# the only way to reach Dolphin's own titlebar and task-bar icon.
HICOLOR = pathlib.Path('/usr/share/icons/hicolor/scalable/apps')

HEX = re.compile(r'#([0-9a-fA-F]{6})\b')

# Monochrome status glyphs the panel shows. Breeze draws these with a
# `.ColorScheme-Text` stylesheet that KIconLoader rewrites to the palette's text
# colour at load time, so in a panel they come out near-white whatever the theme
# does — and a bar whose own type is dim grey and cyan then ends in a run of
# bright white outlines that belong to nothing.
#
# Re-emitted under this theme with the colour baked, which `FollowsColorScheme=
# false` in index.theme then keeps. The list is deliberately narrow: the tray
# this theme configures (network, volume, bluetooth, notifications, battery)
# plus the panel's own show-desktop button, and nothing an application draws in
# its own toolbars.
TRAY_FAMILIES = (
    'audio-volume-', 'microphone-sensitivity-',
    'network-wireless-', 'network-wired-', 'network-mobile-',
    'network-vpn', 'network-offline', 'network-connect', 'network-disconnect',
    'network-flightmode',
    'battery-',
    'bluetooth', 'preferences-system-bluetooth',
    'notification', 'preferences-desktop-notification',
    'user-desktop',
)
SCHEME_TEXT = re.compile(r'(\.ColorScheme-Text\s*\{[^}]*?color:\s*)#[0-9a-fA-F]{6}')
HUE_LO, HUE_HI = 188.0, 265.0     # blue band: past cyan-green, short of violet
MIN_SAT = 0.18                    # below this it is a grey and must stay one


def _rotate(text, cyan_hue):
    """Move every blue in `text` to `cyan_hue`, keeping lightness and saturation."""
    hits = 0

    def sub(m):
        nonlocal hits
        h = m.group(1)
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        hh, l, s = colorsys.rgb_to_hls(r, g, b)
        if s < MIN_SAT or not (HUE_LO <= hh * 360 <= HUE_HI):
            return m.group(0)
        hits += 1
        nr, ng, nb = colorsys.hls_to_rgb(cyan_hue, l, s)
        return '#%02x%02x%02x' % (round(nr * 255), round(ng * 255), round(nb * 255))

    return HEX.sub(sub, text), hits


def _dir_specs(index_theme):
    """{directory: [lines]} from breeze's own index.theme.

    Its Size/Context/Type/MinSize/MaxSize/Scale are reused verbatim. Guessing
    them is how a theme ends up with an unparseable entry, and a theme with one
    bad directory is skipped whole in favour of its parent.
    """
    specs, cur = {}, None
    for line in index_theme.splitlines():
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            cur = line[1:-1]
            if cur != 'Icon Theme':
                specs[cur] = []
        elif cur and cur != 'Icon Theme' and '=' in line:
            specs[cur].append(line)
    return specs


def build(T, DIST, THEME_ID, THEME_NAME, folder_hex, app_glyph_hex):
    if not BREEZE.is_dir():
        return ['  ! breeze-dark icons not installed — icon theme skipped']

    import shutil
    dst = DIST / 'icons' / THEME_ID
    if dst.exists():
        shutil.rmtree(dst)

    # The hue the whole set is pulled towards, taken from the palette rather
    # than hard-coded, so changing accent.cyan moves every icon with it.
    c = T['accent.cyan'].lstrip('#')
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    cyan_hue = colorsys.rgb_to_hls(r, g, b)[0]

    specs = _dir_specs((BREEZE / 'index.theme').read_text(errors='ignore'))
    dirs, n_written, n_hits = set(), 0, 0

    stems = set()

    def emit(rel, text):
        nonlocal n_written
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding='utf-8')
        stems.add(out.stem)
        n_written += 1

    for svg in sorted(BREEZE.rglob('*.svg')):
        rel = svg.relative_to(BREEZE)
        if rel.parts[0] == 'index.theme':
            continue
        real = svg.resolve()            # symlinks are flattened into real files
        if not real.is_file():
            continue
        try:
            text = real.read_text(encoding='utf-8')
        except Exception:
            continue
        new, hits = _rotate(text, cyan_hue)
        if not hits:
            continue                    # unchanged: let it resolve in breeze-dark
        emit(str(rel), new)
        dirs.add(str(rel.parent))
        n_hits += hits

    n_apps = 0
    if HICOLOR.is_dir():
        for svg in sorted(HICOLOR.glob('*.svg')):
            real = svg.resolve()
            if not real.is_file():
                continue
            try:
                text = real.read_text(encoding='utf-8')
            except Exception:
                continue
            new, hits = _rotate(text, cyan_hue)
            if not hits:
                continue
            emit(f'apps/scalable/{svg.name}', new)
            dirs.add('apps/scalable')
            n_apps += 1

    # Panel status glyphs, colour baked. Both the plain and the `-symbolic`
    # spelling, because which one the tray asks for depends on the applet, and a
    # bright twin left behind would be the one that answers.
    n_tray = 0
    for svg in sorted(BREEZE.rglob('*.svg')):
        stem = svg.stem
        base = stem[:-len('-symbolic')] if stem.endswith('-symbolic') else stem
        if not base.startswith(TRAY_FAMILIES):
            continue
        real = svg.resolve()
        if not real.is_file():
            continue
        try:
            text = real.read_text(encoding='utf-8')
        except Exception:
            continue
        new, n = SCHEME_TEXT.subn(r'\g<1>' + T['text.dim'], text)
        if not n:
            continue                    # not a monochrome glyph; leave it alone
        rel = svg.relative_to(BREEZE)
        emit(str(rel), new)
        dirs.add(str(rel.parent))
        n_tray += 1

    # Symbolic hand-off. Asked for `<name>-symbolic`, KIconLoader strips the
    # suffix and looks for `<name>` IN THIS THEME before it falls through to
    # breeze-dark — so every icon recoloured above also answers for its
    # monochrome twin, and anything that wanted the flat outline got the colour
    # one instead. That is why the panel's show-desktop button came up as a
    # cyan-and-magenta monitor: kiconfinder6 resolved
    #   user-desktop-symbolic -> NeonNoir/places/32/user-desktop.svg
    #
    # Shipping breeze's symbolic file unchanged puts the exact name back in this
    # theme, where it wins outright. None of them carries a blue in the band, so
    # these copies restyle nothing; they are here to route.
    #
    # Snapshotted, because emit() adds to `stems` as it goes: tested against the
    # live set, shipping places/22 would mark the name done and the 32, 48 and
    # 64 variants would be skipped — leaving one small size in this theme to
    # answer every size, since a hit in the current theme beats a better-sized
    # hit in the parent. 235 names, 588 files.
    n_sym, recoloured = 0, set(stems)
    for svg in sorted(BREEZE.rglob('*-symbolic.svg')):
        base = svg.stem[:-len('-symbolic')]
        if base not in recoloured or svg.stem in recoloured:
            continue
        real = svg.resolve()
        if not real.is_file():
            continue
        try:
            text = real.read_text(encoding='utf-8')
        except Exception:
            continue
        rel = svg.relative_to(BREEZE)
        emit(str(rel), _rotate(text, cyan_hue)[0])
        dirs.add(str(rel.parent))
        n_sym += 1

    if not dirs:
        return ['  ! nothing to recolour — icon theme skipped']

    lines = ['[Icon Theme]', f'Name={THEME_NAME}',
             'Comment=Neon Noir — Breeze icons, every blue rotated to cyan',
             'Inherits=breeze-dark,breeze,hicolor',
             # Breeze's SVGs carry a `current-color-scheme` stylesheet that
             # KIconLoader rewrites at load time, which would undo the rotation
             # on any icon that uses it.
             'FollowsColorScheme=false',
             f'Directories={",".join(sorted(dirs))}', '']
    for d in sorted(dirs):
        lines.append(f'[{d}]')
        if d in specs:
            lines += specs[d]
        else:                            # apps/scalable is ours, not Breeze's
            lines += ['Size=48', 'MinSize=8', 'MaxSize=512',
                      'Context=Applications', 'Type=Scalable']
        lines.append('')
    (dst / 'index.theme').write_text('\n'.join(lines))
    return [f'icons/{THEME_ID}/  ({n_written} icons, {n_hits} colours rotated, '
            f'{n_apps} from hicolor, {n_tray} panel glyphs dimmed, '
            f'{n_sym} symbolic kept mono, {len(dirs)} dirs; '
            f'everything untouched inherits breeze-dark)']
