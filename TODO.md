# To fix

Worked one item at a time, top to bottom. `x` means done and verified on screen.

## Start menu

- [x] Background matches the theme instead of a lighter grey slab
- [x] Avatar is a cyan-to-magenta disc with the account initial (`--desktop` only;
      writes ~/.face, backed up, restored by uninstall)
- [ ] No subtitle under the name (design: `resolute · Plasma 6.6.6`)
- [ ] Brightness and power belong in the header, not a footer strip
- [x] Search field no longer swells on hover; focus ring drawn over it, not around
- [x] Sidebar categories use our outline glyphs
- [x] Compact list with a subtitle per row instead of a grid of tiles
- [x] Selected row is a teal fill with a 2px cyan leading edge (also fixes KRunner)

## KRunner

- [x] Checked: ships with plasma-workspace, already on the theme
- [ ] Third-party result icons are vendor logos

## Tray

- [x] Clipboard, vault, night-colour, disks & devices, KDE Connect, input
      method and display configuration showed filled Breeze glyphs — they use
      app/action names, so the status sweep never reached them

## Konsole

- [x] Compared against artboard 06. Chrome already matches: titlebar, line icon,
      JetBrains Mono, #0D131A ground, 10px margin, cyan block cursor, no
      menubar/tab bar/scrollbar
- [x] Shell prompt: cyan path, magenta branch, `❯`, blank line between commands.
      bash and zsh both, sourced from ~/.bashrc / ~/.zshrc (`--desktop` only;
      rc files backed up, block removed by uninstall)

## Kate

- [x] Compared against artboard 06
- [x] Kate and Konsole shared a `>_`-in-a-box glyph. Kate is now a page and pencil
- [x] Menubar and url nav bar hidden. katerc's `Show Menu Bar` is NOT enough —
      KXmlGui restores the menubar from `[MainWindow<n> Settings] MenuBar` in the
      session file, and that wins. Both are written; sessions are backed up
- [ ] Status bar reads `1:1 INSERT en_US Soft Tabs…`; design has
      `Line 9, Col 1 · Bash · UTF-8` and `Saved`. Kate's own widget, not themeable
- [ ] Toolbar still shown in some windows; state is per-window in the session

## Dolphin

- [x] File icons are grey line art — all 517 mimetype names swept by pattern
- [x] Sidebar place icons are our outline glyphs (small sizes only, so folders
      in the file view stay cyan and filled)
- [ ] Sidebar section headers are plain grey; design is cyan caps
- [x] Focus outline around the file view is the popup grey #454F58, not an accent

## Other apps

- [x] Checked buttons are a quiet teal box with cyan text, not a solid slab

## Taskbar

- [ ] Pinned icons can be dragged out of order
- [ ] Firefox keeps its snap logo — `Icon=` is an absolute path, unreachable from an icon theme

## Kate without a menubar

Ctrl+M shows the menubar, Ctrl+N makes a new document, Ctrl+Shift+I opens the
command bar, which reaches every action the menubar had. Read off the running
instance over D-Bus, not from documentation.

## Rejected

- Cyan-to-magenta gradient on the window top hairline. Solid cyan instead.

## Known dead ends

Kept here so they are not re-attempted.

- Filled-cyan primary button: Kvantum's only default-button hook is a small
  corner marker, not the fill.
- `TUE 15 SEP` in the clock: Qt date formats have no uppercase.
- Tray expander chevron: Plasma always draws one when anything is hidden.
- Lock screen layout: loaded from the Plasma shell package, not the theme.
- ` — Konsole` suffix on the window title: KMainWindow appends the application
  name; Konsole exposes no key for it.
- Brightness and power in the launcher header: Plasma 6 Kickoff's footer is
  fixed, with no configuration for it.
