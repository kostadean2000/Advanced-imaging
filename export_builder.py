#!/usr/bin/env python3
"""Exports the site as copy-and-paste blocks for website builders.

Writes web-builder/:
  styles.css          paste into the builder's site-wide custom CSS
  script.js           paste into the site-wide footer code / custom JS
  html/<page>.html    one custom HTML block per page (header, content, footer)
  all-in-one/<page>.html  CSS + HTML + JS in a single block, for builders
                      whose HTML embeds run in an isolated frame (e.g. Wix)

  gohighlevel/        GoHighLevel version: scoped CSS for Settings > Custom CSS,
                      JS for the footer tracking code, one Custom Code block per
                      page, image files, and copy-paste.html with Copy buttons

Run after build.py:  python3 export_builder.py
"""
import base64
import json
import pathlib
import re

import build

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "web-builder"

# Page URLs inside the web builder. Change these to match your builder's page URLs.
ROUTES = {
    "index.html": "/",
    "services.html": "/services",
    "about.html": "/about",
    "faq.html": "/faq",
    "contact.html": "/contact",
}

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp"}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800'
         '&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">')


def data_uri(path):
    p = ROOT / path
    return f"data:{MIME[p.suffix]};base64," + base64.b64encode(p.read_bytes()).decode()


def adapt(html):
    # Internal links -> builder routes (keeps #anchors)
    def link(m):
        page, anchor = m.group(1), m.group(2) or ""
        return f'href="{ROUTES.get(page, page)}{anchor}"'
    html = re.sub(r'href="([a-z-]+\.html)(#[^"]*)?"', link, html)
    # Use the smaller WebP photo only (supported by all current browsers)
    html = re.sub(r'\s*<source srcset="assets/img/dean-kefalas\.webp" type="image/webp">', "", html)
    html = html.replace("assets/img/dean-kefalas.jpg", "assets/img/dean-kefalas.webp")
    # Local images -> embedded data URIs
    html = re.sub(r'(src|srcset)="(assets/img/[^"]+)"', lambda m: f'{m.group(1)}="{data_uri(m.group(2))}"', html)
    # JS is delivered separately
    html = html.replace('<script src="assets/js/main.js" defer></script>', "")
    return html.strip()


def page_block(slug, file, label, title, desc):
    body = (ROOT / "pages" / file).read_text()
    for k, v in build.SITE.items():
        body = body.replace("{{" + k + "}}", v)
    schemas = [build.org_schema()]
    extra = ROOT / "pages" / (slug + ".schema.json")
    if extra.exists():
        schemas.append(json.loads(extra.read_text().replace("{{url}}", build.SITE["url"])))
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    html = (f"<!-- Advanced Imaging | {label} page | custom HTML block -->\n"
            f"<!-- SEO title: {title} -->\n<!-- SEO description: {desc} -->\n"
            f"{FONTS}\n{ld}\n<div class=\"ai-site\">\n{build.header(slug)}\n<main id=\"main\">\n{body.strip()}\n</main>\n{build.footer(slug)}\n</div>")
    return adapt(html)


SCOPE = ".ai-site"


def scope_selector(sel):
    sel = sel.strip()
    if sel in (":root", "html") or sel.startswith("@"):
        return sel
    if sel == "body":
        return SCOPE
    if sel in ("*", "*::before", "*::after"):
        return f"{SCOPE}{sel[1:]}, {SCOPE} {sel}" if sel != "*" else f"{SCOPE}, {SCOPE} *"
    return f"{SCOPE} {sel}"


def scope_css(css):
    """Prefix every selector with .ai-site so the styles only affect the pasted
    blocks, not the builder's own page elements. Handles flat rules and @media."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0

    def rules(block):
        res = []
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", block):
            sels = ", ".join(scope_selector(x) for x in m.group(1).split(","))
            res.append(f"{sels} {{{m.group(2).rstrip()} }}")
        return res

    while i < len(css):
        at = css.find("@media", i)
        if at == -1:
            out += rules(css[i:]); break
        out += rules(css[i:at])
        open_ = css.index("{", at)
        depth, j = 1, open_ + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[j], 0); j += 1
        inner = rules(css[open_ + 1:j - 1])
        out.append(css[at:open_].strip() + " {\n  " + "\n  ".join(inner) + "\n}")
        i = j
    return "\n".join(out) + "\n"


GHL_STEPS = [
    ("css", "1. Custom CSS", "Paste into Sites → (your website or funnel) → Settings → Custom CSS. Raw CSS, no &lt;style&gt; tags needed."),
    ("js", "2. Footer tracking code", "Paste into Settings → Tracking Code → Footer. Includes the &lt;script&gt; tags."),
]


def export_ghl(css, js, blocks):
    g = OUT / "gohighlevel"
    (g / "images").mkdir(parents=True, exist_ok=True)
    for img in ("logo-icon.png", "dean-kefalas.webp", "dean-kefalas.jpg"):
        (g / "images" / img).write_bytes((ROOT / "assets/img" / img).read_bytes())
    scoped = scope_css(css)
    footer_js = f"<script>\n{js.strip()}\n</script>\n"
    (g / "1-custom-css.css").write_text(scoped)
    (g / "2-footer-tracking-code.html").write_text(footer_js)
    for n, (name, label, title, desc, block) in enumerate(blocks, start=3):
        (g / f"{n}-{name}").write_text(block + "\n")
    # Copy-paste helper page
    import html as h
    items = [("css", "1. Custom CSS", "Sites → your website/funnel → <b>Settings → Custom CSS</b>. Paste as-is.", scoped),
             ("js", "2. Footer tracking code", "<b>Settings → Tracking Code → Footer Code</b>. Paste as-is (includes the script tags).", footer_js)]
    for n, (name, label, title, desc, block) in enumerate(blocks, start=3):
        items.append((name.replace(".html", ""), f"{n}. {label} page: Custom Code block",
                      f"Page path <code>{ROUTES[name if name != 'home.html' else 'index.html']}</code>. Add a full-width section with 0 padding, drop in a <b>Custom JS/HTML</b> (Code) element, paste. "
                      f"SEO title: <i>{h.escape(title)}</i>", block))
    cards = "\n".join(
        f"""<section class="item"><div class="head"><div><h2>{label}</h2><p>{where}</p></div>
