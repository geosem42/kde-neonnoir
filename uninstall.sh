#!/usr/bin/env bash
# Neon Noir — remove the theme and restore the settings saved at first install.
#   ./uninstall.sh            restore and remove
#   ./uninstall.sh --dry-run  show what would happen
#   ./uninstall.sh --system   also remove the root-owned pieces (SDDM, Plymouth)
set -euo pipefail

THEME_ID="NeonNoir"
PKG_ID="org.neonnoir.desktop"
APPLET_ID="org.neonnoir.sysmon"
SHARE="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
BACKUP="$CONF/neon-noir-backup"
# Whatever was active before Neon Noir was installed; Breeze Dark only as a
# last resort if that was never recorded.
FALLBACK="$(cat "$BACKUP/PREVIOUS_SCHEME" 2>/dev/null || echo BreezeDark)"
FALLBACK_CURSOR="$(cat "$BACKUP/PREVIOUS_CURSOR" 2>/dev/null || echo breeze_cursors)"

DRY=0; SYSTEM=0
for a in "$@"; do case "$a" in
  --dry-run) DRY=1 ;;
  --system)  SYSTEM=1 ;;
esac; done
c_ok=$'\033[38;2;109;201;125m'; c_ac=$'\033[38;2;54;215;215m'
c_dim=$'\033[38;2;161;169;176m'; c_wn=$'\033[38;2;225;165;54m'; c_0=$'\033[0m'
say()  { printf '%s::%s %s\n' "$c_ac" "$c_0" "$*"; }
ok()   { printf '   %s✔%s %s\n' "$c_ok" "$c_0" "$*"; }
skip() { printf '   %s·%s %s\n' "$c_dim" "$c_0" "$*"; }
warn() { printf '   %s!%s %s\n' "$c_wn" "$c_0" "$*"; }
run()  { if [ "$DRY" = 1 ]; then printf '   %swould:%s %s\n' "$c_dim" "$c_0" "$*"; else "$@"; fi; }
SUDO=""; [ "$(id -u)" != 0 ] && SUDO="sudo"
srun() { if [ "$DRY" = 1 ]; then printf '   %swould:%s %s %s\n' "$c_dim" "$c_0" "$SUDO" "$*"
         else ${SUDO:+$SUDO} "$@"; fi; }

say "Switching back to $FALLBACK"
if command -v plasma-apply-colorscheme >/dev/null; then
  run plasma-apply-colorscheme "$FALLBACK" || skip "could not switch automatically"
fi

if command -v plasma-apply-cursortheme >/dev/null; then
  run plasma-apply-cursortheme "$FALLBACK_CURSOR" >/dev/null 2>&1 \
    || skip "could not switch the pointer back automatically"
fi

say "Kate chrome"
if [ -d "$BACKUP/kate" ]; then
  if pgrep -x kate >/dev/null 2>&1; then
    warn "Kate is running — close it and re-run to restore its menubar"
  else
    for f in "$BACKUP"/kate/*.katesession; do
      [ -f "$f" ] || continue
      n="$(basename "$f")"
      if [ "$n" = "anonymous.katesession" ]; then d="$SHARE/kate/$n"
      else d="$SHARE/kate/sessions/$n"; fi
      [ -f "$d" ] && { run cp "$f" "$d"; ok "$n"; }
    done
  fi
fi

say "Shell prompt"
for sh in bash zsh; do
  rc="$HOME/.${sh}rc"
  [ -f "$rc" ] || continue
  if grep -q '^# >>> neon noir prompt >>>$' "$rc" 2>/dev/null; then
    run sed -i '/^# >>> neon noir prompt >>>$/,/^# <<< neon noir prompt <<<$/d' "$rc"
    ok "~/.${sh}rc"
  fi
done
run rm -rf "$SHARE/neon-noir"

say "Restoring saved settings"
if [ -d "$BACKUP" ]; then
  for f in "$BACKUP"/*; do
    [ -f "$f" ] || continue
    b="$(basename "$f")"
    case "$b" in MANIFEST|PREVIOUS_SCHEME|PREVIOUS_CURSOR) continue ;;
                 home-gtkrc-2.0) run cp "$f" "$HOME/.gtkrc-2.0"; ok "~/.gtkrc-2.0"; continue ;;
                 home-.face|home-.face.icon|home-.bashrc|home-.zshrc)
                   run cp "$f" "$HOME/${b#home-}"; ok "~/${b#home-}"; continue ;; esac
    run cp "$f" "$CONF/$b"; ok "$b"
  done
  if [ -f "$BACKUP/fontconfig/fonts.conf" ]; then
    run cp "$BACKUP/fontconfig/fonts.conf" "$CONF/fontconfig/fonts.conf"; ok "fontconfig/fonts.conf"
  elif [ -f "$CONF/fontconfig/fonts.conf" ]; then
    run rm -f "$CONF/fontconfig/fonts.conf"; ok "fontconfig/fonts.conf removed"
  fi
  if [ -f "$BACKUP/Kvantum/kvantum.kvconfig" ]; then
    run cp "$BACKUP/Kvantum/kvantum.kvconfig" "$CONF/Kvantum/kvantum.kvconfig"
    ok "Kvantum/kvantum.kvconfig"
  elif [ -f "$CONF/Kvantum/kvantum.kvconfig" ]; then
    run rm -f "$CONF/Kvantum/kvantum.kvconfig"; ok "Kvantum/kvantum.kvconfig removed"
  fi
  if [ -f "$BACKUP/xsettingsd/xsettingsd.conf" ]; then
    run cp "$BACKUP/xsettingsd/xsettingsd.conf" "$CONF/xsettingsd/xsettingsd.conf"
    ok "xsettingsd.conf"
  fi
  if [ -n "$(ls -A "$BACKUP/kdedefaults" 2>/dev/null)" ]; then
    run rm -rf "$CONF/kdedefaults"
    run cp -r "$BACKUP/kdedefaults" "$CONF/kdedefaults"
    ok "kdedefaults/ restored"
  fi
  for g in gtk-3.0 gtk-4.0; do
    for f in gtk.css settings.ini; do
      if [ -f "$BACKUP/$g/$f" ]; then
        run cp "$BACKUP/$g/$f" "$CONF/$g/$f"; ok "$g/$f"
      elif [ -f "$CONF/$g/$f" ]; then
        # we created it; there was nothing there before
        run rm -f "$CONF/$g/$f"; ok "$g/$f removed"
      fi
    done
  done
else skip "no backup directory — nothing to restore"; fi

say "Firefox and VS Code"
if [ -f "$BACKUP/vscode-settings.json" ]; then
  run cp "$BACKUP/vscode-settings.json" "$CONF/Code/User/settings.json"
  ok "VS Code settings.json restored"
fi
for d in "$HOME/.vscode/extensions/neon-noir-theme" "$HOME/.vscode-oss/extensions/neon-noir-theme"; do
  if [ -d "$d" ]; then run rm -rf "$d"; ok "${d/#$HOME/\~}"; fi
done
for base in "$HOME/.mozilla/firefox" "$HOME/snap/firefox/common/.mozilla/firefox"; do
  [ -d "$base" ] || continue
  for prof in "$base"/*/; do
    [ -f "$prof/prefs.js" ] || continue
    name="$(basename "$prof")"
    for f in userChrome.css userContent.css; do
      [ -f "$prof/chrome/$f" ] && { run rm -f "$prof/chrome/$f"; ok "$name/chrome/$f"; }
    done
    if [ -f "$BACKUP/firefox/$name/user.js" ]; then
      run cp "$BACKUP/firefox/$name/user.js" "$prof/user.js"; ok "$name/user.js restored"
    elif [ -f "$prof/user.js" ]; then
      run rm -f "$prof/user.js"; ok "$name/user.js removed"
    fi
  done
