#!/usr/bin/env python3
"""
Focus Writing (324 pages, "Learner's SO-26 Batch", Bangla + English) → short memorize edition.
Keeps only data and main lines of each topic's English version:
title · thesis (intro: first + last sentence) · the full "at a glance" data table ·
each section heading with its numbered points reduced to "point title — the sentence that carries the number" ·
conclusion (first + last sentence).
Input: OCR text per page (tesseract ben+eng) in --ocr DIR (tNNN.txt). Output: final_pdfs/SO_Focus_Writing_Memorize_Edition.pdf
Also adds the 31-page "SO-26.English Focus" topics (text PDF) in the same short format.
"""
import argparse, glob, html, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PDF = os.path.join(ROOT, "final_pdfs", "SO_Focus_Writing_Memorize_Edition.pdf")
FONT_BN = os.path.join(ROOT, "answer_book", "fonts", "TiroBangla-400.ttf")
BN_CH = re.compile(r"[ঀ-৿]")
DIGIT = re.compile(r"\d")
e = html.escape


def bn_ratio(s):
    s2 = re.sub(r"\s", "", s)
    return len(BN_CH.findall(s2)) / max(1, len(s2))


def clean(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("—", " – ")
    s = re.sub(r"[ঀ-৿]+", "", s)          # stray Bangla OCR from figures
    s = re.sub(r"\b0l\b|\b01 the\b", "of the", s)
    s = s.replace("Tiirkiye", "Türkiye").replace("_", " ")
    s = re.sub(r" 8110 ", " and ", s); s = re.sub(r" (ae|ee|oe) ", " ", s)
    s = re.sub(r"\s{2,}", " ", s).strip(" .;,-•")
    return s


def ok_sentence(x):
    w = x.split()
    caps = sum(1 for t in w if t[:1].isupper())
    return len(w) >= 5 and "|" not in x and caps / len(w) < 0.45


def sentences(text):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if ok_sentence(x.strip())]


TOPIC = re.compile(r"^\s*(\d{1,2})\s*[.,]\s+([A-Z].{8,})$")
SECTION = re.compile(r"^\s*(\d)\s*\.\s+([A-Z][^:]{6,110})$")
POINT = re.compile(r"^\s*(?:\d\s*[.,]\s*)?(\d)\s*[.,]?\s+([A-Z][^:]{3,80}):\s*(.*)$")


def load_lines(ocr_dir):
    lines = []
    for f in sorted(glob.glob(os.path.join(ocr_dir, "t*.txt"))):
        for ln in open(f, encoding="utf-8"):
            ln = ln.rstrip()
            if not ln.strip() or "Learner" in ln or "SO-26 Batch" in ln:
                continue
            lines.append(ln)
    return lines


def split_topics(lines):
    starts, last_n = [], 0
    for i, ln in enumerate(lines):
        s = ln.strip()
        m0 = re.match(r"^(.*\s)?Introduction(?::\s+(.*))?$", s)
        if not m0 or (m0.group(1) and len(m0.group(1)) > 90):
            continue
        head, rest = (m0.group(1) or "").strip(), m0.group(2)
        cand, k = ([head] if head else []), i - 1
        while k >= 0 and i - k <= 3 and not (cand and re.match(r"^\d{1,2}\s*[.,]\s", cand[0])):
            prev = lines[k].strip()
            if bn_ratio(prev) > 0.2 or prev.endswith(".") or len(prev) > 110:
                break
            cand.insert(0, prev); k -= 1
        m = re.match(r"^(\d{1,2})\s*[.,]\s+(.+)$", cand[0]) if cand else None
        n = int(m.group(1)) if m else last_n + 1
        title = clean(" ".join(([m.group(2)] if m else cand[:1]) + cand[1:])) if cand else ""
        last_n = n
        starts.append((i, n, title, rest))
    # essays printed without an "Introduction" heading: English title line right after Bangla text, "at a Glance" table soon after
    have = {i for i, *_ in starts}
    for i, ln in enumerate(lines[1:], 1):
        s = ln.strip()
        if (bn_ratio(lines[i - 1]) > 0.5 and bn_ratio(s) < 0.05 and 20 < len(s) < 110 and ":" in s and not s.endswith(".")
                and any("at a Glance" in x for x in lines[i + 1:i + 8]) and not any(abs(i - h) < 40 for h in have)):
            prev_n = max([n for j, n, *_ in starts if j < i] or [0])
            starts.append((i, prev_n + 1, clean(re.sub(r"^[a-z]\s+", "", s)), None))
    starts.sort()
    topics = []
    for k, (i, n, title, rest) in enumerate(starts):
        end = starts[k + 1][0] - 3 if k + 1 < len(starts) else len(lines)
        body = ["Introduction", rest] if rest else ["Introduction"]
        for ln in lines[i + 1:end]:
            if bn_ratio(ln) > 0.35:
                if len(body) > 25 and re.match(r"^\s*[০-৯]{1,2}\s*[.।]", ln.strip()):
                    break
                continue
            body.append(ln)
        topics.append((n, title, body))
    return topics


