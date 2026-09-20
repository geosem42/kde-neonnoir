/*
    Neon Noir tiler — automatic window tiling for KWin 6.

    Pop!_OS-shaped: a new window SPLITS the focused one rather than joining a
    master/stack. The layout is a binary tree per screen-and-desktop; every leaf
    is a window, every branch is a split with a ratio. Opening a window turns the
    focused leaf into a branch holding the old window and the new one; closing a
    window replaces its branch with its sibling, so the space it held goes back
    to the neighbour it was split from rather than to a global reshuffle.

    Splits follow the SHAPE of the rectangle being divided, not a fixed
    alternation: a wide rect splits vertically, a tall one horizontally. That is
    what keeps windows near square as the tree deepens, and it is the single
    rule that makes the result feel automatic rather than arbitrary.

    Nothing here is remembered across a restart. KWin gives a script no storage
    that survives it, and a stale tree would place windows against a screen
    layout that may no longer exist — so the tree is rebuilt from the windows
    that are actually open whenever the script loads.
*/

const GAP_OUTER = 12;   // screen edge to window
const GAP_INNER = 8;   // window to window

/* The floor for a tile when nothing better is known. Real windows declare their
   own minimum and that is what gets used; this only covers the ones that do
   not. */
const MIN_TILE = 240;

// One tree per screen-and-desktop. Keyed by output name and desktop id, which
// is what a window's own properties report, so re-homing a window that moves
// between them is a key comparison rather than a search.
const forests = {};

// Set while we are writing geometry. Every frameGeometry write echoes back as a
// change signal, and without this the first retile would trigger the next.
let applying = false;

function key(w) {
    const out = w.output ? w.output.name : "?";
    const desk = (w.desktops && w.desktops.length) ? w.desktops[0].id : "all";
    return out + "|" + desk;
}

/* A window is ours to place only if it is an ordinary, resizable, visible
   top-level window. Dialogs, utility windows and anything that cannot be
   resized are left exactly where the application put them — a tiler that
   stretches a modal file picker across half the screen is a broken tiler. */
function manageable(w) {
    return w && w.normalWindow && !w.transient && !w.dialog
        && !w.skipTaskbar && !w.skipPager
        && w.moveable && w.resizeable
        && !w.fullScreen && !w.minimized
        && !w.onAllDesktops;
}

function leaf(w) {
    return { win: w, a: null, b: null };
}

function isLeaf(n) {
    return n && n.win !== null && n.win !== undefined;
}

/* Depth-first search for the branch holding a window, and the branch above it.
   Returned together because removal needs the parent to splice. */
function find(node, w, parent) {
    if (!node) {
        return null;
    }
    if (isLeaf(node)) {
        return node.win === w ? { node: node, parent: parent } : null;
    }
    return find(node.a, w, node) || find(node.b, w, node);
}

function leaves(node, acc) {
    if (!node) {
        return acc;
    }
    if (isLeaf(node)) {
        acc.push(node);
        return acc;
    }
    leaves(node.a, acc);
    return leaves(node.b, acc);
}

function minOf(w, axis) {
    if (w && w.minSize) {
        const v = (axis === "w") ? w.minSize.width : w.minSize.height;
        if (v > 0) {
            return v;
        }
    }
    return MIN_TILE;
}

/* Whether a leaf can be halved and still hold BOTH windows.

   The first version compared the tile against one constant, which is the wrong
   rule: what a tile has to satisfy is the largest minimum among the windows
   that will live in it. Firefox asks for 500px and a terminal for far less, so
   a 468px tile is fine for one and overflows the other — and an overflowing
   window clamps itself back up and sits on top of its neighbour, which reads as
   the tiler having lost the layout entirely.

   The split axis is decided the same way layout() decides it, from the shape of
   the rect, so this asks about the dimension that will actually be halved. */
function roomToSplit(node, incoming) {
    if (!node || !node.rect) {
        return true;        // never laid out yet: it is the whole screen
    }
    const r = node.rect;
    const axis = (r.width >= r.height) ? "w" : "h";
    const half = ((axis === "w" ? r.width : r.height) - GAP_INNER) / 2;
    return half >= Math.max(minOf(node.win, axis), minOf(incoming, axis));
}

/* The roomiest leaf that can still take a split, falling back to the roomiest
   of all when none can. Two passes rather than one, because "biggest" and "big
   enough" are different questions and only the second one keeps windows from
   overlapping. */
function biggestLeaf(root, incoming) {
    const all = leaves(root, []);
    let best = null;
    let bestArea = -1;
    let any = null;
    let anyArea = -1;
    for (let i = 0; i < all.length; i++) {
        const r = all[i].rect;
        const area = r ? r.width * r.height : 0;
        if (area > anyArea) {
            anyArea = area;
            any = all[i];
        }
        if (roomToSplit(all[i], incoming) && area > bestArea) {
            bestArea = area;
            best = all[i];
        }
    }
    return best || any;
}

