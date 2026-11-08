# Advanced Imaging on GoHighLevel

Easiest: open `copy-paste.html` in a browser and use the **Copy** buttons. Or copy from the numbered files:

| # | File | Paste into GoHighLevel |
|---|---|---|
| 1 | `1-custom-css.css` | Sites → your website/funnel → **Settings → Custom CSS** (raw CSS, no `<style>` tags) |
| 2 | `2-footer-tracking-code.html` | **Settings → Tracking Code → Footer Code** (includes `<script>` tags) |
| 3 | `3-home.html` | Home page (path `/`): **Custom JS/HTML** element |
| 4 | `4-services.html` | `/services` page: **Custom JS/HTML** element |
| 5 | `5-about.html` | `/about` page: **Custom JS/HTML** element |
| 6 | `6-faq.html` | `/faq` page: **Custom JS/HTML** element |
| 7 | `7-contact.html` | `/contact` page: **Custom JS/HTML** element |

## Page setup
1. Create the 5 pages with the paths above. If you use different paths, find-and-replace the `href="/…"` links in the blocks.
2. On each page, add one **full-width** section and set the section, row and column padding to 0. Add a **Custom JS/HTML** element and paste that page's block.
3. Don't add GoHighLevel's own header or footer. Each block already includes the Advanced Imaging menu and footer.
4. Copy the SEO title and description from the comment at the top of each block into the page's **SEO Meta Data** settings.

## Notes
- The CSS only applies inside the pasted blocks (everything is scoped to `.ai-site`), so it won't restyle other GoHighLevel pages or elements.
- The logo and photo are embedded in the HTML. If a block feels too large for the editor, upload the files in `images/` to the GoHighLevel **Media Library** and replace each long `src="data:image/…"` value with the media URL.
- **Leads into your CRM:** the consultation form opens the visitor's email app by default. To capture leads in GoHighLevel, either:
  - replace the `<form id="consult-form">…</form>` in block 7 with your GoHighLevel form's embed code, or
  - create a Workflow with an **Inbound Webhook** trigger and put its URL in the form's `data-endpoint=""` attribute. The fields are sent as JSON. Submit a test lead to confirm it arrives.
- Replace the placeholder phone, email and domain before going live.
