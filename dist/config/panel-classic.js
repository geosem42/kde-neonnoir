// Shared by every panel variant: the pinned apps, the tray contents, the
// per-widget configuration, and the reset that gives a variant a clean panel to
// build into. Concatenated ahead of each variant file at build time, so a change
// to how a widget is configured cannot reach one layout and miss another.

// Pinned apps, in the artboard's order. Resolved at install time against the
// desktop files that actually exist — a launcher pointing at a missing .desktop
// still takes a slot in the task bar and draws a blank page icon, and which
// file a browser installs to depends on whether it came from apt, a snap or a
// flatpak.
var LAUNCHERS = "@LAUNCHERS@";

// The tray the artboard draws: network, volume, bluetooth, notifications,
// battery. Everything else goes behind the expander rather than sitting in the
// bar — including kscreen, whose icon is the one full-colour glyph left in the
// tray. Plasma keeps an expander arrow whenever anything is hidden, so the
// arrow the artboard does not show is unavoidable.
var TRAY_SHOWN = [
    "org.kde.plasma.networkmanagement",
    "org.kde.plasma.volume",
    "org.kde.plasma.bluetooth",
    "org.kde.plasma.notifications",
    "org.kde.plasma.battery"
];
var TRAY_HIDDEN = [
    "org.kde.plasma.clipboard", "org.kde.kscreen", "org.kde.plasma.brightness",
    "org.kde.plasma.keyboardlayout", "org.kde.plasma.keyboardindicator",
    "org.kde.plasma.cameraindicator", "org.kde.plasma.devicenotifier",
    "org.kde.plasma.printmanager", "org.kde.plasma.vault",
    "org.kde.plasma.manage-inputmethod", "org.kde.plasma.mediacontroller",
    "org.kde.plasma.weather", "org.kde.kdeconnect", "org.kde.kupapplet"
];

function configure(w) {
    if (w.type === "org.kde.plasma.kickoff") {
        w.currentConfigGroup = ["General"];
        w.writeConfig("icon", "@MARK@");
        w.writeConfig("menuLabel", "");
        // 1 = list, 0 = grid. The artboard shows a compact list with a
        // subtitle per row, not a wall of tiles.
        w.writeConfig("applicationsDisplay", 1);
        w.writeConfig("favoritesDisplay", 1);
        w.reloadConfig();

    } else if (w.type === "org.kde.plasma.icontasks") {
        w.currentConfigGroup = ["General"];
        w.writeConfig("launchers", LAUNCHERS);
        // The point of a second desktop is a second set of windows. With this
        // false every task button is on every desktop, so switching changes the
        // wallpaper and nothing else.
        w.writeConfig("showOnlyCurrentDesktop", true);
        w.writeConfig("showOnlyCurrentActivity", true);
        w.writeConfig("showOnlyCurrentScreen", false);
        w.writeConfig("maxStripes", 1);
        w.writeConfig("forceStripes", true);
        w.writeConfig("groupingStrategy", 1);
        // Manual, so a pinned icon can still be dragged into place, and
        // separateLaunchers off so it KEEPS that place once the app is running.
        // With separateLaunchers on, starting a pinned app moves its button out
        // of the pinned run and into the task order.
        w.writeConfig("sortingStrategy", 1);
        w.writeConfig("separateLaunchers", false);
        w.writeConfig("iconSpacing", 2);
        w.writeConfig("indicateAudioStreams", false);
        w.writeConfig("fill", true);
        w.reloadConfig();

    } else if (w.type === "org.neonnoir.hud") {
        w.currentConfigGroup = ["General"];
        // Same pinned list as the other variants, so switching taskbar does not
        // lose the apps. The HUD writes this key back itself when something is
        // pinned or unpinned from its menu.
        w.writeConfig("launchers", LAUNCHERS);
        w.reloadConfig();

    } else if (w.type === "org.kde.plasma.pager") {
        w.currentConfigGroup = ["General"];
        // 0 = Number, 1 = Name, 2 = None. A number is legible in a 24px tile;
        // a desktop name is not, and "None" leaves two identical boxes.
        w.writeConfig("displayedText", 0);
        // The thumbnail windows inside each tile are two or three pixels at
        // this size — noise, not information.
        w.writeConfig("showWindowOutlines", false);
        w.writeConfig("showWindowIcons", false);
        w.writeConfig("showOnlyCurrentScreen", false);
        // Scrolling past the last desktop comes back to the first.
        w.writeConfig("wrapPage", true);
        // 0 = DoNothing. Clicking the desktop you are already on should not
        // minimise everything on it.
        w.writeConfig("currentDesktopSelected", 0);
        // 1 = Horizontal. Left unset, KWin's desktop grid decides, and a 2x1
        // grid can come back as two stacked 24px-wide slivers.
        w.writeConfig("pagerLayout", 1);
        w.reloadConfig();

    } else if (w.type === "org.kde.plasma.systemtray") {
        w.currentConfigGroup = ["General"];
        w.writeConfig("shownItems", TRAY_SHOWN.join(","));
        w.writeConfig("hiddenItems", TRAY_HIDDEN.join(","));
        w.reloadConfig();

    } else if (w.type === "org.kde.plasma.digitalclock") {
        w.currentConfigGroup = ["Appearance"];
        // 2, not 1. The key is a tri-state: 0 forces 12-hour, 1 means "follow
        // the locale" (which is what left the clock at 12:35 PM), 2 forces 24.
        w.writeConfig("use24hFormat", 2);
        w.writeConfig("showDate", true);
        w.writeConfig("dateDisplayFormat", "BelowTime");
        w.writeConfig("dateFormat", "custom");
        w.writeConfig("customDateFormat", "ddd d MMM");
        w.writeConfig("showSeconds", "Never");
        // The family is ignored unless autoFontAndSize is off.
        w.writeConfig("autoFontAndSize", false);
        w.writeConfig("fontFamily", "JetBrains Mono");
        w.writeConfig("fontWeight", 700);
        w.writeConfig("fontStyleName", "Bold");
        w.writeConfig("fontSize", 11);
        w.reloadConfig();

    } else if (w.type === "org.kde.plasma.minimizeall") {
        w.currentConfigGroup = ["General"];
        // The applet's own default, written out rather than left implicit: the
        // symbolic variant is the flat monitor outline, which sits beside the
        // tray glyphs. Plain `user-desktop` is the full-colour one, and this
        // theme recolours it — a lone cyan monitor next to white glyphs.
        w.writeConfig("icon", "user-desktop-symbolic");
        w.reloadConfig();
    }
}

