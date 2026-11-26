#!/usr/bin/env python3
"""
Focus Writing — সম্পূর্ণ বাংলা মুখস্থ সংস্করণ (most important → least important).
Sources (Bangla text = the authors' own Bangla version of each essay, OCR'd):
  FT  = "Learner's SO26 Final Touch" (61 pages, Nov 2026)        --ft  OCR dir
  CTI = "CTI Based Focus Writing, Learner's SO-26 Batch" (324 pp) --cti OCR dir
  EF  = "SO-26 English Focus" (English only) → Bangla cards written by hand in engine/focus_bangla_extra.py
Each card keeps only: title, 2-line intro, at-a-glance data, every point's title + its data sentence, 2-line conclusion.
Hard terms get the English word in brackets (GLOSSARY) so it can be written in the exam.
Output: final_pdfs/SO_Focus_Writing_Bangla_Memorize.pdf
"""
import argparse, glob, html, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from focus_bangla_extra import EXTRA_CARDS, RANK, SKIP, TITLE_FIX, GLOSSARY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PDF = os.path.join(ROOT, "final_pdfs", "SO_Focus_Writing_Bangla_Memorize.pdf")
FONT_BN = os.path.join(ROOT, "answer_book", "fonts", "TiroBangla-400.ttf")
BN = re.compile(r"[ঀ-৿]")
EN = re.compile(r"[A-Za-z]")
BD = "০১২৩৪৫৬৭৮৯"
e = html.escape

