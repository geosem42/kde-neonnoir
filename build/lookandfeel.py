"""The global theme (look-and-feel) package, and the KSplash stage inside it.

A Plasma/LookAndFeel package is what System Settings > Global Theme lists. Its
contents/defaults file is the single place that names every other piece of the
theme, so switching to it in one click pulls in the colour scheme, Plasma style,
decoration, icons, cursor and wallpaper together.

The splash is the only screen in the package that this Plasma version actually
renders from here. The lock screen is NOT: kscreenlocker_greet loads
lockscreenmainscript from the SHELL package
(/usr/share/plasma/shells/org.kde.plasma.desktop/contents/lockscreen/), and its
binary contains no look-and-feel lookup at all, so a contents/lockscreen/ here
would be silently ignored. The lock screen is themed instead through the
scheme's [Colors:Complementary] group — which is the colour set
LockScreenUi.qml pins itself to — plus its own wallpaper key.
"""
import json, shutil


SPLASH_QML = '''/*
    Neon Noir splash — the same lockup Plymouth draws, so the handover from
    boot to session start has no visible seam.

    ksplashqml drives `stage` from 0 upwards as startup proceeds. Breeze fades
    in at 2 and starts fading out at 5; the progress rule here maps the same
    range so the bar is full exactly as the desktop appears.
*/
import QtQuick

Rectangle {{
    id: root
    color: "{void}"

    property int stage

    readonly property real u: Math.max(8, Math.round(Math.min(width, height) / 90))

    onStageChanged: {{
        if (stage >= 2) {{
            content.opacity = 1;
        }}
        if (stage >= 6) {{
            content.opacity = 0;
        }}
    }}

    Image {{
        anchors.fill: parent
        source: "images/ground.png"
        fillMode: Image.PreserveAspectCrop
        asynchronous: false
    }}

    Item {{
        id: content
        anchors.fill: parent
        opacity: 0
        Behavior on opacity {{ NumberAnimation {{ duration: 420; easing.type: Easing.OutCubic }} }}

        Column {{
            anchors.centerIn: parent
            spacing: root.u * 3.0

            Image {{
                id: mark
                anchors.horizontalCenter: parent.horizontalCenter
                source: "images/mark.png"
                sourceSize.width: root.u * 19
                sourceSize.height: root.u * 19
                width: root.u * 19
                height: root.u * 19
            }}

            Text {{
                anchors.horizontalCenter: parent.horizontalCenter
                text: "{wordmark}"
                color: "{text}"
                font.family: "{font}"
                font.weight: Font.Medium
                font.pixelSize: root.u * 2.5
                font.letterSpacing: root.u * 0.85
                // letterSpacing pads the right of the last glyph too; pull back
                // by half so the word stays optically centred under the mark.
                // An x binding would be ignored here — Column children may use
                // horizontal anchors, and the anchor wins over x.
                anchors.horizontalCenterOffset: -font.letterSpacing / 2
            }}

            Item {{
                id: track
                anchors.horizontalCenter: parent.horizontalCenter
                width: root.u * 28
                height: 2

                Rectangle {{
                    anchors.fill: parent
                    color: "{rule}"
                    opacity: 0.55
                }}
                Rectangle {{
                    height: parent.height
                    color: "{cyan}"
                    width: parent.width * Math.min(1, Math.max(0, (root.stage - 1) / 5))
                    Behavior on width {{
                        NumberAnimation {{ duration: 320; easing.type: Easing.OutCubic }}
                    }}
                }}
            }}
        }}
    }}
}}
'''


