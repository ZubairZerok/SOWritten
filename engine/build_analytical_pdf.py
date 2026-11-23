#!/usr/bin/env python3
"""
docs/17_analytical_40_marks.md → docs/Analytical_40_Marks_Guide.pdf (A4, প্রিন্টের উপযোগী)
চালান:  python3 engine/build_analytical_pdf.py      (Playwright/Chromium লাগে)
"""
import os, re, subprocess, sys
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "17_analytical_40_marks.md")
OUT_HTML = os.path.join(ROOT, "docs", "Analytical_40_Marks_Guide.html")
OUT_PDF = os.path.join(ROOT, "docs", "Analytical_40_Marks_Guide.pdf")
FONTS = "../answer_book/fonts/"

CSS = """
@font-face { font-family: "TiroB"; src: url("%(f)sTiroBangla-400.ttf"); }
@font-face { font-family: "TinosL"; src: url("%(f)sTinos-400.ttf"); font-weight: 400; }
@font-face { font-family: "TinosL"; src: url("%(f)sTinos-700.ttf"); font-weight: 700; }
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
:root { --ink: #16213a; --ink2: #4b5873; --rule: #d6dce8; --acc: #1f6f55; --accsoft: #e6f3ec; --warn: #9a5b00; --warnsoft: #fdf3e1; --red: #b3372d; }
* { box-sizing: border-box; }
body { font-family: "TinosL", "TiroB", serif; color: var(--ink); font-size: 10.6pt; line-height: 1.55; margin: 0; }
:lang(bn), body { font-family: "TinosL", "TiroB", serif; }
h1 { font-size: 19pt; line-height: 1.25; margin: 0 0 6pt; color: var(--ink); }
h2 { font-size: 14.5pt; margin: 0 0 8pt; padding: 6pt 10pt; background: var(--ink); color: #fff; border-radius: 4pt; margin-top: 14pt; break-after: avoid; }
h2.first { break-before: auto; }
h3 { font-size: 11.8pt; margin: 14pt 0 5pt; color: var(--acc); border-bottom: 1px solid var(--rule); padding-bottom: 2pt; break-after: avoid; }
p { margin: 4pt 0; }
ul, ol { margin: 3pt 0 6pt; padding-left: 18pt; }
li { margin: 1.5pt 0; }
table { border-collapse: collapse; width: 100%%; margin: 6pt 0 8pt; font-size: 9.6pt; break-inside: auto; }
th, td { border: 1px solid var(--rule); padding: 3.5pt 6pt; vertical-align: top; text-align: left; }
th { background: #eef1f7; font-weight: 700; }
tr { break-inside: avoid; }
blockquote { margin: 6pt 0; padding: 6pt 10pt; background: var(--accsoft); border-left: 3pt solid var(--acc); border-radius: 3pt; }
blockquote p { margin: 2pt 0; }
code { font-family: "TinosL", monospace; background: #f1f3f8; padding: 0 3pt; border-radius: 2pt; font-size: 9.4pt; }
hr { border: 0; height: 0; margin: 0; }
strong { color: #0f1a33; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; border: 2pt solid var(--ink); border-radius: 6pt; padding: 22mm 18mm; position: relative; }
.cover .tag { font-size: 10pt; letter-spacing: .08em; text-transform: uppercase; color: var(--ink2); }
.cover h1 { font-size: 26pt; margin: 8pt 0 10pt; }
.cover .sub { font-size: 12.5pt; color: var(--ink2); }
.cover .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8pt; margin: 18pt 0; }
.cover .card { border: 1px solid var(--rule); border-radius: 5pt; padding: 8pt; }
.cover .card b { display: block; font-size: 15pt; color: var(--acc); }
.cover .foot { position: absolute; bottom: 14mm; left: 18mm; right: 18mm; font-size: 9pt; color: var(--ink2); border-top: 1px solid var(--rule); padding-top: 6pt; }
.model { border: 1px solid var(--rule); border-left: 3pt solid var(--warn); background: var(--warnsoft); padding: 6pt 10pt; border-radius: 3pt; margin: 6pt 0; }
.toc { columns: 2; column-gap: 14pt; font-size: 10.4pt; }
.toc div { break-inside: avoid; padding: 2pt 0; border-bottom: 1px dotted var(--rule); }
"""


