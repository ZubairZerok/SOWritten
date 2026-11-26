#!/usr/bin/env python3
"""ALAL's Finance & Banking Hour (2026) → Bangla memorize edition, ranked by exam importance.
Content: engine/finance_bangla_data.py. Output: final_pdfs/SO_Finance_Banking_Bangla_Memorize.pdf"""
import html, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from finance_bangla_data import SECTIONS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "final_pdfs", "SO_Finance_Banking_Bangla_Memorize.pdf")
FONT_BN = os.path.join(ROOT, "answer_book", "fonts", "TiroBangla-400.ttf")
e = html.escape
NUM = re.compile(r"((?:USD|Tk|\$)\s?[0-9০-৯][0-9০-৯,.]*\s?(?:%|bn|crore|lakh)?|[0-9০-৯][0-9০-৯,.]*\s?%)")


def fmt(s):
    out, last = [], 0
    for m in NUM.finditer(s):
        out.append(e(s[last:m.start()])); out.append(f'<span class="num">{e(m.group(0))}</span>'); last = m.end()
    out.append(e(s[last:]))
    t = "".join(out)
    return re.sub(r"\(([A-Za-z][^()]{1,80})\)", r'<span class="en">(\1)</span>', t)


def item(it):
    if it[0] == "kv":
        return f'<div class="kv"><b>{fmt(it[1])}</b><span>{fmt(it[2])}</span></div>'
    if it[0] == "tbl":
        th = "".join(f"<th>{e(h)}</th>" for h in it[1])
        tr = "".join("<tr>" + "".join(f"<td>{fmt(c)}</td>" for c in r) + "</tr>" for r in it[2])
        return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"
    return f'<div class="note">{fmt(it[1])}</div>'


CSS = """
@font-face { font-family: "TiroB"; src: url("file://__BN__"); }
@page { size: A4; margin: 11mm 11mm 13mm 11mm; }
* { box-sizing: border-box; }
body { font-family: "TiroB", "Inter", sans-serif; color: #0f172a; font-size: 10.3pt; line-height: 1.48; margin: 0; }
.tag { font-family: Inter; font-size: 8.5pt; letter-spacing: .14em; text-transform: uppercase; color: #2563eb; font-weight: 700; }
h1 { font-size: 24pt; margin: 6pt 0; line-height: 1.2; }
.sub { color: #334155; font-size: 11pt; }
.how { background: #ecfdf5; border-left: 3pt solid #047857; padding: 7pt 10pt; margin: 9pt 0; font-size: 10.6pt; }
.toc div { padding: 2pt 0; border-bottom: 1px solid #e5eaf1; } .toc b { color: #2563eb; font-family: Inter; display: inline-block; min-width: 18pt; } .toc i { color: #b45309; font-style: normal; }
h2.tier { break-before: page; font-size: 15pt; border-bottom: 2px solid #0f172a; padding-bottom: 4pt; margin: 0 0 8pt; }
section.sec { margin: 0 0 12pt; }
section.sec h3 { font-size: 13pt; margin: 6pt 0 2pt; color: #0f172a; break-after: avoid; }
section.sec h3 span { display: inline-block; background: #0f172a; color: #fff; border-radius: 4pt; padding: 0 5pt; margin-right: 5pt; font-family: Inter; font-size: 9pt; vertical-align: 2pt; }
section.sec h3 i { color: #dc2626; font-style: normal; font-size: 10pt; }
.lead { color: #475569; margin: 0 0 5pt; font-size: 10pt; }
.kv { display: grid; grid-template-columns: 34% 1fr; gap: 0 9pt; padding: 3pt 0; border-bottom: 1px solid #e5eaf1; break-inside: avoid; }
.kv b { font-family: Inter, TiroB; font-size: 9.4pt; color: #1d4ed8; }
table { width: 100%; border-collapse: collapse; margin: 4pt 0 7pt; font-size: 9.4pt; }
th { text-align: left; background: #f1f5f9; color: #475569; font-size: 8.6pt; padding: 3pt 5pt; }
td { padding: 2.6pt 5pt; border-bottom: 1px solid #e5eaf1; vertical-align: top; } tr { break-inside: avoid; }
.note { background: #fff7ed; border-left: 3pt solid #b45309; padding: 5pt 9pt; margin: 4pt 0 6pt; font-size: 10pt; }
.num { background: #fef3c7; border-radius: 2pt; padding: 0 1.5pt; }
.en { font-family: Inter; font-size: 8.6pt; color: #1d4ed8; }
"""


