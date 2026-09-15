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
    // Icons only. The artboard labels each task, but a label as wide as a
    // window title crowds the bar, so this deliberately departs from it.
    "org.kde.plasma.icontasks",
    "org.kde.plasma.systemtray",
    "org.neonnoir.separator",
    "org.kde.plasma.digitalclock"
];

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
        w.writeConfig("showOnlyCurrentDesktop", false);
        w.writeConfig("showOnlyCurrentActivity", true);
        w.writeConfig("showOnlyCurrentScreen", false);
        w.writeConfig("maxStripes", 1);
        w.writeConfig("forceStripes", true);
        w.writeConfig("groupingStrategy", 1);
        w.writeConfig("iconSpacing", 2);
        w.writeConfig("indicateAudioStreams", false);
        w.writeConfig("fill", true);
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
    }
}

var out = [];
var ps = panels();
for (var i = 0; i < ps.length; i++) {
    var p = ps[i];
    if (p.location !== "bottom" && p.location !== "top") { continue; }

    p.height = 48;
    p.floating = true;
    // "fill", not "fit". Fit shrinks the panel to its contents, which reads as a
    // small box in the middle of the screen; the design is a full-width bar that
    // floats clear of the edges.
    p.lengthMode = "fill";
    p.alignment = "center";
    p.opacityMode = "adaptive";
    out.push("panel: 48px floating, full width");

    var ids = p.widgetIds;
    var current = [];
    for (var j = 0; j < ids.length; j++) {
        current.push(p.widgetById(ids[j]).type);
    }

    if (current.join("|") !== TARGET.join("|")) {
        for (var k = 0; k < ids.length; k++) {
            p.widgetById(ids[k]).remove();
        }
        for (var m = 0; m < TARGET.length; m++) {
            configure(p.addWidget(TARGET[m]));
        }
        out.push("widgets: " + TARGET.length + " rebuilt in design order");
    } else {
        for (var n = 0; n < ids.length; n++) {
            configure(p.widgetById(ids[n]));
        }
        out.push("widgets: already in design order, reconfigured");
    }
}
print(out.length ? out.join("; ") : "no horizontal panel found");
