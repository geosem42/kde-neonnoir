"""Second-stage artefacts: wallpaper, Konsole profile, GTK CSS, config settings.

Imported by generate.py. Everything here is derived from design/palette.json.
"""
import json, math

def build(T, ANSI, DIST, THEME_ID, THEME_NAME, need, PKG_ID):
    out = []

    # ── fonts ──────────────────────────────────────────────────────────────────
    UI   = 'IBM Plex Sans'     # fonts-ibm-plex, in the Ubuntu 26.04 archive
    MONO = 'JetBrains Mono'    # fonts-jetbrains-mono, likewise
    def qfont(fam, size, weight=400):
        # Qt6 font spec: family,pointSize,pixelSize,styleHint,weight,italic,
        # underline,strikeout,fixedPitch,rawMode,...,styleName
        return f'{fam},{size},-1,5,{weight},0,0,0,0,0,0,0,0,0,0,1'

    # ── wallpaper ──────────────────────────────────────────────────────────────
    def wallpaper_svg(w=3840, h=2160):
        s = min(w, h) / 1080.0
        void, view = T['surface.void'], T['surface.view']
        cy, mg = T['accent.cyan'], T['accent.magenta']
        g = int(64 * s)                      # grid pitch scales with resolution
        cx1, cy1 = w * 0.79, h * 0.80
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="ground" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{T['surface.sheet']}"/>
      <stop offset="55%" stop-color="{void}"/>
      <stop offset="100%" stop-color="{view}"/>
    </linearGradient>
    <radialGradient id="bloomA" cx="0.16" cy="0.10" r="0.40">
      <stop offset="0%" stop-color="{cy}" stop-opacity="0.075"/>
      <stop offset="55%" stop-color="{cy}" stop-opacity="0.022"/>
      <stop offset="100%" stop-color="{cy}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="bloomB" cx="0.86" cy="0.86" r="0.38">
      <stop offset="0%" stop-color="{mg}" stop-opacity="0.055"/>
      <stop offset="100%" stop-color="{mg}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vig" cx="0.5" cy="0.45" r="0.78">
      <stop offset="40%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000205" stop-opacity="0.66"/>
    </radialGradient>
    <pattern id="grid" width="{g}" height="{g}" patternUnits="userSpaceOnUse">
      <path d="M {g} 0 L 0 0 0 {g}" fill="none" stroke="{cy}"
            stroke-opacity="0.055" stroke-width="{max(1, round(1*s))}"/>
    </pattern>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#ground)"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <rect width="{w}" height="{h}" fill="url(#bloomA)"/>
  <rect width="{w}" height="{h}" fill="url(#bloomB)"/>
  <g fill="none" stroke="{cy}" stroke-opacity="0.17" stroke-width="{max(1, round(1.2*s))}">
    <circle cx="{cx1:.0f}" cy="{cy1:.0f}" r="{200*s:.0f}"/>
    <circle cx="{cx1:.0f}" cy="{cy1:.0f}" r="{300*s:.0f}"/>
    <circle cx="{cx1:.0f}" cy="{cy1:.0f}" r="{410*s:.0f}"/>
  </g>
  <g fill="none" stroke="{mg}" stroke-opacity="0.16" stroke-width="{max(1, round(1.2*s))}">
    <path d="M 0 {h*0.593:.0f} L {w*0.262:.0f} {h*0.593:.0f} L {w*0.325:.0f} {h*0.5:.0f} L {w} {h*0.5:.0f}"/>
    <path d="M 0 {h*0.626:.0f} L {w*0.245:.0f} {h*0.626:.0f} L {w*0.308:.0f} {h*0.533:.0f} L {w} {h*0.533:.0f}"/>
  </g>
  <circle cx="{w*0.325:.0f}" cy="{h*0.5:.0f}" r="{4*s:.0f}" fill="{mg}" fill-opacity="0.5"/>
  <circle cx="{w*0.308:.0f}" cy="{h*0.533:.0f}" r="{4*s:.0f}" fill="{cy}" fill-opacity="0.45"/>
  <rect width="{w}" height="{h}" fill="url(#vig)"/>
