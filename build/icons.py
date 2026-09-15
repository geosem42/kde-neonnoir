"""Icon theme: inherit breeze-dark, recolour the folders, redraw the app glyphs.

Breeze paints folders in its brand blue #3daee9. We swap that for a cyan at the
same perceptual lightness so folders stay as readable as Breeze's, rather than
using the full-strength UI accent, which is far too loud across 500 icons.

On top of that we override the handful of application icons the design draws as
monochrome outlines (see appicons.py). Everything we do not ship falls back to
breeze-dark via Inherits.
"""
import re, shutil, pathlib

import appicons, statusicons

SRC_BLUE = re.compile(r'#3daee9', re.I)

def build(T, DIST, THEME_ID, THEME_NAME, folder_hex, app_glyph_hex):
    src = pathlib.Path('/usr/share/icons/breeze-dark')
    if not src.is_dir():
        return ['  ! breeze-dark icons not installed — icon theme skipped']
    dst = DIST / 'icons' / THEME_ID
    if dst.exists():
        shutil.rmtree(dst)

    dirs, n_files, n_recoloured = [], 0, 0
    for places in sorted(src.glob('places/*')):
        if not places.is_dir():
            continue
        size = places.name
        outdir = dst / 'places' / size
        made = False
        for svg in sorted(places.glob('folder*.svg')):
            real = svg.resolve()                      # flatten symlinks
            if not real.is_file():
                continue
            try:
                text = real.read_text(encoding='utf-8')
            except Exception:
                continue
            new, hits = SRC_BLUE.subn(folder_hex, text)
            if not made:
                outdir.mkdir(parents=True, exist_ok=True); made = True
            (outdir / svg.name).write_text(new, encoding='utf-8')
            n_files += 1
            n_recoloured += 1 if hits else 0
        if made:
            dirs.append(f'places/{size}')

    if not dirs:
        return ['  ! no folder icons found — icon theme skipped']

    # Outline app glyphs. One scalable directory rather than a copy per size:
    # they are pure vector, and a Scalable entry with a wide Min/Max range wins
    # the lookup at every size a panel or menu asks for.
    apps = dst / 'apps' / 'scalable'
    apps.mkdir(parents=True, exist_ok=True)
    glyphs = appicons.svgs(app_glyph_hex)
    for name, svg in sorted(glyphs.items()):
        (apps / f'{name}.svg').write_text(svg, encoding='utf-8')

    # Tray glyphs. Written into every context we declare rather than into the
    # one breeze happens to file each name under: the same name lives in
    # different contexts at different sizes (network-wireless-connected-100 is
    # in devices/16 but status/22), and icon lookup scans directories, not
    # contexts.
    status = statusicons.svgs(T, src)
    for d in statusicons.DIRS:
        outdir = dst / d
        outdir.mkdir(parents=True, exist_ok=True)
        for name, svg in sorted(status.items()):
            (outdir / f'{name}.svg').write_text(svg, encoding='utf-8')

    scalable = ['apps/scalable'] + list(statusicons.DIRS)
    lines = ['[Icon Theme]', f'Name={THEME_NAME}',
             'Comment=Neon Noir — cyan folders and outline glyphs',
             'Inherits=breeze-dark,breeze,hicolor',
             f'Directories={",".join(dirs + scalable)}', '']
    for d in dirs:
        size = d.split('/')[1]
        lines += [f'[{d}]', f'Size={size}', 'Context=Places',
                  'Type=Fixed' if size.isdigit() else 'Type=Scalable', '']
    CONTEXT = {'apps': 'Applications', 'status': 'Status',
               'devices': 'Devices', 'actions': 'Actions',
               'preferences': 'Preferences'}
    for d in scalable:
        lines += [f'[{d}]', 'Size=24', 'MinSize=8', 'MaxSize=512',
                  f'Context={CONTEXT[d.split("/")[0]]}', 'Type=Scalable', '']
    (dst / 'index.theme').write_text('\n'.join(lines))
    return [f'icons/{THEME_ID}/  ({n_files} folder icons, {n_recoloured} recoloured, '
            f'{len(glyphs)} app glyphs, {len(status)} tray glyphs, '
            f'{len(dirs) + len(scalable)} dirs; inherits breeze-dark)']
