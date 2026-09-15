#!/usr/bin/env bash
# Neon Noir — install for Kubuntu 26.04 / KDE Plasma 6.6
#
#   ./install.sh              copy artefacts into place (nothing visibly changes)
#   ./install.sh --apply      copy, then switch the live session to the theme
#   ./install.sh --dry-run    show what would happen, touch nothing
#   ./install.sh --system     also install the root-owned pieces (SDDM, Plymouth)
#
# Idempotent: re-running is a no-op. Every config file this script edits is copied
# to $BACKUP first, and only the FIRST time, so the backup always holds your
# pristine pre-Neon-Noir settings no matter how often you re-run.
set -euo pipefail

THEME_ID="NeonNoir"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST="$HERE/dist"
SHARE="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
BACKUP="$CONF/neon-noir-backup"

DRY=0; APPLY=0; SYSTEM=0
for a in "$@"; do case "$a" in
  --dry-run) DRY=1 ;;
  --apply)   APPLY=1 ;;
  --system)  SYSTEM=1 ;;
  -h|--help) sed -n '2,12p' "$0" | sed 's/^# \?//'; exit 0 ;;
  *) echo "unknown option: $a" >&2; exit 2 ;;
esac; done

c_ok=$'\033[38;2;109;201;125m'; c_ac=$'\033[38;2;54;215;215m'
c_wn=$'\033[38;2;225;165;54m'; c_dim=$'\033[38;2;161;169;176m'; c_0=$'\033[0m'
say()  { printf '%s::%s %s\n' "$c_ac" "$c_0" "$*"; }
ok()   { printf '   %s✔%s %s\n' "$c_ok" "$c_0" "$*"; }
warn() { printf '   %s!%s %s\n' "$c_wn" "$c_0" "$*"; }
skip() { printf '   %s·%s %s\n' "$c_dim" "$c_0" "$*"; }
run()  { if [ "$DRY" = 1 ]; then printf '   %swould:%s %s\n' "$c_dim" "$c_0" "$*"; else "$@"; fi; }

[ -d "$DIST" ] || { echo "dist/ missing — run: python3 build/generate.py" >&2; exit 1; }

# ── back up anything we are about to edit, once ────────────────────────────────
say "Backing up current settings"
run mkdir -p "$BACKUP" "$BACKUP/gtk-3.0" "$BACKUP/gtk-4.0"
for f in kdeglobals kwinrc plasmarc breezerc konsolerc kcminputrc ksplashrc \
         kscreenlockerrc plasmashellrc plasma-org.kde.plasma.desktop-appletsrc; do
  if [ -f "$CONF/$f" ]; then
    if [ -e "$BACKUP/$f" ]; then skip "$f already backed up"
    else run cp "$CONF/$f" "$BACKUP/$f"; ok "$f"; fi
  fi
done
for g in gtk-3.0 gtk-4.0; do
  if [ -f "$CONF/$g/gtk.css" ]; then
    if [ -e "$BACKUP/$g/gtk.css" ]; then skip "$g/gtk.css already backed up"
    else run cp "$CONF/$g/gtk.css" "$BACKUP/$g/gtk.css"; ok "$g/gtk.css"; fi
  fi
done
# Record the colour scheme that was active BEFORE we touch anything, so
# uninstall restores what you actually had rather than assuming Breeze Dark.
if [ "$DRY" = 0 ] && [ ! -f "$BACKUP/PREVIOUS_SCHEME" ]; then
  prev="$(kreadconfig6 --file kdeglobals --group General --key ColorScheme 2>/dev/null || true)"
  [ -z "$prev" ] && prev="BreezeDark"
  [ "$prev" = "$THEME_ID" ] || printf '%s\n' "$prev" > "$BACKUP/PREVIOUS_SCHEME"
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
  run mkdir -p "$dst"; run cp -r "$src/." "$dst/"; ok "${dst/#$HOME/\~}"
}

say "Colour scheme"
install_file "$DIST/color-schemes/$THEME_ID.colors" "$SHARE/color-schemes/$THEME_ID.colors"

say "Application schemes"
install_file "$DIST/konsole/$THEME_ID.colorscheme" "$SHARE/konsole/$THEME_ID.colorscheme"
install_file "$DIST/konsole/$THEME_ID.profile"     "$SHARE/konsole/$THEME_ID.profile"
install_file "$DIST/syntax-highlighting/neon-noir.theme" \
             "$SHARE/org.kde.syntax-highlighting/themes/neon-noir.theme"

say "GTK 3 / 4 / libadwaita"
install_file "$DIST/gtk/gtk-3.0.css" "$CONF/gtk-3.0/gtk.css"
install_file "$DIST/gtk/gtk-4.0.css" "$CONF/gtk-4.0/gtk.css"

say "Plasma style"
install_tree "$DIST/desktoptheme/$THEME_ID" "$SHARE/plasma/desktoptheme/$THEME_ID"

say "Window decoration"
install_tree "$DIST/aurorae/$THEME_ID" "$SHARE/aurorae/themes/$THEME_ID"

say "Icon theme"
install_tree "$DIST/icons/$THEME_ID" "$SHARE/icons/$THEME_ID"

say "Wallpaper"
install_tree "$DIST/wallpapers/$THEME_ID" "$SHARE/wallpapers/$THEME_ID"

say "Configuration"
if [ -f "$DIST/config/settings.tsv" ]; then
  n=0
  while IFS=$'\t' read -r file group key value; do
    [ -z "${file:-}" ] && continue
    run kwriteconfig6 --file "$file" --group "$group" --key "$key" "$value"
    n=$((n+1))
  done < "$DIST/config/settings.tsv"
  ok "$n settings written (decoration, effects, fonts, blur)"
else skip "no settings.tsv"; fi

if [ "$SYSTEM" = 1 ]; then
  say "System components"
  warn "SDDM and Plymouth are not built yet — skipping"
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

  if [ -d "$SHARE/icons/$THEME_ID" ]; then
    run kwriteconfig6 --file kdeglobals --group Icons --key Theme "$THEME_ID"
    command -v gtk-update-icon-cache >/dev/null && \
      run gtk-update-icon-cache -qtf "$SHARE/icons/$THEME_ID" 2>/dev/null || true
    ok "icon theme"
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

  # Reload the compositor so decoration/blur/animation changes take effect now.
  if command -v qdbus6 >/dev/null; then
    run qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
    ok "KWin reconfigured"
  fi
  warn "GTK apps and already-open Qt apps need a restart to pick up the new look"
else
  say "Not applied"
  printf '   %sPick "%s" in System Settings > Colours, or re-run with --apply%s\n' \
         "$c_dim" "$THEME_ID" "$c_0"
fi

printf '\n%s Neon Noir installed.%s  Revert at any time: %s./uninstall.sh%s\n' \
       "$c_ok" "$c_0" "$c_ac" "$c_0"