</svg>
'''

    wp = DIST / 'wallpapers' / THEME_ID / 'contents' / 'images'
    wp.mkdir(parents=True, exist_ok=True)
    svg = wallpaper_svg(3840, 2160)
    (wp / '3840x2160.svg').write_text(svg)
    out.append(f'wallpapers/{THEME_ID}/contents/images/3840x2160.svg')
    try:
        import cairosvg, sys as _sys
        _sys.path.insert(0, str(DIST.parent / 'build'))
        import brand
        for w, h in ((3840, 2160), (1920, 1080)):
            cairosvg.svg2png(bytestring=wallpaper_svg(w, h).encode(),
                             write_to=str(wp / f'{w}x{h}.png'),
                             output_width=w, output_height=h)
            # A near-black gradient steps visibly in 8-bit; dither hides the rings.
            brand.dither(wp / f'{w}x{h}.png')
            out.append(f'wallpapers/{THEME_ID}/contents/images/{w}x{h}.png')
    except Exception as e:                              # pragma: no cover
        out.append(f'  ! PNG render skipped: {e}')
    (DIST / 'wallpapers' / THEME_ID / 'metadata.json').write_text(json.dumps({
        'KPlugin': {'Id': THEME_ID, 'Name': THEME_NAME,
                    'Description': 'Neon Noir desktop wallpaper',
                    'License': 'CC-BY-SA-4.0', 'Version': '1.0',
                    'Authors': [{'Name': 'Neon Noir'}]},
        'KPackageStructure': 'Wallpaper/Images',
    }, indent=2) + '\n')
    out.append(f'wallpapers/{THEME_ID}/metadata.json')

    # ── Konsole profile ────────────────────────────────────────────────────────
    p = DIST / 'konsole' / f'{THEME_ID}.profile'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f'''[Appearance]
ColorScheme={THEME_ID}
Font={qfont(MONO, 11)}
UseFontLineChararacters=false

[General]
Command=/bin/bash
Name={THEME_NAME}
Parent=FALLBACK/
TerminalCenter=false
TerminalMargin=10

[Cursor Options]
CursorShape=0
CustomCursorColor={T['accent.cyan']}
UseCustomCursorColor=true

[Interaction Options]
AutoCopySelectedText=false
TrimLeadingSpacesInSelectedText=true
TrimTrailingSpacesInSelectedText=true
UnderlineFilesEnabled=true

[Scrolling]
HistoryMode=2
ScrollBarPosition=2

