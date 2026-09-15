#!/usr/bin/env bash
# Neon Noir — install for Kubuntu 26.04 / KDE Plasma 6.6
#
#   ./install.sh              copy artefacts into place (nothing visibly changes)
#   ./install.sh --apply      copy, then switch the live session to the theme
#   ./install.sh --dry-run    show what would happen, touch nothing
#   ./install.sh --system     also install the root-owned pieces (SDDM, Plymouth)
#   ./install.sh --desktop    also place the clock, system card and media widget
#
# Idempotent: re-running is a no-op. Every config file this script edits is copied
# to $BACKUP first, and only the FIRST time, so the backup always holds your
# pristine pre-Neon-Noir settings no matter how often you re-run.
set -euo pipefail

THEME_ID="NeonNoir"
THEME_NAME="Neon Noir"
PKG_ID="org.neonnoir.desktop"
APPLET_ID="org.neonnoir.sysmon"
SEPARATOR_ID="org.neonnoir.separator"
NN_MARK_BEGIN="# >>> neon noir prompt >>>"
NN_MARK_END="# <<< neon noir prompt <<<"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST="$HERE/dist"
SHARE="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
BACKUP="$CONF/neon-noir-backup"
# libXcursor's search path is compiled in as ~/.icons:/usr/share/icons:
# /usr/share/pixmaps — ~/.local/share/icons is NOT on it, so a cursor theme
# installed there is invisible to both the KCM and the compositor.
ICONS="$HOME/.icons"

DRY=0; APPLY=0; SYSTEM=0; DESKTOP=0
for a in "$@"; do case "$a" in
  --dry-run) DRY=1 ;;
  --apply)   APPLY=1 ;;
  --system)  SYSTEM=1 ;;
  --desktop) DESKTOP=1 ;;
  -h|--help) sed -n '2,13p' "$0" | sed 's/^# \?//'; exit 0 ;;
  *) echo "unknown option: $a" >&2; exit 2 ;;
esac; done

c_ok=$'\033[38;2;109;201;125m'; c_ac=$'\033[38;2;54;215;215m'
c_wn=$'\033[38;2;225;165;54m'; c_dim=$'\033[38;2;161;169;176m'; c_0=$'\033[0m'
say()  { printf '%s::%s %s\n' "$c_ac" "$c_0" "$*"; }
ok()   { printf '   %s✔%s %s\n' "$c_ok" "$c_0" "$*"; }
warn() { printf '   %s!%s %s\n' "$c_wn" "$c_0" "$*"; }
skip() { printf '   %s·%s %s\n' "$c_dim" "$c_0" "$*"; }
run()  { if [ "$DRY" = 1 ]; then printf '   %swould:%s %s\n' "$c_dim" "$c_0" "$*"; else "$@"; fi; }
SUDO=""; [ "$(id -u)" != 0 ] && SUDO="sudo"
# Same as run(), but for the two components that cannot live in $HOME.
srun() { if [ "$DRY" = 1 ]; then printf '   %swould:%s %s %s\n' "$c_dim" "$c_0" "$SUDO" "$*"
         else ${SUDO:+$SUDO} "$@"; fi; }

[ -d "$DIST" ] || { echo "dist/ missing — run: python3 build/generate.py" >&2; exit 1; }

# ── back up anything we are about to edit, once ────────────────────────────────
say "Backing up current settings"
run mkdir -p "$BACKUP" "$BACKUP/gtk-3.0" "$BACKUP/gtk-4.0" "$BACKUP/Kvantum" \
             "$BACKUP/fontconfig" "$BACKUP/firefox" "$BACKUP/xsettingsd" \
             "$BACKUP/kdedefaults"
for f in kdeglobals kwinrc plasmarc breezerc konsolerc katerc dolphinrc \
         kcminputrc ksplashrc \
         kscreenlockerrc plasmashellrc plasma-org.kde.plasma.desktop-appletsrc \
         gtkrc gtkrc-2.0 Trolltech.conf; do
  if [ -f "$CONF/$f" ]; then
    if [ -e "$BACKUP/$f" ]; then skip "$f already backed up"
    else run cp "$CONF/$f" "$BACKUP/$f"; ok "$f"; fi
  fi
done
if [ -f "$CONF/xsettingsd/xsettingsd.conf" ] && [ ! -e "$BACKUP/xsettingsd/xsettingsd.conf" ]; then
  run cp "$CONF/xsettingsd/xsettingsd.conf" "$BACKUP/xsettingsd/xsettingsd.conf"
  ok "xsettingsd.conf"
