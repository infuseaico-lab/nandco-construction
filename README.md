# Nandco Construction website

Static site in `site/`, built on the Algazy Group template (`algazy-group-full`, branch `claude/pensive-ride-pfstra`):
`index.html`, `privacy.html`, `terms.html`, `assets/css/style.css`, `assets/js/main.js`,
plus the ad landing page `free-estimate.html` (`assets/css/lp.css`, `assets/js/lp.js`; noindex, not linked from the main page).
Open `site/index.html` in a browser.

Pages: `index.html` (home), `estimate.html` (free estimate form), `services/*.html` (one page per service, linked from the Services menu), `free-estimate.html` (ad landing page), `privacy.html`, `terms.html`.
The service pages, the estimate page and the legal page headers are generated from the homepage's header, footer and icons plus the content in `tools/build_pages.py`. After editing either, run:

```
python3 tools/build_pages.py
```

Gallery page: `site/gallery.html` (generated; edit the `GALLERY` list in `tools/build_pages.py` to add or reorder photos).

Business content and source notes: `content/business-info.md`.

## Photos

All photos are WebP in `site/assets/img/`: `name.webp` (full size) plus `name-768.webp` for phones. To add or replace one, drop a JPG or PNG with the target name into that folder and run:

    python3 tools/images.py

It converts the photo to both WebP sizes, deletes the original, and updates the image markup on every page. `og-image.jpg` (1200x630) is the link preview for social networks and stays JPG.

Real Nandco photos: `living-room`, `kitchen-oak`, `team`, `office-sign`, `tony-nguyen`, `collin-morgan`.

AI-generated (OpenAI image model, styled on Nandco project photos), to be replaced with real project photos before launch under the same names:
`house-dusk`, `kitchen-pendants`, `pool-house`, `farmhouse-back`, `farmhouse-front`, `kitchen-galley`, `dining-blue`, `kitchen-marble`, `bathroom`, `adu`, `site-visit`, `selections`, `permits`, `rough-in`, `hero-home-exterior`, `hero-great-room`, the nine `svc-*` images used in each service page's "What's Included" section, the eight `g-*` gallery-page photos, and `cta-home` (background of the homepage "Not Sure Where to Start?" card).

## Speed and SEO

- Fonts are self-hosted in `site/assets/fonts/` (latin subset), so there is no request to Google Fonts before first paint.
- Each page has a canonical URL, Open Graph and Twitter tags, and structured data: GeneralContractor and FAQPage on the homepage, Service and BreadcrumbList on service pages.
- `site/sitemap.xml` and `site/robots.txt` assume the site lives at https://nandcoconstruction.com/. Regenerate the sitemap's dates when pages change.
- `free-estimate.html` is the paid-ads landing page and is `noindex` on purpose.
- `site/_headers` sets long cache times on Netlify or Cloudflare Pages. On another host, set the same rules there.
- Decorative backgrounds and the signature fonts load only as their section nears the screen (`.is-near` in `main.js`).

## Estimate forms

With `data-endpoint` empty on `#quote-form` (main page) or `#quiz-form` / `#book-form` (landing page), sending opens an email to hello@nandcoconstruction.com with the answers filled in. To receive submissions directly, set `data-endpoint` to a form service URL (Formspree, Basin, Netlify Forms).
