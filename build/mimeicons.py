"""Line-art file icons for the file manager.

Breeze ships 519 distinct mimetype names as filled colour glyphs; the artboard
draws files as grey outlines on the same 24px grid as everything else. Picking
a handful by hand would leave the two styles side by side in one folder, which
looks worse than not overriding at all — so every name breeze-dark ships is
classified by pattern and gets an outline.

`inode-directory` is deliberately excluded: folders keep the recoloured Breeze
icon, which the artboard draws cyan and filled, not as an outline.
"""
import re

from appicons import GLYPHS, STROKE, VIEWBOX

DIRS = ('mimetypes/scalable',)

# Extra glyphs that only file types need.
EXTRA = {
    'note': '<path d="M9.4 18V5.6l9.2-1.8v12.4"/>'
            '<ellipse cx="6.6" cy="18" rx="2.8" ry="2.3"/>'
            '<ellipse cx="15.8" cy="16.2" rx="2.8" ry="2.3"/>',

    # Perforations down both edges, not full-height rules: with rules it was
    # a 3x2 grid, indistinguishable from the spreadsheet glyph.
    'film': '<rect x="2.6" y="4.6" width="18.8" height="14.8" rx="2.2"/>'
            '<path d="M2.6 8.4h3.6M2.6 12h3.6M2.6 15.6h3.6"/>'
            '<path d="M17.8 8.4h3.6M17.8 12h3.6M17.8 15.6h3.6"/>'
            '<path d="M6.2 4.6v14.8M17.8 4.6v14.8"/>',

    'book': '<path d="M3.4 5a1.6 1.6 0 0 1 1.6-1.6h5.4a1.6 1.6 0 0 1 1.6 1.6v14.8'
            'a1.6 1.6 0 0 0-1.6-1.6H3.4z"/>'
            '<path d="M20.6 5a1.6 1.6 0 0 0-1.6-1.6h-5.4A1.6 1.6 0 0 0 12 5v14.8'
            'a1.6 1.6 0 0 1 1.6-1.6h7z"/>',

    'typeface': '<path d="M5.6 3.4h8.4L19 8.4v12.2H5.6z"/>'
                '<path d="M13.8 3.4v5.2H19"/>'
                '<path d="M8.6 17.4l2.8-6.6 2.8 6.6M9.6 15.2h3.6"/>',

    'table': '<rect x="3" y="4.6" width="18" height="14.8" rx="2"/>'
             '<path d="M3 9.6h18M3 14.4h18M9.4 4.6v14.8"/>',

    'slide': '<rect x="2.6" y="4.6" width="18.8" height="12.4" rx="2"/>'
             '<path d="M6.6 8.8h6.8M6.6 12.6h10.8"/>'
             '<path d="M12 17v3.4M8.6 20.4h6.8"/>',

    'unknown': '<path d="M5.6 3.4h8.4L19 8.4v12.2H5.6z"/>'
               '<path d="M13.8 3.4v5.2H19"/>'
               '<path d="M9.6 12.4a2.4 2.4 0 0 1 4.7.8c0 1.6-2.3 2.4-2.3 2.4"/>'
               '<path d="M12 18.2h.01"/>',
}

# Order matters: the first pattern that matches a name wins, so the specific
# rules sit above the catch-alls.
RULES = [
    (r'^inode-(blockdevice|chardevice|mount-point|device)', 'chip'),
    (r'^inode-', 'folder'),
    (r'^image-|^application-x-krita|^application-vnd\.oasis\.opendocument\.graphics',
     'image'),
    (r'^(audio|podcast|audiobook)-|^application-(ogg|x-flac)', 'note'),
    (r'^video-|^application-x-matroska', 'film'),
    (r'^(font|fonts)-|^application-x-font', 'typeface'),
    (r'(zip|tar|compress|archive|rpm|deb$|deb-|7z|rar|gzip|bzip|lzma|xz|'
     r'package|cab|iso9660|cd-image|appimage|snap|flatpak)', 'archive'),
    (r'^(application-pdf|viewpdf|viewps|viewdvi|viewbib)|postscript|djvu|'
     r'epub|mobi|ebook', 'book'),
    (r'spreadsheet|-xls|ms-excel|opendocument\.chart|csv|tab-separated', 'table'),
    (r'presentation|-ppt|ms-powerpoint|opendocument\.presentation', 'slide'),
    (r'wordprocessing|-doc$|-doc-|msword|opendocument\.text|text-rtf|'
     r'application-vnd\.oasis\.opendocument\.master', 'document'),
    # Shells and binaries only. A .py is source, not a shell script, and
    # matching `-python` here put every language file behind a `>_`.
    (r'shellscript|-shellscript|executable|sharedlib|-object|-core|'
     r'application-x-ms-dos', 'terminal'),
    (r'json|xml|yaml|toml|html|xhtml|-css|javascript|typescript|-script|'
     r'text-x-(c|c\+\+|chdr|csrc|java|go|rust|php|sql|patch|diff|makefile|'
     r'cmake|meson|qml|vala|haskell|scala|kotlin|swift|objc|python|ruby|perl|'
     r'lua|awk|tcl|erlang|lisp|scheme|r-source|julia|nim|zig|dart)', 'code'),
    (r'^message-|mail|rfc822|vcard|vcalendar|calendar', 'mail'),
    (r'^(unknown|none|application-octet-stream)', 'unknown'),
    (r'^text-', 'document'),
]

FALLBACK = 'document'


def _glyph_for(name):
    stem = re.sub(r'-(symbolic|rtl)$', '', name)
    stem = re.sub(r'-(symbolic|rtl)$', '', stem)
    for pattern, glyph in RULES:
        if re.search(pattern, stem):
            return glyph
    return FALLBACK


def svgs(stroke_hex, breeze_root):
    """{icon-name: svg} for every mimetype name breeze-dark ships."""
    pool = dict(GLYPHS)
    pool.update(EXTRA)
    names = set()
    for svg in (breeze_root / 'mimetypes').rglob('*.svg'):
        names.add(svg.stem)
    out = {}
    for n in sorted(names):
        if n.startswith('inode-directory'):
            continue          # folders stay cyan and filled
        body = pool[_glyph_for(n)]
        out[n] = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{VIEWBOX}" '
            f'height="{VIEWBOX}" viewBox="0 0 {VIEWBOX} {VIEWBOX}">'
            f'<g fill="none" stroke="{stroke_hex}" stroke-width="{STROKE}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n'
        )
    return out