fi
# plasma-apply-lookandfeel writes its values into this cascade layer, not into
# ~/.config, and it never removes stale keys left by the previous theme.
if [ -d "$CONF/kdedefaults" ] && [ -z "$(ls -A "$BACKUP/kdedefaults" 2>/dev/null)" ]; then
  run cp -r "$CONF/kdedefaults/." "$BACKUP/kdedefaults/"
  ok "kdedefaults/ (the global-theme cascade layer)"
fi
if [ -f "$CONF/Code/User/settings.json" ]; then
  if [ -e "$BACKUP/vscode-settings.json" ]; then skip "VS Code settings already backed up"
  else run cp "$CONF/Code/User/settings.json" "$BACKUP/vscode-settings.json"
       ok "VS Code settings.json"; fi
fi
if [ -f "$CONF/fontconfig/fonts.conf" ]; then
  if [ -e "$BACKUP/fontconfig/fonts.conf" ]; then skip "fontconfig/fonts.conf already backed up"
  else run cp "$CONF/fontconfig/fonts.conf" "$BACKUP/fontconfig/fonts.conf"
       ok "fontconfig/fonts.conf"; fi
fi
if [ -f "$CONF/Kvantum/kvantum.kvconfig" ]; then
  if [ -e "$BACKUP/Kvantum/kvantum.kvconfig" ]; then skip "Kvantum/kvantum.kvconfig already backed up"
  else run cp "$CONF/Kvantum/kvantum.kvconfig" "$BACKUP/Kvantum/kvantum.kvconfig"
       ok "Kvantum/kvantum.kvconfig"; fi
fi
for g in gtk-3.0 gtk-4.0; do
  for f in gtk.css settings.ini; do
    if [ -f "$CONF/$g/$f" ]; then
      if [ -e "$BACKUP/$g/$f" ]; then skip "$g/$f already backed up"
      else run cp "$CONF/$g/$f" "$BACKUP/$g/$f"; ok "$g/$f"; fi
    fi
  done
done
# Record the colour scheme that was active BEFORE we touch anything, so
# uninstall restores what you actually had rather than assuming Breeze Dark.
if [ "$DRY" = 0 ] && [ ! -f "$BACKUP/PREVIOUS_SCHEME" ]; then
  prev="$(kreadconfig6 --file kdeglobals --group General --key ColorScheme 2>/dev/null || true)"
  [ -z "$prev" ] && prev="BreezeDark"
  [ "$prev" = "$THEME_ID" ] || printf '%s\n' "$prev" > "$BACKUP/PREVIOUS_SCHEME"
fi
# Same for the pointer: kcminputrc may not exist yet, in which case the live
# theme is a default that restoring the file would not bring back.
if [ "$DRY" = 0 ] && [ ! -f "$BACKUP/PREVIOUS_CURSOR" ]; then
  prevc="$(kreadconfig6 --file kcminputrc --group Mouse --key cursorTheme 2>/dev/null || true)"
  [ -z "$prevc" ] && prevc="breeze_cursors"
  [ "$prevc" = "$THEME_ID-cursors" ] || printf '%s\n' "$prevc" > "$BACKUP/PREVIOUS_CURSOR"
fi
if [ "$DRY" = 0 ] && [ ! -f "$BACKUP/MANIFEST" ]; then
  { echo "Neon Noir backup of pre-install KDE configuration."
    echo "Restore with: $HERE/uninstall.sh"; } > "$BACKUP/MANIFEST"
fi

# ── install artefacts ──────────────────────────────────────────────────────────
install_file() {  # <src> <dest>
  local src="$1" dst="$2"
  [ -f "$src" ] || { skip "$(basename "$src") not built yet"; return 0; }
  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then skip "$(basename "$dst") unchanged"; return 0; fi
  run install -Dm644 "$src" "$dst"; ok "${dst/#$HOME/\~}"
}
install_tree() { # <srcdir> <destdir>
  local src="$1" dst="$2"
  [ -d "$src" ] || { skip "$(basename "$src") not built yet"; return 0; }
  if [ -d "$dst" ] && diff -rq "$src" "$dst" >/dev/null 2>&1; then
    skip "${dst/#$HOME/\~} unchanged"; return 0; fi
  # Replace rather than merge: copying over an existing tree would leave
  # behind files this build no longer produces.
  run rm -rf "$dst"
  run mkdir -p "$dst"; run cp -r "$src/." "$dst/"; ok "${dst/#$HOME/\~}"
}

