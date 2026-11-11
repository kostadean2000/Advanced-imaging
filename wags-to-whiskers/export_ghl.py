#!/usr/bin/env python3
"""Exports the Wags to Whiskers landing page as three GoHighLevel copy-paste blocks.

Writes gohighlevel-landing/:
  1-custom-css.css     paste into the funnel/website page: Settings > Custom CSS
  2-custom-html.html   paste into one Custom JS/HTML (Code) element on the page
  3-custom-js.html     paste into the page's Settings > Tracking Code > Footer
  copy-paste.html      open in a browser: every block with a Copy button
  README.md            step-by-step instructions

Run after build.py:  python3 build.py && python3 export_ghl.py
"""
import base64
import html as h
import json
import pathlib
import re

import build

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "gohighlevel-landing"
SCOPE = ".wtw-lp"

# Where the footer links point inside GoHighLevel. Change to match your page paths,
# or point them at full URLs (e.g. "https://www.wagsgrooming.com/services").
ROUTES = {
    "index.html": "/",
    "services.html": "/services",
    "about.html": "/about",
    "faq.html": "/faq",
    "contact.html": "/contact",
}

# Photos load from Unsplash's image CDN (free under the Unsplash License), so there's
# nothing to upload. To use your own, upload to GoHighLevel Media and swap the URLs.
PHOTOS = {
    "hero-dog-grooming.webp": "1516734212186-a967f81ad0d7",
    "dogs-running.webp": "1548199973-03cce0bbc87b",
    "cat-tabby.webp": "1574158622682-e40e69881006",
    "dog-beagle.webp": "1543466835-00a7907e9de1",
    "puppy-corgi.webp": "1537151625747-768eb6cf92b2",
    "cat-window.webp": "1514888286974-6c03e2ca1dba",
    "dog-pug.webp": "1517849845537-4d257902454a",
}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
         '&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">')


def photo_url(name):
    w = 1600 if name in ("hero-dog-grooming.webp", "dogs-running.webp", "cat-window.webp") else 900
    return f"https://images.unsplash.com/photo-{PHOTOS[name]}?w={w}&q=70&auto=format&fit=crop"


def logo_uri():
    return "data:image/svg+xml;base64," + base64.b64encode((ROOT / "assets/img/logo.svg").read_bytes()).decode()


# ---- CSS -----------------------------------------------------------------------
def scope_selector(sel):
    sel = sel.strip()
    if sel == "html" or sel.startswith("@"):
        return sel
    if sel in (":root", "body"):
        return SCOPE
    if sel == "*":
        return f"{SCOPE}, {SCOPE} *"
    return f"{SCOPE} {sel}"


