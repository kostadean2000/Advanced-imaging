#!/usr/bin/env python3
"""Builds the static Wags to Whiskers pet grooming site.

Shared header, footer, SEO tags and structured data live here.
Edit SITE below, then run:  python3 build.py
Page bodies live in pages/*.html; generated pages are written next to this file.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent

# ---- Site settings (from wagsgrooming.com) ----------------------------------
SITE = {
    "name": "Wags to Whiskers",
    "tagline": "Because We Love Pets",
    "url": "https://www.wagsgrooming.com",
    "email": "eric@wagsgrooming.com",
    "phone": "(562) 430-5161",
    "phone_href": "+15624305161",
    "street": "5505 E Stearns St",
    "location_note": "Los Altos Shopping Center, plenty of free parking",
    "city": "Long Beach",
    "state": "CA",
    "zip": "90815",
    "hours": "Tue&ndash;Sat 8:00am&ndash;5:00pm",
    "hours_schema": ["Tu-Sa 08:00-17:00"],
    # Optional: form service / CRM webhook URL (Formspree, GoHighLevel, etc.).
    # Empty = the forms open the visitor's email app pre-filled.
    "form_endpoint": "",
}

PAGES = [
    # slug, file, nav label, title tag (<60 chars), meta description (<160 chars)
    ("index", "index.html", "Home",
     "Dog & Cat Grooming in {city} | Wags to Whiskers",
     "Wags to Whiskers offers gentle, professional dog and cat grooming in {city}. Baths, haircuts, nail trims and spa care. Book your free grooming consultation."),
    ("services", "services.html", "Services",
     "Dog & Cat Grooming Services | Wags to Whiskers",
     "Full grooming, bath & tidy, puppy and kitten intros, cat grooming, nail trims, teeth brushing and de-shedding in {city}. Free consultation for new clients."),
    ("about", "about.html", "About",
     "About Our Pet Groomers | Wags to Whiskers {city}",
     "Meet the caring, experienced groomers at Wags to Whiskers. Fear-free handling, safe products and a calm salon for dogs and cats in {city}."),
    ("faq", "faq.html", "FAQ",
     "Pet Grooming FAQ: Prices, Timing & Care | Wags to Whiskers",
     "Answers to common pet grooming questions: how often to groom, pricing, vaccinations, anxious pets, matted coats and what happens at your free consultation."),
    ("contact", "contact.html", "Book Now",
     "Book a Free Pet Grooming Consultation | Wags to Whiskers",
     "Book your free, no-obligation grooming consultation for your dog or cat in {city}. Meet your groomer, get a custom plan and an exact quote. Request a time today."),
]


# Stand-alone ad / campaign landing page: own header (no menu), same footer and styles.
LANDING = ("landing", "landing.html", "Book an Appointment",
           "Pet Grooming in Long Beach, CA | Book an Appointment",
           "Voted Long Beach's best groomer seven times. Dog & cat grooming at Los Altos, Tue-Sat 8-5. Book your Wags to Whiskers grooming appointment today.")


def fill(text):
    for k, v in SITE.items():
        if isinstance(v, str):
            text = text.replace("{{" + k + "}}", v).replace("{" + k + "}", v)
    return text


def landing_header():
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Wags to Whiskers home">
      <img src="assets/img/logo.svg" alt="Wags to Whiskers paw print logo" width="48" height="48">
      <span class="brand-text"><span class="brand-name">Wags to Whiskers</span><span class="brand-tag">Pet Grooming</span></span>
    </a>
    <div class="header-actions">
      <a class="header-phone" href="tel:{SITE['phone_href']}">{SITE['phone']}</a>
      <a class="btn btn-cta" href="#book">Book Appointment</a>
    </div>
  </div>
</header>"""


def header(active):
    items = []
    for slug, file, label, *_ in PAGES:
        if slug == "contact":
            continue
        cur = ' aria-current="page"' if slug == active else ""
        items.append(f'<li><a href="{file}"{cur}>{label}</a></li>')
    items.append('<li><a class="btn btn-cta" href="contact.html">Free Consultation</a></li>')
    nav = "\n        ".join(items)
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="container topbar-inner">
  <span>{SITE['hours']}</span>
  <a href="tel:{SITE['phone_href']}">Call {SITE['phone']}</a>
</div></div>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Wags to Whiskers home">
      <img src="assets/img/logo.svg" alt="Wags to Whiskers paw print logo" width="48" height="48">
      <span class="brand-text"><span class="brand-name">Wags to Whiskers</span><span class="brand-tag">Pet Grooming</span></span>
    </a>
    <button class="nav-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
        {nav}
      </ul>
    </nav>
  </div>
