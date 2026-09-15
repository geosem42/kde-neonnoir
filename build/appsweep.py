"""Line-art application icons — every app name, not just the curated few.

`appicons.MAP` names the handful of applications the design calls out, and it
stays authoritative. It covers about 100 names; a real machine has several
hundred, so the launcher list and KRunner's results were a column of our grey
outlines interrupted by vendor logos — Blender's, GIMP's, KTorrent's, the whole
LibreOffice family.

So every name breeze-dark ships an `apps/` icon for is classified by pattern
here, exactly as the actions, places and mimetypes are, plus a list of common
third-party names breeze does not ship (those applications install their own
icon into hicolor, and an icon theme wins over hicolor by name).

An unmatched name falls back to `hexagon`, the same neutral mark
`applications-other` uses — it reads as "an application" without claiming to be
a particular one.

What this cannot reach: a desktop entry whose `Icon=` is an absolute path.
Nothing in an icon theme is consulted for those; see install.sh.
"""
import re

from appicons import GLYPHS, _wrap

# Ordered: the first match wins, so specific rules sit above general ones.
RULES = [
    # ── Terminals, editors, IDEs ──────────────────────────────────────────────
    (r'^(yakuake|konsole|terminal|utilities-terminal|xterm|alacritty|kitty|'
     r'tilix|guake|wezterm|foot)$', 'terminal'),
    (r'^(kate|kwrite|accessories-text-editor|text-editor|gedit|pluma|mousepad|'
     r'featherpad|notepadqq|sublime.*|obsidian|antigravity|zed|micro|nano|'
     r'vim|gvim|nvim|neovim|emacs)$', 'editor'),
    (r'^(kdevelop|kapptemplate|kdesrc-build|code|code-oss|vscodium|'
     r'android-studio|jetbrains-.*|.*-pycharm|.*-idea|.*-clion|.*-goland|'
     r'.*-webstorm|.*-rubymine|.*-phpstorm|.*-datagrip|.*-rider|eclipse|'
     r'netbeans|qtcreator|arduino|geany|codeblocks|lazarus)$', 'code'),
    (r'^(kcachegrind|massif-visualizer|hotspot|valgrind)$', 'chip'),
    (r'^(kompare|kdiff3|meld|cervisia|kdesvn|git.*|github-desktop|gitg|'
     r'gitkraken|smartgit|sourcetree)$', 'nodes'),
    (r'^(umbrello|dia|drawio|.*draw\.io.*)$', 'dividers'),
    (r'^(okteta|hexedit|ghex)$', 'code'),
    (r'^(python.*|.*jupyter.*|.*ipython.*|.*rstudio.*)$', 'code'),
    (r'^(.*snapcraft.*|.*flatpak.*|.*appimage.*)$', 'archive'),
    (r'^(kuiviewer|cuttlefish|kirigami-gallery|iconexplorer|ikona|'
     r'symboleditor)$', 'palette'),
    (r'^(baloo|sharedlib|kjournaldbrowser)$', 'drive'),

    # ── Browsers and the web ──────────────────────────────────────────────────
    (r'^(firefox.*|librewolf|waterfox|tor-browser|zen-browser|'
     r'.*\.firefox.*)$', 'browser-flame'),
    (r'^(google-chrome.*|.*\.chrome|chrome)$', 'browser-spokes'),
    (r'^chrome-', 'browser-spokes'),      # Chrome's per-site app shortcuts
    (r'^chromium.*$', 'browser-ring'),
    (r'^(falkon|konqueror|qupzilla|rekonq|internet-web-browser|web-browser|'
     r'brave.*|opera.*|vivaldi.*|epiphany|midori)$', 'globe'),
    (r'^(plasma-browser-integration|kubuntu-web-link|puremaps|marble|'
     r'.*insomnia|postman|bruno|httpie)$', 'globe'),

    # ── Mail, calendars, contacts, notes ──────────────────────────────────────
    (r'^(kmail|kube-mail|mail-client|internet-mail|akonadi|ktnef|kontact|'
     r'thunderbird.*|evolution|geary|bluemail|mailspring)$', 'mail'),
    (r'^(kaddressbook|office-address-book|kuser|.*contacts?)$', 'person'),
    (r'^(korganizer|korgac|korg-todo|office-calendar|kalarm|zanshin|kongress|'
     r'calindori|.*calendar.*)$', 'clock'),
    (r'^(knotes|buho|nota|.*notes?)$', 'document'),
    (r'^(ktimer|ktimetracker|kronometer|kteatime|.*stopwatch.*)$', 'clock'),

    # ── Chat and social ───────────────────────────────────────────────────────
    (r'^(konversation|kopete|choqok|quassel|telepathy.*|.*neochat|hexchat|'
     r'pidgin|discord.*|.*slack.*|element.*|.*\.riot.*|.*zapzap.*|whatsapp.*|'
     r'signal.*|.*telegram.*|.*matrix.*|.*revolt.*|.*mattermost.*|'
     r'kde-im-log-viewer)$', 'bubble'),
    (r'^(internet-telephony|.*skype.*|.*zoom.*|.*jitsi.*|.*teams.*|linphone|'
     r'.*webex.*)$', 'phone'),
    (r'^(akregator|alligator|blogilo|blogger|kblogger|.*feedreader.*|.*rss.*)$', 'list'),

    # ── Games ─────────────────────────────────────────────────────────────────
    (r'^(bomber|bovo|granatier|kapman|katomic|kblackbox|kblocks|kbreakout|'
     r'kdiamond|kfourinline|kgoldrunner|kigo|kiriki|kjumpingcube|klickety|'
     r'klines|kmahjongg|kmines|knavalbattle|knetwalk|knights|kolf|kollision|'
     r'konquest|kpat|kreversi|kshisen|ksirk|ksnakeduel|kspaceduel|ksquares|'
     r'ksudoku|ktuberling|kubrick|lskat|palapeli|picmi|skladnik|kajongg|'
     r'fifteenpuzzle|kblackjack|.*steam.*|lutris|heroic|.*minecraft.*)$',
     'gamepad'),

    # ── Education and science ─────────────────────────────────────────────────
    (r'^(kalzium|step|kstars|.*stellarium.*|.*celestia.*)$', 'atom'),
    (r'^(kbruch|kalgebra|kalgebrabackend|kmplot|kig|cantor|octave|'
     r'octavebackend|juliabackend|rocs|.*sagemath.*|.*geogebra.*|.*maxima.*)$', 'maths'),
    (r'^(kanagram|khangman|kiten|kturtle|ktouch|parley|artikulate|blinken|'
     r'kwordquiz|kgeography|marble-.*|gcompris.*|minuet|.*anki.*)$', 'cap'),
    (r'^(labplot.*|kchart|.*scidavis.*|.*veusz.*|.*gnuplot.*)$', 'table'),
    (r'^(kalzium.*|.*avogadro.*|.*pymol.*|.*chimera.*)$', 'flask'),

    # ── Graphics and photography ──────────────────────────────────────────────
    (r'^(gwenview|showfoto|kphotoalbum|digikam|graphics-viewer-document|'
     r'kipi-.*|'
     r'photolayoutseditor|.*shotwell.*|.*eog.*|.*nomacs.*|.*feh.*|'
     r'.*imageviewer.*)$', 'image'),
    (r'^(kolourpaint|karbon|calligrakarbon|kimagemapeditor|kxstitch|'
     r'kcolorchooser|.*krita.*|gimp.*|.*inkscape.*|.*mypaint.*|.*pinta.*|'
     r'.*aseprite.*|.*figma.*)$', 'palette'),
    (r'^(blender|.*freecad.*|.*openscad.*|.*sweethome.*|.*librecad.*|'
     r'.*qcad.*|.*kicad.*)$', 'dividers'),
    (r'^(spectacle|ksnapshot|accessories-screenshot-tool|.*screenshooter.*|'
     r'.*flameshot.*|.*shutter.*)$', 'camera'),
    (r'^(kamoso|.*cheese.*|.*guvcview.*|.*webcam.*)$', 'camera'),
    (r'^(scanner|skanlite|skanpage|.*simple-scan.*|.*xsane.*)$', 'printer'),

    # ── Audio and video ───────────────────────────────────────────────────────
    (r'^(amarok|elisa|juk|cantata|vvave|.*audacious.*|.*clementine.*|'
     r'.*strawberry.*|.*rhythmbox.*|.*lollypop.*|.*spotify.*|qmmp|'
     r'.*tauon.*)$', 'note'),
    (r'^(dragonplayer|kaffeine|kmplayer|vlc|haruna|.*mpv.*|.*smplayer.*|'
     r'.*totem.*|.*celluloid.*|plasma-media-center|.*kodi.*|.*jellyfin.*|'
     r'.*plex.*|.*stremio.*)$', 'play'),
    (r'^(kdenlive|subtitlecomposer|.*flowblade.*|.*shotcut.*|.*openshot.*|'
     r'.*pitivi.*|.*davinci.*|.*handbrake.*|.*avidemux.*)$', 'film'),
    (r'^(kwave|.*audacity.*|.*ardour.*|.*lmms.*|.*tenacity.*|'
     r'.*mixxx.*)$', 'record'),
    (r'^(.*gpu_screen_recorder.*|.*obs.*|.*simplescreenrecorder.*|'
     r'.*peek.*)$', 'record'),
    (r'^(.*soundrecorder.*|.*qrca.*)$', 'record'),
    (r'^(kmix|multimedia-volume-control|phonon-.*|.*pavucontrol.*|'
     r'.*easyeffects.*)$', 'speaker'),
    (r'^(k3b|.*brasero.*|.*xfburn.*)$', 'archive'),

    # ── Office and documents ──────────────────────────────────────────────────
    (r'^(okular|acroread|.*evince.*|.*zathura.*|.*xpdf.*|.*foxit.*|'
     r'.*qpdfview.*)$', 'book'),
    (r'^(calligrawords|kword|words|.*libreoffice-writer|.*abiword.*|'
     r'.*wps-office-wpsmain.*|.*onlyoffice-desktopeditors.*)$', 'document'),
    (r'^(calligrasheets|kspread|sheets|kexi|calligrakexi|'
     r'.*libreoffice-calc|.*gnumeric.*|.*libreoffice-base)$', 'table'),
    (r'^(calligrastage|kpresenter|stage|.*libreoffice-impress)$', 'slide'),
    (r'^(.*libreoffice-draw)$', 'palette'),
    (r'^(.*libreoffice-math|.*libreoffice-formula)$', 'maths'),
    (r'^(libreoffice.*|.*libreoffice.*|.*onlyoffice.*|.*wps-office.*|'
     r'.*softmaker.*)$', 'briefcase'),
    (r'^(calligraplan|calligraplanwork|kplato|plan|planner|planwork|'
     r'.*projectlibre.*|.*ganttproject.*)$', 'table'),
    (r'^(kmymoney|skrooge|skrooge-black|skrooge-initial|.*homebank.*|'
     r'.*gnucash.*)$', 'table'),
    (r'^(lokalize|crow-translate|crowtranslate|.*poedit.*)$', 'bubble'),
    (r'^(kile|.*texstudio.*|.*texmaker.*|.*lyx.*)$', 'document'),

    # ── Files, archives, search ───────────────────────────────────────────────
    (r'^(system-file-manager|krusader_root|krusader_user|krusader|'
     r'.*nautilus.*|.*thunar.*|.*pcmanfm.*|.*nemo.*|.*doublecmd.*)$', 'folder'),
    (r'^(ark|utilities-file-archiver|.*file-roller.*|.*xarchiver.*|'
     r'.*peazip.*)$', 'archive'),
    (r'^(kfind|system-search|.*catfish.*|.*recoll.*|rofi.*|'
     r'.*albert.*|.*ulauncher.*)$', 'search'),
    (r'^(krename|.*thunar-bulk-rename.*)$', 'pencil'),
    (r'^(filelight|.*baobab.*|.*qdirstat.*|.*ncdu.*)$', 'drive'),
    (r'^(kup|.*timeshift.*|.*deja-dup.*|.*backintime.*|.*borg.*|'
     r'.*restic.*)$', 'save'),

    # ── Networking and transfers ──────────────────────────────────────────────
    (r'^(ktorrent|.*transmission.*|.*qbittorrent.*|.*deluge.*|'
     r'.*jackett.*|.*qbittorrent.*)$', 'download'),
    (r'^(kget|.*freedownloadmanager.*|.*jdownloader.*|.*uget.*|'
     r'kubuntu-manage-software)$', 'download'),
    (r'^(krdc|krfb|.*remmina.*|.*teamviewer.*|.*anydesk.*|.*rustdesk.*|'
     r'.*vinagre.*|.*x2goclient.*)$', 'monitor'),
    (r'^(smb4k|knetattach|network-manager|.*nm-.*|.*filezilla.*|'
     r'.*winscp.*|.*cyberduck.*)$', 'nodes'),
    (r'^(kdeconnect.*|ktrip|kirogi|.*syncthing.*|.*nextcloud.*|.*dropbox.*|'
     r'.*megasync.*|.*insync.*)$', 'sync'),

    # ── Security ──────────────────────────────────────────────────────────────
    (r'^(kgpg|kleopatra|kwalletmanager.*|plasmavault|.*keepass.*|'
     r'.*bitwarden.*|.*1password.*|.*seahorse.*|.*authenticator.*)$', 'lock'),
    (r'^(fingerprint-gui|firewall-config|.*gufw.*|.*ufw.*)$', 'lock'),

    # ── Databases and virtualisation ──────────────────────────────────────────
    (r'^(antares|.*dbeaver.*|.*mysql-workbench.*|.*pgadmin.*|.*sqlite.*|'
     r'.*beekeeper.*|.*tableplus.*)$', 'drive'),
    (r'^(virt-manager|.*virtualbox.*|.*vmware.*|.*gnome-boxes.*|'
     r'.*qemu.*|.*docker.*|.*podman.*|.*distrobox.*)$', 'monitor'),

    # ── System, settings, hardware ────────────────────────────────────────────
    (r'^(systemsettings|breeze-settings|preferences-system|kmenuedit|'
     r'.*gnome-control-center.*|.*xfce4-settings.*)$', 'sliders'),
    (r'^preferences-|^emblem-system', 'sliders'),
    (r'^(.*conky.*|.*scrcpy.*)$', 'monitor'),
    (r'^(utilities-system-monitor|ksysguardd|htop|.*btop.*|'
     r'.*gnome-system-monitor.*|.*mission-center.*)$', 'chip'),
    (r'^(utilities-log-viewer|.*ksystemlog.*)$', 'list'),
    (r'^(utilities-energy-monitor|.*powerdevil.*|.*tlp.*)$', 'power'),
    (r'^(hwinfo|.*cpu-x.*|.*hardinfo.*|.*lshw.*|jockey|'
     r'.*driver-manager.*)$', 'chip'),
    (r'^(partitionmanager|kfloppy|ntfs-config|usb-creator-kde|'
     r'.*gparted.*|.*etcher.*|.*rufus.*|.*ventoy.*)$', 'drive'),
    (r'^(calamares|ubiquity-kde|.*anacondainstaller.*|'
     r'.*installer.*)$', 'download'),
    (r'^(muon|muondiscover|plasmadiscover|apper|system-software-install|'
     r'system-software-update|.*synaptic.*|.*gnome-software.*|'
     r'.*pamac.*|.*octopi.*)$', 'download'),
    (r'^(sweeper|.*bleachbit.*|.*stacer.*)$', 'trash'),
    (r'^(kwin|wayland|xorg|plasma|plasma-nano|plasma-mobile-phone|'
     r'kde|kdeapp|kde-frameworks|planetkde|homerun|latte-dock|plank|'
     r'.*polybar.*|.*waybar.*)$', 'window'),
    (r'^(wine|.*bottles.*|.*playonlinux.*|.*proton.*|.*lutris.*)$', 'window'),
    (r'^(kfontview|.*font-manager.*)$', 'typeface'),
    (r'^(accessories-character-map|kcharselect|'
     r'.*emoji.*|.*emoticons.*)$', 'typeface'),
    (r'^(kmag|kmousetool|kmouth|onboard|.*orca.*|.*accessibility.*)$',
     'keyboard'),
    (r'^(kruler|.*screenruler.*)$', 'dividers'),
    (r'^(klipper|.*clipboard.*|.*copyq.*)$', 'clipboard'),
    (r'^(accessories-calculator|kcalc|.*galculator.*|'
     r'.*qalculate.*)$', 'calculator'),
    (r'^(help-browser|system-help|ktip|kubuntu-.*|.*yelp.*|'
     r'.*devhelp.*)$', 'question'),
    (r'^(tools-report-bug|apport|.*bugreport.*|.*drkonqi.*)$', 'bug'),
    (r'^(system-run|.*krunner.*)$', 'play'),
    (r'^(kcolorchooser|kontrast|.*colorpicker.*|.*gpick.*)$', 'droplet'),
    (r'^(kvantum.*|.*theme.*|.*appearance.*)$', 'palette'),
    (r'^(printer|.*cups.*|.*print-manager.*|hplj.*|.*hp-.*)$', 'printer'),
]