def parse(body):
    """→ intro, glance rows, sections[(heading, intro_sentence, [(pt, fact)])], conclusion."""
    mode, intro, glance, sections, concl = "intro", [], [], [], []
    global GLANCE_HEAD
    GLANCE_HEAD = ""
    cur = None
    for ln in body:
        s = ln.strip()
        if re.match(r"^Introduction\b", s):
            mode = "intro"; continue
        if re.search(r"at a Glance|At a Glance|AT A GLANCE", s) and len(s) < 140:
            mode = "glance"; GLANCE_HEAD = GLANCE_HEAD or clean(re.sub(r"(?i)\s*at a glance.*", "", s)); continue
        if re.match(r"^(Key Item|Indicator|Item|Topic|Subject)\b.*(Information|Statistics|Data|Value)", s):
            continue
        if re.match(r"^Sources?\s*:", s):
            mode = "body"; continue
        if re.match(r"^Conclusion\b", s):
            mode = "concl"; rest = s[len("Conclusion"):].strip()
            if rest: concl.append(rest)
            continue
        if s.startswith("Figure") or re.match(r"^(Five|Four|Six|Three|Seven)\s+[A-Z]", s):
            continue
        if mode == "glance":
            if SECTION.match(s) or POINT.match(s) or len(s) > 150 or len(glance) >= 26:
                mode = "body"
            elif len(s) > 6:
                glance.append(clean(s))
            continue
        if mode == "intro":
            intro.append(s); continue
        if mode == "concl":
            concl.append(s); continue
        pm, sm = POINT.match(s), SECTION.match(s)
        if pm:
            cur = cur or {"h": "Key points", "lead": [], "pts": []}
            if cur not in sections:
                sections.append(cur)
            cur["pts"].append([clean(pm.group(2)), [pm.group(3)]])
        elif sm and not s.endswith(".") and len(s) < 120:
            cur = {"h": clean(sm.group(2)), "lead": [], "pts": []}
            sections.append(cur)
        elif cur is not None:
            if cur["pts"]:
                cur["pts"][-1][1].append(s)
            else:
                cur["lead"].append(s)
        else:
            intro.append(s)
    return intro, glance, sections, concl


def fact_of(text):
    ss = sentences(clean(" ".join(text)))
    data = [x for x in ss if DIGIT.search(x)]
    pick = data[0] if data else (ss[0] if ss else "")
    return pick if len(pick) < 260 else pick[:257].rsplit(" ", 1)[0] + " …"


def summarize(n, title, body):
    intro, glance, sections, concl = parse(body)
    isent = sentences(clean(" ".join(intro)))
    csent = sentences(clean(" ".join(concl)))
    secs = []
    for s in sections:
        pts = [(p, fact_of(t)) for p, t in s["pts"] if p]
        if pts:
            secs.append((s["h"], pts))
    return {"n": n, "title": title, "gh": GLANCE_HEAD,
            "thesis": [x for x in (isent[:1] + isent[-1:] if len(isent) > 1 else isent)],
            "glance": glance, "sections": secs,
            "end": [x for x in (csent[:1] + csent[-1:] if len(csent) > 1 else csent)]}


