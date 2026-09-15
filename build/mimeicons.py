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
    pool = GLYPHS
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
