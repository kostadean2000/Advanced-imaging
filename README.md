# Advanced Imaging website

Static 5-page lead-generation site for Advanced Imaging (Nuclear Medicine, SPECT/CT, PET/CT) aimed at hospitals and imaging clinics.

Pages: `index.html` (Home), `services.html`, `about.html` (Dean's photo, credentials, experience & equipment), `faq.html`, `contact.html` (free consultation form).

## Editing
- Page content lives in `pages/*.html`. Shared header, footer, meta tags and structured data live in `build.py`.
- Set the live domain, phone, email and service area in the `SITE` block of `build.py`, then run `python3 build.py`.
- Add Dean's LinkedIn background to `pages/about.html` (marked with a TODO comment).
- Consultation form: set `form_endpoint` in `build.py` to a form service URL (Formspree, HubSpot, Netlify Forms…) to receive submissions in an inbox. Without it, the form opens the visitor's email app pre-filled.

## SEO
One H1 per page with keyword-focused H2s, unique titles and meta descriptions, canonical and Open Graph tags, JSON-LD (ProfessionalService, BreadcrumbList, FAQPage), `sitemap.xml` and `robots.txt`.

Deploy by uploading the repo root to any static host (GitHub Pages, Netlify, etc.).
