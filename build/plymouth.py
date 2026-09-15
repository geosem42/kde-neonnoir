"""Plymouth boot splash (script module).

Three things about Plymouth on this machine that are not what the tutorials say:

  - plymouth-set-default-theme is NOT installed (the plymouth package ships only
    /usr/bin/plymouth and /usr/sbin/plymouthd). Selection goes through
    update-alternatives, exactly as the Kubuntu theme packages do it.
  - The theme DIRECTORY NAME must equal the .plymouth basename, because the
    Ubuntu initramfs hook rebuilds the path as themes/<name>/<name>.plymouth
    from the basename and silently drops a mismatch.
  - The splash boots from the initrd copy, not from /usr/share, so nothing
    changes until update-initramfs -u runs.

The hook also copies only the Ubuntu font family into the initrd, which is why
the mark and wordmark are pre-rendered PNGs rather than Image.Text calls.
"""
import shutil


PLYMOUTH_INI = '''[Plymouth Theme]
Name=@NAME@
Description=@DESC@
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/@ID@
ScriptFile=/usr/share/plymouth/themes/@ID@/@ID@.script
'''

# Registered as the default.plymouth.grub slave. Without it, selecting this
# theme leaves /usr/share/plymouth/themes/default.grub dangling and
# /etc/grub.d/05_debian_theme quietly stops setting GRUB's colours.
GRUB_SNIPPET = '''if background_color @GRUBBG@; then
  clear
fi

color_normal=light-gray/black
color_highlight=black/light-cyan
'''


def floats(hexcolour):
    h = hexcolour.lstrip('#')
    return ', '.join(f'{int(h[i:i+2], 16) / 255:.4f}' for i in (0, 2, 4))


def decimals(hexcolour):
    h = hexcolour.lstrip('#')
    return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))


def build(T, DIST, THEME_ID, THEME_NAME, template_dir):
    import brand, lookandfeel
    from PIL import Image
    out = []
    root = DIST / 'plymouth' / THEME_ID
    root.mkdir(parents=True, exist_ok=True)

    subs = {
        '@NAME@': THEME_NAME,
        '@DESC@': 'Neon noir boot splash',
        '@ID@': THEME_ID,
        '@BG@': floats(T['surface.void']),
        '@TEXT@': floats(T['text.normal']),
        '@DIM@': floats(T['text.dim']),
        '@GRUBBG@': decimals(T['surface.void']),
    }

    def fill(text):
        for k, v in subs.items():
            text = text.replace(k, v)
        return text

    (root / f'{THEME_ID}.plymouth').write_text(fill(PLYMOUTH_INI))
    (root / f'{THEME_ID}.grub').write_text(fill(GRUB_SNIPPET))
    (root / f'{THEME_ID}.script').write_text(
        fill((template_dir / 'plymouth-NeonNoir.script').read_text()))
    out.append(f'plymouth/{THEME_ID}/{THEME_ID}.plymouth, .script, .grub')

    brand.png(lookandfeel.ground_svg(T, 1920, 1080), root / 'background.png', 1920, 1080)
    brand.dither(root / 'background.png')
    brand.png(brand.mark_svg(T, 384), root / 'mark.png', 384, 384)
    shutil.copy(DIST / 'brand' / 'wordmark.png', root / 'wordmark.png')
    for name in ('bar-track', 'bar-fill'):
        shutil.copy(DIST / 'brand' / f'{name}.png', root / f'{name}.png')
    brand.png(f'<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" '
              f'viewBox="0 0 12 12"><circle cx="6" cy="6" r="4.5" '
              f'fill="{T["accent.cyan"]}"/></svg>', root / 'bullet.png', 12, 12)
    out.append(f'plymouth/{THEME_ID}/  (background, mark, wordmark, bar, bullet)')

    # The KCM and every packaged theme ship a 640x400 preview.
    prev = Image.open(root / 'background.png').convert('RGBA').resize((640, 400), Image.LANCZOS)
    u = max(8, 400 // 90)
    m = Image.open(root / 'mark.png').resize((u * 19, u * 19), Image.LANCZOS)
    w = Image.open(root / 'wordmark.png')
    w = w.resize((u * 20, max(1, round(u * 20 * w.height / w.width))), Image.LANCZOS)
    total = u * 19 + u * 3 + w.height + u * 3 + 2
    top = (400 - total) // 2
    prev.alpha_composite(m, ((640 - m.width) // 2, top))
    prev.alpha_composite(w, ((640 - w.width) // 2, top + u * 19 + u * 3))
    prev.convert('RGB').save(root / 'preview.png')
    out.append(f'plymouth/{THEME_ID}/preview.png')
    return out