<button type="button" data-target="t-{key}">Copy</button></div>
<textarea id="t-{key}" readonly spellcheck="false">{h.escape(code)}</textarea>
<p class="size">{len(code.encode())//1024} KB</p></section>""" for key, label, where, code in items)
    (g / "copy-paste.html").write_text(COPY_PAGE.replace("{{cards}}", cards))


def main():
    (OUT / "html").mkdir(parents=True, exist_ok=True)
    (OUT / "all-in-one").mkdir(parents=True, exist_ok=True)
    css = (ROOT / "assets/css/styles.css").read_text()
    js = (ROOT / "assets/js/main.js").read_text()
    (OUT / "styles.css").write_text(css)
    (OUT / "script.js").write_text(js)
    blocks = []
    for page in build.PAGES:
        slug, file = page[0], page[1]
        block = page_block(*page)
        name = "home.html" if slug == "index" else file
        (OUT / "html" / name).write_text(block + "\n")
        (OUT / "all-in-one" / name).write_text(f"<style>\n{css}\n</style>\n{block}\n<script>\n{js}\n</script>\n")
        blocks.append((name, page[2] if slug != "contact" else "Free Consultation", page[3], page[4], block))
    export_ghl(css, js, blocks)
    print("Exported", len(build.PAGES), "pages to", OUT)


COPY_PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GoHighLevel Copy Blocks</title>
<style>
:root { --navy:#05355f; --accent:#1c9cc4; --cta:#e8772e; --ink:#1b2733; --muted:#5a6b7b; --line:#dde5ec; --bg:#f4f7fa; --card:#fff; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --navy:#8fc3ec; --ink:#e3eaf1; --muted:#9fb0c0; --line:#2b3a48; --bg:#0f1720; --card:#16212c; } }
:root[data-theme="dark"] { --navy:#8fc3ec; --ink:#e3eaf1; --muted:#9fb0c0; --line:#2b3a48; --bg:#0f1720; --card:#16212c; }
* { box-sizing:border-box; }
body { margin:0; font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; color:var(--ink); background:var(--bg); }
main { max-width:960px; margin:0 auto; padding:32px 16px 60px; }
h1 { color:var(--navy); margin:0 0 6px; font-size:1.7rem; }
.intro { color:var(--muted); margin:0 0 24px; }
.item { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px; margin-bottom:18px; }
.head { display:flex; justify-content:space-between; gap:16px; align-items:flex-start; }
h2 { font-size:1.1rem; color:var(--navy); margin:0 0 4px; }
.head p { margin:0; color:var(--muted); font-size:.93rem; }
button { flex:none; background:var(--cta); color:#fff; border:0; border-radius:8px; padding:10px 22px; font-weight:700; font-size:1rem; cursor:pointer; min-width:110px; }
button.done { background:#2e8b57; }
textarea { width:100%; height:130px; margin-top:12px; font:12px/1.4 ui-monospace,Menlo,Consolas,monospace; color:var(--ink); background:var(--bg); border:1px solid var(--line); border-radius:8px; padding:10px; resize:vertical; }
.size { margin:6px 0 0; font-size:.8rem; color:var(--muted); }
ol { padding-left:20px; color:var(--ink); } li { margin-bottom:4px; }
.box { background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); border-radius:8px; padding:14px 18px; margin-bottom:24px; }
@media (max-width:600px) { .head { flex-direction:column; } button { width:100%; } }
</style></head>
<body><main>
<h1>Advanced Imaging: GoHighLevel Copy Blocks</h1>
<p class="intro">Click <b>Copy</b>, then paste into the GoHighLevel spot named on each block.</p>
<div class="box"><b>Setup order</b><ol>
<li>Create 5 pages in your GoHighLevel website with paths <code>/</code> (Home), <code>/services</code>, <code>/about</code>, <code>/faq</code>, <code>/contact</code>.</li>
<li>Paste block 1 (CSS) and block 2 (footer code) once, in the website's Settings.</li>
<li>On each page: add a full-width section, set section/row/column padding to 0, add a <b>Custom JS/HTML</b> element, and paste that page's block.</li>
<li>Copy each page's SEO title and description (top of each block) into that page's SEO settings.</li>
</ol></div>
{{cards}}
</main>
<script>
document.addEventListener('click', function (e) {
  var b = e.target.closest('button[data-target]'); if (!b) return;
  var t = document.getElementById(b.dataset.target);
  function ok() { b.textContent = 'Copied!'; b.classList.add('done'); setTimeout(function () { b.textContent = 'Copy'; b.classList.remove('done'); }, 1800); }
  function fallback() { t.focus(); t.select(); try { document.execCommand('copy'); ok(); } catch (err) { b.textContent = 'Press Ctrl/Cmd+C'; } }
  if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(t.value).then(ok, fallback); else fallback();
});
</script>
</body></html>
"""


if __name__ == "__main__":
    main()
