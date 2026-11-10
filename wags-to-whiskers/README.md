# Wags to Whiskers website

Static 5-page lead-generation site for Wags to Whiskers, a dog and cat grooming salon, aimed at local pet owners. Every page drives visitors to a **free grooming consultation**.

Pages: `index.html` (Home), `services.html`, `about.html`, `faq.html`, `contact.html` (free consultation booking form).

## Before going live
1. Open `build.py` and replace every `TODO` in the `SITE` block: domain, phone, email, street address, city, state, ZIP and hours.
2. Search `pages/*.html` for `TODO` comments and add real details: the owner's story, groomer names and photos, real customer reviews, and the satisfaction policy wording.
3. Run `python3 build.py` to regenerate the five pages, `sitemap.xml` and `robots.txt`.

## Booking form
Set `form_endpoint` in `build.py` to a form service or CRM webhook (Formspree, GoHighLevel, HubSpot…) to receive requests as JSON. Left empty, the form opens the visitor's email app pre-filled with the request.

## SEO
- One keyword-focused H1 per page, descriptive H2s for each section
- Unique `<title>` (under 60 characters) and meta description per page, with the city filled in from `SITE`
- Canonical and Open Graph tags
- JSON-LD: LocalBusiness (address, hours, free-consultation offer), BreadcrumbList, FAQPage
- `sitemap.xml` and `robots.txt`

Homepage calls to action: hero buttons (book + call), the hero card's "Claim My Free Consultation", "Schedule a Free Meet & Greet", "Start With Step One", and the closing CTA band. The header and the sticky mobile bar also link to booking.

Deploy by uploading this folder to any static host (Netlify, GitHub Pages, etc.).
