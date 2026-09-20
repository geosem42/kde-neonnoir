// Dock variant — one centred island sized to its contents, rather than a bar
// that spans the screen.
//
// One panel, not three. Separate left/centre/right islands were tried first and
// Plasma will not place them: `offset` is silently ignored for a floating panel
// in "fit" mode, so the left island sat hard against x=0 and the right against
// the far edge with no way to inset either. A single centred panel needs no
// offset at all.
//
// The gap beneath it is Plasma's, not ours, and it closes on its own whenever a
// maximised window reaches the panel. That is how floating panels behave here
// and there is no setting for it.

var TARGET = [
    "org.kde.plasma.kickoff",
    "org.neonnoir.separator",
    // No pager: Plasma hides it below two desktops, and in a panel sized to its
    // contents a widget that disappears would change the dock's width.
    "org.kde.plasma.icontasks",
    "org.neonnoir.separator",
    "org.kde.plasma.systemtray",
    "org.kde.plasma.digitalclock",
    "org.neonnoir.control",
    "org.kde.plasma.minimizeall"
];

var p = resetPanel();
p.height = 46;
p.floating = true;
p.lengthMode = "fit";
p.alignment = "center";
p.opacityMode = "adaptive";

for (var m = 0; m < TARGET.length; m++) {
    var w = p.addWidget(TARGET[m]);
    configure(w);
    if (w.type === "org.kde.plasma.icontasks") {
        w.currentConfigGroup = ["General"];
        // Off, unlike the full-width bar: "fill" makes the task area claim all
        // the room it can, which in a panel that sizes itself to its contents
        // means the dock grows to the width of the screen.
        w.writeConfig("fill", false);
        w.reloadConfig();
    } else if (w.type === "org.kde.plasma.digitalclock") {
        w.currentConfigGroup = ["Appearance"];
        // Beside, not below: the dock is 46px and two stacked lines at that
        // height leave the date clipped.
        w.writeConfig("dateDisplayFormat", "BesideTime");
        w.writeConfig("fontSize", 10);
        w.reloadConfig();
    }
}
print("dock: 46px floating, fit to " + TARGET.length + " widgets");
