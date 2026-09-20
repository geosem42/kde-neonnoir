/*
    Hand every window its titlebar back.

    KWin applies a Force `noborder` rule to windows that are ALREADY open, but
    it does not put the border back when the rule goes away — the window keeps
    the state it was handed. Removing the rule therefore fixes new windows and
    nothing else, so leaving Riced would strand every window that happened to be
    open at the time without a titlebar until it was reopened.

    Run after the rule is removed and BEFORE `reconfigure`, so that any rule of
    the user's own that legitimately asks for a borderless window is re-asserted
    immediately afterwards rather than quietly undone here.
*/
var ws = workspace.windowList();
for (var i = 0; i < ws.length; i++) {
    var c = ws[i];
    if (c.normalWindow && c.noBorder) {
        c.noBorder = false;
    }
}