def scope_css(css):
    """Prefix every selector with .wtw-lp so the styles only touch the pasted block,
    never GoHighLevel's own elements. Handles flat rules and @media blocks."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0

    def rules(block):
        res = []
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", block):
            sels = ", ".join(scope_selector(x) for x in m.group(1).split(","))
            res.append(f"{sels} {{ {m.group(2).strip()} }}")
        return res

    while i < len(css):
        at = css.find("@media", i)
        if at == -1:
            out += rules(css[i:])
            break
        out += rules(css[i:at])
        open_ = css.index("{", at)
        depth, j = 1, open_ + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        out.append(css[at:open_].strip() + " {\n  " + "\n  ".join(rules(css[open_ + 1:j - 1])) + "\n}")
        i = j
    return "\n".join(out) + "\n"


def export_css():
    css = (ROOT / "assets/css/styles.css").read_text()
    # Prefix custom properties so they can't clash with GoHighLevel's own variables
    names = set(re.findall(r"--([a-z-]+)\s*:", css))
    for n in sorted(names, key=len, reverse=True):
        css = re.sub(rf"--{n}\b", f"--wtw-{n}", css)
    css = css.replace("url(../img/logo.svg)", f'url("{logo_uri()}")')
    scoped = scope_css(css)
    reset = (f"/* Wags to Whiskers landing page | GoHighLevel Custom CSS | every rule is scoped to {SCOPE} */\n"
             f"{SCOPE} {{ width:100%; overflow-x:clip; }}\n"
             f"{SCOPE} h1, {SCOPE} h2, {SCOPE} h3 {{ letter-spacing:normal; text-transform:none; }}\n"
             f"{SCOPE} ul {{ margin-top:0; }}\n")
    return reset + scoped


# ---- HTML ----------------------------------------------------------------------
def export_html():
    slug, file, label, title, desc = build.LANDING
    page = build.render(*build.LANDING)
    body = page[page.index("<body>") + 6:page.index("</body>")]
    body = body.replace('<script src="assets/js/main.js" defer></script>', "").strip()
    ld = "\n".join(re.findall(r'<script type="application/ld\+json">.*?</script>', page))

    def link(m):
        return f'href="{ROUTES.get(m.group(1), m.group(1))}{m.group(2) or ""}"'
    body = re.sub(r'href="([a-z-]+\.html)(#[^"]*)?"', link, body)
    body = body.replace('src="assets/img/logo.svg"', f'src="{logo_uri()}"')
    body = re.sub(r'assets/img/([a-z-]+\.webp)', lambda m: photo_url(m.group(1)), body)
    head = (f"<!-- Wags to Whiskers | landing page | GoHighLevel Custom JS/HTML element -->\n"
            f"<!-- SEO title: {build.fill(title)} -->\n<!-- SEO description: {build.fill(desc)} -->\n")
    return f'{head}{FONTS}\n{ld}\n<div class="wtw-lp">\n{body}\n</div>\n'


def export_js():
    js = (ROOT / "assets/js/main.js").read_text().strip()
    return f"<!-- Wags to Whiskers | landing page | Footer tracking code -->\n<script>\n{js}\n</script>\n"


STEPS = [
    ("css", "1-custom-css.css", "Custom CSS",
     "In your funnel or website, open the landing page's <b>Settings</b> (gear icon) and choose <b>Custom CSS</b>. Paste it in as-is. No &lt;style&gt; tags are needed."),
    ("html", "2-custom-html.html", "Custom HTML",
     "In the page editor, add a <b>full-width section</b> with 0 padding, then a full-width row with 1 column. Drag in a <b>Custom JS/HTML</b> element (Elements > Custom JS/HTML), click <b>Open Code Editor</b>, paste and save."),
    ("js", "3-custom-js.html", "Custom JS",
     "Page <b>Settings</b> > <b>Tracking Code</b> > <b>Footer Code</b>. Paste as-is, script tags included. You can also paste it into a second Custom JS/HTML element below the first."),
]


def helper_page(blocks, standalone):
    cards = []
    for n, (key, fname, label, where) in enumerate(STEPS, 1):
        code = blocks[key]
        kb = max(1, round(len(code.encode()) / 1024))
        cards.append(f"""<section class="step" aria-labelledby="h-{key}">
  <div class="step-head">
    <span class="num" aria-hidden="true">{n}</span>
    <div class="step-text"><h2 id="h-{key}">{label} <span class="file">{fname} &middot; {kb} KB</span></h2><p>{where}</p></div>
    <button type="button" class="copy" data-target="t-{key}">Copy {label}</button>
  </div>
  <textarea id="t-{key}" readonly spellcheck="false" aria-label="{label} code">{h.escape(code)}</textarea>
</section>""")
    s = build.SITE
    title = build.fill(build.LANDING[3])
    desc = build.fill(build.LANDING[4])
    doc = f"""{'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' if standalone else ''}