def main():
    stars = {1: "★★★", 2: "★★", 3: "★"}
    names = {1: "স্তর ১ · সবচেয়ে গুরুত্বপূর্ণ (★★★) — আগে এগুলো", 2: "স্তর ২ · গুরুত্বপূর্ণ (★★)", 3: "স্তর ৩ · সময় থাকলে (★)"}
    toc = "".join(f'<div><b>{i + 1}</b>{e(t)} <i>{stars[tier]}</i></div>' for i, (tier, t, _, _) in enumerate(SECTIONS))
    body, last = "", 0
    for i, (tier, title, lead, items) in enumerate(SECTIONS):
        if tier != last:
            body += f'<h2 class="tier">{names[tier]}</h2>'; last = tier
        body += f'<section class="sec"><h3><span>{i + 1}</span>{e(title)} <i>{stars[tier]}</i></h3><p class="lead">{e(lead)}</p>' + "".join(item(x) for x in items) + "</section>"
    n = sum(len(x[3]) for x in SECTIONS)
    cover = f"""<section><div class="tag">SO Written · 27 November 2026 · Financial &amp; Banking Knowledge (10 marks)</div>
<h1>ফাইন্যান্স ও ব্যাংকিং — বাংলা মুখস্থ সংস্করণ</h1>
<div class="sub">আলাল'স <b>Finance &amp; Banking Hour (2026)</b>-এর ১৫টি অধ্যায় — বাংলায়, শুধু তথ্য ও মূল লাইন, <b>সবচেয়ে গুরুত্বপূর্ণ থেকে কম গুরুত্বপূর্ণ</b> ক্রমে ({n}টি এন্ট্রি)। ইংরেজি পরিভাষা ও পূর্ণরূপ <span class="en">(নীল)</span>, মুখস্থের সংখ্যা <span class="num">হলুদ</span>। বইয়ের যেসব সংখ্যা পুরোনো (নীতি সুদহার, ডিজিটাল ব্যাংকের মূলধন, আমানত বিমা ইত্যাদি), সেগুলো নভেম্বর ২০২৬-এর যাচাই করা সংখ্যা দিয়ে বদলে 'পুরোনো' বলে চিহ্নিত করা হয়েছে।</div>
<div class="how"><b>প্রশ্নের ধরন (প্রশ্ন ৯):</b> ৫টি ছোট প্রশ্ন × ২ নম্বর, উত্তর <b>ইংরেজিতে</b> — পূর্ণরূপ, এক বাক্যে সংজ্ঞা, পরিভাষার নাম, বা চলতি সংখ্যা।<br><b>২ নম্বরের সূত্র:</b> এক বাক্যে পূর্ণ উত্তর → মূল শব্দ আন্ডারলাইন → একটি বাড়তি তথ্য (কে ঠিক করে / বর্তমান হার / সাল)। উদাহরণ: <i>CRR is the portion of a bank's deposits that it must keep as cash with the central bank; Bangladesh Bank sets it at 4%.</i></div>
<div class="toc">{toc}</div></section>"""
    doc = f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><title>Finance Banking Bangla</title><style>{CSS.replace("__BN__", FONT_BN)}</style></head><body>{cover}{body}</body></html>'
    hp = OUT.replace(".pdf", ".html"); open(hp, "w", encoding="utf-8").write(doc)
    js = os.path.join(ROOT, "final_pdfs", ".mkfb.js")
    open(js, "w").write(r"""const { chromium } = require("playwright");
(async () => { const [inp, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
 await p.goto("file://" + inp); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;text-align:center;font-family:Inter,Arial;font-size:7.5px;color:#64748b">Finance & Banking (Bangla) · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
 await b.close(); })().catch((e) => { console.error(e); process.exit(1); });""")
    try:
        subprocess.run(["node", js, hp, OUT], check=True, cwd=ROOT)
    finally:
        os.remove(js); os.remove(hp)
    print("PDF:", OUT)


if __name__ == "__main__":
    main()
