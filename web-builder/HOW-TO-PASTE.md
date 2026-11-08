# Pasting the Advanced Imaging site into a web builder

## Files
| File | Where it goes |
|---|---|
| `styles.css` | Site-wide **Custom CSS** (Squarespace: Design → Custom CSS; WordPress: Appearance → Customize → Additional CSS; Webflow: Site settings → Custom code → Head, wrapped in `<style>…</style>`) |
| `script.js` | Site-wide **footer code injection**, wrapped in `<script>…</script>` |
| `html/home.html`, `html/services.html`, `html/about.html`, `html/faq.html`, `html/contact.html` | One **Custom HTML / Code block** on each matching page |
| `all-in-one/*.html` | Use **instead of the three above** if your builder's HTML embed runs in its own frame (Wix "Embed HTML", some GoDaddy/Weebly embeds). Each file already contains the CSS, HTML and JS for that page. |

## Steps
1. Create five pages in your builder with these URLs: `/` (Home), `/services`, `/about`, `/faq`, `/contact`.
2. Paste `styles.css` and `script.js` into the site-wide settings above.
3. On each page, add one Custom HTML/Code block and paste in that page's file from `html/`.
4. Hide the builder's own header and footer on these pages. Each block already includes the Advanced Imaging menu and footer.
5. Copy the **SEO title** and **SEO description** from the comment at the top of each HTML file into that page's SEO settings.

## Good to know
- Images (logo and photo) are embedded directly in the HTML, so there's nothing to upload. Any images you upload to the builder later can replace them.
- If your page URLs differ, edit `ROUTES` in `export_builder.py` and run `python3 build.py && python3 export_builder.py`, or find-and-replace the `href="/…"` links.
- The CSS sets base fonts and colors on `body`, headings and links, so it can restyle the builder's own elements on the same site.
- The consultation form opens the visitor's email app until you connect a form service. Set its URL as `data-endpoint` on the `<form id="consult-form">` tag. Also replace the placeholder phone, email and domain.
