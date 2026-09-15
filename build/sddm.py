"""SDDM greeter theme.

Written in plain QtQuick on purpose. Three things the greeter does NOT give a
theme, all verified on this box rather than assumed:

  - QtQuick.Controls resolves to the Basic style (there is no
    qtquickcontrols2.conf anywhere and the greeter sets no QQuickStyle), so a
    QQC2 Button or TextField renders as flat white Qt chrome. Every control
    here is a Rectangle + TextInput + MouseArea.
  - i18n/i18nd/i18nc/i18ndc are undefined in the greeter context — the shipped
    breeze theme calls them anyway, so copying breeze code imports a
    ReferenceError. All strings here are literals.
  - Kirigami loads but its palette returns #000000 for every role, and no icon
    theme is loaded. Colours are baked in from the palette and every glyph is
    an SVG shipped inside the theme directory.

Also: every theme.conf value arrives in QML as a STRING, so booleans are
compared against "true".
"""
import json, shutil

ICONS = {
    'lock': 'M 7 10 V 7.5 a 5 5 0 0 1 10 0 V 10 M 5.6 10 h 12.8 a 1.4 1.4 0 0 1 1.4 1.4 '
            'v 7.2 a 1.4 1.4 0 0 1 -1.4 1.4 H 5.6 a 1.4 1.4 0 0 1 -1.4 -1.4 v -7.2 '
            'a 1.4 1.4 0 0 1 1.4 -1.4 Z',
    'eye': 'M 1.8 12 C 4.6 7.4 8.1 5.1 12 5.1 c 3.9 0 7.4 2.3 10.2 6.9 '
           'C 19.4 16.6 15.9 18.9 12 18.9 C 8.1 18.9 4.6 16.6 1.8 12 Z '
           'M 12 8.7 a 3.3 3.3 0 1 0 0 6.6 a 3.3 3.3 0 1 0 0 -6.6 Z',
    'eye-off': 'M 1.8 12 C 4.6 7.4 8.1 5.1 12 5.1 c 1.4 0 2.8 0.3 4.1 0.9 '
               'M 22.2 12 c -1.4 2.3 -3 4 -4.8 5.1 M 12 8.7 a 3.3 3.3 0 0 1 3.3 3.3 '
               'M 12 15.3 A 3.3 3.3 0 0 1 8.7 12 M 3.5 3.5 L 20.5 20.5',
    'arrow': 'M 5 12 H 19 M 13 6 L 19 12 L 13 18',
    'chevron': 'M 7 10 L 12 15 L 17 10',
    'power': 'M 12 3.5 V 11 M 6.6 6.4 a 7.6 7.6 0 1 0 10.8 0',
    'restart': 'M 20 5.5 v 5.2 h -5.2 M 19.3 13 A 7.6 7.6 0 1 1 18.4 8.2 L 20 10.7',
    'suspend': 'M 19.5 14.6 A 8 8 0 0 1 9.4 4.5 a 8 8 0 1 0 10.1 10.1 Z',
    'keyboard': 'M 3.5 6.5 h 17 v 11 h -17 Z M 7 10 h 0.01 M 11 10 h 0.01 M 15 10 h 0.01 '
                'M 7 13.5 h 10',
}


def icon_svg(path, colour, w=1.7):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
            f'viewBox="0 0 24 24"><path d="{path}" fill="none" stroke="{colour}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def distro_name():
    """Whatever this machine calls itself, upper-cased for the top rule."""
    try:
        with open('/etc/os-release') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    return line.split('=', 1)[1].strip().strip('"').upper()
    except OSError:
        pass
    return 'LINUX'


THEME_CONF = '''[General]
type=image
background=images/background.png
color=@VOID@
needsFullUserModel=false
'''

METADATA = '''[SddmGreeterTheme]
Name=@NAME@
Description=@DESC@
Author=George
Copyright=George
License=GPL-3.0-or-later
Type=sddm-theme
Version=1.0
Website=
Screenshot=preview.png
MainScript=Main.qml
ConfigFile=theme.conf
TranslationsDirectory=
Theme-Id=@ID@
Theme-API=2.0
QtVersion=6
'''


def build(T, DIST, THEME_ID, THEME_NAME, template_dir):
    import brand
    out = []
    root = DIST / 'sddm' / THEME_ID
    (root / 'images').mkdir(parents=True, exist_ok=True)

    subs = {
        '@VOID@': T['surface.void'],   '@CARD@': T['surface.raised'],
        '@VIEW@': T['surface.view'],   '@RAISED@': T['surface.float'],
        '@HAIR@': T['border.hairline'], '@FLOAT@': T['surface.float'],
        '@HOVER@': T['surface.hover'], '@TEXT@': T['text.normal'],
        '@DIM@': T['text.dim'],        '@CYAN@': T['accent.cyan'],
        '@CYANHI@': T['accent.cyan.hover'], '@MAGENTA@': T['accent.magenta'],
        '@INK@': T['text.oncolor'],    '@NEG@': T['status.negative'],
        '@NEUTRAL@': T['status.neutral'], '@FONT@': 'IBM Plex Sans',
        '@DISTRO@': distro_name(),
        '@NAME@': THEME_NAME, '@ID@': THEME_ID,
        '@DESC@': 'Neon noir login — cyan and magenta on blue-black',
    }

    def fill(text):
        for k, v in subs.items():
            text = text.replace(k, str(v))
        return text

    qml = (template_dir / 'sddm-Main.qml').read_text()
    left = [k for k in subs if k in qml and k not in ('@NAME@', '@ID@', '@DESC@')]
    (root / 'Main.qml').write_text(fill(qml))
    (root / 'theme.conf').write_text(fill(THEME_CONF))
    (root / 'metadata.desktop').write_text(fill(METADATA))
    out.append(f'sddm/{THEME_ID}/Main.qml  ({len(left)} tokens substituted)')
    out.append(f'sddm/{THEME_ID}/theme.conf, metadata.desktop')

    # No icon theme is loaded in the greeter, so every glyph ships here.
    for name, path in ICONS.items():
        colour = {'arrow': T['text.oncolor']}.get(name, T['text.dim'])
        (root / 'images' / f'{name}.svg').write_text(icon_svg(path, colour))
    out.append(f'sddm/{THEME_ID}/images/*.svg  ({len(ICONS)} glyphs)')

    # Self-contained background: the greeter runs as the sddm user and cannot
    # read a wallpaper under /home.
    wall = DIST / 'wallpapers' / THEME_ID / 'contents' / 'images' / '1920x1080.png'
    if wall.exists():
        shutil.copy(wall, root / 'images' / 'background.png')
        out.append(f'sddm/{THEME_ID}/images/background.png')
    shot = DIST.parent / 'design' / 'png' / '07-boot-chain.png'
    if shot.exists():
        from PIL import Image
        im = Image.open(shot).convert('RGB')
        im.crop((44, 140, 946, 656)).resize((640, 366), Image.LANCZOS).save(root / 'preview.png')
        out.append(f'sddm/{THEME_ID}/preview.png')
    return out