done

say "Dolphin view"
rc="$SHARE/kxmlgui5/dolphin/dolphinui.rc"
if [ -f "$BACKUP/dolphinui.rc" ]; then
  run cp "$BACKUP/dolphinui.rc" "$rc"; ok "toolbar layout restored"
elif [ -f "$rc" ]; then
  run rm -f "$rc"; ok "toolbar layout removed"
fi
vp="$SHARE/dolphin/view_properties/global/.directory"
if [ -f "$BACKUP/dolphin-global-directory" ]; then
  run cp "$BACKUP/dolphin-global-directory" "$vp"; ok "view properties restored"
elif [ -f "$vp" ]; then
  run rm -f "$vp"; ok "view properties removed"
else skip "no view properties to restore"; fi

say "Removing installed files"
for p in "$SHARE/color-schemes/$THEME_ID.colors" \
         "$SHARE/konsole/$THEME_ID.colorscheme" \
         "$SHARE/konsole/tabbar.qss" \
         "$SHARE/konsole/$THEME_ID.profile" \
         "$SHARE/org.kde.syntax-highlighting/themes/neon-noir.theme"; do
  if [ -e "$p" ]; then run rm -f "$p"; ok "${p/#$HOME/\~}"; else skip "${p/#$HOME/\~} absent"; fi
done
for d in "$SHARE/plasma/desktoptheme/$THEME_ID" "$SHARE/aurorae/themes/$THEME_ID" \
         "$SHARE/icons/$THEME_ID" "$HOME/.icons/$THEME_ID-cursors" \
         "$SHARE/plasma/look-and-feel/$PKG_ID" "$CONF/Kvantum/$THEME_ID" \
         "$SHARE/plasma/plasmoids/$APPLET_ID"; do
  if [ -d "$d" ]; then run rm -rf "$d"; ok "${d/#$HOME/\~}"; else skip "${d/#$HOME/\~} absent"; fi
done
if [ -d "$SHARE/wallpapers/$THEME_ID" ]; then
  run rm -rf "$SHARE/wallpapers/$THEME_ID"; ok "~/.local/share/wallpapers/$THEME_ID"
else skip "wallpaper absent"; fi
if [ "$SYSTEM" = 1 ]; then
  say "Removing system components (sudo)"
  P="/usr/share/plymouth/themes/$THEME_ID"
  if [ -e "$P/$THEME_ID.plymouth" ]; then
    srun update-alternatives --remove default.plymouth "$P/$THEME_ID.plymouth"
    # Back to automatic, which picks the highest-priority packaged theme again.
    srun update-alternatives --auto default.plymouth
    ok "boot splash deregistered"
  fi
  for p in "/usr/share/sddm/themes/$THEME_ID" "/usr/share/icons/$THEME_ID-cursors" \
           /etc/sddm.conf.d/zz-neon-noir.conf "$P"; do
    if [ -e "$p" ]; then srun rm -rf "$p"; ok "$p"; else skip "$p absent"; fi
  done
  say "Rebuilding the initramfs (this takes a moment)"
  srun update-initramfs -u
  [ -f /boot/grub/grub.cfg ] && srun update-grub
  ok "boot image restored"
fi

if command -v qdbus6 >/dev/null; then
  run qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true; ok "KWin reconfigured"
fi

printf '\n%s Neon Noir removed.%s  The backup is kept at %s%s%s\n' \
       "$c_ok" "$c_0" "$c_ac" "${BACKUP/#$HOME/\~}" "$c_0"