def english_focus():
    """31-page SO-26.English Focus: already short; keep headings + bullets, drop filler."""
    p = os.path.join(ROOT, "Some Other Books", "SO-26.English Focus.pdf")
    txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
    txt = re.sub(r"\n\s*Page \d+\s*\n", "\n", txt)
    out, cur, sec = [], None, None
    lines = [l.strip() for l in txt.splitlines()]
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r"^(\d{1,2})\.\s+(.{6,})$", l)
        if m and i + 3 < len(lines) and any(x == "Introduction" for x in lines[i + 1:i + 4]):
            title = m.group(2)
            j = i + 1
            while lines[j] != "Introduction":
                title += " " + lines[j]; j += 1
            cur = {"n": int(m.group(1)), "title": title, "parts": []}
            out.append(cur); i = j; continue
        if cur is not None and l in ("Introduction", "Challenges", "Opportunities", "Policy Recommendations", "Conclusion") or \
                (cur is not None and re.match(r"^(Challenges|Opportunities)\s*\(", l)):
            sec = [l, ""]; cur["parts"].append(sec); i += 1; continue
        if cur is not None and sec is not None and l:
            sec[1] += (" " if sec[1] and not l.startswith("•") else ("\n" if l.startswith("•") else "")) + l
        i += 1
    res = []
    for t in out:
        parts = []
        for h, body in t["parts"]:
            if "•" in body:
                items = [clean(x) for x in body.split("•") if len(clean(x)) > 3]
            else:
                ss = sentences(clean(body.replace("\n", " ")))
                items = ss[:2] if h in ("Introduction", "Conclusion") else ss
            parts.append((h, items))
        res.append({"n": t["n"], "title": clean(t["title"]), "parts": parts})
    return res


TITLES = {
    1: "Bangladesh at COP31: Expectations, Opportunities and Challenges", 3: "A Lasting Solution to the Wage Crisis in the Garment Industry",
    7: "UDYOG: Youth Entrepreneurship through Financial Inclusion", 9: "New Horizons of Digital Banking in Bangladesh",
    11: "Digital Nano Loans in Bangladesh's Economy", 12: "Banking Sector Reform and the Pace of Economic Growth",
    13: "Non-Performing Loans and Their Potential Consequences", 20: "Mongla Port: A New Gateway to Economic Development",
    27: "Economic Dividends of Remittances: Prospects and Challenges", 35: "The Trillion-Dollar Economy and CMSME Lending in Bangladesh",
    37: "The Token Economy: Opportunities, Challenges and Measures", 36: "Expanding GI Products in the Export Market", 38: "Behavioral Economics: The Bangladesh Context",
    46: "The AI Cold War: US–China Technological Competition and Bangladesh's Priorities", 47: "Data Sovereignty and the Challenges Ahead",
    48: "AI and the Future of Banking Services", 50: "New Challenges in Cybersecurity", 51: "The AI Economy and Bangladesh",
    52: "National AI Roadmap 2026–2030", 53: "Technology, Women Workers and Government Responsibilities",
    54: "Artificial Intelligence and New Horizons in Tourism", 55: "The Technological Revolution of the Global South",
    56: "New Opportunities for Bangladesh amid Climate Challenges", 57: "Bangladesh's Strategic Progress towards Climate Justice",
    58: "The Impact of Climate Change on the National Economy", 59: "Climate Diplomacy", 60: "International Resources, Climate Justice and Sustainable Development",
    61: "Circular Economy", 62: "Renewal of the Ganges Water-Sharing Treaty", 63: "People-to-People Diplomacy: The Quiet Strength of Bangladesh–China Relations",
    64: "China–Japan Competition and Bangladesh", 65: "Can Bangladesh Escape the Low-Growth Trap?", 66: "Israeli and US Elections and the Future of the Iran War",
    67: "New Doors for Bangladesh–Russia Trade", 68: "The Mecca Agreement", 69: "China–Myanmar–Bangladesh Economic Corridor",
}