FIX = [  # frequent OCR slips in Bangla
    ("খণ", "ঋণ"), ("ঝণ", "ঋণ"), ("খাণ", "ঋণ"), ("এঁতিহাসিক", "ঐতিহাসিক"), ("চ্যালেজ", "চ্যালেঞ্জ"), ("চ্যালে।", "চ্যালেঞ্জ"),
    ("রাষ্ত্ীয়", "রাষ্ট্রীয়"), ("রাষ্্ীয়", "রাষ্ট্রীয়"), ("শুন্ক", "শুল্ক"), ("মূল্যক্ষীতি", "মূল্যস্ফীতি"), ("মূল্যস্ফী�", "মূল্যস্ফীতি"),
    ("আ্যা", "অ্যা"), ("রেমিট্যাসস", "রেমিট্যান্স"), ("রোহিঙগী", "রোহিঙ্গা"), ("শক্তিশীলীকরণ", "শক্তিশালীকরণ"), ("ন্যাধ্য", "ন্যায্য"),
    ("আশাব্যঞ্ক", "আশাব্যঞ্জক"), ("পরিচ্ছনন", "পরিচ্ছন্ন"), ("কুটনৈতিক", "কূটনৈতিক"), ("ক্ষতিত্স্ত", "ক্ষতিগ্রস্ত"), ("বাস্ত্যুতি", "বাস্তুচ্যুতি"),
    ("দুর্যোগর্ুকি", "দুর্যোগঝুঁকি"), ("সুশীসন", "সুশাসন"), ("কার্ষকর", "কার্যকর"), ("নিজন্ব", "নিজস্ব"), ("প্রস্ততি", "প্রস্তুতি"),
    ("পারিকল্নানা", "পরিকল্পনা"), ("আভিযোজন", "অভিযোজন"), ("উদ্যোক্তী", "উদ্যোক্তা"), ("নিরাপত্তী", "নিরাপত্তা"), ("অন্ততুক্তি", "অন্তর্ভুক্তি"),
    ("ই-গভর্ন্যা্স", "ই-গভর্ন্যান্স"), ("ই-গভর্ন্যান্ের", "ই-গভর্ন্যান্সের"), ("ই-গভর্ম্যান্স", "ই-গভর্ন্যান্স"), ("মন্থ্রতী", "মন্থরতা"),
    ("স্থৃবিরতা", "স্থবিরতা"), ("হাস", "হ্রাস"), ("হাঁস", "হ্রাস"), ("প্রণৌদনা", "প্রণোদনা"), ("অশ্রযাত্র", "অগ্রযাত্রা"), ("কনজ্যমারস", "কনজ্যুমারস"),
    ("প্রত্যাশী,", "প্রত্যাশা,"), ("জৌয়ার", "জোয়ার"), ("জ্বীলানি", "জ্বালানি"), ("ভ্বালানি", "জ্বালানি"), ("ধারণী", "ধারণা"), ("সম্ভীবনা", "সম্ভাবনা"),
    ("গ্রীমীণ", "গ্রামীণ"), ("জৌরদার", "জোরদার"), ("ম্যানঘৌভ", "ম্যানগ্রোভ"), ("সমঘ্বিত", "সমন্বিত"), ("জীববৈচিত্র্ের", "জীববৈচিত্র্যের"),
    ("বু ইকোনমি", "ব্লু ইকোনমি"), ("দারিদ্রের", "দারিদ্র্যের"), ("কার্ষপদ্ধতি", "কার্যপদ্ধতি"), ("কারযপন্ধতি", "কার্যপদ্ধতি"), ("দিমুখী", "দ্বিমুখী"),
    ("ঐতিহ্রাসিক", "ঐতিহাসিক"), ("ব্যাকিং", "ব্যাংকিং"), ("লাইসেল", "লাইসেন্স"), ("লাইসেসের", "লাইসেন্সের"), ("ন্[নতম", "ন্যূনতম"), ("১৮৭%", "১৮.৭%"),
    ("০0729", "কপ-২৯"), ("00729", "কপ-২৯"), ("00731", "কপ-৩১"), ("00০31", "কপ-৩১"), ("০0০31", "কপ-৩১"), ("০0731", "কপ-৩১"), ("০0০31", "কপ-৩১"),
    ("COP31-4%", "COP31-এর"), ("COP31-4", "COP31-এ"), ("তন্তর্জাতিক", "আন্তর্জাতিক"), ("সম্ভাবনাগ্ডলো", "সম্ভাবনাগুলো"), ("ভাবনাগ্ডলো", "ভাবনাগুলো"),
    ("নিরাপজা", "নিরাপত্তা"), ("ঐতিহ্যাসিক", "ঐতিহাসিক"), ("সত্বেও", "সত্ত্বেও"), ("পাঁজল", "পাজল"), ("দারিদ্র ", "দারিদ্র্য "), ("ক্ষুত্র", "ক্ষুদ্র"), ("ঋণরুঁকি", "ঋণঝুঁকি"),
]


KEEP = {"ICJ", "COP", "AI", "GDP", "IMF", "ADB", "UN", "UNDP", "NDC", "NAP", "SME", "MFS", "QR", "ATM", "IPO", "BFIU", "ACC", "FDI", "EPA", "CEPA",
        "FTA", "PTA", "RMG", "IT", "ICT", "USD", "US", "EU", "UK", "WTO", "GSP", "ETP", "IRF", "OIC", "LDC", "NBR", "BIDA", "BEZA", "IoT", "TIB",
        "BSS", "GI", "OTT", "EV", "PM", "BERC", "CAB", "NCQG", "VAT", "PPP", "ADP", "EPZ", "SEZ", "ESG", "CSR", "KYC", "AML", "API", "OTP", "CBDC",
        "GPT", "LNG", "LPG", "MW", "GW", "SDG", "BB", "Data", "and", "of", "the", "Bank", "Fund", "Loss", "Card", "Flow", "Act", "Plan", "Gap"}