function firstLeaf(node) {
    if (!node) {
        return null;
    }
    return isLeaf(node) ? node : (firstLeaf(node.a) || firstLeaf(node.b));
}

function insert(k, w, focused) {
    const forest = forests[k];
    if (!forest.root) {
        forest.root = leaf(w);
        return;
    }
    // Split the focused window when it lives in this tree, otherwise the first
    // leaf — which is what happens when a window opens while the pointer is on
    // another screen, or straight from the desktop with nothing focused.
    let target = focused ? find(forest.root, focused, null) : null;
    let spot = target ? target.node : firstLeaf(forest.root);
    // ...unless that window is already too small to halve, in which case the
    // roomiest one gives way instead. Splitting the focused window is the rule
    // that makes tiling feel deliberate; producing an unusable sliver is not
    // worth honouring it.
    if (!roomToSplit(spot, w)) {
        const roomy = biggestLeaf(forest.root, w);
        // If nothing on this desktop can take it either, the split happens
        // anyway at the roomiest spot. There is no third option that keeps the
        // window visible, and hiding it would be worse than a tight fit.
        if (roomy) {
            spot = roomy;
        }
    }
    const old = spot.win;
    spot.win = null;
    spot.dir = "?";          // decided in layout(), from the rect it gets
    spot.ratio = 0.5;
    spot.a = leaf(old);
    spot.b = leaf(w);
}

function remove(k, w) {
    const forest = forests[k];
    if (!forest || !forest.root) {
        return false;
    }
    const hit = find(forest.root, w, null);
    if (!hit) {
        return false;
    }
    if (!hit.parent) {
        forest.root = null;
        return true;
    }
    // The sibling takes the parent's place, inheriting the space both held.
    const sib = (hit.parent.a === hit.node) ? hit.parent.b : hit.parent.a;
    hit.parent.win = sib.win;
    hit.parent.dir = sib.dir;
    hit.parent.ratio = sib.ratio;
    hit.parent.a = sib.a;
    hit.parent.b = sib.b;
    return true;
}

function place(w, x, y, width, height) {
    // Guard against a tile smaller than the window will accept: KWin would
    // clamp it and the neighbour would then overlap it. Better to hand it the
    // minimum and let it spill than to compute a layout the window ignores.
    let ww = Math.max(1, Math.round(width));
    let hh = Math.max(1, Math.round(height));
    if (w.minSize) {
        ww = Math.max(ww, w.minSize.width);
        hh = Math.max(hh, w.minSize.height);
    }
    w.frameGeometry = {
        x: Math.round(x), y: Math.round(y), width: ww, height: hh
    };
}

function layout(node, x, y, width, height) {
    if (!node) {
        return;
    }
    if (isLeaf(node)) {
        node.rect = { x: x, y: y, width: width, height: height };
        place(node.win, x, y, width, height);
        return;
    }
    // Split across the longer side, so the pieces stay close to square.
    const dir = (width >= height) ? "v" : "h";
    node.dir = dir;
    if (dir === "v") {
        const aw = (width - GAP_INNER) * node.ratio;
        layout(node.a, x, y, aw, height);
        layout(node.b, x + aw + GAP_INNER, y, width - aw - GAP_INNER, height);
    } else {
        const ah = (height - GAP_INNER) * node.ratio;
        layout(node.a, x, y, width, ah);
        layout(node.b, x, y + ah + GAP_INNER, width, height - ah - GAP_INNER);
    }
}

function retile(k) {
    const forest = forests[k];
    if (!forest || !forest.root) {
        return;
    }
    const probe = firstLeaf(forest.root);
    if (!probe) {
        return;
    }
    const area = workspace.clientArea(KWin.PlacementArea, probe.win.output,
                                      workspace.currentDesktop);
    applying = true;
    layout(forest.root,
           area.x + GAP_OUTER, area.y + GAP_OUTER,
           area.width - GAP_OUTER * 2, area.height - GAP_OUTER * 2);
    applying = false;
}

function forestFor(k) {
    if (!forests[k]) {
        forests[k] = { root: null };
    }
    return forests[k];
}

function add(w) {
    if (!manageable(w)) {
        return;
    }
    const k = key(w);
    forestFor(k);
    if (find(forests[k].root, w, null)) {
        return;
    }
    insert(k, w, workspace.activeWindow);
    retile(k);
}

function drop(w) {
    // The window may have moved between desktops since it was placed, so every
    // tree is asked rather than only the one its current key names.
    for (const k in forests) {
        if (remove(k, w)) {
            retile(k);
        }
    }
}

/* A window that is minimised, made fullscreen or sent to another desktop stops
   being part of the layout it was in, and rejoins wherever it lands. Both sides
   are the same two calls, so one handler covers every case. */
