"""Line-art action icons — the glyphs inside menus, toolbars and dialogs.

Breeze ships 2,224 action names. Roughly half are the generic freedesktop
families every application uses (edit-, document-, go-, view-, zoom-, format-,
media-, window-, dialog-, help-, system-, list-, tab-); the rest belong to
particular applications — gnumeric, labplot, kdenlive, KTorrent, digiKam's
batch queue, the vector-editor node and path tools.

Only the generic half is swept. The specialist sets are left on Breeze on
purpose: a node-editing tool given a generic outline is not a style
improvement, it is a tool the user can no longer identify. The mixed-style
problem that made a partial sweep wrong elsewhere does not apply, because
those icons only ever appear together inside their own application's toolbar.

An unmatched generic name falls back to `dots`, which reads as "an action"
without claiming to be a specific one.
"""
import re

from appicons import GLYPHS, _wrap

# Names outside these prefixes keep Breeze's icon.
GENERIC = re.compile(
    r'^(edit|document|go|view|zoom|format|media|window|dialog|help|system|'
    r'list|tab|bookmark|bookmarks|folder|archive|object|mail|insert|color|'
    r'call|search|find|configure|settings|preferences|overflow-menu|'
    r'application-menu|open-menu|show|hide|run|debug|code|vcs|tag|flag|star|'
    r'rate|trash|download|upload|cloud|link|share|print|lock|unlock|security|'
    r'password|visibility|checkbox|checkmark|arrow|add|remove|delete|new|open|'
    r'save|close|quit|exit|refresh|sync|tools|text|image|games|office|'
    r'selection|layer)(-|$)')

