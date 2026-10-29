"""Builds the free estimate page and the nine service pages from the homepage's header, footer and icons.

Run from the repository root after editing site/index.html or the content below:
    python3 tools/build_pages.py
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
HOME = (SITE / "index.html").read_text()

PHONE = "(213) 444-6596"
TEL = "+12134446596"


def between(start, end, text=HOME, include_end=True):
    a = text.index(start)
    b = text.index(end, a) + (len(end) if include_end else 0)
    return text[a:b]


SPRITE = between('<svg width="0" height="0"', "</svg>\n", include_end=True)
SPRITE = SPRITE[: SPRITE.index("</defs>\n</svg>") + len("</defs>\n</svg>")] if "</defs>" in SPRITE else SPRITE
SPRITE = between('<svg width="0" height="0"', "</defs>\n</svg>")
HEADER = between('<header class="bar" id="top">', "</header>")
FOOTER = between('<footer class="foot">', "</footer>")
DOCK = between('<div class="dock" data-dock>', "</div>")


def relink(html, up):
    """Point the homepage's own links at the right place from a page in another folder."""
    html = html.replace('href="#top"', f'href="{up}index.html"')
    # homepage section links in the shared header and footer
    html = re.sub(r'href="#(projects|services|process|gallery|team|promises|reviews|areas|questions)"', rf'href="{up}index.html#\1"', html)
    html = re.sub(r'(src|href|srcset)="assets/', rf'\1="{up}assets/', html)
    html = html.replace(", assets/", f", {up}assets/")
    for page in ("index.html", "estimate.html", "privacy.html", "terms.html", "services/"):
        html = html.replace(f'href="{page}', f'href="{up}{page}')
    return html


def page(path, title, description, body, active=None, body_class=""):
    up = "../" * path.count("/")
    header = relink(HEADER, up).replace('id="top"', "")
    if active:
        header = header.replace(f'href="{up}services/{active}.html"', f'href="{up}services/{active}.html" aria-current="page"')
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#FAF7EE">
  <link rel="icon" type="image/png" sizes="32x32" href="{up}assets/brand/icon-32.png">
  <link rel="icon" type="image/png" sizes="512x512" href="{up}assets/brand/icon-512.png">
  <link rel="apple-touch-icon" href="{up}assets/brand/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{up}assets/css/style.css">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body id="top"{f' class="{body_class}"' if body_class else ""}>

{SPRITE}

<a class="skip" href="#main">Skip to content</a>

{header}

<main id="main">
{relink(body, up)}
</main>

{relink(FOOTER, up)}

{relink(DOCK, up)}

