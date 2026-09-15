"""Line-art tray icons — network, volume, bluetooth, notifications, battery.

Breeze draws these as filled silhouettes; the artboard draws them as outlines on
the same 24px grid as the app glyphs, and the battery reads green rather than
grey. The tray is the densest cluster of icons on the panel, so leaving it on
Breeze is what keeps the right-hand end looking stock.

Coverage comes from scanning breeze-dark rather than from a hand-written list.
These families are large — 142 battery names alone, across `-charging`,
`-profile-*` and `-symbolic` variants — and a name we miss silently falls back
to Breeze's filled version, which looks worse than not overriding at all
because the two styles then sit side by side.
"""
import re

STROKE = 1.7
DIRS = ('status/scalable', 'devices/scalable', 'actions/scalable',
        'preferences/scalable')

# Which breeze-dark families we take over. Anything else keeps Breeze's icon.
FAMILIES = ('battery', 'audio-volume-', 'network-wireless', 'network-wired',
            'network-bluetooth', 'notification', 'preferences-system-bluetooth')


def _svg(body, extra=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
            'viewBox="0 0 24 24">' + body + extra + '</svg>\n')


def _g(paths, colour, width=STROKE, opacity=None):
    o = f' opacity="{opacity}"' if opacity is not None else ''
    return (f'<g fill="none" stroke="{colour}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{o}>{paths}</g>')


def _slash(colour):
    """The disabled/off diagonal, drawn over the glyph."""
    return _g('<path d="M4.2 4.2l15.6 15.6"/>', colour)


# ── glyphs ────────────────────────────────────────────────────────────────────

def wifi(level, colour, dim):
    """Three arcs and a dot above a common centre; unlit arcs stay faint."""
    cx, cy = 12.0, 18.6
    lit, unlit = [], []
    for i, r in enumerate((4.6, 8.0, 11.4), start=2):
        dx = r * 0.7071
        d = (f'M{cx - dx:.2f} {cy - dx:.2f}'
             f'A{r} {r} 0 0 1 {cx + dx:.2f} {cy - dx:.2f}')
        (lit if level >= i else unlit).append(f'<path d="{d}"/>')
    out = ''
    if unlit:
        out += _g(''.join(unlit), dim, opacity=0.35)
    if lit:
        out += _g(''.join(lit), colour)
    # The dot is the first "bar": at level 0 it too goes faint.
    out += (f'<circle cx="{cx}" cy="{cy - 0.4}" r="1.25" fill="{colour}"/>'
            if level >= 1 else
            f'<circle cx="{cx}" cy="{cy - 0.4}" r="1.25" fill="{dim}" '
            f'opacity="0.35"/>')
    return out


def speaker(waves, colour):
    body = ('<path d="M3.4 9.4h3.3L11.4 5.3a.7.7 0 0 1 1.2.55v12.3'
            'a.7.7 0 0 1-1.2.55L6.7 14.6H3.4a.9.9 0 0 1-.9-.9v-3.4'
            'a.9.9 0 0 1 .9-.9z"/>')
    arcs = ''
    if waves >= 1:
        arcs += '<path d="M15.6 9.6a3.6 3.6 0 0 1 0 4.8"/>'
    if waves >= 2:
        arcs += '<path d="M18.4 7a7.4 7.4 0 0 1 0 10"/>'
    return _g(body + arcs, colour)


def speaker_muted(colour):
    return _g('<path d="M3.4 9.4h3.3L11.4 5.3a.7.7 0 0 1 1.2.55v12.3'
              'a.7.7 0 0 1-1.2.55L6.7 14.6H3.4a.9.9 0 0 1-.9-.9v-3.4'
              'a.9.9 0 0 1 .9-.9z"/>'
              '<path d="M15.8 9.8l4.8 4.4M20.6 9.8l-4.8 4.4"/>', colour)


def battery(pct, colour, charging=False, missing=False, cut=None):
    shell = ('<rect x="2.3" y="7.7" width="16.6" height="8.6" rx="2.3"/>'
             '<path d="M21 10.7v2.6"/>')
    out = _g(shell, colour)
    if missing:
        return out + _g('<path d="M8.4 12h5.2"/>', colour)
    inner_w = 12.8
    w = round(inner_w * max(0.0, min(1.0, pct)), 2)
    if w > 0.4:
        out += (f'<rect x="4.3" y="9.7" width="{w}" height="4.6" rx="1.2" '
                f'fill="{colour}"/>')
    if charging:
        # Knocked out in the panel colour. Drawing the bolt in the battery's
        # own colour makes it vanish into the fill it sits on top of.
        out += ('<path d="M12.6 8.4l-3.6 4.6h2.6l-.9 3.2 3.7-4.7h-2.7z" '
                f'fill="{cut}" stroke="{cut}" stroke-width="1.2" '
                'stroke-linejoin="round"/>')
    return out


def bluetooth(colour):
    return _g('<path d="M7.2 7.6L16.8 16.4 12 20.6V3.4l4.8 4.2L7.2 16.4"/>',
              colour)


