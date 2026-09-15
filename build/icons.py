"""Icon theme: inherit breeze-dark, recolour the folders, change nothing else.

Breeze paints folders in its brand blue #3daee9. We swap that for a cyan at the
same perceptual lightness so folders stay as readable as Breeze's, rather than
using the full-strength UI accent, which is far too loud across 500 icons.

That recolour is the whole theme. An earlier version also redrew about 6,150
icons as monochrome outlines — apps, categories, places, mimetypes, actions and
the tray. It matched the artboards, and it was the wrong call: an icon is
something you recognise before you read it, and replacing a set the user already
knows costs them that recognition everywhere at once. Shapes stay Breeze's.

The outline glyphs and their pattern sweeps are in the history if they are ever
wanted back — see the commit that removed them.
"""
import re, shutil, pathlib

SRC_BLUE = re.compile(r'#3daee9', re.I)

# Folder COLOUR variants are left exactly as Breeze drew them. Dolphin's context
# menu shows them as a row of swatches where the colour IS the content, so
# recolouring their accent turned `folder-blue` cyan — neither blue nor distinct
# from the cyan one beside it.
COLOUR_VARIANT = re.compile(
    r'^folder-(black|blue|brown|cyan|green|grey|magenta|orange|red|violet|'
    r'yellow)(-|$)')


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
            if COLOUR_VARIANT.match(svg.stem):
                new, hits = text, 0
            else:
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

    lines = ['[Icon Theme]', f'Name={THEME_NAME}',
             'Comment=Neon Noir — Breeze icons with cyan folders',
             'Inherits=breeze-dark,breeze,hicolor',
             # Breeze's SVGs carry a `current-color-scheme` stylesheet that
             # KIconLoader rewrites at load time. Our folders are baked from the
             # palette already, so opting out keeps the colour we generated.
             'FollowsColorScheme=false',
             f'Directories={",".join(dirs + mime_dirs)}', '']
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
    (dst / 'index.theme').write_text('\n'.join(lines))
    return [f'icons/{THEME_ID}/  ({n_files} folder icons, {n_recoloured} recoloured, '
            f'{n_mime} inode-directory, {len(dirs) + len(mime_dirs)} dirs; '
            f'everything else inherits breeze-dark)']