<script src="{up}assets/js/main.js" defer></script>
</body>
</html>
"""
    out = SITE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


def cta_band(project=None):
    href = "estimate.html" + (f"?project={project}" if project else "")
    return f"""  <section class="cta-band deco deco--glow" aria-labelledby="cta-title">
    <div class="wrap cta-band__in" data-reveal>
      <div>
        <span class="pill">{ico('arrow')}Get Started</span>
        <h2 class="h2" id="cta-title">Ready to Start Your Project?</h2>
        <p>A free on-site visit and a written, line-item estimate, with no obligation.</p>
      </div>
      <div class="cta-band__acts">
        <a class="btn btn--accent btn--lg" href="{href}">Get a Free Estimate {ico('arrow')}</a>
        <a class="btn btn--outline btn--lg" href="tel:{TEL}">{ico('phone')} {PHONE}</a>
      </div>
    </div>
  </section>"""


CITIES = ["Los Angeles", "Bel Air", "Hollywood", "West Hollywood", "Beverly Hills", "Brentwood", "Santa Monica",
          "Pacific Palisades", "Malibu", "Culver City", "Sherman Oaks", "Encino", "Studio City", "Tarzana",
          "Woodland Hills", "Van Nuys", "Valley Village", "Toluca Lake", "Burbank", "Pasadena", "Arcadia",
          "Torrance", "Redondo Beach", "Palos Verdes"]

# Timelines are typical ranges for Los Angeles projects, to be confirmed by Nandco.
SERVICES = [
    dict(slug="kitchen-remodeling", detail="Remodeled kitchen corner with white-oak cabinets, a marble backsplash and a brass pot filler over the range", name="Kitchen Remodeling", project="kb", hero="hero-2", img="kitchen-pendants", img2="kitchen-galley",
         alt="White kitchen with an oak island under three brass globe pendants",
         line="Kitchens rebuilt around how you cook and gather: layout, cabinetry, counters, lighting and appliances.",
         intro=["A kitchen is the hardest-working room in the house and the one with the most decisions in it. We start with how you use it, then settle the layout, cabinetry, counters and appliances before demolition begins.",
                "Line-item estimates mean you can see where the budget goes, and our purchase coordinators order and track every selection to keep the schedule."],
         included=["Layout changes, islands and opened walls", "Custom or semi-custom cabinetry", "Stone or quartz counters and backsplash", "Appliance planning and ventilation", "Lighting, electrical and plumbing updates", "Flooring and finish carpentry"],
         before=[("Site visit and estimate", "1 wk"), ("Design and selections", "3–5 wks"), ("Permits and ordering", "2–6 wks")],
         build=[("Demolition and rough-in", "2–3 wks"), ("Cabinets and counters", "3–5 wks"), ("Finishes and appliances", "1–2 wks")],
         total="3–5 months", result="Your new kitchen"),
    dict(slug="bathroom-remodeling", detail="Remodeled primary bathroom with a freestanding tub, a double oak vanity and a walk-in glass shower", name="Bathroom Remodeling", project="kb", hero="hero-4", img="bathroom", img2="kitchen-marble",
         alt="Remodeled bathroom with a white-oak vanity, brass fixtures and a frameless glass shower",
         line="Primary suites, guest baths and powder rooms, with the waterproofing done right under every tile.",
         intro=["What makes a bathroom last is mostly out of sight: the waterproofing, the slope of the shower floor, the ventilation. We get those right first, then build the tile, glass and fixtures you chose on top of them.",
                "From curbless showers to a simple powder-room refresh, the scope and the cost are written down line by line before work starts."],
         included=["Layout changes and curbless showers", "Waterproofing and tile", "Vanities, fixtures and glass", "Ventilation and lighting", "Heated floors, if you want them", "Grab bars and accessible layouts"],
         before=[("Site visit and estimate", "1 wk"), ("Design and selections", "2–4 wks"), ("Permits and ordering", "2–4 wks")],
         build=[("Demolition and rough-in", "1–2 wks"), ("Waterproofing and tile", "2–3 wks"), ("Fixtures and glass", "1 wk")],
         total="2–3 months", result="Your new bathroom"),
    dict(slug="home-remodeling", detail="Open-plan great room after a whole-home remodel, with kitchen, dining and living areas under white beams", name="Home Remodeling", project="home", hero="hero-1", img="living-room", img2="dining-blue",
         alt="Living room with a white beamed ceiling and a wood slat wall",
         line="Whole-house and multi-room remodels, from opened-up floor plans to new systems behind the walls.",
         intro=["A whole-home remodel touches everything at once: structure, plumbing, electrical, finishes and the way rooms connect. We plan it as one project with one schedule, so the kitchen, the baths and the new floor plan come together instead of in pieces.",
                "Your project coordinator keeps you informed at every stage, and our purchase coordinators track every finish you select so nothing holds up the crew."],
         included=["Floor plan changes and wall removal, with structural engineering", "Electrical, plumbing and HVAC upgrades", "Windows, doors and exterior updates", "Flooring, millwork, paint and lighting", "Kitchens and bathrooms as part of the whole", "City permits and inspections, handled by us"],
         before=[("Site visit and estimate", "1–2 wks"), ("Design and selections", "4–8 wks"), ("Permits and ordering", "4–12 wks")],
         build=[("Demolition and structure", "3–6 wks"), ("Systems and rough-in", "3–5 wks"), ("Finishes", "6–10 wks")],
         total="6–10 months", result="Your finished home"),
    dict(slug="home-additions", detail="New second-story bedroom addition with a vaulted ceiling and a skylight", name="Home Additions", project="adu", hero="hero-4", img="farmhouse-back", img2="farmhouse-front",
         alt="Back of a white farmhouse with a pergola and open folding doors",
         line="More room on the lot you already own: ground-floor additions, second stories and expanded rooms.",
         intro=["An addition should look as if it was always there. That means matching the roof line, the windows and the finishes, and tying the new structure and systems into the old ones properly.",
                "Before design begins we review what your lot and your city allow, so the plans you approve are plans that can be permitted."],
         included=["Feasibility and zoning review", "Architectural and structural plans", "Foundation and framing", "Second-story additions", "Roof, systems and finishes tied into the existing house", "City permits and inspections"],
         before=[("Site visit and feasibility", "1–2 wks"), ("Design and engineering", "6–10 wks"), ("Permits and ordering", "8–16 wks")],
         build=[("Foundation and framing", "4–8 wks"), ("Systems and rough-in", "4–6 wks"), ("Finishes and tie-in", "6–10 wks")],
         total="9–14 months", result="Your added space"),
    dict(slug="adus", detail="Interior of a backyard ADU with an oak kitchenette, a small dining table and a glass door to the garden", name="Accessory Dwelling Units (ADUs)", project="adu", hero="hero-3", img="adu", img2="farmhouse-back",
         alt="Detached backyard ADU with white stucco, oak siding and black-framed windows",
         line="Detached ADUs, garage conversions and junior ADUs for family, guests or rental income.",
         intro=["An ADU is a small house with all the requirements of a big one: its own foundation, utilities, kitchen and bath, and its own permit. We review your lot first, then design and build the unit that fits it.",
                "Whether it is a detached backyard unit, a converted garage or a junior ADU inside the house, we handle the city submission and every inspection."],
         included=["Lot and feasibility review", "Detached new-build ADUs", "Garage conversions", "Junior ADUs inside the existing house", "Utility connections and separate meters where needed", "Permits through your city"],
         before=[("Site visit and feasibility", "1–2 wks"), ("Design and selections", "4–8 wks"), ("Permits and ordering", "8–16 wks")],
         build=[("Foundation and utilities", "3–5 wks"), ("Framing and roof", "4–6 wks"), ("Systems and finishes", "8–12 wks")],
         total="8–12 months", result="Your finished ADU"),
    dict(slug="home-restoration", detail="Restored 1920s living room with the original arched doorway, refinished trim and a tiled fireplace", name="Restoration & Fire Rebuilds", project="home", hero="hero-1", img="dining-blue", img2="house-dusk",
         alt="Open kitchen and dining room with blue cabinetry and wood floors",
         line="Fire and damage rebuilds coordinated with your insurance adjuster, and older homes brought back with their character kept.",
         intro=["After a fire or major damage, the work starts before the build: assessing what can be saved, documenting the loss, and working with your insurance adjuster on scope. We take on that coordination so you are not managing it alone.",
                "For older homes, restoration means repairing structure and systems while keeping the trim, windows and floors that make the house what it is."],
         included=["Fire and damage assessment", "Working directly with your insurance adjuster", "Structural, foundation and seismic repair", "Rewiring and repiping", "Matching original trim, windows and flooring", "Permits and inspections through the rebuild"],
         before=[("Assessment and adjuster meeting", "1–2 wks"), ("Scope, design and selections", "3–6 wks"), ("Permits and ordering", "2–8 wks")],
         build=[("Demolition and structure", "4–8 wks"), ("Systems and rough-in", "3–6 wks"), ("Finishes", "4–8 wks")],
         total="5–9 months", result="Back home"),
    dict(slug="pool-house", detail="Pool house lounge with a built-in bar and folding glass doors open to the pool", name="Pool House Design & Construction", project="adu", hero="hero-3", img="pool-house", img2="farmhouse-back",
         alt="Modern black house with a pool, spa and lounge chairs on a paver-and-turf deck",
         line="Pool houses and cabanas with changing rooms, baths, outdoor kitchens and covered lounge space.",
         intro=["A pool house lives between indoors and out. We design it to match the main house, then build the plumbing, gas and electrical it needs for a bath, a kitchen or a bar.",
                "Wide openings, covered space and durable finishes make it a room you use all year, not only in summer."],
         included=["Design to match the main house", "Bathrooms and changing rooms", "Outdoor kitchen and bar", "Covered patios and doors that open fully", "Electrical, plumbing and gas", "Permits and inspections"],
         before=[("Site visit and estimate", "1–2 wks"), ("Design and selections", "4–6 wks"), ("Permits and ordering", "6–12 wks")],
         build=[("Foundation and framing", "4–6 wks"), ("Systems and rough-in", "2–4 wks"), ("Finishes", "4–6 wks")],
         total="6–9 months", result="Your pool house"),
    dict(slug="new-home-construction", detail="Double-height living room in a new farmhouse with an oak staircase and tall black-framed windows", name="New Home Construction", project="new", hero="hero-2", img="farmhouse-front", img2="farmhouse-back",
         alt="White two-story modern farmhouse with a black garage door",
         line="Ground-up homes built from approved plans, with pre-construction budgeting and one team on site.",
         intro=["A new home is hundreds of decisions and dozens of trades. We bring them under one schedule and one budget, starting with pre-construction work that prices the plans before ground is broken.",
                "Our project managers run the site, our project engineers solve the technical details, and your project coordinator is the one person you call."],
         included=["Pre-construction budgeting and scheduling", "Site preparation, grading and foundation", "Framing, roofing and windows", "Plumbing, electrical and HVAC", "Interior and exterior finishes", "Final inspections and sign-off"],
         before=[("Plan review and budgeting", "2–4 wks"), ("Engineering and selections", "8–16 wks"), ("Permits and ordering", "12–24 wks")],
         build=[("Site work and foundation", "6–10 wks"), ("Framing and roof", "8–12 wks"), ("Systems and finishes", "18–24 wks")],
         total="16–24 months", result="Your new home"),
    dict(slug="custom-home", detail="Custom home entry with a floating oak staircase, a limestone floor and a walnut pivot door", name="Custom Homes", project="new", hero="hero-3", img="kitchen-marble", img2="pool-house",
         alt="Inset cream cabinetry, a marble-topped walnut island and a black range",
         line="One-of-a-kind homes built with you from the first sketch, with one team responsible through move-in.",
         intro=["A custom home starts long before construction: with a budget that matches the design, and a builder at the table while the architect is still drawing. We join early so the plans you fall in love with are plans you can afford to build.",
                "Our purchase coordinators manage every selection and order, and your project coordinator keeps you informed from the first sketch to the final walkthrough."],
         included=["Pre-design budgeting", "Coordination with your architect and engineers", "Selections and procurement managed for you", "Construction management on site", "Regular updates from your project coordinator", "Final walkthrough and punch list"],
         before=[("Pre-design and budgeting", "2–4 wks"), ("Design development", "16–24 wks"), ("Permits and ordering", "12–24 wks")],
         build=[("Site work and foundation", "6–10 wks"), ("Framing and roof", "10–14 wks"), ("Systems and finishes", "24–36 wks")],
         total="18–30 months", result="Your custom home"),
]
BY_SLUG = {s["slug"]: s for s in SERVICES}
ALT = {s["img"]: s["alt"] for s in SERVICES}
ALT.update({"kitchen-galley": "White shaker galley kitchen with herringbone tile and a pro range",
            "house-dusk": "Remodeled single-story home with cedar siding and lit windows at dusk"})


def esc(t):
    return t.replace("&", "&amp;")


def stage(title, rows):
    items = "".join(f"<li><span>{esc(w)}</span><b>{d}</b></li>" for w, d in rows)
    return f'<div class="stage" data-reveal><h3 class="h3">{title}</h3><ol>{items}</ol></div>'


def service_page(s):
    others = [o for o in SERVICES if o["project"] == s["project"] and o["slug"] != s["slug"]]
    others += [o for o in SERVICES if o["project"] != s["project"]]
    related = "".join(f"""
        <li class="card" data-reveal>
          <img decoding="async" class="card__img" src="assets/img/{o['img']}.jpg" width="1536" height="1024" alt="{o['alt']}" loading="lazy">
          <div class="card__body">
            <h3 class="h3"><a class="card__link" href="services/{o['slug']}.html">{esc(o['name'])}</a></h3>
            <p>{o['line']}</p>
          </div>
        </li>""" for o in others[:3])
    grid = "".join(f'<li data-reveal>{ico("check")}<span>{esc(i)}</span></li>' for i in s["included"])
    cities = "".join(f"<li>{ico('pin')}{c}</li>" for c in CITIES)
    body = f"""
  <section class="hero hero--page" aria-labelledby="hero-title">
    <div class="hero__media">
      <img decoding="async" class="is-on" src="assets/img/{s['img']}.jpg" width="1536" height="1024" alt="{s['alt']}" fetchpriority="high">
    </div>
    <div class="hero__copy">
      <p class="crumbs"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="index.html#services">Services</a><span aria-hidden="true">/</span><span>{esc(s['name'])}</span></p>
      <h1 class="hero__title" id="hero-title">{esc(s['name'])} in Los Angeles</h1>
      <p class="hero__lead">{s['line']}</p>
      <div class="hero__actions" data-hero-actions>
        <a class="btn btn--accent btn--lg" href="estimate.html?project={s['project']}">Get a Free Estimate {ico('arrow')}</a>
        <a class="btn btn--outline btn--lg" href="tel:{TEL}">{ico('phone')} Call {PHONE}</a>
      </div>
    </div>
  </section>

  <section class="section deco deco--dots" id="included" aria-labelledby="included-title">
    <div class="wrap">
      <div class="incl">
        <header class="incl__head" data-reveal>
          <div>
            <span class="pill">{ico('layers')}What's Included</span>
            <h2 class="h2" id="included-title">{esc(s['name'])}, Start to Finish</h2>
          </div>
          <div class="incl__intro">{''.join(f'<p>{p}</p>' for p in s['intro'])}</div>
        </header>
        <figure class="incl__photo" data-reveal>
          <img decoding="async" src="assets/img/svc-{s['slug']}.jpg" width="1536" height="1024" alt="{s['detail']}" loading="lazy">
        </figure>
        <ul class="incl__grid">{grid}</ul>
        <p class="incl__cta" data-reveal><a class="btn btn--accent btn--lg" href="estimate.html?project={s['project']}">Get a Free Estimate {ico('arrow')}</a></p>
      </div>
    </div>
  </section>

  <section class="section section--card" id="timeline" aria-labelledby="timeline-title">
    <div class="wrap">
      <header class="section__head" data-reveal>
        <span class="pill">{ico('clipboard')}How It Runs</span>
        <h2 class="h2" id="timeline-title">Typical Timeline</h2>
        <p class="section__intro">Typical ranges for Los Angeles projects. Your written schedule is set after the site visit.</p>
      </header>
      <div class="stages">
        {stage('Before the Build', s['before'])}
        {stage('The Build', s['build'])}
        {stage('Handover', [('Final inspection', '1 wk'), ('Walkthrough and punch list', '1 wk')])}
      </div>
      <p class="stages__total" data-reveal><b>{s['result']}</b><span>About {s['total']} from first visit, design and permits included</span></p>
    </div>
  </section>

  <section class="section deco deco--view" id="areas" aria-labelledby="areas-title">
    <div class="wrap">
      <header class="section__head section__head--inline" data-reveal>
        <span class="pill">{ico('pin')}Service Area</span>
        <h2 class="h2" id="areas-title">Where We Work</h2>
        <p class="section__intro section__intro--line">24 neighborhoods across Los Angeles County.</p>
      </header>
      <ul class="cities" data-reveal>{cities}</ul>
    </div>
  </section>

  <section class="section section--card" id="related" aria-labelledby="related-title">
    <div class="wrap">
      <header class="section__head" data-reveal>
        <span class="pill">{ico('layers')}More Services</span>
        <h2 class="h2" id="related-title">Related Services</h2>
      </header>
      <ul class="cards cards--related">{related}
      </ul>
    </div>
  </section>

