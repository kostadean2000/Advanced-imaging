#!/usr/bin/env python3
"""Builds the static Advanced Imaging site.

Shared header, footer and SEO tags live here so every page stays consistent.
Edit the SITE settings below, then run:  python3 build.py
Page bodies live in pages/*.html; generated pages are written to the repo root.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent

# ---- Site settings: update these before going live ----------------------
SITE = {
    "name": "Advanced Imaging",
    "tagline": "Advanced Imaging. Better Answers.",
    "url": "https://www.your-domain.com",       # TODO: live domain, no trailing slash
    "email": "info@your-domain.com",            # TODO: lead inbox
    "phone": "(555) 555-0100",                  # TODO: business phone
    "phone_href": "+15555550100",               # TODO: same number, digits only
    "region": "United States",                  # TODO: service area
    "linkedin": "https://www.linkedin.com/in/dean-kefalas",
    "owner": "Dean Kefalas",
    # Optional: form service URL (Formspree, HubSpot, etc.). Empty = mailto fallback.
    "form_endpoint": "",
}

PAGES = [
    # slug, file, nav label, title tag, meta description
    ("index", "index.html", "Home",
     "Nuclear Medicine, SPECT/CT & PET/CT Solutions | Advanced Imaging",
     "Advanced Imaging helps hospitals and imaging clinics plan, acquire and optimize Nuclear Medicine, SPECT/CT and PET/CT systems. Book a free consultation today."),
    ("services", "services.html", "Services",
     "SPECT/CT, PET/CT & Nuclear Medicine Equipment Services | Advanced Imaging",
     "Equipment planning, acquisition, upgrades, site readiness and workflow optimization for SPECT/CT, PET/CT and gamma camera programs. Free consultation."),
    ("meet-dean", "meet-dean.html", "Meet Dean",
     "Dean Kefalas, CNMT, ARRT(N) | Nuclear Medicine Technologist | Advanced Imaging",
     "Meet Dean Kefalas, CNMT, ARRT(N): Loma Linda University Nuclear Medicine Technology graduate and 2026 Highest Academic Achievement Award recipient."),
    ("about", "about.html", "About",
     "About Dean Kefalas & Advanced Imaging | Molecular Imaging Expertise",
     "Meet Dean Kefalas and Advanced Imaging, a trusted partner for hospitals and imaging centers building Nuclear Medicine, SPECT/CT and PET/CT programs."),
    ("faq", "faq.html", "FAQ",
     "Nuclear Medicine & PET/CT Equipment FAQ | Advanced Imaging",
     "Answers to common questions from hospitals and imaging clinics about SPECT/CT and PET/CT acquisition, upgrades, site planning, timelines and consultations."),
    ("contact", "contact.html", "Free Consultation",
     "Book a Free Imaging Consultation | Advanced Imaging",
     "Schedule a free, no-obligation consultation on your Nuclear Medicine, SPECT/CT or PET/CT program. Hospitals and imaging clinics: talk to Advanced Imaging today."),
]


def header(active):
    items = []
    for slug, file, label, *_ in PAGES:
        if slug == "contact":
            continue
        cur = ' aria-current="page"' if slug == active else ""
        items.append(f'<li><a href="{file}"{cur}>{label}</a></li>')
    items.append('<li><a class="btn btn-cta" href="contact.html">Free Consultation</a></li>')
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Advanced Imaging home">
      <img src="assets/img/logo-icon.png" alt="Advanced Imaging logo: SPECT/CT and PET/CT scanner" width="62" height="46">
      <span class="brand-text"><span class="brand-name">Advanced Imaging</span><span class="brand-tag">Better Answers</span></span>
    </a>
    <button class="nav-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
        {chr(10).join('        ' + i for i in items).strip()}
      </ul>
    </nav>
  </div>
</header>"""


def footer(active=""):
    s = SITE
    sticky = "" if active == "contact" else '<div class="mobile-cta"><a class="btn btn-cta" href="contact.html">Book a Free Consultation</a></div>'
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <p class="footer-brand">Advanced Imaging</p>
        <p>Nuclear Medicine, SPECT/CT and PET/CT solutions for hospitals and imaging clinics.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
          <li><a href="services.html#spect-ct">SPECT/CT Systems</a></li>
          <li><a href="services.html#pet-ct">PET/CT Systems</a></li>
          <li><a href="services.html#nuclear-medicine">Nuclear Medicine</a></li>
          <li><a href="services.html#planning">Planning &amp; Acquisition</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="meet-dean.html">Meet Dean</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="contact.html">Free Consultation</a></li>
          <li><a href="{s['linkedin']}" rel="noopener" target="_blank">LinkedIn</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{s['phone_href']}">{s['phone']}</a></li>
          <li><a href="mailto:{s['email']}">{s['email']}</a></li>
          <li>Serving hospitals &amp; imaging centers across the {s['region']}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> Advanced Imaging. All rights reserved.</span>
      <span>Advanced Imaging. Better Answers.</span>
    </div>
  </div>
</footer>
{sticky}
<script src="assets/js/main.js" defer></script>"""


def org_schema():
    s = SITE
    return {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": s["name"],
        "slogan": s["tagline"],
        "url": s["url"] + "/",
        "logo": s["url"] + "/assets/img/logo-original.png",
        "image": s["url"] + "/assets/img/logo-original.png",
        "email": s["email"],
        "telephone": s["phone_href"],
        "areaServed": s["region"],
        "description": "Nuclear Medicine, SPECT/CT and PET/CT equipment planning, acquisition and optimization for hospitals and imaging clinics.",
        "founder": {"@type": "Person", "name": s["owner"], "sameAs": [s["linkedin"]]},
        "sameAs": [s["linkedin"]],
        "knowsAbout": ["Nuclear Medicine", "SPECT/CT", "PET/CT", "Molecular Imaging", "Gamma Cameras", "Medical Imaging Equipment"],
    }


def render(slug, file, label, title, desc):
    body = (ROOT / "pages" / file).read_text()
    for k, v in SITE.items():
        body = body.replace("{{" + k + "}}", v)
    canonical = SITE["url"] + "/" + ("" if file == "index.html" else file)
    schemas = [org_schema()]
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
        schemas.append(json.loads(extra.read_text().replace("{{url}}", SITE["url"])))
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas
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
<meta property="og:site_name" content="Advanced Imaging">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['url']}/assets/img/logo-original.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#05355f">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
{ld}
</head>
<body>
{header(slug)}
<main id="main">
{body.strip()}
</main>
{footer(slug)}
</body>
</html>
"""


def main():
    for page in PAGES:
        (ROOT / page[1]).write_text(render(*page))
    urls = "\n".join(
        f"  <url><loc>{SITE['url']}/{'' if p[1] == 'index.html' else p[1]}</loc>"
        f"<priority>{'1.0' if p[0] in ('index', 'contact') else '0.8'}</priority></url>"
        for p in PAGES
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    )
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    print("Built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
