// Shape the panel to the design's "Panel variants": floating, 48px, the
// hexagon mark as the launcher, time over date on the right.
// Layout only — it never adds or removes widgets, so an arrangement the user
// has built stays intact.
var out = [];
var ps = panels();
for (var i = 0; i < ps.length; i++) {
    var p = ps[i];
    if (p.location !== "bottom" && p.location !== "top") { continue; }
    p.height = 48;
    // The design's default panel variant: a floating, centred island rather
    // than a full-width bar. lengthMode "fit" is what actually detaches it
    // from the screen edges; floating alone leaves it edge-to-edge.
    p.lengthMode = "fit";
    p.alignment = "center";
    p.floating = true;
    out.push("panel " + p.location + ": 48px, floating island");

    var ids = p.widgetIds;
    for (var j = 0; j < ids.length; j++) {
        var w = p.widgetById(ids[j]);
        if (w.type === "org.kde.plasma.kickoff") {
            w.currentConfigGroup = ["General"];
            w.writeConfig("icon", "@MARK@");
            w.writeConfig("compactDisplay", "true");
            w.reloadConfig();
            out.push("launcher: hexagon mark");
        } else if (w.type === "org.kde.plasma.digitalclock") {
            w.currentConfigGroup = ["Appearance"];
            w.writeConfig("showDate", true);
            w.writeConfig("use24hFormat", 1);
            w.writeConfig("dateFormat", "custom");
            w.writeConfig("customDateFormat", "ddd d MMM");
            w.writeConfig("dateDisplayFormat", "BesideTime");
            w.reloadConfig();
            out.push("clock: 24h + date");
        }
    }
}
print(out.length ? out.join("; ") : "no horizontal panel found");