# Ordered: the first match wins, so specific rules sit above general ones.
RULES = [
    # Clipboard and editing.
    (r'^edit-copy', 'copy'),
    (r'^edit-cut', 'scissors'),
    (r'^edit-paste', 'clipboard'),
    (r'^edit-undo', 'undo'),
    (r'^edit-redo', 'redo'),
    (r'^edit-delete|^delete|^edit-clear|^trash-empty', 'trash'),
    (r'^edit-find|^edit-rename.*find|^search|^find', 'search'),
    (r'^edit-rename|^edit-entry|^edit-text', 'pencil'),
    (r'^edit-select', 'check'),
    (r'^edit-(add|new)|^list-add|^add-|^new-', 'plus'),
    (r'^edit-remove|^list-remove|^remove-', 'minus'),
    (r'^edit-image', 'image'),
    (r'^edit-download', 'download'),
    (r'^edit-link', 'link'),
    (r'^edit-', 'pencil'),

    # Documents.
    (r'^document-new|^folder-new', 'plus'),
    (r'^document-open-recent', 'clock'),
    (r'^document-open|^open', 'folder'),
    (r'^document-save', 'save'),
    (r'^document-print|^print', 'printer'),
    (r'^document-close|^close|^window-close|^tab-close', 'cross'),
    (r'^document-properties|^document-edit', 'pencil'),
    (r'^document-revert|^document-replace', 'undo'),
    (r'^document-export|^document-send|^document-share|^share', 'share'),
    (r'^document-import', 'download'),
    (r'^document-encrypt|^document-decrypt|^document-sign', 'lock'),
    (r'^document-preview', 'eye'),
    (r'^document-multiple|^document-duplicate', 'copy'),
    (r'^document-', 'document'),

    # Navigation.
    (r'^go-previous|^go-first|^arrow-left', 'arrow-left'),
    (r'^go-next|^go-last|^arrow-right', 'arrow-right'),
    (r'^go-up|^arrow-up|^go-parent', 'arrow-up'),
    (r'^go-down|^arrow-down|^go-bottom', 'arrow-down'),
    (r'^go-home', 'house'),
    (r'^go-jump|^go-', 'arrow-right'),

    # Views.
    (r'^view-refresh|^refresh|^view-sync|^sync', 'refresh'),
    (r'^view-fullscreen|^view-restore', 'fullscreen'),
    (r'^view-list-details|^view-list-text|^view-list-tree|^view-split', 'list'),
    (r'^view-list-icons|^view-grid|^view-choose', 'grid4'),
    (r'^view-preview|^view-visible|^visibility$|^show', 'eye'),
    (r'^view-hidden|^view-invisible|^hide', 'eye-off'),
    (r'^view-filter|^view-sort-filter', 'funnel'),
    (r'^view-sort', 'sort'),
    (r'^view-media|^view-multiple-objects', 'play'),
    (r'^view-calendar|^view-history|^view-time', 'clock'),
    (r'^view-statistics|^view-table|^view-financial', 'table'),
    (r'^view-task|^view-process', 'chip'),
    (r'^view-certificate|^view-private|^view-lock', 'lock'),
    (r'^view-pim-mail|^view-pim-contacts', 'mail'),
    (r'^view-', 'eye'),

    # Zoom.
    (r'^zoom-in', 'zoom-in'),
    (r'^zoom-out', 'zoom-out'),
    (r'^zoom-fit|^zoom-select|^zoom-draw', 'zoom-fit'),
    (r'^zoom', 'search'),

    # Rich text.
    (r'^format-text-bold', 'bold'),
    (r'^format-text-italic', 'italic'),
    (r'^format-text-underline|^format-text-strike', 'underline'),
    (r'^format-justify-left|^format-align-.*left', 'align-left'),
    (r'^format-justify-center|^format-align-.*center', 'align-center'),
    (r'^format-justify-right|^format-align-.*right', 'align-right'),
    (r'^format-justify-fill', 'align-justify'),
    (r'^format-indent', 'indent'),
    (r'^format-list-unordered|^format-list-.*bullet', 'bullets'),
    (r'^format-list-ordered|^format-list-.*number', 'numbers'),
    (r'^format-fill-color|^format-stroke|^color-|^fill-color', 'droplet'),
    (r'^format-font|^format-text-', 'typeface'),
    (r'^format-layer|^layer-', 'layers'),
    (r'^format-', 'align-left'),

    # Media transport.
    (r'^media-playback-start|^media-seek', 'play'),
    (r'^media-playback-pause', 'pause'),
    (r'^media-playback-stop', 'stop'),
    (r'^media-skip-forward|^media-seek-forward', 'skip-forward'),
    (r'^media-skip-backward|^media-seek-backward', 'skip-back'),
    (r'^media-record', 'record'),
    (r'^media-eject', 'eject'),
    (r'^media-repeat|^media-playlist-repeat', 'repeat'),
    (r'^media-shuffle|^media-playlist-shuffle', 'shuffle'),
    (r'^media-volume|^audio-volume', 'speaker'),
    (r'^media-mount|^media-optical', 'book'),
    (r'^media-', 'play'),

    # Windows and tabs.
    (r'^window-new|^tab-new|^tab-duplicate', 'plus'),
    (r'^window-minimize|^window-shade', 'minus'),
    (r'^window-pin|^window-keep', 'pin'),
    (r'^window-|^tab-', 'window'),

    # Dialogs and messages.
    (r'^dialog-ok|^checkmark|^checkbox|^dialog-apply', 'check'),
    (r'^dialog-cancel|^dialog-close', 'cross'),
    (r'^dialog-warning|^dialog-question', 'warning'),
    (r'^dialog-error', 'error'),
    (r'^dialog-information|^dialog-messages', 'info'),
    (r'^dialog-', 'info'),

    # System.
    (r'^system-shutdown|^system-suspend', 'power'),
    (r'^system-reboot|^system-restart', 'refresh'),
    (r'^system-log-out|^system-switch-user|^system-lock-screen', 'logout'),
    (r'^system-search|^system-file-manager', 'folder'),
    (r'^system-run|^run-|^debug-', 'play'),
    (r'^system-help|^help-', 'question'),
    (r'^system-', 'gear'),

    # Everything else with an obvious home.
    (r'^configure|^settings-|^preferences-|^tools-', 'gear'),
    (r'^overflow-menu|^application-menu|^open-menu', 'menu'),
    (r'^bookmark', 'bookmark'),
    (r'^folder', 'folder'),
    (r'^archive', 'archive'),
    (r'^mail-send|^mail-forward', 'send'),
    (r'^mail-reply', 'reply'),
    (r'^mail-', 'mail'),
    (r'^insert-image|^image-', 'image'),
    (r'^insert-link|^link', 'link'),
    (r'^insert-table', 'table'),
    (r'^insert-text|^text-', 'typeface'),
    (r'^insert-', 'plus'),
    (r'^call-', 'phone'),
    (r'^object-rotate|^transform-rotate', 'rotate'),
    (r'^object-flip|^transform-', 'flip'),
    (r'^object-crop|^crop', 'crop'),
    (r'^object-order|^object-group|^object-', 'layers'),
    (r'^vcs-|^code-', 'nodes'),
    (r'^tag|^flag', 'tag'),
    (r'^star|^rate', 'star'),
    (r'^trash', 'trash'),
    (r'^download|^cloud-download', 'download'),
    (r'^upload|^cloud-upload', 'upload'),
    (r'^cloud', 'globe'),
    (r'^lock|^security-|^password', 'lock'),
    (r'^unlock', 'lock'),
    (r'^games-', 'gamepad'),
    (r'^office-', 'briefcase'),
    (r'^selection-', 'crop'),
    (r'^quit|^exit', 'logout'),
    (r'^new', 'plus'),
    (r'^save', 'save'),
    (r'^open', 'folder'),
    (r'^show', 'eye'),
    (r'^hide', 'eye-off'),
    (r'^list-', 'list'),
]

FALLBACK = 'dots'


def _stem(name):
    s = re.sub(r'-(symbolic|rtl)$', '', name)
    return re.sub(r'-(symbolic|rtl)$', '', s)


def glyph_for(name):
    """The glyph for one action name, or None to leave Breeze's icon alone."""
    stem = _stem(name)
    if not GENERIC.match(stem):
        return None
    for pattern, glyph in RULES:
        if re.search(pattern, stem):
            return glyph
    return FALLBACK


def svgs(stroke_hex, breeze_root):
    """{icon-name: svg} for the generic action families."""
    names = {p.stem for p in (breeze_root / 'actions').rglob('*.svg')}
    out = {}
    for n in sorted(names):
        g = glyph_for(n)
        if g:
            out[n] = _wrap(GLYPHS[g], stroke_hex)
    return out