<title>Wags to Whiskers GHL Blocks</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap">
<style>
/* Layout: one narrow column of numbered paste steps, each with its code and a Copy button */
:root{{--bg:#f6faf9;--surface:#ffffff;--fg:#1f2a2e;--muted:#56666a;--line:#d9e4e2;--accent:#0f6e6e;--accent-fg:#ffffff;--sun:#f2a541;--code-bg:#f0f5f4;
  --display:"Fredoka",system-ui,sans-serif;--text:"Nunito",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0f1a1b;--surface:#162426;--fg:#e4eeec;--muted:#9fb3b0;--line:#26393b;--accent:#4fb8ad;--accent-fg:#0b1414;--sun:#f2a541;--code-bg:#0b1415;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f1a1b;--surface:#162426;--fg:#e4eeec;--muted:#9fb3b0;--line:#26393b;--accent:#4fb8ad;--accent-fg:#0b1414;--sun:#f2a541;--code-bg:#0b1415;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 var(--text)}}
.wrap{{max-width:900px;margin:0 auto;padding-block:40px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:20px}}
h1,h2{{font-family:var(--display);font-weight:600;text-wrap:balance;margin:0}}
h1{{font-size:clamp(1.6rem,4vw,2.2rem);color:var(--accent)}}
.intro p{{margin:.4em 0 0;color:var(--muted);max-width:65ch}}
.step,.note{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:20px}}
.step-head{{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start}}
.step-text{{min-width:0}}
.num{{width:34px;height:34px;border-radius:50%;background:var(--sun);color:#1f2a2e;display:grid;place-items:center;font-family:var(--display);font-weight:600}}
h2{{font-size:1.2rem}}
.file{{font:400 .78rem var(--mono);color:var(--muted);margin-left:6px;white-space:nowrap}}
.step-text p{{margin:.3em 0 0;color:var(--muted)}}
.step-text b{{color:var(--fg)}}
.copy{{font:600 .95rem var(--display);background:var(--accent);color:var(--accent-fg);border:0;border-radius:999px;padding:10px 18px;cursor:pointer;white-space:nowrap}}
.copy:focus-visible,textarea:focus-visible{{outline:3px solid var(--sun);outline-offset:2px}}
.copy.done{{background:var(--sun);color:#1f2a2e}}
textarea{{width:100%;height:220px;margin-top:14px;font:12.5px/1.5 var(--mono);color:var(--fg);background:var(--code-bg);border:1px solid var(--line);border-radius:10px;padding:12px;resize:vertical;white-space:pre;overflow:auto}}
.note h2{{font-size:1.05rem;margin-bottom:.4em}}
.note ul{{margin:0;padding-left:1.2em;color:var(--muted);display:grid;gap:6px}}
.note b{{color:var(--fg)}}
code{{font:.88em var(--mono)}}
@media (max-width:600px){{.step-head{{grid-template-columns:auto 1fr}}.copy{{grid-column:1/-1;width:100%}}}}
@media (prefers-reduced-motion:no-preference){{.copy{{transition:background .15s}}}}
</style>
{'</head><body>' if standalone else ''}
<main class="wrap">
  <header class="intro">
    <h1>Wags to Whiskers landing page for GoHighLevel</h1>
    <p>Three blocks: CSS, HTML and JS. Paste them in order, then publish. Photos load from the web, so there's nothing to upload.</p>
  </header>
  {chr(10).join(cards)}
  <section class="note" aria-labelledby="h-after">
    <h2 id="h-after">After pasting</h2>
    <ul>
      <li><b>SEO:</b> in page Settings &gt; SEO Meta Data, set the title to <code>{h.escape(title)}</code> and use this description: <i>{h.escape(desc)}</i></li>
      <li><b>Booking form:</b> requests open the visitor's email app addressed to {h.escape(s['email'])}. To capture leads in GoHighLevel, create a workflow with an <b>Inbound Webhook</b> trigger and paste its URL into <code>data-endpoint=""</code> on the <code>&lt;form id="booking-form"&gt;</code> tag in block 2.</li>
      <li><b>Footer links</b> point to <code>/services</code>, <code>/about</code> and <code>/faq</code>. Change them in block 2 if your page paths differ.</li>
      <li><b>Header:</b> the block has its own header and footer, so hide the funnel's default header and footer on this page if it has them.</li>
    </ul>
  </section>
</main>
<script>
document.addEventListener('click', function (e) {{
  var b = e.target.closest('.copy'); if (!b) return;
  var t = document.getElementById(b.dataset.target), label = b.textContent;
  function ok() {{ b.textContent = 'Copied'; b.classList.add('done'); setTimeout(function () {{ b.textContent = label; b.classList.remove('done'); }}, 1800); }}
  function fallback() {{ t.focus(); t.select(); try {{ if (document.execCommand('copy')) {{ ok(); return; }} }} catch (err) {{}} b.textContent = 'Selected: press Ctrl/Cmd+C'; }}
  if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t.value).then(ok, fallback); else fallback();
}});
</script>
{'</body></html>' if standalone else ''}
"""
    return doc.strip() + "\n"


def main():
    OUT.mkdir(exist_ok=True)
    blocks = {"css": export_css(), "html": export_html(), "js": export_js()}
    for key, fname, *_ in STEPS:
        (OUT / fname).write_text(blocks[key])
    (OUT / "copy-paste.html").write_text(helper_page(blocks, standalone=True))
    print("Wrote", ", ".join(f for _, f, *_ in STEPS), "and copy-paste.html to", OUT.name)
    return blocks


if __name__ == "__main__":
    main()