function rehome(w) {
    drop(w);
    add(w);
}

function attach(w) {
    w.minimizedChanged.connect(function () { rehome(w); });
    w.fullScreenChanged.connect(function () { rehome(w); });
    if (w.desktopsChanged) {
        w.desktopsChanged.connect(function () { rehome(w); });
    }
    if (w.outputChanged) {
        w.outputChanged.connect(function () { rehome(w); });
    }
}

/* ── Moving a window inside the layout ────────────────────────────────────

   Swapping two leaves, not re-inserting: the tree keeps its shape and only the
   windows in it trade places, so moving a window left and then right again puts
   the layout back exactly as it was.

   The neighbour is chosen geometrically, from the rects layout() stamped —
   nearest centre in the requested direction, and only where that direction
   dominates, so "left" cannot pick a window that is really above. Walking the
   tree structurally instead would follow the split order, which is not what the
   screen looks like. */
function neighbour(root, from, dx, dy) {
    const all = leaves(root, []);
    if (!from || !from.rect) {
        return null;
    }
    const cx = from.rect.x + from.rect.width / 2;
    const cy = from.rect.y + from.rect.height / 2;
    let best = null;
    let bestDist = Infinity;
    for (let i = 0; i < all.length; i++) {
        const n = all[i];
        if (n === from || !n.rect) {
            continue;
        }
        const ox = n.rect.x + n.rect.width / 2 - cx;
        const oy = n.rect.y + n.rect.height / 2 - cy;
        if (dx !== 0) {
            if (ox * dx <= 0 || Math.abs(ox) < Math.abs(oy)) {
                continue;
            }
        } else {
            if (oy * dy <= 0 || Math.abs(oy) < Math.abs(ox)) {
                continue;
            }
        }
        const dist = ox * ox + oy * oy;
        if (dist < bestDist) {
            bestDist = dist;
            best = n;
        }
    }
    return best;
}

function moveActive(dx, dy) {
    const w = workspace.activeWindow;
    if (!manageable(w)) {
        return;
    }
    const k = key(w);
    const forest = forests[k];
    if (!forest || !forest.root) {
        return;
    }
    const hit = find(forest.root, w, null);
    if (!hit) {
        return;
    }
    const other = neighbour(forest.root, hit.node, dx, dy);
    if (!other) {
        return;
    }
    const tmp = hit.node.win;
    hit.node.win = other.win;
    other.win = tmp;
    retile(k);
    // Focus follows the window, not the position — moving a window and then
    // typing into whatever happened to take its place is never what was meant.
    workspace.activeWindow = w;
}

function toggleFullScreen() {
    const w = workspace.activeWindow;
    if (w && w.fullScreenable) {
        // The layout follows by itself: fullScreenChanged is connected, and a
        // fullscreen window fails manageable(), so it drops out of the tree and
        // the others close over its space until it comes back.
        w.fullScreen = !w.fullScreen;
    }
}

/* Arrow keys are only half available: Meta+Shift+Left and Meta+Shift+Right are
   KDE's "move window to next/previous screen". Rather than take those away —
   they are global, and this script is not — the four directions are on H J K L,
   with the two free arrows registered as well. */
registerShortcut("NeonNoirTileMoveLeft", "Neon Noir: move window left",
                 "Meta+Shift+H", function () { moveActive(-1, 0); });
registerShortcut("NeonNoirTileMoveRight", "Neon Noir: move window right",
                 "Meta+Shift+L", function () { moveActive(1, 0); });
registerShortcut("NeonNoirTileMoveUp", "Neon Noir: move window up",
                 "Meta+Shift+K", function () { moveActive(0, -1); });
registerShortcut("NeonNoirTileMoveDown", "Neon Noir: move window down",
                 "Meta+Shift+J", function () { moveActive(0, 1); });
registerShortcut("NeonNoirTileMoveUpArrow", "Neon Noir: move window up (arrow)",
                 "Meta+Shift+Up", function () { moveActive(0, -1); });
registerShortcut("NeonNoirTileMoveDownArrow", "Neon Noir: move window down (arrow)",
                 "Meta+Shift+Down", function () { moveActive(0, 1); });
registerShortcut("NeonNoirTileFullScreen", "Neon Noir: toggle fullscreen",
                 "Meta+F", toggleFullScreen);

workspace.windowAdded.connect(function (w) {
    attach(w);
    add(w);
});

workspace.windowRemoved.connect(function (w) {
    drop(w);
});

// Adopt what is already open. The script can be enabled at any moment, and a
// tiler that only managed windows opened after it started would look broken
// for as long as the session lasted.
const existing = workspace.windowList();
for (let i = 0; i < existing.length; i++) {
    attach(existing[i]);
    add(existing[i]);
}
