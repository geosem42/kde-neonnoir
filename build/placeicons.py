"""Line-art place icons for the file-manager sidebar.

Breeze ships 112 distinct place names — 88 of them `folder-*` variants — and a
sidebar shows whichever ones the user has. Covering a chosen few leaves our
outlines next to Breeze's filled glyphs in the same list, so every name is
classified by pattern here, exactly as the mimetypes are.

These are written ONLY into the small fixed sizes. Breeze itself ships
monochrome places below 32px and coloured ones at 32 and up; a file manager
draws its sidebar from the small set and its file view from the large set.
Keeping that split is what lets the sidebar be outlines while folders in the
view stay cyan and filled.
"""
import re

from appicons import GLYPHS, STROKE, VIEWBOX, _wrap

# Order matters: the first pattern that matches wins.
RULES = [
    # Named user directories.
    (r'^user-home$|^folder-home', 'house'),
    (r'^(user-)?desktop$|^folder-desktop', 'monitor'),
    (r'^user-trash|^folder-trash|^trash-', 'trash'),
    (r'^user-identity', 'person'),
    (r'^start-here', 'hexagon'),

    # Topic folders.
    (r'folder-(documents|text|txt|notes|sign|print)', 'document'),
    (r'folder-(downloads?)', 'download'),
    (r'folder-(music|sound|podcast)|library-music', 'note'),
    (r'folder-(video|videos)', 'film'),
    (r'folder-(picture|pictures|image|images|image-people|drawing|paint)', 'image'),
    (r'folder-(design)', 'palette'),
    (r'folder-(games|godot)', 'gamepad'),
    # Anchored: without it `folder-bookmark` matches `book`.
    (r'folder-(book|comic|library)$', 'book'),
    (r'folder-(bookmark|favorites|important)|^favorites$', 'bookmark'),
    (r'folder-(development|build|script|java|language)', 'wrench'),
    (r'folder-(git|activities|extension)', 'nodes'),
    (r'folder-(html|cloud|dropbox|gdrive|onedrive|owncloud)', 'globe'),
    (r'folder-(network|remote|public|publicshare)|^network-workgroup|gigolo', 'nodes'),
    (r'folder-(locked|unlocked|encrypted|decrypted)|^certificate-server', 'lock'),
    (r'folder-(mail)|^mail-', 'mail'),
    # Anchored: without it `folder-templates` matches `temp`.
    (r'folder-(recent|temp)$', 'clock'),
    (r'folder-(root|database)|^network-server|^server-database', 'drive'),
    (r'folder-(templates|presentation)', 'slide'),
    (r'folder-(table|chart|calculate)', 'table'),
    (r'folder-(deb|rpm|snap|flatpak|tar|appimage|docker)|^repository', 'archive'),
    (r'folder-(android)', 'phone'),
    (r'folder-(mac|windows)', 'monitor'),
    (r'folder-(blender)', 'dividers'),
    (r'folder-(crash|log)', 'unknown'),
    (r'^document-multiple', 'document'),

    # Colour variants and anything else that is simply a folder.
    (r'^folder|^stock_folder', 'folder'),
]

FALLBACK = 'folder'


def _glyph_for(name):
    stem = re.sub(r'-(symbolic|rtl)$', '', name)
    stem = re.sub(r'-(symbolic|rtl)$', '', stem)
    for pattern, glyph in RULES:
        if re.search(pattern, stem):
            return glyph
    return FALLBACK


def svgs(stroke_hex, breeze_root, size=24):
    """{icon-name: svg} for every place name breeze-dark ships.

    `size` must match the Fixed directory the files are written into.
    """
    names = set()
    for svg in (breeze_root / 'places').rglob('*.svg'):
        names.add(svg.stem)
    return {n: _wrap(GLYPHS[_glyph_for(n)], stroke_hex, size) for n in sorted(names)}
