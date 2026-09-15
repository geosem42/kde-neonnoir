#!/usr/bin/env bash
# Neon Noir — remove the theme and restore the settings saved at first install.
#   ./uninstall.sh            restore and remove
#   ./uninstall.sh --dry-run  show what would happen
set -euo pipefail

THEME_ID="NeonNoir"
PKG_ID="org.neonnoir.desktop"
SHARE="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
BACKUP="$CONF/neon-noir-backup"
# Whatever was active before Neon Noir was installed; Breeze Dark only as a
# last resort if that was never recorded.
FALLBACK="$(cat "$BACKUP/PREVIOUS_SCHEME" 2>/dev/null || echo BreezeDark)"
FALLBACK_CURSOR="$(cat "$BACKUP/PREVIOUS_CURSOR" 2>/dev/null || echo breeze_cursors)"

DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1
c_ok=$'\033[38;2;109;201;125m'; c_ac=$'\033[38;2;54;215;215m'
c_dim=$'\033[38;2;161;169;176m'; c_0=$'\033[0m'
say()  { printf '%s::%s %s\n' "$c_ac" "$c_0" "$*"; }
ok()   { printf '   %s✔%s %s\n' "$c_ok" "$c_0" "$*"; }
skip() { printf '   %s·%s %s\n' "$c_dim" "$c_0" "$*"; }
run()  { if [ "$DRY" = 1 ]; then printf '   %swould:%s %s\n' "$c_dim" "$c_0" "$*"; else "$@"; fi; }

say "Switching back to $FALLBACK"
if command -v plasma-apply-colorscheme >/dev/null; then
  run plasma-apply-colorscheme "$FALLBACK" || skip "could not switch automatically"
fi

if command -v plasma-apply-cursortheme >/dev/null; then
  run plasma-apply-cursortheme "$FALLBACK_CURSOR" >/dev/null 2>&1 \
    || skip "could not switch the pointer back automatically"
fi

say "Restoring saved settings"
if [ -d "$BACKUP" ]; then
  for f in "$BACKUP"/*; do
    [ -f "$f" ] || continue
    b="$(basename "$f")"
    case "$b" in MANIFEST|PREVIOUS_SCHEME|PREVIOUS_CURSOR) continue ;; esac
    run cp "$f" "$CONF/$b"; ok "$b"
  done
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

say "Removing installed files"
for p in "$SHARE/color-schemes/$THEME_ID.colors" \
         "$SHARE/konsole/$THEME_ID.colorscheme" \
         "$SHARE/konsole/$THEME_ID.profile" \
         "$SHARE/org.kde.syntax-highlighting/themes/neon-noir.theme"; do
  if [ -e "$p" ]; then run rm -f "$p"; ok "${p/#$HOME/\~}"; else skip "${p/#$HOME/\~} absent"; fi
done
for d in "$SHARE/plasma/desktoptheme/$THEME_ID" "$SHARE/aurorae/themes/$THEME_ID" \
         "$SHARE/icons/$THEME_ID" "$HOME/.icons/$THEME_ID-cursors" \
         "$SHARE/plasma/look-and-feel/$PKG_ID"; do
  if [ -d "$d" ]; then run rm -rf "$d"; ok "${d/#$HOME/\~}"; else skip "${d/#$HOME/\~} absent"; fi
done
if [ -d "$SHARE/wallpapers/$THEME_ID" ]; then
  run rm -rf "$SHARE/wallpapers/$THEME_ID"; ok "~/.local/share/wallpapers/$THEME_ID"
else skip "wallpaper absent"; fi
if command -v qdbus6 >/dev/null; then
  run qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true; ok "KWin reconfigured"
fi

printf '\n%s Neon Noir removed.%s  The backup is kept at %s%s%s\n' \
       "$c_ok" "$c_0" "$c_ac" "${BACKUP/#$HOME/\~}" "$c_0"