CSS = """
@font-face { font-family: "TiroB"; src: url("file://__BN__"); }
@page { size: A4; margin: 11mm 11mm 13mm 11mm; }
* { box-sizing: border-box; }
body { font-family: "Inter", "TiroB", sans-serif; color: #0f172a; font-size: 9pt; line-height: 1.38; margin: 0; }
.cover { padding: 4mm 2mm 0; }
.tag { font-size: 8.5pt; letter-spacing: .14em; text-transform: uppercase; color: #2563eb; font-weight: 700; }
h1 { font-size: 24pt; margin: 4pt 0 6pt; letter-spacing: -.02em; line-height: 1.1; }
.sub { color: #475569; font-family: "TiroB", "Inter"; font-size: 10.6pt; line-height: 1.55; }
.how { background: #ecfdf5; border-left: 3pt solid #047857; padding: 7pt 10pt; margin: 9pt 0; font-family: "TiroB", "Inter"; font-size: 10.2pt; line-height: 1.55; }
.toc { columns: 2; column-gap: 14pt; font-size: 8.8pt; margin-top: 8pt; }
.toc div { break-inside: avoid; padding: 1.6pt 0; border-bottom: 1px solid #e5eaf1; }
.toc b { color: #2563eb; display: inline-block; min-width: 20pt; }
h2.part { break-before: page; font-size: 15pt; border-bottom: 2px solid #0f172a; padding-bottom: 4pt; margin: 0 0 8pt; }
.card { border: 1px solid #dbe3ee; border-radius: 7pt; padding: 7pt 9pt 6pt; margin: 0 0 8pt; }
.card h3, .sec { break-after: avoid; } li { break-inside: avoid; }
.card h3 { margin: 0 0 4pt; font-size: 11pt; line-height: 1.25; }
.card h3 span { display: inline-block; background: #0f172a; color: #fff; border-radius: 4pt; padding: 0 5pt; margin-right: 5pt; font-size: 9pt; }
.thesis { color: #334155; font-style: italic; margin: 0 0 5pt; }
.glance { columns: 2; column-gap: 10pt; margin: 3pt 0 5pt; font-size: 8.4pt; background: #f8fafc; border-radius: 5pt; padding: 4pt 7pt; }
.glance div { break-inside: avoid; padding: 1.2pt 0; border-bottom: 1px solid #e8edf3; }
.sec { margin: 4pt 0 2pt; font-weight: 700; color: #2563eb; font-size: 9.2pt; }
ul { margin: 0; padding-left: 13pt; } li { margin: 0 0 1.6pt; }
li b { color: #0f172a; } .num { background: #fef3c7; border-radius: 2pt; padding: 0 1.5pt; }
.end { margin-top: 4pt; padding-top: 4pt; border-top: 1px dashed #dbe3ee; color: #047857; }
"""


NUMRE = re.compile(r"(?<![A-Za-z0-9])((?:USD|Tk\.?|BDT|\$)\s?)?\d(?:[\d,.]*\d)?(?:\s?(?:%|percent|billion|million|crore|lakh|trillion|thousand|MW|GW|km))?")


def hl(s):
    out, last = [], 0
    for m in NUMRE.finditer(s):
        out.append(e(s[last:m.start()])); out.append(f'<span class="num">{e(m.group(0))}</span>'); last = m.end()
    out.append(e(s[last:]))
    return "".join(out)


def card_html(t):
    h = f'<div class="card"><h3><span>{t["n"]}</span>{e(t["title"])}</h3>'
    if t["thesis"]:
        h += f'<p class="thesis">{hl(" ".join(t["thesis"]))}</p>'
    if t["glance"]:
        h += '<div class="glance">' + "".join(f"<div>{hl(g)}</div>" for g in t["glance"]) + "</div>"
    for head, pts in t["sections"]:
        h += f'<div class="sec">{e(head)}</div><ul>' + "".join(
            f"<li><b>{e(p)}</b>{' – ' + hl(f) if f else ''}</li>" for p, f in pts) + "</ul>"
    if t["end"]:
        h += f'<div class="end"><b>Conclusion:</b> {hl(" ".join(t["end"]))}</div>'
    return h + "</div>"