def build_html():
    md = open(SRC, encoding="utf-8").read()
    md = md.replace("- [ ] ", "- ☐ ")
    # Python-Markdown তালিকার আগে ফাঁকা লাইন চায় (GitHub চায় না): দরকার হলে যোগ করি
    lines, out = md.split("\n"), []
    is_item = lambda l: bool(re.match(r"\s*(\d+\.|[-*])\s", l))
    for i, l in enumerate(lines):
        if is_item(l) and out and out[-1].strip() and not is_item(out[-1]) and not out[-1].lstrip().startswith(("|", ">")) and not re.match(r"\s{2,}", l):
            out.append("")
        out.append(l)
    md = "\n".join(out)
    md = re.sub(r"(?m)^   - ", "    - ", md)  # নেস্টেড তালিকা: ৪ স্পেস
    title = md.split("\n", 1)[0].lstrip("# ").strip()
    body = markdown.markdown(md.split("\n", 1)[1], extensions=["tables", "sane_lists"])
    # প্রথম h2 আলাদা পাতা শুরু করবে না (কভার + সূচির পরে)
    body = body.replace("<h2>", '<h2 class="first">', 1)
    # মডেল উত্তরের অনুচ্ছেদগুলো হালকা বাক্সে (ইংরেজি উত্তর আলাদা চোখে পড়বে)
    body = re.sub(r"<p>(<strong>(?:Introduction|Arguments for|Arguments against|Position|Argument \d|Counter-argument|Recommendations|Conclusion|The conclusion is not justified|A better approach)[^<]*</strong>.*?)</p>",
                  r'<div class="model"><p>\1</p></div>', body, flags=re.S)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", body)
    toc = "".join(f"<div>{t}</div>" for t in h2s)
    cover = f"""
<section class="cover">
  <div class="tag">SO Written · ২৭ নভেম্বর ২০২৬ · প্রশ্ন ৬ (৪০ নম্বর)</div>
  <h1>Analytical Reasoning, Critical Thinking<br>ও Argumentative Writing</h1>
  <div class="sub">৪ ধরনের প্রশ্ন, প্রতিটির নির্দিষ্ট পদ্ধতি · আসল প্রশ্নের সমাধান · কম্পিউটারে যাচাই করা নতুন পাজল · মডেল উত্তর · ৪ দিনের প্ল্যান</div>
  <div class="grid">
    <div class="card"><b>(a)</b>লজিক পাজল<br>৬ মিনিট</div>
    <div class="card"><b>(b)</b>সিদ্ধান্তের সমালোচনা<br>৫ মিনিট</div>
    <div class="card"><b>(c)</b>লুকানো অনুমান<br>৩ মিনিট</div>
    <div class="card"><b>(d)</b>পক্ষে-বিপক্ষে যুক্তি<br>৮ মিনিট</div>
  </div>
  <div><b>সূচি</b></div>
  <div class="toc">{toc}</div>
  <div class="foot">উৎস: জুন ২০২৬ ও জুন ২০২৫ SO প্রশ্ন, রিপোর আর্গুমেন্ট রাইটিং PDF (২টি), আর্গুমেন্ট প্লেবুক, ২০ নভেম্বর ২০২৬-এর যাচাই করা তথ্য। অনুশীলনের প্রশ্ন: নিজে বানানো, প্রতিটির ঠিক একটি সমাধান কম্পিউটারে যাচাই করা।</div>
</section>"""
    html = f"""<!doctype html><html lang="bn"><head><meta charset="utf-8"><title>{title}</title><style>{CSS % {"f": FONTS}}</style></head>
<body>{cover}{body}</body></html>"""
    open(OUT_HTML, "w", encoding="utf-8").write(html)
    return OUT_HTML


JS = r"""
const { chromium } = require("playwright");
(async () => {
  const [inp, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + inp, { waitUntil: "load" }); await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({ media: "print" });
  await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
    footerTemplate: '<div style="width:100%;text-align:center;font-family:Times New Roman,serif;font-size:8px;color:#666">Analytical Reasoning &amp; Argumentative Writing (40) · SO Written 27 Nov 2026 · Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>' });
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def main():
    html = build_html()
    if "--no-pdf" in sys.argv:
        print("HTML:", html); return
    js = os.path.join(ROOT, "docs", ".make_pdf_tmp.js")
    open(js, "w").write(JS)
    try:
        subprocess.run(["node", js, html, OUT_PDF], check=True, cwd=ROOT)
    finally:
        os.remove(js)
    print("PDF:", OUT_PDF)


if __name__ == "__main__":
    main()
