"""Icon theme: inherit breeze-dark, recolour only the folders.

Breeze paints folders in its brand blue #3daee9. We swap that for a cyan at the
same perceptual lightness so folders stay as readable as Breeze's, rather than
using the full-strength UI accent, which is far too loud across 500 icons.
Everything we do not ship falls back to breeze-dark via Inherits.
"""
import re, shutil, pathlib

SRC_BLUE = re.compile(r'#3daee9', re.I)

def build(T, DIST, THEME_ID, THEME_NAME, folder_hex):
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

    lines = ['[Icon Theme]', f'Name={THEME_NAME}',
             'Comment=Neon Noir — Breeze Dark with cyan folders',
             'Inherits=breeze-dark,breeze,hicolor',
             f'Directories={",".join(dirs)}', '']
    for d in dirs:
        size = d.split('/')[1]
        lines += [f'[{d}]', f'Size={size}', 'Context=Places',
                  'Type=Fixed' if size.isdigit() else 'Type=Scalable', '']
    (dst / 'index.theme').write_text('\n'.join(lines))
    return [f'icons/{THEME_ID}/  ({n_files} folder icons, {n_recoloured} recoloured, '
            f'{len(dirs)} size dirs; inherits breeze-dark)']