[Terminal Features]
BlinkingCursorEnabled=true
''')
    out.append(f'konsole/{THEME_ID}.profile')

    # ── GTK 3 / 4 ──────────────────────────────────────────────────────────────
    def gtk_css(v4):
        hdr = (f'/* {THEME_NAME} — GTK{"4" if v4 else "3"} / libadwaita colour overrides.\n'
               ' * Generated by build/generate.py from design/palette.json.\n */\n')
        defs = [
            ('window_bg_color',      T['surface.window']), ('window_fg_color',   T['text.normal']),
            ('view_bg_color',        T['surface.view']),   ('view_fg_color',     T['text.normal']),
            ('headerbar_bg_color',   T['titlebar.active']),('headerbar_fg_color',T['text.normal']),
            ('headerbar_border_color', T['border.hairline']),
            ('headerbar_backdrop_color', T['titlebar.inactive']),
            ('sidebar_bg_color',     T['surface.sunken']), ('sidebar_fg_color',  T['text.normal']),
            ('sidebar_backdrop_color', T['surface.window']),
            ('secondary_sidebar_bg_color', T['surface.sunken']),
            ('card_bg_color',        T['surface.raised']), ('card_fg_color',     T['text.normal']),
            ('dialog_bg_color',      T['surface.window']), ('dialog_fg_color',   T['text.normal']),
            ('popover_bg_color',     T['surface.float']),  ('popover_fg_color',  T['text.normal']),
            ('accent_bg_color',      T['accent.cyan']),    ('accent_fg_color',   T['text.oncolor']),
            ('accent_color',         T['accent.cyan']),
            ('destructive_bg_color', T['accent.magenta.deep']),
            ('destructive_fg_color', T['text.normal']),
            ('destructive_color',    T['accent.magenta.calm']),
            ('success_bg_color',     T['status.positive']),('success_fg_color',  T['text.oncolor']),
            ('success_color',        T['status.positive']),
            ('warning_bg_color',     T['status.neutral']), ('warning_fg_color',  T['text.oncolor']),
            ('warning_color',        T['status.neutral']),
            ('error_bg_color',       T['status.negative']),('error_fg_color',    T['text.oncolor']),
            ('error_color',          T['status.negative']),
            ('borders',              T['border.hairline']),
            ('theme_bg_color',       T['surface.window']), ('theme_fg_color',    T['text.normal']),
            ('theme_base_color',     T['surface.view']),   ('theme_text_color',  T['text.normal']),
            ('theme_selected_bg_color', T['selection.bg']),
            ('theme_selected_fg_color', T['selection.fg']),
            ('insensitive_fg_color', T['text.disabled']),
            ('insensitive_bg_color', T['surface.disabled']),
        ]
        body = '\n'.join(f'@define-color {k} {v};' for k, v in defs)
        extra = f'''

