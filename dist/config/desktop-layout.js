// Place the Neon Noir desktop: clock, system card, media controller.
// Run through plasmashell's scripting API rather than by editing
// plasma-org.kde.plasma.desktop-appletsrc — plasmashell holds that file in
// memory and rewrites it on exit, so an edit underneath it is simply lost.
// Idempotent: a widget already on the desktop is left alone.
var all = desktops();
var d = all[0];
for (var i = 0; i < all.length; i++) {
    if (all[i].screen === 0) { d = all[i]; break; }
}

function has(type) {
    var ids = d.widgetIds;
    for (var i = 0; i < ids.length; i++) {
        if (d.widgetById(ids[i]).type === type) { return true; }
    }
    return false;
}

var placed = [];

if (!has("org.kde.plasma.digitalclock")) {
    var clock = d.addWidget("org.kde.plasma.digitalclock", 48, 40, 320, 130);
    clock.currentConfigGroup = ["Appearance"];
    clock.writeConfig("showDate", true);
    // 2, not 1. The key is a tri-state: 0 forces 12-hour, 1 means "follow the
    // locale" — which is what left this clock at 9:12 PM while the panel
    // clock, already set to 2, read 21:12.
    clock.writeConfig("use24hFormat", 2);
    clock.writeConfig("dateFormat", "custom");
    clock.writeConfig("customDateFormat", "ddd d MMM");
    clock.writeConfig("autoFontAndSize", false);
    clock.writeConfig("fontSize", 44);
    clock.writeConfig("fontWeight", 700);
    clock.reloadConfig();
    placed.push("clock");
}

if (!has("org.neonnoir.sysmon")) {
    d.addWidget("org.neonnoir.sysmon", 48, 190, 320, 200);
    placed.push("system");
}

if (!has("org.kde.plasma.mediacontroller")) {
    d.addWidget("org.kde.plasma.mediacontroller", 48, 410, 320, 120);
    placed.push("media");
}

print(placed.length ? "placed: " + placed.join(", ") : "everything was already there");
