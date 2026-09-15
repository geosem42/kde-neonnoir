# To fix

Worked one item at a time, top to bottom. `x` means done and verified on screen.

## Start menu

- [x] Background matches the theme instead of a lighter grey slab
- [x] Avatar is a cyan-to-magenta disc with the account initial (`--desktop` only;
      writes ~/.face, backed up, restored by uninstall)
- [x] Search field no longer swells on hover; focus ring drawn over it, not around
- [x] Compact list with a subtitle per row instead of a grid of tiles
- [x] Selected row is a teal fill with a 2px cyan leading edge (also fixes KRunner)

## KRunner

- [x] Checked: ships with plasma-workspace, already on the theme

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
- [x] Menubar and url nav bar hidden. katerc's `Show Menu Bar` is NOT enough —
      KXmlGui restores the menubar from `[MainWindow<n> Settings] MenuBar` in the
      session file, and that wins. Both are written; sessions are backed up
- [x] Accepted as it stands. Two differences from the artboard remain and are
      deliberate: the status bar reads `1:1 INSERT en_US Soft Tabs…` rather than
      `Line 9, Col 1 · Bash · UTF-8` — that is Kate's own widget with no theming
      hook — and the toolbar still shows in windows whose session recorded it,
      since that state is per-window

## Dolphin

- [x] Details list for every folder, sorted column header in cyan, Size and
      Modified columns — the artboard's layout. `GlobalViewProps=true` plus a
      written `view_properties/global/.directory`; ViewMode=1 is Details
      (0 is Icons, 2 is Compact)
- [x] Folder previews off, file previews on. Two different controls: the
      artboard draws folders as plain glyphs, but a file manager that cannot
      show you a picture is worse than one that does not match a drawing.
      Dropping the `directorythumbnail` plugin keeps folders plain and leaves
      image, video and document previews working
- [x] No expander arrows on folders (`ExpandableFolders=false`)
- [x] Flat rows. The zebra stripe was one step off the ground, which reads as
      banding at Dolphin's row height; the artboard's list is flat, so
      `Colors:View` alternate now equals normal
- [x] Borders match the artboard exactly, measured off it rather than eyeballed:
      one 1px `border.hairline` rule under the toolbar across the full width, one
      full-height 1px rule dividing the sidebar from the file view, and a 1px
      rule above the status bar. Square — the view frame's radius is 1, not 7.
      The divider is the view frame's left edge with `splitter_width=1` closing
      the 4px dock gap; Kvantum's `[Dock]` frame does nothing here because Qt
      only draws that for a FLOATING dock. With tabs open the divider breaks for
      the tab-bar strip — the artboard has no tabs, so there is nothing to match
      there
- [x] Toolbar cut to the artboard's row: back, forward, up, path, then search
      and the menu at the right end, icon only. View-mode and Split view moved
      to the hamburger. A KXmlGui override in `kxmlgui5` — still kxmlgui5 under
      KF6, verified, not kxmlgui6 — whose `version` must exceed Dolphin's or the
      file is silently discarded
- [x] install.sh now refuses to run while Dolphin, Kate or Konsole are open.
      All three hold their config in memory and write it back on exit, silently
      undoing what was just installed — Dolphin to `view_properties/global/
      .directory`, Kate to its session file, Konsole to konsolerc. Each cost a
      debugging round. `--force` overrides with a warning

## Other apps

- [x] Checked buttons are a quiet teal box with cyan text, not a solid slab

## Taskbar

- [x] Pinned apps are Konsole, Dolphin, Firefox in that order, one slot each.
      `separateLaunchers=false` is what keeps a pinned icon in its slot once the
      app starts — with it on, launching moves the button out of the pinned run
      and into the task order. Sorting stays Manual so the order can still be
      dragged. The old launcher loop pinned `firefox` AND `firefox_firefox` when
      both existed, giving the browser two slots
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

## Reverted

- The whole outline icon set — ~6,150 files across apps, categories, places,
  mimetypes, actions and the tray. It matched the artboards and it was the wrong
  call: an icon is something you recognise before you read it, and replacing a
  set the user already knows costs that recognition everywhere at once. Breeze's
  shapes are back; the theme now recolours folders and nothing else. The glyph
  pool and its pattern sweeps are in the history if they are ever wanted back.
- The `.desktop` icon overrides that went with it. They pointed absolute-path
  entries at names only our theme shipped, so once the glyphs went those names
  resolved to nothing. Firefox, Chromium, Thunderbird and the rest have their
  own logos again.

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
- Locking the taskbar order. Plasma 6 has no lock for it: pinned slots hold
  once set and only a deliberate drag moves them, but a running window keeps a
  remembered position, so the pinned order only shows once that app is closed or
  the session restarts. The only true lock is making the whole applet immutable,
  which also blocks unpinning and configuring it.
- Cyan caps for Dolphin's sidebar section headers. The colour is reachable but
  not separable: KFilePlacesView draws PLACES/REMOTE/DEVICES from Kvantum's
  `window.text.color` at about 63% alpha — proved by probing it to magenta,
  which moved the headers and left the item labels alone (those come from
  `[ItemView] text.normal.color`). But `window.text.color` is the general window
  text colour for every label, checkbox and group title in every Qt app, so
  cyan there is cyan everywhere. The caps and letter-spacing have no mechanism
  at all: Qt style sheets have no text-transform and Kvantum exposes none.
- A background behind Dolphin's path, on one toolbar row. Dolphin calls
  `KUrlNavigator::setBackgroundEnabled(false)` whenever the navigator lives in
  the toolbar and exposes no setting for it. Kvantum cannot reach the breadcrumb
  either — Dolphin paints those buttons itself, flat, and a fill on `toolbtn`
  changed nothing. There is no persistent "editable location bar" setting that
  would give a real framed line edit on the same row; `setUrlEditable` exists in
  the API but only Ctrl+L reaches it. Pulling `url_navigators` out of the
  toolbar DOES restore the frame, on a second row — built, shown, and one bar
  was preferred.
- Launcher header layout — the `hostname · Plasma 6.6.6` subtitle, the search
  field on its own row, brightness and power in the header instead of the
  footer. Plasma 6.6 compiles the whole Kickoff UI into
  `org.kde.plasma.kickoff.so` as a QML module; `Header.qml`, `Footer.qml` and
  `LeaveButtons.qml` exist only as bytecode, with no file on disk to override
  and no config key for any of it. Only a fork of the applet would do it.