say "Colour scheme"
install_file "$DIST/color-schemes/$THEME_ID.colors" "$SHARE/color-schemes/$THEME_ID.colors"

say "Application schemes"
install_file "$DIST/konsole/$THEME_ID.colorscheme" "$SHARE/konsole/$THEME_ID.colorscheme"
install_file "$DIST/konsole/$THEME_ID.profile"     "$SHARE/konsole/$THEME_ID.profile"
install_file "$DIST/konsole/tabbar.qss"             "$SHARE/konsole/tabbar.qss"
install_file "$DIST/syntax-highlighting/neon-noir.theme" \
             "$SHARE/org.kde.syntax-highlighting/themes/neon-noir.theme"

say "GTK 3 / 4 / libadwaita"
install_file "$DIST/gtk/gtk-3.0.css" "$CONF/gtk-3.0/gtk.css"
install_file "$DIST/gtk/gtk-4.0.css" "$CONF/gtk-4.0/gtk.css"

say "Plasma style"
# KSvg caches rendered elements per theme path; a reconfigure alone keeps
# showing the old artwork.
for c in "$HOME/.cache/ksvg-elements" "$HOME/.cache/plasma_theme_$THEME_ID.kcache"; do
  [ -e "$c" ] && run rm -rf "$c"
done
install_tree "$DIST/desktoptheme/$THEME_ID" "$SHARE/plasma/desktoptheme/$THEME_ID"

say "Window decoration"
install_tree "$DIST/aurorae/$THEME_ID" "$SHARE/aurorae/themes/$THEME_ID"

say "Icon theme"
install_tree "$DIST/icons/$THEME_ID" "$SHARE/icons/$THEME_ID"

say "Cursor theme"
install_tree "$DIST/cursors/$THEME_ID-cursors" "$ICONS/$THEME_ID-cursors"

say "Widget style"
install_tree "$DIST/kvantum/$THEME_ID" "$CONF/Kvantum/$THEME_ID"

say "Panel widgets"
install_tree "$DIST/plasmoids/$APPLET_ID" "$SHARE/plasma/plasmoids/$APPLET_ID"
install_tree "$DIST/plasmoids/$SEPARATOR_ID" "$SHARE/plasma/plasmoids/$SEPARATOR_ID"

say "Global theme package"
install_tree "$DIST/look-and-feel/$PKG_ID" "$SHARE/plasma/look-and-feel/$PKG_ID"

say "Wallpaper"
install_tree "$DIST/wallpapers/$THEME_ID" "$SHARE/wallpapers/$THEME_ID"

say "Font rendering"
install_file "$DIST/fontconfig/fonts.conf" "$CONF/fontconfig/fonts.conf"

say "VS Code"
vs_found=0
for d in "$HOME/.vscode/extensions" "$HOME/.vscode-oss/extensions"; do
  [ -d "$d" ] || continue
  install_tree "$DIST/vscode/neon-noir-theme" "$d/neon-noir-theme"
  vs_found=1
done
[ "$vs_found" = 1 ] || skip "no VS Code extensions directory"
# Installing the extension does not select it — VS Code keeps whatever
# workbench.colorTheme already says, so the setting is rewritten here. The file
# is JSONC, so the value is patched textually rather than reparsed.
if [ -f "$CONF/Code/User/settings.json" ] && [ "$DRY" = 0 ]; then
  python3 - "$CONF/Code/User/settings.json" "$THEME_NAME" <<'PYEOF'
import re, sys, pathlib
p, name = pathlib.Path(sys.argv[1]), sys.argv[2]
s = p.read_text()
m = re.search(r'("workbench\.colorTheme"\s*:\s*")([^"]*)(")', s)
if m and m.group(2) != name:
    p.write_text(s[:m.start(2)] + name + s[m.end(2):])
elif not m:
    p.write_text(re.sub(r'^\s*\{', '{\n    "workbench.colorTheme": "%s",' % name, s, count=1))
PYEOF
  ok "VS Code colour theme selected (restart VS Code — new extensions are not hot-loaded)"
elif [ "$DRY" = 1 ]; then
  printf '   %swould:%s select the VS Code colour theme\n' "$c_dim" "$c_0"
fi

