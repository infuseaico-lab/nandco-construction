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

Business content and source notes: `content/business-info.md`.

## Photos

Real Nandco photos: `living-room.jpg`, `kitchen-oak.jpg`, `team.jpg`, `office-sign.jpg`, `tony-nguyen.jpg`, `collin-morgan.jpg`.

AI-generated (OpenAI image model, styled on Nandco project photos) and to be replaced with real project photos before launch, keeping the same file names in `site/assets/img/`:
`house-dusk.jpg`, `kitchen-pendants.jpg`, `pool-house.jpg`, `farmhouse-back.jpg`, `farmhouse-front.jpg`, `kitchen-galley.jpg`, `dining-blue.jpg`, `kitchen-marble.jpg`, `bathroom.jpg`, `adu.jpg`, `site-visit.jpg`, `selections.jpg`, `permits.jpg`, `rough-in.jpg`.

Plain backgrounds, no longer used by the pages: `hero-1.jpg` to `hero-4.jpg`.

## Estimate forms

With `data-endpoint` empty on `#quote-form` (main page) or `#quiz-form` / `#book-form` (landing page), sending opens an email to hello@nandcoconstruction.com with the answers filled in. To receive submissions directly, set `data-endpoint` to a form service URL (Formspree, Basin, Netlify Forms).