</header>"""


def footer(active):
    s = SITE
    if active == "landing":
        blurb = f"Gentle, professional dog and cat grooming in {s['city']}. Voted best groomer in Long Beach seven times."
        book_link = '<a href="#book">Book Appointment</a>'
    else:
        blurb = f"Gentle, professional dog and cat grooming in {s['city']}. Every visit starts with a free consultation."
        book_link = '<a href="contact.html">Book a Free Consultation</a>'
    if active == "contact":
        sticky = ""
    elif active == "landing":
        sticky = '<div class="mobile-cta"><a class="btn btn-cta" href="#book">Book Appointment</a></div>'
    else:
        sticky = '<div class="mobile-cta"><a class="btn btn-cta" href="contact.html">Book a Free Consultation</a></div>'
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <p class="footer-brand">Wags to Whiskers</p>
        <p>{blurb}</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
          <li><a href="services.html#dog-grooming">Dog Grooming</a></li>
          <li><a href="services.html#cat-grooming">Cat Grooming</a></li>
          <li><a href="services.html#puppy">Puppy &amp; Kitten Intro</a></li>
          <li><a href="services.html#add-ons">Spa Add-Ons</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li>{book_link}</li>
        </ul>
      </div>
      <div>
        <h2>Visit Us</h2>
        <address>
          {s['street']}<br>{s['city']}, {s['state']} {s['zip']}<br>
          <a href="tel:{s['phone_href']}">{s['phone']}</a><br>
          <a href="mailto:{s['email']}">{s['email']}</a><br>
          {s['hours']}
        </address>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Wags to Whiskers. All rights reserved.</span>
      <span>{s['tagline']}</span>
    </div>
  </div>
</footer>
{sticky}
<script src="assets/js/main.js" defer></script>"""


def business_schema():
    s = SITE
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "PetStore"],
        "additionalType": "https://en.wikipedia.org/wiki/Pet_grooming",
        "name": s["name"],
        "slogan": s["tagline"],
        "url": s["url"] + "/",
        "logo": s["url"] + "/assets/img/logo.svg",
        "image": s["url"] + "/assets/img/logo.svg",
        "email": s["email"],
        "telephone": s["phone_href"],
        "priceRange": "$$",
        "areaServed": ["Long Beach, CA", "Orange County, CA"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s["street"],
            "addressLocality": s["city"],
            "addressRegion": s["state"],
            "postalCode": s["zip"],
            "addressCountry": "US",
        },
        "openingHours": s["hours_schema"],
        "description": "Professional dog and cat grooming: full grooms, baths, haircuts, nail trims, de-shedding and spa add-ons, with a free consultation for every new client.",
        "makesOffer": {
            "@type": "Offer",
            "name": "Free Pet Grooming Consultation",
            "price": "0",
            "priceCurrency": "USD",
            "url": s["url"] + "/contact.html",
        },
    }


def render(slug, file, label, title, desc):
    title, desc = fill(title), fill(desc)
    body = fill((ROOT / "pages" / file).read_text())
    canonical = SITE["url"] + "/" + ("" if file == "index.html" else file)
    schemas = [business_schema()]
    if slug != "index":
        schemas.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["url"] + "/"},
                {"@type": "ListItem", "position": 2, "name": label, "item": canonical},
            ],
        })
    extra = ROOT / "pages" / (slug + ".schema.json")
    if extra.exists():
        schemas.append(json.loads(fill(extra.read_text())))
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in schemas
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wags to Whiskers">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['url']}/assets/img/{'hero-dog-grooming.webp' if slug == 'landing' else 'logo.svg'}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0f6e6e">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
{ld}
</head>
<body>
{landing_header() if slug == "landing" else header(slug)}
<main id="main">
{body.strip()}
</main>
{footer(slug)}
</body>
</html>
"""


def main():
    for page in PAGES + [LANDING]:
        (ROOT / page[1]).write_text(render(*page))
    urls = "\n".join(
        f"  <url><loc>{SITE['url']}/{'' if p[1] == 'index.html' else p[1]}</loc>"
        f"<priority>{'1.0' if p[0] in ('index', 'contact') else '0.8'}</priority></url>"
        for p in PAGES + [LANDING]
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    )
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    print("Built", len(PAGES) + 1, "pages")


if __name__ == "__main__":
    main()
