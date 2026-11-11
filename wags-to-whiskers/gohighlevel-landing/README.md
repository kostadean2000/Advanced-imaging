# Wags to Whiskers landing page: GoHighLevel copy & paste

Open `copy-paste.html` in a browser for every block with a **Copy** button, or copy from the files below.

| Step | File | Where it goes in GoHighLevel |
|---|---|---|
| 1 | `1-custom-css.css` | Landing page **Settings → Custom CSS**. Paste as-is, without `<style>` tags. |
| 2 | `2-custom-html.html` | Add a full-width section (0 padding) with one full-width column, then drag in a **Custom JS/HTML** element → **Open Code Editor** → paste. |
| 3 | `3-custom-js.html` | Page **Settings → Tracking Code → Footer Code**. Paste as-is, `<script>` tags included. |

Then:
- **SEO:** copy the title and description from the comment at the top of `2-custom-html.html` into page Settings → SEO Meta Data.
- **Hide** the funnel's default header and footer. The block has its own.
- **Leads:** to capture bookings in GoHighLevel, create a workflow with an **Inbound Webhook** trigger and paste its URL into `data-endpoint=""` on `<form id="booking-form">` in block 2. Until then the form opens the visitor's email app addressed to the salon.
- **Footer links** go to `/services`, `/about` and `/faq`. Edit `ROUTES` in `export_ghl.py`, or the links in block 2, if your paths differ.

The CSS is scoped to `.wtw-lp`, so it won't restyle the rest of your GoHighLevel site. Photos load from Unsplash's image CDN, so there's nothing to upload.

Regenerate after editing the site: `python3 build.py && python3 export_ghl.py`