// Every variant builds from scratch rather than reshaping what is there. The
// variants differ in the NUMBER of panels as well as their contents — the dock
// is one, an earlier islands attempt was three — so "adjust the existing panel"
// has no single meaning. Removing and re-adding is also the only way to reorder:
// Plasma's scripting API can append a widget but cannot move one.
function resetPanel() {
    var ps = panels();
    for (var i = 0; i < ps.length; i++) {
        if (ps[i].location === "bottom" || ps[i].location === "top") {
            ps[i].remove();
        }
    }
    var p = new Panel;
    p.location = "bottom";
    p.hiding = "none";
    // Cleared explicitly. A new panel inherits the length bounds of the one it
    // replaces, and a stale minimumLength of 1920 pins a "fit" panel to the full
    // width — which is what made the first islands attempt look like one bar.
    p.minimumLength = 0;
    p.maximumLength = 100000;
    return p;
}

// Build the panel the design specifies, rather than recolouring the stock one.
//
// Artboard 04 "Panel variants" gives the default: floating, 48px, full width
// with a gap at each screen edge. Artboard 01 gives the contents, left to
// right: framed hexagon launcher, rule, task buttons WITH LABELS and an
// underline indicator, then the tray, a rule, and the clock as time over date.
//
// The widget list is rebuilt wholesale when it does not already match, because
// Plasma's scripting API can append a widget but cannot reorder one.

var TARGET = [
    "org.kde.plasma.kickoff",
    "org.neonnoir.separator",
    // Not on the artboard, which was drawn against a single desktop. With two
    // or more there is otherwise no way to see which one you are on, and no way
    // to switch without alt-tabbing into a window that happens to live there.
    // No second rule after it: Plasma hides the pager outright when there is
    // only one desktop, and a rule on each side would then collapse into two
    // parallel lines with a gap between them.
    "org.kde.plasma.pager",
    // Icons only. The artboard labels each task, but a label as wide as a
    // window title crowds the bar, so this deliberately departs from it.
    "org.kde.plasma.icontasks",
    "org.kde.plasma.systemtray",
    "org.neonnoir.separator",
    "org.kde.plasma.digitalclock",
    // The theme's own options popup, beside the clock rather than in the tray:
    // the tray hides what it does not have room for, and a control that can
    // move the panel out from under you should not be the thing that vanishes.
    "org.neonnoir.control",
    // Last, hard against the right edge, where every desktop since CDE has put
    // it. minimizeall, not showdesktop: showdesktop asks KWin to slide the
    // windows aside and slides them back the moment anything takes focus, which
    // is a peek, not a "clear the screen". This one minimises for real and
    // restores the same set on a second click.
    "org.kde.plasma.minimizeall"
];

var p = resetPanel();
p.height = 48;
p.floating = true;
// "fill", not "fit". Fit shrinks the panel to its contents, which reads as a
// small box in the middle of the screen; this variant is a full-width bar that
// floats clear of the edges.
p.lengthMode = "fill";
p.alignment = "center";
p.opacityMode = "adaptive";

for (var m = 0; m < TARGET.length; m++) {
    configure(p.addWidget(TARGET[m]));
}
print("panel: 48px floating full width, " + TARGET.length + " widgets");
