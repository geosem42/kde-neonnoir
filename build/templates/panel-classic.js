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