def ground_svg(T, w, h):
    """A plain dark ground with one cyan and one magenta bloom — no filters, so
    it renders identically in cairosvg here and in Plymouth's framebuffer."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0%" stop-color="{T['surface.sheet']}"/>
      <stop offset="60%" stop-color="{T['surface.void']}"/>
      <stop offset="100%" stop-color="{T['surface.view']}"/>
    </linearGradient>
    <radialGradient id="a" cx="0.5" cy="0.42" r="0.45">
      <stop offset="0%" stop-color="{T['accent.cyan']}" stop-opacity="0.055"/>
      <stop offset="100%" stop-color="{T['accent.cyan']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="b" cx="0.5" cy="0.42" r="0.20">
      <stop offset="0%" stop-color="{T['accent.magenta']}" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="{T['accent.magenta']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="v" cx="0.5" cy="0.45" r="0.75">
      <stop offset="45%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000205" stop-opacity="0.6"/>
    </radialGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#g)"/>
  <rect width="{w}" height="{h}" fill="url(#a)"/>
  <rect width="{w}" height="{h}" fill="url(#b)"/>
  <rect width="{w}" height="{h}" fill="url(#v)"/>
</svg>
'''

def dither(path, amount=1):
    """Break up banding in a near-black gradient.

    At these lightnesses an 8-bit ramp steps visibly; a fixed-seed +/-1 LSB of
    noise hides the rings. Seeded so the build stays byte-reproducible.
    """
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(path).convert('RGB'), dtype=np.int16)
    rng = np.random.default_rng(20260916)
    a = np.clip(a + rng.integers(-amount, amount + 1, a.shape, dtype=np.int16), 0, 255)
    Image.fromarray(a.astype('uint8')).save(path)


def build(T, DIST, THEME_ID, THEME_NAME, PKG_ID, widget_style='Breeze'):
    import brand
    out = []
    root = DIST / 'look-and-feel' / PKG_ID
    (root / 'contents' / 'splash' / 'images').mkdir(parents=True, exist_ok=True)
    (root / 'contents' / 'previews').mkdir(parents=True, exist_ok=True)
    (root / 'contents' / 'layouts').mkdir(parents=True, exist_ok=True)

    (root / 'metadata.json').write_text(json.dumps({
        'KPackageStructure': 'Plasma/LookAndFeel',
        'KPlugin': {
            'Id': PKG_ID,
            'Name': THEME_NAME,
            'Description': 'Neon noir: cyan and magenta on blue-black, '
                           'accent only where something is focused, selected or running',
            'Authors': [{'Name': 'George', 'Email': 'geosem042@gmail.com'}],
            'License': 'GPL-3.0-or-later',
            'Category': '',
            'Website': '',
        },
    }, indent=4) + '\n')
    out.append(f'look-and-feel/{PKG_ID}/metadata.json')

    # Every other piece of the theme, named in one place. Applying the global
    # theme pulls all of these in; it does NOT touch the panel layout unless
    # plasma-apply-lookandfeel is given --resetLayout.
    (root / 'contents' / 'defaults').write_text(f'''[kdeglobals][KDE]
widgetStyle={widget_style}

[kdeglobals][General]
ColorScheme={THEME_ID}

[kdeglobals][Icons]
Theme={THEME_ID}

[plasmarc][Theme]
name={THEME_ID}

[Wallpaper]
Image={THEME_ID}

[kcminputrc][Mouse]
cursorTheme={THEME_ID}-cursors

[kwinrc][org.kde.kdecoration2]
library=org.kde.kwin.aurorae
theme=__aurorae__svg__{THEME_ID}

[kwinrc][org.kde.kdecoration3]
library=org.kde.kwin.aurorae
theme=__aurorae__svg__{THEME_ID}

[KSplash]
Theme={PKG_ID}
''')
    out.append(f'look-and-feel/{PKG_ID}/contents/defaults')

    # Only read when the user explicitly asks for a layout reset.
    (root / 'contents' / 'layouts' / 'org.kde.plasma.desktop-layout.js').write_text(
        'loadTemplate("org.kde.plasma.desktop.defaultPanel")\n\n'
        'var desktops = desktopsForActivity(currentActivity());\n'
        'for (var i = 0; i < desktops.length; i++) {\n'
        "    desktops[i].wallpaperPlugin = 'org.kde.image';\n"
        '}\n')
    out.append(f'look-and-feel/{PKG_ID}/contents/layouts/org.kde.plasma.desktop-layout.js')

    splash = root / 'contents' / 'splash'
    (splash / 'Splash.qml').write_text(SPLASH_QML.format(
        void=T['surface.void'], text=T['text.normal'], cyan=T['accent.cyan'],
        rule=T['border.float'], font='IBM Plex Sans', wordmark='NEON NOIR'))
    brand.png(brand.mark_svg(T, 384), splash / 'images' / 'mark.png', 384, 384)
    brand.png(ground_svg(T, 1920, 1080), splash / 'images' / 'ground.png', 1920, 1080)
    dither(splash / 'images' / 'ground.png')
    out.append(f'look-and-feel/{PKG_ID}/contents/splash/  (Splash.qml, mark, ground)')

    prev = root / 'contents' / 'previews'
    from PIL import Image
    wall = DIST / 'wallpapers' / THEME_ID / 'contents' / 'images' / '1920x1080.png'
    if wall.exists():
        Image.open(wall).convert('RGB').save(prev / 'fullscreenpreview.jpg', quality=92)
        out.append(f'look-and-feel/{PKG_ID}/contents/previews/fullscreenpreview.jpg')
    desktop_shot = DIST.parent / 'design' / 'png' / '01-desktop.png'
    if desktop_shot.exists():
        Image.open(desktop_shot).convert('RGB').resize((600, 337), Image.LANCZOS) \
             .save(prev / 'preview.png')
        out.append(f'look-and-feel/{PKG_ID}/contents/previews/preview.png')
    # The splash preview is the splash itself at the moment the bar is full.
    sp = Image.open(splash / 'images' / 'ground.png').convert('RGBA').resize((300, 169), Image.LANCZOS)
    mark = Image.open(splash / 'images' / 'mark.png').resize((58, 58), Image.LANCZOS)
    sp.alpha_composite(mark, (121, 42))
    wm = DIST / 'brand' / 'wordmark.png'
    if wm.exists():
        w = Image.open(wm)
        w = w.resize((96, max(1, round(96 * w.height / w.width))), Image.LANCZOS)
        sp.alpha_composite(w, ((300 - w.width) // 2, 112))
    sp.convert('RGB').save(prev / 'splash.png')
    out.append(f'look-and-feel/{PKG_ID}/contents/previews/splash.png')
    return out