def card2_html(t):
    h = f'<div class="card"><h3><span>E{t["n"]}</span>{e(t["title"])}</h3>'
    for head, items in t["parts"]:
        if head == "Introduction":
            h += f'<p class="thesis">{hl(" ".join(items))}</p>'
        elif head == "Conclusion":
            h += f'<div class="end"><b>Conclusion:</b> {hl(" ".join(items))}</div>'
        else:
            h += f'<div class="sec">{e(head)}</div><ul>' + "".join(f"<li>{hl(x)}</li>" for x in items) + "</ul>"
    return h + "</div>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ocr", required=True)
    a = ap.parse_args()
    topics = [summarize(*t) for t in split_topics(load_lines(a.ocr))]
    # keep one card per topic number (first occurrence = the full English version)
    seen, T = set(), []
    for t in topics:
        t["title"] = TITLES.get(t["n"], t["title"]) or t["gh"]
        key = re.sub(r"[^a-z0-9]", "", ((t["thesis"][0] if t["thesis"] else t["title"]) + (t["glance"][0] if t["glance"] else "")).lower())[:90]
        if key in seen or (not t["glance"] and not t["sections"]):
            continue
        seen.add(key); T.append(t)
    E = english_focus()
    json.dump({"focus_writing_final": T, "english_focus": E}, open(os.path.join(ROOT, "data", "focus_writing_memorize.json"), "w"), ensure_ascii=False, indent=1)
    toc = "".join(f"<div><b>{t['n']}</b>{e(t['title'])}</div>" for t in T) + "".join(f"<div><b>E{t['n']}</b>{e(t['title'])}</div>" for t in E)
    cover = f"""<section class="cover"><div class="tag">SO Written · 27 November 2026 · Focus Writing</div>
<h1>Focus Writing — Memorize Edition</h1>
<div class="sub">৩২৪ পাতার "CTI Based Focus Writing (Learner's SO-26 Batch)"-এর {len(T)}টি টপিক এবং ৩১ পাতার "SO-26 English Focus"-এর {len(E)}টি টপিক — শুধু <b>ডেটা আর মূল লাইন</b>। প্রতিটি কার্ডে: মূল বক্তব্য (ভূমিকা), At a glance ডেটা টেবিল হুবহু, প্রতিটি অংশের পয়েন্ট + যে বাক্যে সংখ্যা আছে সেটি, উপসংহার। হলুদ = মুখস্থ করার সংখ্যা।</div>
<div class="how"><b>পরীক্ষায় কীভাবে লিখবেন:</b> ভূমিকা = কার্ডের প্রথম লাইন + ১টি সংখ্যা · তারপর At a glance টেবিল থেকে ৫–৬ সারি দিয়ে একটি টেবিল · প্রতিটি অংশ = হেডিং + ৩–৫টি পয়েন্ট, প্রতিটিতে একটি সংখ্যা · শেষে উপসংহারের লাইন। একটি টপিক ১০–১২ মিনিটে পড়ুন, তারপর না দেখে টেবিলটা খাতায় লিখুন।</div>
<div class="toc">{toc}</div></section>"""
    body = '<h2 class="part">Part A · CTI Based Focus Writing (SO-26 Batch)</h2>' + "".join(card_html(t) for t in T)
    body += '<h2 class="part">Part B · SO-26 English Focus (Bangladesh Economy & Banking)</h2>' + "".join(card2_html(t) for t in E)
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Focus Writing Memorize Edition</title><style>{CSS.replace("__BN__", FONT_BN)}</style></head><body>{cover}{body}</body></html>'
    hp = OUT_PDF.replace(".pdf", ".html")
    open(hp, "w", encoding="utf-8").write(doc)
    js = os.path.join(ROOT, "final_pdfs", ".mkpdf.js")
    open(js, "w").write(r"""const { chromium } = require("playwright");
(async () => { const [inp, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
 await p.goto("file://" + inp); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;text-align:center;font-family:Inter,Arial;font-size:7.5px;color:#64748b">Focus Writing · Memorize Edition · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
 await b.close(); })().catch((e) => { console.error(e); process.exit(1); });""")
    try:
        subprocess.run(["node", js, hp, OUT_PDF], check=True, cwd=ROOT)
    finally:
        os.remove(js); os.remove(hp)
    print("topics:", len(T), "+", len(E), "→", OUT_PDF)


if __name__ == "__main__":
    main()