/* Focus ring matches the Qt side: 1px accent border, no glow at rest. */
*:focus-visible {{ outline: 1px solid {T['accent.cyan']}; outline-offset: -1px; }}
'''
        return hdr + body + extra

    for ver in ('3.0', '4.0'):
        g = DIST / 'gtk' / f'gtk-{ver}.css'
        g.parent.mkdir(parents=True, exist_ok=True)
        g.write_text(gtk_css(ver == '4.0'))
        out.append(f'gtk/gtk-{ver}.css')
    need('text.normal', 'surface.window', 7.0, 'GTK window text')
    need('text.oncolor', 'accent.cyan', 4.5, 'GTK accent label')

    # ── config settings applied with kwriteconfig6 ─────────────────────────────
    # file <TAB> group(/subgroup) <TAB> key <TAB> value
    # Applied individually so the user's unrelated settings are never clobbered.
    S = []
    def add(f, g, k, v): S.append((f, g, k, str(v)))

    # Window decoration. The CONFIG GROUP in Plasma 6.6 is still
    # [org.kde.kdecoration2] — verified in
    # /usr/share/config.kcfg/kwindecorationsettings.kcfg. Only the plugin
    # namespace moved to kdecoration3. Writing kdecoration3 alone does nothing;
    # both are written so the theme survives a future group rename.
    for grp in ('org.kde.kdecoration3', 'org.kde.kdecoration2'):
        add('kwinrc', grp, 'library', 'org.kde.kwin.aurorae')
        add('kwinrc', grp, 'theme', '__aurorae__svg__' + THEME_ID)
        add('kwinrc', grp, 'BorderSize', 'None')
        add('kwinrc', grp, 'BorderSizeAuto', 'false')
        add('kwinrc', grp, 'ButtonsOnRight', 'IAX')
        add('kwinrc', grp, 'ButtonsOnLeft', 'M')
    # Breeze decoration: flat, thin, no gradient — the scheme supplies the colour.
    add('breezerc', 'Common', 'OutlineCloseButton', 'true')
    add('breezerc', 'Common', 'ShadowSize', 'ShadowLarge')
    add('breezerc', 'Common', 'ShadowStrength', '200')
    add('breezerc', 'Common', 'ShadowColor', '0,2,5')
    add('breezerc', 'Windeco', 'DrawBackgroundGradient', 'false')
    add('breezerc', 'Windeco', 'DrawTitleBarSeparator', 'false')
    add('breezerc', 'Windeco', 'TitleAlignment', 'AlignLeft')
    add('breezerc', 'Windeco', 'ButtonSize', 'ButtonDefault')
    add('breezerc', 'Style', 'MenuOpacity', '92')
    # Effects: blur on, measured animation speed.
    add('kwinrc', 'Plugins', 'blurEnabled', 'true')
    add('kwinrc', 'Plugins', 'contrastEnabled', 'true')
    add('kwinrc', 'Effect-blur', 'BlurStrength', '7')
    add('kwinrc', 'Effect-blur', 'NoiseStrength', '0')
    add('kdeglobals', 'KDE', 'AnimationDurationFactor', '0.5')
    # Typography.
    add('kdeglobals', 'General', 'font',                 qfont(UI, 10))
    add('kdeglobals', 'General', 'fixed',                qfont(MONO, 10))
    add('kdeglobals', 'General', 'smallestReadableFont', qfont(UI, 8))
    add('kdeglobals', 'General', 'toolBarFont',          qfont(UI, 10))
    add('kdeglobals', 'General', 'menuFont',             qfont(UI, 10))
    add('kdeglobals', 'WM',      'activeFont',           qfont(UI, 10, 500))
    add('kdeglobals', 'Icons', 'Theme', THEME_ID)
    add('plasmarc', 'Theme', 'name', THEME_ID)
    # Pointer. 24 is the nominal size, which the theme renders as a 32px image.
    add('kcminputrc', 'Mouse', 'cursorTheme', THEME_ID + '-cursors')
    add('kcminputrc', 'Mouse', 'cursorSize', '24')
    # Widget style. The style plugin registers exactly two keys, 'kvantum' and
    # 'kvantum-dark'; only 'kvantum' is verified to load the named theme.
    # The selection file needs a plain [General] group — [%General] there loads
    # the built-in default theme instead, silently.
    add('kdeglobals', 'KDE', 'widgetStyle', 'kvantum')
    add('Kvantum/kvantum.kvconfig', 'General', 'theme', THEME_ID)
    # Splash. The kcfg default for this key is 'org.kde.breeze.desktop', so the
    # value is a look-and-feel package id, not a display name
    # (/usr/share/config.kcfg/splashscreensettings.kcfg).
    add('ksplashrc', 'KSplash', 'Engine', 'KSplashQML')
    add('ksplashrc', 'KSplash', 'Theme', PKG_ID)
    # Lock screen. kscreenlocker_greet loads its QML from the SHELL package, not
    # from look-and-feel, so the only things a theme can change are the colours
    # (it pins itself to the scheme's Complementary set) and this wallpaper.
    # @SHARE@ is expanded by install.sh.
    add('kscreenlockerrc', 'Greeter', 'WallpaperPlugin', 'org.kde.image')
    add('kscreenlockerrc', 'Greeter/Wallpaper/org.kde.image/General', 'Image',
        f'file://@SHARE@/wallpapers/{THEME_ID}')
    # GTK reads its own cursor and icon keys. Plasma's gtkconfig kded normally
    # mirrors kcminputrc into these, but only on its own schedule, so they are
    # written directly too.
    for ver in ('gtk-3.0', 'gtk-4.0'):
        add(f'{ver}/settings.ini', 'Settings', 'gtk-cursor-theme-name', THEME_ID + '-cursors')
        add(f'{ver}/settings.ini', 'Settings', 'gtk-cursor-theme-size', '24')
        add(f'{ver}/settings.ini', 'Settings', 'gtk-icon-theme-name', THEME_ID)

    c = DIST / 'config' / 'settings.tsv'
    c.parent.mkdir(parents=True, exist_ok=True)
    c.write_text(''.join('\t'.join(r) + '\n' for r in S))
    out.append(f'config/settings.tsv  ({len(S)} settings)')
    return out