def fix(s):
    for a, b in FIX:
        s = s.replace(a, b)
    s = re.sub(r"^\s*(?:8|81)\s*[,.।]\s*", "৪. ", s)
    s = re.sub(r"^\s*(?:€|©)\s*[,.।]\s*", "৫. ", s)
    s = re.sub(r"^\s*Ol\s*[,.।]?\s*", "৩. ", s)
    s = re.sub(r"\(100\)", "(ICJ)", s)
    s = re.sub(r"[|]\s*$", "", s)
    # drop stray Latin OCR tokens sitting inside Bangla text (keep real acronyms)
    s = re.sub(r"(?<=[\u0980-\u09FF।,] )([A-Za-z]{2,4})(?=[ ।,]|$)", lambda m: m.group(1) if m.group(1) in KEEP else "", s)
    s = re.sub(r"(?<=[\u0980-\u09FF])\s+[a-z]{1,3}\s*$", "", s)
    s = re.sub(r"^[>&]\.\s*", "", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def ratio(s):
    b, a = len(BN.findall(s)), len(EN.findall(s))
    return b / max(1, a + b)


def runs(ocr_dir):
    """Line-level segmentation into Bangla runs (one run ≈ one essay's Bangla version)."""
    lines = []
    for f in sorted(glob.glob(os.path.join(ocr_dir, "t*.txt"))):
        for ln in open(f, encoding="utf-8"):
            s = ln.strip()
            if not s or "Learner" in s or "Final Touch" in s or "SO-26 Batch" in s or re.match(r"^পৃষ্ঠা\s*[০-৯0-9]+", s):
                continue
            lines.append(s)
    out, cur, en_streak = [], [], 0
    for s in lines:
        r = ratio(s)
        if r >= 0.5:
            if en_streak >= 6 and cur:
                out.append(cur); cur = []
            en_streak = 0
            cur.append(fix(s))
        elif len(EN.findall(s)) > 25:
            en_streak += 1
    if cur:
        out.append(cur)
    out = [r for r in out if len(r) >= 25]
    final = []
    for r in out:
        final.extend(split_run(r))
    return [r for r in final if len(r) >= 25]


def is_title(x):
    return len(x) < 95 and not x.endswith("।") and not re.match(r"^[০-৯]", x) and ":" not in x[:-1] and "একনজরে" not in x and x != "ভূমিকা"


def title_like(x):
    return len(x) < 95 and not x.endswith("।") and not re.match(r"^[০-৯]", x) and "একনজরে" not in x and x != "ভূমিকা"


def split_run(r):
    """A run can hold several essays when no English text separates them: split at the title before a 2nd 'একনজরে' table."""
    cuts, seen = [0], False
    for j, x in enumerate(r):
        if "একনজরে" in x and len(x) < 110:
            if seen:
                for k in range(j - 1, max(cuts[-1] + 5, j - 16), -1):
                    if r[k] == "ভূমিকা" and len(r[k - 1]) < 100 and not r[k - 1].endswith("।"):
                        cuts.append(k - 1); break
                    if title_like(r[k]) and (r[k - 1].endswith("।") or r[k - 1].startswith("উপসংহার") or "|" in r[k - 1]) and len(r[k]) > 12:
                        cuts.append(k); break
            seen = True
    cuts.append(len(r))
    return [r[a:b] for a, b in zip(cuts, cuts[1:])]


NUM = r"(?:[০-৯]{1,2}(?:\s*[.,]\s*[০-৯])?)"
HEAD = re.compile(rf"^{NUM}\s*[.,।]\s*([^:।]{{4,90}})$")
POINT = re.compile(rf"^(?:{NUM}\s*[.,।]?\s*)?([^:।]{{3,60}}):\s*(.*)$")
TITLE_NUM = re.compile(r"^[০-৯]{1,2}\s*[.।]\s*")


def tidy(x):
    x = re.sub(r"\[[^\]\u0980-\u09FF]*\]?", "", x)                      # [junk]
    x = re.sub(r"\b\d{4,}\b(?![-–]\d)", lambda m: m.group(0) if re.match(r"^(19|20)\d\d$", m.group(0)) else "", x)
    def latin(m):
        w = m.group(0)
        return w if w in KEEP or w.strip(",.") in KEEP else ""
    # Latin words outside parentheses between Bangla words are OCR noise from figures
    parts = re.split(r"(\([^)]*\))", x)
    parts = [pt if pt.startswith("(") else re.sub(r"(?<![A-Za-z(])[A-Za-z][A-Za-z,.']{0,14}(?![A-Za-z)])", latin, pt) for pt in parts]
    x = "".join(parts)
    x = re.sub(r"\b[\w-]+\.(?:int|org|gov|com|net)(?:\.bd)?\b", "", x)
    x = re.sub(r"চিত্র\s*[০-৯0-9]+\s*:?", "", x)
    x = re.sub(r"\(\s*\)", "", x)
    return re.sub(r"\s{2,}", " ", x).strip(" ,|")


def bsent(text):
    return [tidy(x.strip()) + "।" for x in re.split(r"[।?!]\s*", text) if len(x.strip()) > 12]


def pick(text):
    ss = bsent(text)
    dat = [x for x in ss if re.search(r"[০-৯0-9]", x)]
    x = dat[0] if dat else (ss[0] if ss else "")
    return x if len(x) < 230 else x[:227].rsplit(" ", 1)[0] + " …"


def parse(run):
    if re.search(r"সংকলন|পরিশিষ্ট", run[0]):
        run = run[1:]
    title = TITLE_NUM.sub("", run[0])
    mode, intro, glance, secs, concl = "intro", [], [], [], []
    cur = None
    for idx, s in enumerate(run[1:], 1):
        nxt = run[idx + 1] if idx + 1 < len(run) else ""
        if mode != "glance" and is_title(s) and len(s) < 75 and POINT.match(nxt) and (run[idx - 1].endswith("।") or "|" in run[idx - 1]):
            cur = {"h": s, "lead": [], "pts": []}; secs.append(cur); mode = "body"; continue
        if s in ("ভূমিকা",) or s.startswith("চিত্র") or re.match(r"^(সূত্র|তথ্যসূত্র|সংক্ষিপ্ত তথ্যসূত্র|উৎস|Sey|Source)", s):
            if re.match(r"^(সূত্র|তথ্যসূত্র|সংক্ষিপ্ত তথ্যসূত্র|উৎস|Sey|Source)", s):
                mode = "body" if mode == "glance" else mode
            continue
        if "একনজরে" in s and len(s) < 110:
            mode = "glance"; continue
        if re.match(r"^গুরুত্বপূর্ণ বিষয়|^বিষয়\s", s) and mode == "glance":
            continue
        if s.startswith("উপসংহার"):
            mode = "concl"; rest = s.replace("উপসংহার", "", 1).strip(" :")
            if rest: concl.append(rest)
            continue
        if mode == "glance":
            if HEAD.match(s) or POINT.match(s) or len(s) > 140 or len(glance) > 24:
                mode = "body"
            else:
                glance.append(s); continue
        if mode == "concl":
            concl.append(s); continue
        pm, hm = POINT.match(s), HEAD.match(s)
        if hm and not s.endswith("।"):
            h = max(hm.group(1).split("|"), key=lambda x: len(BN.findall(x))).strip(" ()|")
            cur = {"h": h, "lead": [], "pts": []}; secs.append(cur); mode = "body"; continue
        if pm and len(pm.group(1)) < 60 and not pm.group(1).startswith(("যেমন", "অর্থাৎ")):
            if cur is None:
                cur = {"h": "মূল পয়েন্ট", "lead": [], "pts": []}; secs.append(cur)
            cur["pts"].append([pm.group(1).strip(), [pm.group(2)]]); mode = "body"; continue
        if mode == "intro":
            intro.append(s)
        elif cur is not None:
            (cur["pts"][-1][1] if cur["pts"] else cur["lead"]).append(s)
    isent = bsent(" ".join(intro))
    csent = bsent(" ".join(concl))
    sections = []
    for c in secs:
        pts = [(p, pick(" ".join(t))) for p, t in c["pts"]]
        lead = bsent(" ".join(c["lead"]))
        if pts:
            sections.append((c["h"], pts, ""))
        elif lead:  # paragraph-only section (often the closing paragraph in Final Touch)
            sections.append((c["h"], [], " ".join(lead[:1] + lead[-1:] if len(lead) > 1 else lead)))
    return {"title": title, "intro": isent[:1] + isent[-1:] if len(isent) > 1 else isent, "glance": glance,
            "sections": sections, "end": csent[:1] + csent[-1:] if len(csent) > 1 else csent}


# ───────── rendering ─────────
NUMRE = re.compile(r"((?:USD|Tk|\$)?\s?[০-৯0-9](?:[০-৯0-9,.]*[০-৯0-9])?\s?(?:%|শতাংশ|বিলিয়ন|মিলিয়ন|কোটি|লাখ|ট্রিলিয়ন|হাজার|ডলার|টাকা|মেগাওয়াট|বছর|টি)?)")


def gloss(s, used):
    for bn, en in GLOSSARY:
        if bn in used or bn not in s or f"({en}" in s:
            continue
        i = s.find(bn); j = i + len(bn)
        while j < len(s) and not s[j].isspace() and s[j] not in "।,;:()|—-.":
            j += 1
        s = s[:j] + f" ⟨{en}⟩" + s[j:]; used.add(bn)
    return s


def hl(s, used):
    s = gloss(s, used)
    out, last = [], 0
    for m in NUMRE.finditer(s):
        out.append(e(s[last:m.start()])); out.append(f'<span class="num">{e(m.group(0))}</span>'); last = m.end()
    out.append(e(s[last:]))
    return "".join(out).replace("⟨", '<span class="en">(').replace("⟩", ")</span>")


def card(i, t, tier):
    used = set()
    star = {1: "★★★", 2: "★★", 3: "★"}[tier]
    h = f'<div class="card t{tier}"><h3><span class="no">{i}</span>{hl(t["title"], used)} <i>{star}</i></h3>'
    if t.get("src"):
        h += f'<div class="src">{e(t["src"])}</div>'
    if t["intro"]:
        h += f'<p class="intro"><b>ভূমিকা:</b> {hl(" ".join(t["intro"]), used)}</p>'
    if t["glance"]:
        h += '<div class="glance"><div class="gh">একনজরে তথ্য</div>' + "".join(f"<div>{hl(g, used)}</div>" for g in t["glance"]) + "</div>"
    for head, pts, para in t["sections"]:
        h += f'<div class="sec">{hl(head, used)}</div>'
        if pts:
            h += "<ul>" + "".join(f"<li><b>{hl(p, used)}</b>{' — ' + hl(f, used) if f else ''}</li>" for p, f in pts) + "</ul>"
        elif para:
            h += f'<p class="para">{hl(para, used)}</p>'
    if t["end"]:
        h += f'<div class="end"><b>উপসংহার:</b> {hl(" ".join(t["end"]), used)}</div>'
    return h + "</div>"


CSS = """
@font-face { font-family: "TiroB"; src: url("file://__BN__"); }
@page { size: A4; margin: 11mm 11mm 13mm 11mm; }
* { box-sizing: border-box; }
body { font-family: "TiroB", "Inter", sans-serif; color: #0f172a; font-size: 10.4pt; line-height: 1.5; margin: 0; }
.cover h1 { font-size: 25pt; margin: 6pt 0 6pt; line-height: 1.2; }
.tag { font-family: Inter; font-size: 8.5pt; letter-spacing: .14em; text-transform: uppercase; color: #2563eb; font-weight: 700; }
.sub { color: #334155; font-size: 11pt; }
.how { background: #ecfdf5; border-left: 3pt solid #047857; padding: 7pt 10pt; margin: 9pt 0; font-size: 10.6pt; }
.toc { columns: 2; column-gap: 14pt; font-size: 9.6pt; margin-top: 6pt; }
.toc div { break-inside: avoid; padding: 1.4pt 0; border-bottom: 1px solid #e5eaf1; }
.toc b { color: #2563eb; display: inline-block; min-width: 18pt; font-family: Inter; }
.toc i { color: #b45309; font-style: normal; font-size: 8pt; }
h2.tier { break-before: page; font-size: 15pt; border-bottom: 2px solid #0f172a; padding-bottom: 4pt; margin: 0 0 8pt; }
.card { border: 1px solid #dbe3ee; border-left: 4pt solid #94a3b8; border-radius: 6pt; padding: 7pt 10pt 6pt; margin: 0 0 9pt; }
.card.t1 { border-left-color: #dc2626; } .card.t2 { border-left-color: #f59e0b; } .card.t3 { border-left-color: #94a3b8; }
.card h3 { margin: 0 0 3pt; font-size: 12.4pt; line-height: 1.3; break-after: avoid; }
.card h3 .no { display: inline-block; background: #0f172a; color: #fff; border-radius: 4pt; padding: 0 5pt; margin-right: 5pt; font-family: Inter; font-size: 9pt; vertical-align: 2pt; }
.card h3 i { color: #dc2626; font-style: normal; font-size: 10pt; }
.src { font-family: Inter; font-size: 7.4pt; color: #64748b; margin-bottom: 3pt; }
.intro { margin: 0 0 4pt; color: #1e293b; }
.glance { columns: 2; column-gap: 10pt; margin: 3pt 0 5pt; font-size: 9.6pt; background: #f8fafc; border-radius: 5pt; padding: 4pt 7pt; }
.glance .gh { column-span: all; font-weight: 700; color: #2563eb; font-size: 9.6pt; }
.glance div { break-inside: avoid; padding: 1pt 0; border-bottom: 1px solid #e8edf3; }
.sec { margin: 4pt 0 1pt; font-weight: 700; color: #2563eb; break-after: avoid; }
ul { margin: 0; padding-left: 14pt; } li { margin: 0 0 1.6pt; break-inside: avoid; }
.para { margin: 0 0 3pt; }
.num { background: #fef3c7; border-radius: 2pt; padding: 0 1.5pt; }
.en { font-family: Inter; font-size: 8.4pt; color: #1d4ed8; }
.end { margin-top: 4pt; padding-top: 4pt; border-top: 1px dashed #dbe3ee; color: #065f46; }
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ft", required=True)
    ap.add_argument("--cti", required=True)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    cards = []
    for tag, d in (("FT", a.ft), ("CTI", a.cti)):
        for k, r in enumerate(runs(d)):
            c = parse(r); c["id"] = f"{tag}{k + 1:02d}"; c["src"] = "উৎস: SO26 Final Touch" if tag == "FT" else "উৎস: CTI Based Focus Writing (SO-26)"
            c["title"] = TITLE_FIX.get(c["id"], c["title"])
            cards.append(c)
    if a.list:
        for c in cards:
            print(c["id"], "|", c["title"][:70], "| g", len(c["glance"]), "s", [len(p) for _, p, _ in c["sections"]], "e", len(c["end"]))
        return
    cards = [c for c in cards if c["id"] not in SKIP] + EXTRA_CARDS
    for c in cards:
        c["tier"], c["score"] = RANK.get(c["id"], (3, 0))
    cards.sort(key=lambda c: (c["tier"], -c["score"]))
    json.dump(cards, open(os.path.join(ROOT, "data", "focus_writing_bangla.json"), "w"), ensure_ascii=False, indent=1)
    names = {1: "স্তর ১ · সবচেয়ে গুরুত্বপূর্ণ (★★★) — আগে এগুলো", 2: "স্তর ২ · গুরুত্বপূর্ণ (★★)", 3: "স্তর ৩ · সময় থাকলে (★)"}
    toc = "".join(f'<div><b>{i + 1}</b>{e(c["title"])} <i>{"★" * (4 - c["tier"])}</i></div>' for i, c in enumerate(cards))
    body, last = "", 0
    for i, c in enumerate(cards):
        if c["tier"] != last:
            body += f'<h2 class="tier">{names[c["tier"]]}</h2>'; last = c["tier"]
        body += card(i + 1, c, c["tier"])
    n1 = sum(c["tier"] == 1 for c in cards)
    cover = f"""<section class="cover"><div class="tag">SO Written · 27 November 2026 · Focus Writing (Bangla)</div>
<h1>ফোকাস রাইটিং — সম্পূর্ণ বাংলা মুখস্থ সংস্করণ</h1>
<div class="sub">তিনটি বইয়ের ({len(cards)}টি টপিক) শুধু তথ্য ও মূল লাইন: <b>SO26 Final Touch</b> (নভেম্বর ২০২৬), <b>CTI Based Focus Writing</b> (৩২৪ পাতা) ও <b>SO-26 English Focus</b>। একই টপিক একাধিক বইয়ে থাকলে নতুনটি (Final Touch) রাখা হয়েছে। সাজানো হয়েছে <b>সবচেয়ে গুরুত্বপূর্ণ থেকে কম গুরুত্বপূর্ণ</b> ক্রমে। কঠিন শব্দের ইংরেজি <span class="en">(নীল ব্র্যাকেটে)</span>, মুখস্থ করার সংখ্যা <span class="num">হলুদ</span>।</div>
<div class="how"><b>পড়ার নিয়ম:</b> প্রথমে স্তর ১-এর {n1}টি টপিক (লাল দাগ)। প্রতিটি কার্ড: ভূমিকার লাইন → একনজরে তথ্যের ৫–৬টি সংখ্যা → প্রতিটি অংশের পয়েন্টের নাম → উপসংহার। পরীক্ষায়: ভূমিকা (৩–৪ লাইন) + একটি ছোট টেবিল + ৩–৪টি হেডিংয়ে পয়েন্ট (প্রতিটিতে একটি সংখ্যা) + উপসংহার। অজানা টপিক এলে কাছাকাছি কার্ডের সংখ্যা ও পয়েন্ট ব্যবহার করুন।<br><b>গুরুত্ব নির্ধারণ:</b> ব্যাংকিং-অর্থনীতি ও নভেম্বর ২০২৬-এর সবচেয়ে আলোচিত ঘটনা (রোহিঙ্গা রায়, এলডিসি ২০২৯, কপ-৩১, খেলাপি ঋণ, ব্যাংক একীভূতকরণ, ডিজিটাল ব্যাংক, মূল্যস্ফীতি) আগে; বিগত SO প্রশ্নের ধরন, অনলাইন সাজেশন ও রিপোর অনুমান মিলিয়ে।</div>
<div class="toc">{toc}</div></section>"""
    doc = f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><title>Focus Writing Bangla</title><style>{CSS.replace("__BN__", FONT_BN)}</style></head><body>{cover}{body}</body></html>'
    hp = OUT_PDF.replace(".pdf", ".html")
    open(hp, "w", encoding="utf-8").write(doc)
    js = os.path.join(ROOT, "final_pdfs", ".mkbn.js")
    open(js, "w").write(r"""const { chromium } = require("playwright");
(async () => { const [inp, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
 await p.goto("file://" + inp); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;text-align:center;font-family:Inter,Arial;font-size:7.5px;color:#64748b">Focus Writing (Bangla) · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
 await b.close(); })().catch((e) => { console.error(e); process.exit(1); });""")
    try:
        subprocess.run(["node", js, hp, OUT_PDF], check=True, cwd=ROOT)
    finally:
        os.remove(js); os.remove(hp)
    print("cards:", len(cards), "→", OUT_PDF)


if __name__ == "__main__":
    main()
