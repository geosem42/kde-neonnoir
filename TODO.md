# To fix

Worked one item at a time, top to bottom. `x` means done and verified on screen.

## Start menu

- [x] Background matches the theme instead of a lighter grey slab
- [ ] Avatar is the Kubuntu logo; design has a magenta-to-indigo disc with an initial
- [ ] No subtitle under the name (design: `resolute · Plasma 6.6.6`)
- [ ] Brightness and power belong in the header, not a footer strip
- [x] Search field no longer swells on hover; focus ring drawn over it, not around
- [ ] Sidebar categories use Breeze icons, not our outline glyphs
- [ ] Grid of apps; design is a compact list with a category subtitle per row
- [x] Selected row is a teal fill with a 2px cyan leading edge (also fixes KRunner)

## KRunner

- [x] Checked: ships with plasma-workspace, already on the theme
- [ ] Third-party result icons are vendor logos

## Konsole

- [ ] Compare against artboard 06 and list what differs

## Kate

- [ ] Menubar is visible; design has none. Lives in Kate's session file, not katerc
- [ ] Compare the tab bar against artboard 06

## Dolphin

- [ ] File icons are Breeze's colour documents; design is grey line art (`mimetypes/`)
- [ ] Sidebar section headers are plain grey; design is cyan caps
- [ ] Cyan focus outline around the file view is not in the design

## Taskbar

- [ ] Pinned icons can be dragged out of order
- [ ] Firefox keeps its snap logo — `Icon=` is an absolute path, unreachable from an icon theme

## Rejected

- Cyan-to-magenta gradient on the window top hairline. Solid cyan instead.

## Known dead ends

Kept here so they are not re-attempted.

- Filled-cyan primary button: Kvantum's only default-button hook is a small
  corner marker, not the fill.
- `TUE 15 SEP` in the clock: Qt date formats have no uppercase.
- Tray expander chevron: Plasma always draws one when anything is hidden.
- Lock screen layout: loaded from the Plasma shell package, not the theme.
