# To fix

Worked one item at a time, top to bottom. `x` means done and verified on screen.

## Start menu

- [x] Background matches the theme instead of a lighter grey slab
- [x] Avatar is a cyan-to-magenta disc with the account initial (`--desktop` only;
      writes ~/.face, backed up, restored by uninstall)
- [x] Search field no longer swells on hover; focus ring drawn over it, not around
- [x] Sidebar categories use our outline glyphs
- [x] Compact list with a subtitle per row instead of a grid of tiles
- [x] Selected row is a teal fill with a 2px cyan leading edge (also fixes KRunner)

## KRunner

- [x] Checked: ships with plasma-workspace, already on the theme
- [x] Third-party result icons were vendor logos. `appicons.MAP` covered ~100
      curated names; every other installed app fell through. The `apps` and
      `preferences` contexts are now swept by pattern like the actions and
      places, plus a list of common third-party names breeze does not ship —
      805 app names, nothing falling through to the neutral mark. Both the bare
      and `-symbolic` spellings are written: breeze ships 14 names only as
      `-symbolic` (vlc, wine, kgpg, virt-manager…) while their .desktop files
      ask for the plain one

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
- [x] Tab bar matches the artboard: tabs the width of their own label, a 1px
      rule between them and under the bar, and the active tab painted in the
      terminal's own ground so it reads as the terminal continuing up.
      `ExpandTabWidth=false` is what stops the stretch; the borders come from
      Konsole's user stylesheet, the only hook it offers — no Qt style reaches
      that bar, Kvantum included. The path must be written as a `file://` URL:
      Konsole declares the key as a Url and silently ignores a bare path
- [x] Active tab carries the accent as a teal fill, the same selection colour
      the list rows use
- [x] Per-tab close button sat 4px from the tab's right EDGE, not its content
      rect, so neither QSS padding nor a margin on `::close-button` moved it —
      measured, not guessed. `CloseTabButton=OnTabBar` puts one button at the
      end of the bar instead, which is what the artboard shows and keeps the
      affordance

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
- [x] Sidebar place icons are our outline glyphs — all 231 names swept by
      pattern, small sizes only so folders in the file view stay cyan and filled
- [x] Details list for every folder, sorted column header in cyan, Size and
      Modified columns — the artboard's layout. `GlobalViewProps=true` plus a
      written `view_properties/global/.directory`; ViewMode=1 is Details
      (0 is Icons, 2 is Compact)
- [x] No folder thumbnails: the artboard's files carry our glyphs, not previews
- [x] No expander arrows on folders (`ExpandableFolders=false`)
- [x] Flat rows. The zebra stripe was one step off the ground, which reads as
      banding at Dolphin's row height; the artboard's list is flat, so
      `Colors:View` alternate now equals normal
- [ ] Sidebar section headers are plain grey; design is cyan caps
- [ ] Address bar is a bare breadcrumb; design is a bordered pill with a
      separate search pill beside it
- [x] Focus outline around the file view is the popup grey #454F58, not an accent

## Other apps

- [x] Checked buttons are a quiet teal box with cyan text, not a solid slab

## Taskbar

- [ ] Pinned icons can be dragged out of order
- [x] Firefox, Chromium, Thunderbird, Android Studio, JDownloader and micro kept
      their vendor logos: their `Icon=` is an absolute path, and an icon theme is
      only consulted for icons asked for by name. `--desktop` now writes a copy of
      each entry into ~/.local/share/applications with `Icon=` rewritten to a name
      we ship. The copy freezes `Exec=` as it stands, so a package that changes its
      command line later needs a re-run. Each carries `X-NeonNoir-IconOverride`;
      anything of yours that was replaced is backed up and restored by uninstall

## Kate without a menubar

Ctrl+M shows the menubar, Ctrl+N makes a new document, Ctrl+Shift+I opens the
command bar, which reaches every action the menubar had. Read off the running
instance over D-Bus, not from documentation.

## Icon set coverage

Swept by pattern, so a whole context changes at once and styles never mix:
apps, categories, places, mimetypes, status/devices/actions/preferences for the
tray. ~1,100 distinct names.

`actions/` is swept too: 1,833 names across the generic freedesktop families
(edit-, document-, go-, view-, zoom-, format-, media-, window-, dialog-,
system-, list-, tab-). Only 13 fall through to the neutral placeholder.

Left on Breeze on purpose: application-specific toolsets — gnumeric, labplot,
kdenlive, KTorrent, digiKam's batch queue, the vector-editor node and path
tools. Giving a node-editing tool a generic outline does not restyle it, it
makes it unidentifiable, and those icons only ever appear inside their own
application's toolbar so no mixed-style list results.

## Fixed after testing

- Firefox, Chrome and Chromium were the same button. The artboard draws Firefox
  as a globe, which is right for one browser on a panel and useless for three,
  and function cannot separate them — they do the same job. Each now traces its
  own silhouette: a flame, a spoked wheel, a ring in a ring. The globe stays for
  browsers we do not single out.
- Context menu was wide with blank swatches: the places sweep had collapsed all
  eleven `folder-<colour>` variants onto one grey outline. Colour is the content
  in Dolphin's folder-colour row, so those names are excluded from both the
  sweep and the folder recolour.
- Icons in Fixed-size directories were written at 24px regardless of the size
  the directory declares, so a 16px request returned a 24px icon.
- Windows two layers down ghosted into the titlebar during another window's
  minimise/maximise. Not Konsole's opacity and not KWin's blur effect (both
  tested and cleared): Aurorae's `Animation` cross-fades active/inactive by
  blending them with opacity, so the titlebar was briefly translucent every
  time focus moved. `Animation=0`. Konsole is opaque and the decoration's
  `X-KDE-PluginInfo-blur` flag is gone as well — both were wrong regardless.

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
- Launcher header layout — the `hostname · Plasma 6.6.6` subtitle, the search
  field on its own row, brightness and power in the header instead of the
  footer. Plasma 6.6 compiles the whole Kickoff UI into
  `org.kde.plasma.kickoff.so` as a QML module; `Header.qml`, `Footer.qml` and
  `LeaveButtons.qml` exist only as bytecode, with no file on disk to override
  and no config key for any of it. Only a fork of the applet would do it.
