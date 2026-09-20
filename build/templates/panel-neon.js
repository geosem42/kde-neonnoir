// Futuristic variant — a polybar, not a shorter taskbar.
//
// The first attempt at this was the standard row of Plasma applets in a 30px
// panel, and it read as exactly that: the normal bar, smaller. The look comes
// from the modules sharing one grid, one monospaced face and one slant, which
// no arrangement of separate applets can give, so almost the whole bar is a
// single widget — org.neonnoir.hud — that draws the workspaces, the open
// windows, the focused window's title, the telemetry and the clock itself.
//
// Top edge, which is where polybar and its imitators live, and where a status
// bar belongs: the bottom of the screen is where windows put their own
// controls, and a readout competing with those is a taskbar again.
//
// Flush and NOT floating. A floating panel leaves a margin on three sides, and
// margin around a 28px bar is most of its own height again.

var TARGET = [
    // Left of the HUD rather than inside it: reimplementing Kickoff's popup to
    // gain a hexagon is not a trade worth making.
    "org.kde.plasma.kickoff",
    "org.neonnoir.hud",
    // The tray has to stay a stock applet — it hosts other processes' icons.
    // It lands immediately right of the HUD's clock, so the two read as one
    // group at the end of the bar.
    "org.kde.plasma.systemtray",
    "org.neonnoir.control",
    "org.kde.plasma.minimizeall"
];

var p = resetPanel();
p.location = "top";
// 28, not 30: the sparklines need 11px and the state underlines 2px, and 28 is
// the smallest height that leaves the 10px figures optically centred between
// them.
p.height = 28;
p.floating = false;
p.lengthMode = "fill";
p.alignment = "center";
// Opaque, not adaptive. Adaptive fades the background out when no window is
// near it, and the slanted segments only read as segments against a bar.
p.opacityMode = "opaque";

for (var m = 0; m < TARGET.length; m++) {
    configure(p.addWidget(TARGET[m]));
}
print("neon: 28px flush top bar, " + TARGET.length + " widgets");