FALLBACK = 'hexagon'

# Applications whose own icon lives in hicolor rather than breeze, so the sweep
# over breeze's names never sees them. An icon theme is searched before
# hicolor, so defining the name here is enough to win.
EXTRA = [
    'antares', 'antigravity', 'obsidian', 'blender', 'gimp', 'github-desktop',
    'com.google.Chrome', 'google-chrome', 'google-chrome-stable', 'brave',
    'brave-browser', 'vivaldi', 'vivaldi-stable', 'opera', 'zapzap',
    'io.github.jliljebl.Flowblade', 'org.freedownloadmanager.Manager',
    'com.dec05eba.gpu_screen_recorder', 'rest.insomnia.Insomnia', 'insomnia',
    'htop', 'jockey', 'onboard', 'remmina', 'org.remmina.Remmina', 'rofi',
    'libreoffice-startcenter', 'libreoffice-writer', 'libreoffice-calc',
    'libreoffice-impress', 'libreoffice-draw', 'libreoffice-math',
    'libreoffice-base', 'libreoffice-main', 'libreoffice',
    'discord', 'slack', 'telegram', 'signal-desktop', 'element-desktop',
    'spotify', 'spotify-client', 'steam', 'lutris', 'heroic',
    'code', 'code-oss', 'vscodium', 'android-studio', 'jetbrains-studio',
    'sublime-text', 'zed', 'micro', 'postman', 'dbeaver', 'virtualbox',
    'org.qbittorrent.qBittorrent', 'transmission', 'deluge',
    'thunderbird', 'evolution', 'obs', 'com.obsproject.Studio',
    'org.kde.krita', 'krita', 'inkscape', 'org.inkscape.Inkscape',
    'audacity', 'shotcut', 'org.shotcut.Shotcut', 'handbrake',
    'nextcloud', 'syncthing', 'dropbox', 'keepassxc', 'bitwarden',
    'timeshift', 'gparted', 'synaptic', 'docker', 'kvantum',
    'haruna', 'kmines', 'ksudoku', 'knetwalk', 'kreversi', 'kollision',
    'kubrick', 'picmi', 'palapeli', 'lskat', 'ksquares', 'knavalbattle',
    'qmmp', 'qbittorrent', 'org.qbittorrent.qBittorrent', 'gvim', 'scrcpy',
    'conky', 'conky-logomark-violet', 'org.kde.qrca', 'qrca',
    'org.gnome.SoundRecorder', 'com.stremio.Stremio', 'stremio',
    'org.telegram.desktop', 'com.rtosta.zapzap',
    'jdownloader', 'jdownloader2', 'hplj1020', 'python3', 'python3.14',
    'io.snapcraft.SessionAgent',
    'system-search', 'chrome-app-list', 'emblem-system-symbolic',
    'internet-web-browser-symbolic', 'kubuntu-web-link',
    'kubuntu-manage-software', 'tools-report-bug', 'apport',
]