def bell(colour):
    return _g('<path d="M6 17.3c1.05-.95 1.6-2.1 1.6-3.4V11a4.4 4.4 0 0 1 8.8 0'
              'v2.9c0 1.3.55 2.45 1.6 3.4z"/>'
              '<path d="M10.1 20.2a2.1 2.1 0 0 0 3.8 0"/>', colour)


def wired(colour):
    return _g('<rect x="2.6" y="5.4" width="18.8" height="12" rx="2"/>'
              '<path d="M7.4 20.6h9.2"/><path d="M12 17.4v3.2"/>', colour)


# ── name → glyph ──────────────────────────────────────────────────────────────

_BATTERY_WORDS = {'empty': 0.0, 'caution': 0.08, 'low': 0.25,
                  'good': 0.7, 'full': 1.0, 'ups': 1.0}
_WIFI_WORDS = {'none': 0, 'weak': 1, 'ok': 2, 'good': 3, 'excellent': 4}


def _level_from_pct(pct):
    """Breeze labels wireless strength 0-100; the glyph has four steps."""
    if pct <= 0:
        return 0
    if pct < 30:
        return 1
    if pct < 55:
        return 2
    if pct < 80:
        return 3
    return 4


def render(name, T):
    """Return the SVG for one icon name, or None to leave Breeze's alone."""
    dim, norm = T['text.dim'], T['text.normal']
    stem = re.sub(r'-(symbolic|rtl)$', '', name)
    stem = re.sub(r'-(symbolic|rtl)$', '', stem)          # -symbolic-rtl

    if stem.startswith('battery'):
        charging = '-charging' in stem
        s = stem.replace('-charging', '')
        s = re.sub(r'-profile-\w+$', '', s)
        if s in ('battery-missing',):
            return _svg(battery(0, dim, missing=True))
        m = re.match(r'battery-(\d{3})$', s)
        if m:
            pct = int(m.group(1)) / 100.0
        elif s == 'battery-full-charged':
            pct, charging = 1.0, False
        elif s == 'battery':
            pct = 1.0
        else:
            word = s.replace('battery-', '')
            if word not in _BATTERY_WORDS:
                return None
            pct = _BATTERY_WORDS[word]
        colour = (T['status.negative'] if pct < 0.10 else
                  T['status.neutral'] if pct < 0.25 else T['status.positive'])
        return _svg(battery(pct, colour, charging=charging,
                            cut=T['surface.window']))

    if stem.startswith('audio-volume-'):
        warn = '-warning' in stem or '-danger' in stem
        colour = (T['status.negative'] if '-danger' in stem else
                  T['status.neutral'] if warn else dim)
        s = re.sub(r'-(warning|danger)', '', stem)
        if s == 'audio-volume-muted':
            return _svg(speaker_muted(colour))
        waves = {'audio-volume-high': 2, 'audio-volume-medium': 1,
                 'audio-volume-low': 0}.get(s)
        return _svg(speaker(waves, colour)) if waves is not None else None

    if 'bluetooth' in stem:
        colour = dim
        if stem.endswith('-inactive') or stem.endswith('-disabled'):
            return _svg(bluetooth(colour) + _slash(colour))
        if stem.endswith('-activated'):
            colour = T['accent.cyan']
        return _svg(bluetooth(colour))

    if stem.startswith('notification'):
        if '-disabled' in stem:
            return _svg(bell(dim) + _slash(dim))
        body = bell(dim)
        if '-active' in stem:
            body = bell(norm) + (f'<circle cx="17.6" cy="6.4" r="2.7" '
                                 f'fill="{T["accent.magenta"]}"/>')
        return _svg(body)

    if stem.startswith('network-wired'):
        if any(k in stem for k in ('-disconnected', '-unavailable')):
            return _svg(wired(dim) + _slash(dim))
        return _svg(wired(dim))

    if stem.startswith('network-wireless'):
        colour = dim
        if '-limited' in stem:
            colour = T['status.neutral']
        s = re.sub(r'-(limited|locked)$', '', stem)
        if any(k in s for k in ('-disconnected', '-off', '-unavailable')):
            return _svg(wifi(0, colour, dim) + _slash(dim))
        m = re.search(r'-signal-(\w+)$', s)
        if m:
            lvl = _WIFI_WORDS.get(m.group(1))
            return _svg(wifi(lvl, colour, dim)) if lvl is not None else None
        m = re.search(r'-(\d+)$', s)
        if m:
            return _svg(wifi(_level_from_pct(int(m.group(1))), colour, dim))
        if s in ('network-wireless-acquiring',):
            return _svg(wifi(1, colour, dim))
        if s in ('network-wireless', 'network-wireless-available',
                 'network-wireless-on', 'network-wireless-hotspot',
                 'network-wireless-connected'):
            return _svg(wifi(4, colour, dim))
        return None

    return None


def svgs(T, breeze_root):
    """{icon-name: svg} for every name in these families that breeze-dark has.

    Scanning the parent theme is what makes the coverage complete: any name a
    tray applet can ask for is a name breeze-dark already ships.
    """
    names = set()
    for svg in breeze_root.rglob('*.svg'):
        n = svg.stem
        if any(n.startswith(f) for f in FAMILIES):
            names.add(n)
    out = {}
    for n in sorted(names):
        body = render(n, T)
        if body:
            out[n] = body
    return out
