# Nandco Construction website

Static site in `site/`, built on the Algazy Group template (`algazy-group-full`, branch `claude/pensive-ride-pfstra`):
`index.html`, `privacy.html`, `terms.html`, `assets/css/style.css`, `assets/js/main.js`,
plus the ad landing page `free-estimate.html` (`assets/css/lp.css`, `assets/js/lp.js`; noindex, not linked from the main page).
Open `site/index.html` in a browser; no build step.

Business content and source notes: `content/business-info.md`.

## Photos to replace

Each project photo is a placeholder image. Replace the file in `site/assets/img/` with the real photo under the same name (JPG, about 1536px wide).

| File | Photo | Used in |
|---|---|---|
| `house-dusk.jpg` | Remodeled single-story home, cedar siding, at dusk | Hero, gallery |
| `kitchen-pendants.jpg` | White kitchen, oak island, three brass pendants | Hero, Kitchen Remodeling card, gallery |
| `pool-house.jpg` | Modern black house with pool | Hero, New & Custom panel, Pool Houses card, gallery |
| `farmhouse-back.jpg` | White farmhouse back, pergola, folding doors | Hero, ADUs & Additions panel, Home Additions card |
| `farmhouse-front.jpg` | White two-story farmhouse, black garage door | New Home Construction card, gallery, Areas background |
| `kitchen-galley.jpg` | White shaker galley kitchen, herringbone tile | Kitchen & Bath panel |
| `living-room.jpg` | Living room, white beamed ceiling, slat wall | Whole Home panel, Home Remodeling card |
| `dining-blue.jpg` | Blue cabinets, open kitchen and dining | Restoration card, gallery |
| `kitchen-marble.jpg` | Cream inset cabinets, marble island, black range | Custom Homes card, gallery |
| `kitchen-oak.jpg` | Oak and marble waterfall kitchen | Process step 3, Projects background |
| `bathroom.jpg` | A finished bathroom (photo still needed) | Bathroom Remodeling card |
| `adu.jpg` | A finished ADU (photo still needed) | ADU card |
| `site-visit.jpg` | A site visit (photo still needed) | Process step 1 |
| `selections.jpg` | Plans and finish samples (photo still needed) | Process step 2 |
| `permits.jpg` | Permit set and plan check (photo still needed) | Landing page process row |
| `rough-in.jpg` | Framing and rough-in (photo still needed) | Landing page process row |

## Estimate forms

With `data-endpoint` empty on `#quote-form` (main page) or `#quiz-form` / `#book-form` (landing page), sending opens an email to hello@nandcoconstruction.com with the answers filled in. To receive submissions directly, set `data-endpoint` to a form service URL (Formspree, Basin, Netlify Forms).
