#!/usr/bin/env python3
"""Exports the site as copy-and-paste blocks for website builders.

Writes web-builder/:
  styles.css          paste into the builder's site-wide custom CSS
  script.js           paste into the site-wide footer code / custom JS
  html/<page>.html    one custom HTML block per page (header, content, footer)
  all-in-one/<page>.html  CSS + HTML + JS in a single block, for builders
                      whose HTML embeds run in an isolated frame (e.g. Wix)

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


def main():
    (OUT / "html").mkdir(parents=True, exist_ok=True)
    (OUT / "all-in-one").mkdir(parents=True, exist_ok=True)
    css = (ROOT / "assets/css/styles.css").read_text()
    js = (ROOT / "assets/js/main.js").read_text()
    (OUT / "styles.css").write_text(css)
    (OUT / "script.js").write_text(js)
    for page in build.PAGES:
        slug, file = page[0], page[1]
        block = page_block(*page)
        name = "home.html" if slug == "index" else file
        (OUT / "html" / name).write_text(block + "\n")
        (OUT / "all-in-one" / name).write_text(f"<style>\n{css}\n</style>\n{block}\n<script>\n{js}\n</script>\n")
    print("Exported", len(build.PAGES), "pages to", OUT)


if __name__ == "__main__":
    main()
