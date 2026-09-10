"""Build the user guides: docs/*.md -> docs/*.html -> docs/*.pdf.

This is the single production line for the manuals. Markdown is rendered with
python-markdown and the HTML is printed to PDF by headless Chrome, exactly as the
committed PDFs were produced. Run it whenever a guide's Markdown changes, so the
PDF release assets never drift away from their sources:

    python tools/build_guides.py

Requires: markdown (pip install markdown) and a Chrome/Edge binary. Set CHROME to
point at one explicitly if it is not in a standard location.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Markdown extensions the committed HTML was rendered with. Changing these changes
# every heading anchor, so keep them in step with the published guides.
EXTENSIONS = ["extra", "toc", "sane_lists"]

GUIDES = [
    ("KULLANIM_KILAVUZU", "tr", "French Course AI — Kullanım Kılavuzu"),
    ("USER_GUIDE", "en", "French Course AI — User Guide"),
]

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", "Calibri", system-ui, sans-serif; font-size: 10.5pt; line-height: 1.55; color: #14171d; margin: 0; }
h1 { font-size: 24pt; margin: 0 0 4pt; color: #C0392B; border-bottom: 3px solid #C0392B; padding-bottom: 8pt; }
h2 { font-size: 15pt; margin: 22pt 0 6pt; color: #C0392B; border-bottom: 1px solid #d7dbe2; padding-bottom: 3pt; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 14pt 0 4pt; color: #1d2430; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 3pt; color: #38404f; page-break-after: avoid; }
p, li { orphans: 2; widows: 2; }
ul, ol { padding-left: 20pt; margin: 5pt 0; }
li { margin: 2pt 0; }
code { font-family: "Cascadia Mono", Consolas, monospace; font-size: 9pt; background: #eef1f6; padding: 1pt 3pt; border-radius: 3px; }
pre { background: #f4f6fa; border: 1px solid #dde2ea; border-left: 3px solid #C0392B; border-radius: 4px; padding: 8pt 10pt;
      overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.8pt; line-height: 1.4; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.4pt; page-break-inside: avoid; }
th { background: #C0392B; color: #fff; text-align: left; padding: 5pt 7pt; font-weight: 600; }
td { border-bottom: 1px solid #dfe4ec; padding: 5pt 7pt; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fc; }
blockquote { margin: 8pt 0; padding: 6pt 12pt; background: #f4f6fa; border-left: 3px solid #C0392B; color: #38404f; }
a { color: #C0392B; text-decoration: none; }
hr { border: none; border-top: 1px solid #dfe4ec; margin: 14pt 0; }
.subtitle { color: #5b6474; font-size: 10pt; margin: 0 0 14pt; }
"""


def find_chrome() -> str:
    explicit = os.environ.get("CHROME")
    if explicit:
        if not Path(explicit).exists():
            sys.exit(f"CHROME={explicit} bulunamadi.")
        return explicit
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    found = shutil.which("chrome") or shutil.which("chromium") or shutil.which("google-chrome")
    if found:
        return found
    sys.exit("Chrome/Edge bulunamadi. CHROME degiskeni ile yolunu verin.")


def render_html(stem: str, lang: str, title: str) -> Path:
    md_path = DOCS / f"{stem}.md"
    body = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=EXTENSIONS)
    html = (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
        f"<title>{title}</title>\n<style>{CSS}</style></head><body>{body}</body></html>"
    )
    html_path = DOCS / f"{stem}.html"
    html_path.write_text(html, encoding="utf-8")
    return html_path


def print_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            html_path.as_uri(),
        ],
        check=True,
    )
    if not pdf_path.exists():
        sys.exit(f"PDF uretilemedi: {pdf_path}")


def main() -> None:
    chrome = find_chrome()
    for stem, lang, title in GUIDES:
        html_path = render_html(stem, lang, title)
        pdf_path = DOCS / f"{stem}.pdf"
        print_pdf(chrome, html_path, pdf_path)
        print(f"{pdf_path.relative_to(ROOT)} yenilendi ({pdf_path.stat().st_size} bayt)")


if __name__ == "__main__":
    main()