say "Firefox"
# Both the deb and the snap keep profiles in their own tree; a real profile is
# any directory with a prefs.js in it.
ff_found=0
for base in "$HOME/.mozilla/firefox" "$HOME/snap/firefox/common/.mozilla/firefox"; do
  [ -d "$base" ] || continue
  for prof in "$base"/*/; do
    [ -f "$prof/prefs.js" ] || continue
    name="$(basename "$prof")"
    run mkdir -p "$prof/chrome" "$BACKUP/firefox/$name"
    install_file "$DIST/firefox/userChrome.css"  "$prof/chrome/userChrome.css"
    install_file "$DIST/firefox/userContent.css" "$prof/chrome/userContent.css"
    # Firefox ignores userChrome.css unless this pref is on, and it can only be
    # set from user.js — append rather than replace, so other prefs survive.
    if [ -f "$prof/user.js" ]; then
      if [ ! -e "$BACKUP/firefox/$name/user.js" ]; then
        run cp "$prof/user.js" "$BACKUP/firefox/$name/user.js"
      fi
      if grep -q legacyUserProfileCustomizations "$prof/user.js" 2>/dev/null; then
        skip "$name: stylesheet pref already set"
      else
        if [ "$DRY" = 1 ]; then printf '   %swould:%s append the stylesheet pref to %s\n' \
             "$c_dim" "$c_0" "$prof/user.js"
        else cat "$DIST/firefox/user.js" >> "$prof/user.js"; fi
        ok "$name: stylesheet pref"
      fi
    else
      install_file "$DIST/firefox/user.js" "$prof/user.js"
    fi
    ff_found=1
  done
done
if [ "$ff_found" = 1 ]; then warn "Firefox must be fully restarted to pick up the chrome"
else skip "no Firefox profile found"; fi

say "Configuration"
if [ -f "$DIST/config/settings.tsv" ]; then
  n=0
  while IFS=$'\t' read -r file group key value; do
    [ -z "${file:-}" ] && continue
    # A group field may name nested groups separated by "/". kwriteconfig6
    # escapes brackets inside a single --group, so nesting has to be passed as
    # repeated --group arguments.
    gargs=(); IFS='/' read -ra parts <<< "$group"
    for part in "${parts[@]}"; do gargs+=(--group "$part"); done
    # --notify is what emits the KConfigWatcher D-Bus signal; without it the
    # file changes but nothing running reloads it.
    run kwriteconfig6 --file "$file" "${gargs[@]}" --key "$key" "${value//@SHARE@/$SHARE}" --notify
    n=$((n+1))
  done < "$DIST/config/settings.tsv"
  ok "$n settings written (decoration, effects, fonts, blur)"
else skip "no settings.tsv"; fi

if [ "$SYSTEM" = 1 ]; then
  say "System components (sudo)"
  # The greeter runs as the unprivileged 'sddm' user and reads only
  # /usr/share/sddm/themes, so this part cannot live in $HOME.
  if [ -d "$DIST/sddm/$THEME_ID" ]; then
    srun rm -rf "/usr/share/sddm/themes/$THEME_ID"
    srun cp -aT "$DIST/sddm/$THEME_ID" "/usr/share/sddm/themes/$THEME_ID"
    srun chown -R root:root "/usr/share/sddm/themes/$THEME_ID"
    srun chmod -R a+rX "/usr/share/sddm/themes/$THEME_ID"
    ok "/usr/share/sddm/themes/$THEME_ID"

    # The pointer has to be system-wide too, for the same reason.
    if [ -d "$DIST/cursors/$THEME_ID-cursors" ]; then
      srun rm -rf "/usr/share/icons/$THEME_ID-cursors"
      srun cp -aT "$DIST/cursors/$THEME_ID-cursors" "/usr/share/icons/$THEME_ID-cursors"
      srun chmod -R a+rX "/usr/share/icons/$THEME_ID-cursors"
      ok "/usr/share/icons/$THEME_ID-cursors"
    fi

    # A NEW drop-in: 10-wayland.conf, 20-kubuntu.conf and kubuntu_settings.conf
    # all belong to kubuntu-settings-desktop and an upgrade can rewrite them.
    # Digits sort before letters, so zz- is unambiguously last.
    tmp="$(mktemp)"
    { echo "[Theme]"
      echo "Current=$THEME_ID"
      echo "CursorTheme=$THEME_ID-cursors"
      echo "CursorSize=24"
      echo "Font=IBM Plex Sans,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"; } > "$tmp"
    srun install -Dm644 "$tmp" /etc/sddm.conf.d/zz-neon-noir.conf
    rm -f "$tmp"
    ok "/etc/sddm.conf.d/zz-neon-noir.conf"
    warn "the login screen changes at the next reboot or 'sudo systemctl restart sddm'"
  else
    skip "SDDM theme not built"
  fi

  # Plymouth. plymouth-set-default-theme does not exist on Ubuntu 26.04 — the
  # theme is selected through update-alternatives, and the splash boots from
  # the initrd copy, so update-initramfs is what actually applies it.
  if [ -d "$DIST/plymouth/$THEME_ID" ]; then
    P="/usr/share/plymouth/themes/$THEME_ID"
    srun rm -rf "$P"
    srun cp -aT "$DIST/plymouth/$THEME_ID" "$P"
    srun chown -R root:root "$P"
    srun chmod -R a+rX "$P"
    ok "$P"
    # The .grub slave keeps /usr/share/plymouth/themes/default.grub from
    # dangling, which is what /etc/grub.d/05_debian_theme inlines.
    srun update-alternatives --install /usr/share/plymouth/themes/default.plymouth \
         default.plymouth "$P/$THEME_ID.plymouth" 200 \
         --slave /usr/share/plymouth/themes/default.grub default.plymouth.grub \
         "$P/$THEME_ID.grub"
    srun update-alternatives --set default.plymouth "$P/$THEME_ID.plymouth"
    ok "registered as the default boot splash"
    say "Rebuilding the initramfs (this takes a moment)"
    srun update-initramfs -u
    ok "initramfs rebuilt"
    if [ -f /boot/grub/grub.cfg ]; then
      srun update-grub
      ok "GRUB colours updated"
    fi
  else
    skip "Plymouth theme not built"
  fi
fi

if [ "$DESKTOP" = 1 ]; then
  say "Panel and desktop widgets"
  if [ -f "$DIST/config/panel-layout.js" ] && command -v qdbus6 >/dev/null; then
    # The framed-hexagon variant, not brand/mark.svg: kickoff draws no button
    # behind its icon, so the design's border has to be inside the SVG.
    install -Dm644 "$DIST/brand/launcher.svg" "$SHARE/icons/neon-noir-launcher.svg" 2>/dev/null || true
    if [ "$DRY" = 1 ]; then
      printf '   %swould:%s reshape the panel (48px, floating, hexagon launcher)\n' "$c_dim" "$c_0"
    else
      # The artboard's pinned apps, in its order, keeping only the ones whose
      # .desktop file exists: a launcher pointing at a missing file still takes
      # a slot and draws a blank page icon.
      # One slot per app, in this order. Each group is a list of spellings for
      # the SAME app and only the first that exists is pinned — the old flat
      # loop pinned `firefox` AND `firefox_firefox` when both were present,
      # giving the browser two slots.
      launchers=""
      pin() {
        for cand in "$@"; do
          for dir in /usr/share/applications "$SHARE/applications" \
                     /var/lib/snapd/desktop/applications \
                     /var/lib/flatpak/exports/share/applications; do
            if [ -f "$dir/$cand.desktop" ]; then
              launchers="${launchers:+$launchers,}applications:$cand.desktop"
              return
            fi
          done
        done
      }
      pin org.kde.konsole konsole
      pin org.kde.dolphin dolphin
      pin firefox_firefox firefox firefox-esr
      pj="$(sed -e "s|@MARK@|$SHARE/icons/neon-noir-launcher.svg|" \
                -e "s|@LAUNCHERS@|$launchers|" "$DIST/config/panel-layout.js")"
      r="$(qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "$pj" 2>&1 | tail -1)"
      ok "${r:-no response from plasmashell}"
    fi
  fi

  # Kate's menubar. katerc's "Show Menu Bar" is not enough on its own: KXmlGui
  # restores the menubar from the WINDOW state in Kate's session file, and that
  # wins. Verified over D-Bus — options_show_menubar stays true until the
  # session key is set. Kate rewrites the session on exit, so a running Kate
  # would undo this.
  say "Kate chrome"
  if pgrep -x kate >/dev/null 2>&1; then
    warn "Kate is running — close it and re-run to hide its menubar"
  else
    for ks in "$SHARE/kate/anonymous.katesession" "$SHARE"/kate/sessions/*.katesession; do
      [ -f "$ks" ] || continue
      name="$(basename "$ks")"
      [ -e "$BACKUP/kate/$name" ] || { run mkdir -p "$BACKUP/kate"; run cp "$ks" "$BACKUP/kate/$name"; }
      # Every window the session remembers, not just the first.
      for g in $(grep -oE '^\[MainWindow[0-9]+ Settings\]$' "$ks" | tr -d '[]'); do
        run kwriteconfig6 --file "$ks" --group "$g" --key MenuBar Disabled
      done
      ok "$name"
    done
  fi

  # Shell prompt. User data like the account picture: the artboard's terminal
  # shows a cyan path, a magenta branch and a caret, none of which a terminal
  # theme can set — the prompt belongs to the shell.
  say "Shell prompt"
  install -Dm644 "$DIST/shell/prompt.bash" "$SHARE/neon-noir/prompt.bash" 2>/dev/null || true
  install -Dm644 "$DIST/shell/prompt.zsh"  "$SHARE/neon-noir/prompt.zsh"  2>/dev/null || true
  for sh in bash zsh; do
    rc="$HOME/.${sh}rc"
    [ -f "$rc" ] || continue
    if [ ! -e "$BACKUP/home-.${sh}rc" ]; then
      run cp "$rc" "$BACKUP/home-.${sh}rc"; ok ".${sh}rc backed up"
    fi
    if grep -q "$NN_MARK_BEGIN" "$rc" 2>/dev/null; then
      skip ".${sh}rc already sources the prompt"
    elif [ "$DRY" = 1 ]; then
      printf '   %swould:%s source the prompt from ~/.%src\n' "$c_dim" "$c_0" "$sh"
    else
      {
        printf '\n%s\n' "$NN_MARK_BEGIN"
        printf '[ -r "%s/neon-noir/prompt.%s" ] && . "%s/neon-noir/prompt.%s"\n' \
               "$SHARE" "$sh" "$SHARE" "$sh"
        printf '%s\n' "$NN_MARK_END"
      } >> "$rc"
      ok "~/.${sh}rc"
    fi
  done

  # Dolphin's view. The artboard's file manager is a details list with no
  # expander arrows, no thumbnails and one set of properties for every folder;
  # Dolphin defaults to an icon grid with per-folder properties. None of that is
  # style — it is view state, which lives here rather than in the theme package.
  # ViewMode=1 is Details (0 is Icons, 2 is Compact).
  say "Dolphin view"
  vp="$SHARE/dolphin/view_properties/global"
  if [ -f "$vp/.directory" ] && [ ! -e "$BACKUP/dolphin-global-directory" ]; then
    run cp "$vp/.directory" "$BACKUP/dolphin-global-directory"
    ok "view properties backed up"
  fi
  if [ "$DRY" = 1 ]; then
    printf '   %swould:%s set the details view for every folder\n' "$c_dim" "$c_0"
  else
    run mkdir -p "$vp"
    cat > "$vp/.directory" <<'EOF'
[Dolphin]
Version=4
ViewMode=1
PreviewsShown=true
GroupedSorting=false
SortRole=text
SortOrder=0
SortFoldersFirst=true
VisibleRoles=Details_text,Details_size,Details_modificationtime
EOF
    ok "details view, no thumbnails"
  fi
  # Previews on, folder previews off. These are two different controls: the
  # artboard draws folders as plain glyphs, but a file manager that cannot show
  # you a picture is worse than one that does not match a drawing. Dropping the
  # directorythumbnail plugin keeps the folder icon plain and leaves image,
  # video and document previews working.
  plugins="$(kreadconfig6 --file dolphinrc --group PreviewSettings --key Plugins 2>/dev/null)"
  if [ -n "$plugins" ]; then
    trimmed="$(printf '%s' "$plugins" | tr ',' '\n' | grep -vx 'directorythumbnail' \
               | paste -sd, -)"
    run kwriteconfig6 --file dolphinrc --group PreviewSettings --key Plugins "$trimmed"
  fi
  run kwriteconfig6 --file dolphinrc --group General --key GlobalViewProps true
  run kwriteconfig6 --file dolphinrc --group DetailsMode --key ExpandableFolders false
  run kwriteconfig6 --file dolphinrc --group "Toolbar mainToolBar" --key IconText IconOnly

  # Dolphin's toolbar, so the location bar can leave it — see the comment in
  # the .rc. KF6 still reads the user's copy from kxmlgui5, not kxmlgui6.
  if [ -f "$DIST/config/dolphinui.rc" ]; then
    rc="$SHARE/kxmlgui5/dolphin/dolphinui.rc"
    if [ -f "$rc" ] && [ ! -e "$BACKUP/dolphinui.rc" ]; then
      run cp "$rc" "$BACKUP/dolphinui.rc"; ok "toolbar layout backed up"
    fi
    run install -Dm644 "$DIST/config/dolphinui.rc" "$rc"
    ok "toolbar: back, forward, up, search, menu — navigator on its own row"
  fi

  # Account picture. This is user data, not theme: Kickoff reads it through
  # KUser, which resolves ~/.face.icon (normally a symlink to ~/.face), and the
  # same file shows on the lock screen. Backed up, and uninstall puts it back.
  initial="$(printf '%s' "${USER:-u}" | cut -c1 | tr '[:lower:]' '[:upper:]')"
  avatar="$DIST/brand/avatars/$initial.png"
  if [ -f "$avatar" ]; then
    say "Account picture"
    for f in .face .face.icon; do
      if [ -f "$HOME/$f" ] && [ ! -L "$HOME/$f" ] && [ ! -e "$BACKUP/home-$f" ]; then
        run cp "$HOME/$f" "$BACKUP/home-$f"; ok "$f backed up"
      fi
    done
    if [ "$DRY" = 1 ]; then
      printf '   %swould:%s write the %s disc to ~/.face\n' "$c_dim" "$c_0" "$initial"
    else
      run cp "$avatar" "$HOME/.face"
      # Recreate the symlink only if it is missing; overwriting a real file the
      # user put there is what the backup above is for.
      [ -e "$HOME/.face.icon" ] || run ln -s .face "$HOME/.face.icon"
      ok "~/.face  ($initial)"
    fi
  fi

  if [ -f "$DIST/config/desktop-layout.js" ] && command -v qdbus6 >/dev/null; then
    if [ "$DRY" = 1 ]; then
      printf '   %swould:%s place the clock, system card and media widget\n' "$c_dim" "$c_0"
    else
      # Through plasmashell's scripting API, not by editing the appletsrc:
      # plasmashell holds that file in memory and rewrites it on exit.
      r="$(qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript \
           "$(cat "$DIST/config/desktop-layout.js")" 2>&1 | tail -1)"
      ok "${r:-no response from plasmashell}"
    fi
  else skip "plasmashell scripting unavailable"; fi
fi

# ── apply ──────────────────────────────────────────────────────────────────────
if [ "$APPLY" = 1 ]; then
  say "Applying to the running session"
  # Plasma's accent system overrides a colour scheme's DecorationFocus/Hover and
  # ForegroundActive by two separate routes, and BOTH must be cleared BEFORE the
  # scheme is applied or the scheme's contrast-checked accent is silently replaced:
  #   1. accentColorFromWallpaper=true -> accent sampled from the wallpaper
  #   2. an explicit AccentColor key   -> a previously picked custom accent, which
  #      survives switching schemes and outranks the scheme's own values.
  run kwriteconfig6 --file kdeglobals --group General --key accentColorFromWallpaper false
  run kwriteconfig6 --file kdeglobals --group General --key AccentColor --delete
  ok "accent overrides cleared (the scheme owns the accent)"

  if command -v plasma-apply-colorscheme >/dev/null; then
    # plasma-apply-colorscheme is a no-op when the named scheme is already the
    # active one, which would leave the stale accent-tinted colour groups in
    # place. Drop the key first so the apply always rewrites every group.
    run kwriteconfig6 --file kdeglobals --group General --key ColorScheme --delete
    run plasma-apply-colorscheme "$THEME_ID" >/dev/null
    ok "colour scheme"
  fi

  if command -v plasma-apply-desktoptheme >/dev/null; then
    run plasma-apply-desktoptheme "$THEME_ID" >/dev/null 2>&1 \
      && ok "Plasma style" || warn "Plasma style could not be applied"
  fi

  # Select the global theme, so System Settings > Global Theme shows Neon Noir
  # as the current one rather than leaving it on the distro default.
  if command -v plasma-apply-lookandfeel >/dev/null; then
    run plasma-apply-lookandfeel -a "$PKG_ID" >/dev/null 2>&1 \
      && ok "global theme selected" || warn "global theme could not be selected"
  fi

  # plasmashell keeps the old SVGs in memory; nothing short of a restart picks
  # up new desktoptheme artwork.
  if systemctl --user --quiet is-active plasma-plasmashell.service 2>/dev/null; then
    run systemctl --user restart plasma-plasmashell.service
    ok "plasmashell restarted"
  fi

  if [ -d "$SHARE/icons/$THEME_ID" ]; then
    run kwriteconfig6 --file kdeglobals --group Icons --key Theme "$THEME_ID"
    command -v gtk-update-icon-cache >/dev/null && \
      run gtk-update-icon-cache -qtf "$SHARE/icons/$THEME_ID" 2>/dev/null || true
    ok "icon theme"
  fi

  # plasma-apply-cursortheme refuses outright when the named theme is already
  # current, and it never writes cursorSize — that key comes from settings.tsv.
  if command -v plasma-apply-cursortheme >/dev/null \
     && [ -d "$ICONS/$THEME_ID-cursors" ]; then
    cur="$(kreadconfig6 --file kcminputrc --group Mouse --key cursorTheme 2>/dev/null || true)"
    if [ "$cur" = "$THEME_ID-cursors" ]; then
      skip "cursor theme already current"
    else
      run plasma-apply-cursortheme "$THEME_ID-cursors" >/dev/null 2>&1 \
        && ok "cursor theme" || warn "cursor theme could not be applied"
    fi
  fi

  # GTK2 has its own file and nothing in Plasma syncs the cursor into it, so
  # GTK2 apps keep the old pointer until this is patched directly.
  if [ -f "$HOME/.gtkrc-2.0" ]; then
    [ -e "$BACKUP/home-gtkrc-2.0" ] || run cp "$HOME/.gtkrc-2.0" "$BACKUP/home-gtkrc-2.0"
    run sed -i -E "s|^gtk-cursor-theme-name=.*|gtk-cursor-theme-name=\"$THEME_ID-cursors\"|;
                   s|^gtk-cursor-theme-size=.*|gtk-cursor-theme-size=24|" "$HOME/.gtkrc-2.0"
    ok "~/.gtkrc-2.0 pointer"
  fi

  if command -v plasma-apply-wallpaperimage >/dev/null \
     && [ -f "$SHARE/wallpapers/$THEME_ID/contents/images/3840x2160.png" ]; then
    run plasma-apply-wallpaperimage "$SHARE/wallpapers/$THEME_ID" >/dev/null 2>&1 \
      && ok "wallpaper" || warn "wallpaper could not be applied automatically"
  fi

  if [ -f "$SHARE/konsole/$THEME_ID.profile" ]; then
    run kwriteconfig6 --file konsolerc --group "Desktop Entry" \
        --key DefaultProfile "$THEME_ID.profile"
    ok "Konsole default profile (new windows only)"
  fi

  # Tab bar. ExpandTabWidth is what stretches every tab across the window;
  # the artboard sizes each one to its own label. Konsole draws this bar
  # itself and no Qt style reaches it, so the borders come from its user
  # stylesheet — the only hook it offers.
  if [ -f "$SHARE/konsole/tabbar.qss" ]; then
    run kwriteconfig6 --file konsolerc --group TabBar --key ExpandTabWidth false
    run kwriteconfig6 --file konsolerc --group TabBar --key TabBarVisibility ShowTabBarWhenNeeded
    run kwriteconfig6 --file konsolerc --group TabBar --key TabBarPosition Top
    # OnTabBar, not OnEachTab. The artboard's tabs carry a label and nothing
    # else, and Konsole's per-tab close button sits 4px from the tab's right
    # EDGE — not its content rect — so no amount of QSS padding or margin
    # moves it off the rule between tabs. Moving it to the end of the bar is
    # the only way to get a clean tab, and it keeps the affordance.
    run kwriteconfig6 --file konsolerc --group TabBar --key CloseTabButton OnTabBar
    run kwriteconfig6 --file konsolerc --group TabBar --key TabBarUseUserStyleSheet true
    # file:// and not a bare path: Konsole declares this key as a Url, so a
    # plain path is read back as an empty URL and the stylesheet is silently
    # ignored — the tabs resize but keep Breeze's underline.
    run kwriteconfig6 --file konsolerc --group TabBar \
        --key TabBarUserStyleSheetFile "file://$SHARE/konsole/tabbar.qss"
    ok "Konsole tab bar"
  fi

  # Reload the compositor so decoration/blur/animation changes take effect now.
  if command -v qdbus6 >/dev/null; then
    run qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
    ok "KWin reconfigured"
  fi
  warn "Kvantum has no file watcher: Qt apps must be restarted to pick up the widget style"
  warn "GTK apps and already-open Qt apps need a restart to pick up the new look"
else
  say "Not applied"
  printf '   %sPick "%s" in System Settings > Colours, or re-run with --apply%s\n' \
         "$c_dim" "$THEME_ID" "$c_0"
fi

printf '\n%s Neon Noir installed.%s  Revert at any time: %s./uninstall.sh%s\n' \
       "$c_ok" "$c_0" "$c_ac" "$c_0"
