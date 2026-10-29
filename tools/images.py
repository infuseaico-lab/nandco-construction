"""WebP images for the site.

    python3 tools/images.py

converts any JPG or PNG dropped into site/assets/img/ to WebP (full size plus a 768px-wide copy for
phones), deletes the original, and rewrites every page so each photo is served as WebP with a
srcset and its true width/height. build_pages.py runs the page rewrite
on everything it generates, so this only needs running by hand after adding new photos.
"""
import re
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent.parent / "site"
IMG = SITE / "assets" / "img"
SMALL = 768
QUALITY = 80
SIZES = "(min-width: 64em) 50vw, 100vw"


def convert():
    for src in sorted([*IMG.glob("*.jpg"), *IMG.glob("*.jpeg"), *IMG.glob("*.png")]):
        if src.stem == "og-image":
            continue  # social preview stays JPG: not every network reads WebP
        im = Image.open(src).convert("RGB")
        im.save(IMG / f"{src.stem}.webp", "WEBP", quality=QUALITY, method=6)
        if im.width > SMALL + 100:
            h = round(im.height * SMALL / im.width)
            im.resize((SMALL, h), Image.LANCZOS).save(IMG / f"{src.stem}-{SMALL}.webp", "WEBP", quality=QUALITY, method=6)
        src.unlink()
        print("converted", src.name)


_dims = {}


def dims(name):
    if name not in _dims:
        _dims[name] = Image.open(IMG / f"{name}.webp").size
    return _dims[name]


def _img(m):
    tag, prefix, name = m.group(0), m.group(1), m.group(2)
    if not (IMG / f"{name}.webp").exists():
        return tag
    w, h = dims(name)
    tag = re.sub(r'\swidth="\d+"', f' width="{w}"', tag)
    tag = re.sub(r'\sheight="\d+"', f' height="{h}"', tag)
    if "srcset=" not in tag and (IMG / f"{name}-{SMALL}.webp").exists():
        sizes = "100vw" if 'fetchpriority="high"' in tag or "hero" in tag else SIZES
        tag = tag.replace(f'src="{prefix}assets/img/{name}.webp"',
                          f'src="{prefix}assets/img/{name}.webp" srcset="{prefix}assets/img/{name}-{SMALL}.webp {SMALL}w, '
                          f'{prefix}assets/img/{name}.webp {w}w" sizes="{sizes}"')
    return tag


def _preload(m):
    tag, prefix, name = m.group(0), m.group(1), m.group(2)
    if "imagesrcset" in tag or not (IMG / f"{name}-{SMALL}.webp").exists():
        return tag
    w, _ = dims(name)
    return tag.replace(f'href="{prefix}assets/img/{name}.webp"',
                       f'href="{prefix}assets/img/{name}.webp" imagesrcset="{prefix}assets/img/{name}-{SMALL}.webp {SMALL}w, '
                       f'{prefix}assets/img/{name}.webp {w}w" imagesizes="100vw"')


def responsive(html):
    """Point photos at WebP and give each a srcset and its true dimensions."""
    html = re.sub(r'((?:\.\./)*assets/img/[a-z0-9-]+)\.(?:jpe?g|png)(?=["\s,)])',
                  lambda m: m.group(1) + ".webp" if (IMG / (Path(m.group(1)).name + ".webp")).exists() else m.group(0), html)
    html = re.sub(r'<img\b[^>]*?src="((?:\.\./)*)assets/img/([a-z0-9-]+)\.webp"[^>]*>', _img, html)
    html = re.sub(r'<link rel="preload" as="image" href="((?:\.\./)*)assets/img/([a-z0-9-]+)\.webp"[^>]*>', _preload, html)
    # hero photos fill the screen width
    html = re.sub(r'<div class="hero__media"[^>]*>.*?</div>',
                  lambda m: re.sub(r'sizes="[^"]*"', 'sizes="100vw"', m.group(0)), html, flags=re.S)
    return html


if __name__ == "__main__":
    convert()
    for page in [*SITE.glob("*.html"), *SITE.glob("services/*.html")]:
        page.write_text(responsive(page.read_text()))
    print("rewrote page image markup")