def _stem(name):
    s = re.sub(r'\.svg$', '', name)          # org.kde.CrowTranslate.svg
    s = re.sub(r'-symbolic$', '', s)
    s = re.sub(r'^org\.(kde|gnome|freedesktop|xfce)\.', '', s)
    return s.lower()


def glyph_for(name):
    """The glyph for one application icon name. Never None — apps always get one."""
    stem = _stem(name)
    for pattern, glyph in RULES:
        if re.match(pattern, stem):
            return glyph
    return FALLBACK


def svgs(stroke_hex, breeze_root):
    """{icon-name: svg} for every application name we can reach.

    Both the bare name and the `org.kde.` spelling are emitted for each, because
    .desktop files are inconsistent about which one they ask for.
    """
    names = {p.stem for p in (breeze_root / 'apps').rglob('*.svg')}
    # `preferences/` too. A settings module's .desktop asks for its icon by the
    # plain name, and icon lookup scans directories rather than contexts, so a
    # `preferences-desktop-emoticons` written into apps/ answers that request.
    names |= {p.stem for p in (breeze_root / 'preferences').rglob('*.svg')}
    names |= set(EXTRA)
    out = {}
    for n in sorted(names):
        svg = _wrap(GLYPHS[glyph_for(n)], stroke_hex)
        out[n] = svg
        # Breeze ships 14 names ONLY in the -symbolic spelling — vlc, wine,
        # kgpg, virt-manager among them — while their .desktop files ask for
        # the bare name. Emitting just the stem we found leaves those on the
        # vendor logo, so both spellings are written.
        bare = re.sub(r'-symbolic$', '', n)
        out.setdefault(bare, svg)
    return out