{cta_band(s['project'])}
"""
    page(f"services/{s['slug']}.html", f"{esc(s['name'])} in Los Angeles | Nandco Construction",
         f"{s['line']} Serving 24 Los Angeles neighborhoods. CA Lic. 1044615.", body, active=s["slug"], body_class="page-service")


def estimate_page():
    import subprocess
    # the request form is the homepage's original quote section
    form = between('<section class="quote deco deco--glow" id="quote"', "  </section>", text=QUOTE_SOURCE)
    form = form.replace('<section class="quote deco deco--glow" id="quote"', '<section class="quote quote--page deco deco--glow" id="quote"')
    form = form.replace('<h2 class="h2" id="quote-title">Request an Estimate</h2>', '<h1 class="h2" id="quote-title">Get a Free Estimate</h1>')
    form = form.replace('<span class="pill"><svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg>Get Started</span>', '<span class="pill"><svg class="ico" aria-hidden="true"><use href="#i-arrow"/></svg>Free Estimate</span>')
    form = form.replace("We'll call back to talk it through and book a site visit.", "We'll call back to talk it through and book a free site visit.")
    form = form.replace('src="assets/img/office-sign.jpg" width="540" height="270"', 'src="assets/img/team.jpg" width="875" height="520"')
    form = form.replace("Request an Estimate <svg", "Get My Free Estimate <svg")
    steps = f"""
  <section class="section" id="next" aria-labelledby="next-title">
    <div class="wrap">
      <header class="section__head" data-reveal>
        <span class="pill">{ico('clipboard')}What Happens Next</span>
        <h2 class="h2" id="next-title">From Request to Estimate</h2>
      </header>
      <ol class="next-steps">
        <li data-reveal>{ico('phone', 'ico ico--tile')}<h3 class="h3">We call you back</h3><p>We talk through the project and book a time to visit.</p></li>
        <li data-reveal>{ico('home', 'ico ico--tile')}<h3 class="h3">We visit the site</h3><p>We walk the property with you, measure, and look at the structure and systems.</p></li>
        <li data-reveal>{ico('clipboard', 'ico ico--tile')}<h3 class="h3">You get a written estimate</h3><p>A line-item estimate with no hidden markups and no vague allowances, yours to keep with no obligation.</p></li>
      </ol>
    </div>
  </section>"""
    body = "\n  " + form + "\n" + steps + "\n"
    # this page has no hero; the phone dock stays hidden
    page("estimate.html", "Get a Free Estimate | Nandco Construction",
         f"Request a free on-site estimate from Nandco Construction. Call {PHONE} or send the form.", body)


def legal_nav():
    for name in ("privacy.html", "terms.html"):
        p = SITE / name
        html = p.read_text()
        a = html.index('<nav class="bar__nav"')
        b = html.index("</nav>", a) + len("</nav>")
        nav = between('<nav class="bar__nav"', "</nav>", text=HEADER)
        html = html[:a] + nav + html[b:]
        html = html.replace('href="index.html#quote"', 'href="estimate.html"').replace("Request an Estimate", "Get a Free Estimate")
        if 'id="i-down"' not in html:
            html = html.replace("</defs>", '    <symbol id="i-down" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>\n  </defs>', 1)
        p.write_text(html)


QUOTE_SOURCE = (SITE.parent / "tools" / "quote_section.html").read_text()

if __name__ == "__main__":
    if 'id="i-check"' not in SPRITE:
        SPRITE = SPRITE.replace("</defs>", '    <symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>\n  </defs>')
    for s in SERVICES:
        service_page(s)
    estimate_page()
    legal_nav()
    print("built", len(SERVICES), "service pages, estimate.html, and updated legal page headers")
