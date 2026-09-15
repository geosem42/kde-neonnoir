"""Icon theme: inherit breeze-dark, recolour the folders, redraw the app glyphs.

Breeze paints folders in its brand blue #3daee9. We swap that for a cyan at the
same perceptual lightness so folders stay as readable as Breeze's, rather than
using the full-strength UI accent, which is far too loud across 500 icons.

On top of that we override the handful of application icons the design draws as
monochrome outlines (see appicons.py). Everything we do not ship falls back to
breeze-dark via Inherits.
"""
import re, shutil, pathlib

import actionicons, appicons, mimeicons, placeicons, statusicons

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

    # Sidebar places. Written ONLY into the small fixed sizes, which is the set
    # a file manager's sidebar draws from; 32 and up keep the recoloured cyan
    # folders the file view uses. Breeze splits its own place icons the same
    # way, monochrome below 32 and coloured above.
    places = placeicons.svgs(app_glyph_hex, src)
    n_places = 0
    for d in dirs:
        size = d.split('/')[1]
        if int(size.split('@')[0]) >= 32:
            continue
        for name, svg in places.items():
            (dst / d / f'{name}.svg').write_text(svg, encoding='utf-8')
            n_places += 1

    # A directory in a file manager is drawn from the MIME type, not the place:
    # Dolphin asks for `inode-directory`, which breeze keeps in mimetypes/ as a
    # SYMLINK back into its own places/folder.svg. A theme that recolours only
    # places/ therefore changes nothing in the file view — the lookup resolves
    # inside the parent theme and never sees our copy.
    mime_dirs, n_mime = [], 0
    for d in dirs:
        size = d.split('/')[1]
        folder = dst / d / 'folder.svg'
        if not folder.is_file():
            continue
        mdir = dst / 'mimetypes' / size
        mdir.mkdir(parents=True, exist_ok=True)
        (mdir / 'inode-directory.svg').write_text(
            folder.read_text(encoding='utf-8'), encoding='utf-8')
        mime_dirs.append(f'mimetypes/{size}')
        n_mime += 1

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

    # Menu categories. A separate context from apps: the launcher's left-hand
    # list asks for `applications-development` and friends under `categories`,
    # so shipping only apps/ leaves that list on Breeze.
    cats = dst / 'categories' / 'scalable'
    cats.mkdir(parents=True, exist_ok=True)
    category = appicons.category_svgs(app_glyph_hex)
    for name, svg in sorted(category.items()):
        (cats / f'{name}.svg').write_text(svg, encoding='utf-8')

    # File types. Same reason as the tray: a partial override leaves outline
    # and colour glyphs side by side in one folder.
    mt = dst / 'mimetypes' / 'scalable'
    mt.mkdir(parents=True, exist_ok=True)
    mime = mimeicons.svgs(app_glyph_hex, src)
    for name, svg in sorted(mime.items()):
        (mt / f'{name}.svg').write_text(svg, encoding='utf-8')

    # Menu and toolbar glyphs. Only the generic freedesktop families; see
    # actionicons for why the application-specific toolsets stay on Breeze.
    act = dst / 'actions' / 'scalable'
    act.mkdir(parents=True, exist_ok=True)
    action = actionicons.svgs(app_glyph_hex, src)
    for name, svg in sorted(action.items()):
        (act / f'{name}.svg').write_text(svg, encoding='utf-8')

    # Tray applets whose icon name is an app or action rather than a status
    # family — klipper, plasmavault, the night-colour toggle. Written into every
    # scalable context because the tray asks for them under more than one.
    tray = appicons.tray_svgs(app_glyph_hex)
    for d in ('apps/scalable',) + statusicons.DIRS:
        outdir = dst / d
        outdir.mkdir(parents=True, exist_ok=True)
        for name, svg in tray.items():
            (outdir / f'{name}.svg').write_text(svg, encoding='utf-8')

    scalable = (['apps/scalable', 'categories/scalable', 'mimetypes/scalable']
                + list(statusicons.DIRS))
    lines = ['[Icon Theme]', f'Name={THEME_NAME}',
             'Comment=Neon Noir — cyan folders and outline glyphs',
             'Inherits=breeze-dark,breeze,hicolor',
             # Breeze's SVGs carry a `current-color-scheme` stylesheet that
             # KIconLoader rewrites at load time. Ours are baked from the
             # palette already, so opting out keeps the colours we generated.
             'FollowsColorScheme=false',
             f'Directories={",".join(dirs + mime_dirs + scalable)}', '']
    # A "16@2x" directory is size 16 at scale 2, NOT a size called "16@2x".
    # Writing the literal name into Size= makes the entry unparseable, and an
    # icon theme with a bad directory entry is skipped in favour of its parent
    # — which is why every folder stayed Breeze blue despite being recoloured
    # on disk.
    for d in dirs + mime_dirs:
        name = d.split('/')[1]
        size, _, scale = name.partition('@')
        ctx = 'MimeTypes' if d.startswith('mimetypes/') else 'Places'
        lines += [f'[{d}]', f'Size={size}', f'Context={ctx}', 'Type=Fixed']
        if scale:
            lines.append(f'Scale={scale.rstrip("x")}')
        lines.append('')
    CONTEXT = {'apps': 'Applications', 'categories': 'Categories',
               'mimetypes': 'MimeTypes', 'status': 'Status',
               'devices': 'Devices', 'actions': 'Actions',
               'preferences': 'Preferences'}
    for d in scalable:
        lines += [f'[{d}]', 'Size=24', 'MinSize=8', 'MaxSize=512',
                  f'Context={CONTEXT[d.split("/")[0]]}', 'Type=Scalable', '']
    (dst / 'index.theme').write_text('\n'.join(lines))
    return [f'icons/{THEME_ID}/  ({n_files} folder icons, {n_recoloured} recoloured, '
            f'{len(glyphs)} app glyphs, {len(category)} category glyphs, '
            f'{len(status)} tray glyphs, '
            f'{n_mime} inode-directory, {len(mime)} file types, '
            f'{len(places)} places x{n_places // max(1, len(places))} sizes, '
            f'{len(tray)} tray applets, {len(action)} actions, '
            f'{len(dirs) + len(mime_dirs) + len(scalable)} dirs; '
            f'inherits breeze-dark)']
