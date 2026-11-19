#!/usr/bin/env python3
"""
corpus থেকে বিগত পরীক্ষার ট্যাগসহ প্রশ্ন খুঁজে বের করে (যেমন "Role of Commercial Banks in SME [Combined 3 Banks SO — 2018]"),
বিষয়ভিত্তিক থিমে ভাগ করে data/past_questions.json ও docs/12_past_questions.md তৈরি করে।
OCR থেকে আসা — কিছু লাইন অসম্পূর্ণ/ভাঙা থাকতে পারে।
"""
import collections, glob, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "corpus", ".cache")
BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

WRITING_DOCS = ["A2B_Focus_Writing", "Unique_Bank_Focus_Writing_and_Essay", "Focus_Writing_Mini_Recent_Merged",
                "Focus_Writing_July_Edition", "PDF01_BIBM_Question_Analysis", "PDF48_Argumentative_Writing_Technique_2",
                "Argument_Writing_Technique_Sheet_1", "PDF02_Informative_Focus_Writing_Technique"]
MATH_DOCS = ["BIBM_Previous_All_Written_Math_Solution", "Bank_Written_Math_1986-2021"]

TAG = re.compile(r"[\[\(\{|]\s*([A-Za-z0-9 .,&/\-]*?(?:Bank|BB|BHBFC|BHFC|BDBL|RAKUB|BKB|PKB|BIBM|Combined|ICB|SBAC|Investment)"
                 r"[A-Za-z0-9 .,&/()\-]*?\b(?:SO|Senior Officer|Officer|AD|EO|PO|MTO|Cash|TACO|AEO)\b[^\]\)|]*?(?:19|20)\d\d)\s*[\]\)|]?")
YEAR = re.compile(r"((?:19|20)\d\d)")

THEMES = [
    ("banking", r"bank|ব্যাংক|loan|ঋণ|default|খেলাপি|interest rate|সুদ|capital|deposit|sme|credit|fintech|mfs|মোবাইল ব্যাংকিং|agent"),
    ("economy", r"econom|অর্থনী|gdp|budget|বাজেট|inflation|মূল্যস্ফীতি|price|দ্রব্যমূল্য|investment|বিনিয়োগ|export|রপ্তানি|import|remittance|রেমিট্যান্স|reserve|রিজার্ভ|ldc|এলডিসি|garment|পোশাক|poverty|দারিদ্র্য|self.?reliant"),
    ("technology", r"digital|ডিজিটাল|ict|তথ্যপ্রযুক্তি|technology|প্রযুক্তি|internet|cyber|সাইবার|artificial|satellite|স্যাটেলাইট|4ir|online"),
    ("environment", r"climate|জলবায়ু|environment|পরিবেশ|green|সবুজ|pollution|দূষণ|disaster|দুর্যোগ|plastic|energy|জ্বালানি|বিদ্যুৎ|urban|নগর"),
    ("social", r"women|নারী|youth|যুব|education|শিক্ষা|health|স্বাস্থ্য|food|খাদ্য|family|পরিবার|rohingya|রোহিঙ্গা|human rights|মানবাধিকার|employment|কর্মসংস্থান|drug|মাদক|corruption|দুর্নীতি"),
    ("global", r"global|বৈশ্বিক|world|middle east|মধ্যপ্রাচ্য|war|যুদ্ধ|globalization|bri|brics|new development bank|un\b|জাতিসংঘ"),
    ("letter_report", r"আবেদনপত্র|পত্র|প্রতিবেদন|letter|report|application"),
]


def nfc(s):
    return unicodedata.normalize("NFC", s)


def clean(s):
    s = re.sub(r"^[\s\d.|_\-–—•*>\]\[»«~:;,]+", "", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip(" .|_-—–")


def theme(text):
    t = text.lower()
    for name, pat in THEMES:
        if re.search(pat, t):
            return name
    return "other"


def exam_kind(tag):
    t = tag.lower()
    if re.search(r"\bso\b|senior officer", t):
        return "SO"
    if re.search(r"\bad\b", t):
        return "BB AD"
    if "officer" in t or re.search(r"\b(eo|aeo|po|mto)\b", t):
        return "Officer"
    if "cash" in t:
        return "Cash"
    return "Other"


def mine(docs, want_math=False):
    out, seen = [], set()
    for d in docs:
        for f in sorted(glob.glob(os.path.join(CACHE, d, "p*.txt"))):
            page = int(re.search(r"p(\d+)", os.path.basename(f)).group(1))
            lines = re.sub(r"<!--method:\w+-->", "", nfc(open(f, encoding="utf-8").read())).splitlines()
            for i, line in enumerate(lines):
                for m in TAG.finditer(line):
                    tag = m.group(1).strip()
                    text = line[: m.start()]
                    # প্রশ্নের লেখা আগের লাইনে ছড়িয়ে থাকলে জুড়ে নিই
                    if len(clean(text)) < 12 and i > 0:
                        text = lines[i - 1] + " " + text
                    text = clean(re.sub(r"\s\d{2,3}\s*$", "", text))
                    if len(text) < 8 or len(text) > 400:
                        continue
                    y = YEAR.findall(tag)
                    key = (re.sub(r"\W", "", text.lower())[:60], tag[:20])
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({"text": text, "tag": tag, "year": int(y[-1]) if y else None, "kind": exam_kind(tag),
                                "theme": "math" if want_math else theme(text), "source": d, "page": page})
    return out


def main():
    w = mine(WRITING_DOCS)
    m = mine(MATH_DOCS, want_math=True)
    json.dump({"_note": "OCR থেকে স্বয়ংক্রিয় — engine/mine_past_questions.py", "writing": w, "math_tagged": m},
              open(os.path.join(ROOT, "data", "past_questions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    th = collections.Counter(q["theme"] for q in w)
    th_so = collections.Counter(q["theme"] for q in w if q["kind"] == "SO")
    yrs = collections.Counter(q["year"] for q in w if q["year"])
    kinds = collections.Counter(q["kind"] for q in w)
    names = {"banking": "ব্যাংকিং ও আর্থিক খাত", "economy": "অর্থনীতি (মূল্যস্ফীতি, রপ্তানি, রেমিট্যান্স, এলডিসি)",
             "technology": "প্রযুক্তি ও ডিজিটাল", "environment": "পরিবেশ, জলবায়ু ও জ্বালানি", "social": "সামাজিক (নারী, শিক্ষা, স্বাস্থ্য, দুর্নীতি)",
             "global": "আন্তর্জাতিক/বৈশ্বিক", "letter_report": "চিঠি/প্রতিবেদন", "other": "অন্যান্য/শ্রেণিবিহীন"}
    o = ["<!-- স্বয়ংক্রিয়ভাবে তৈরি: engine/mine_past_questions.py -->\n",
         "# ১২ · বিগত লিখিত প্রশ্ন বিশ্লেষণ (রিপোর বই থেকে স্বয়ংক্রিয়ভাবে বের করা)\n",
         f"রিপোর ফোকাস বইগুলোতে পরীক্ষার ট্যাগসহ মোট **{str(len(w)).translate(BN)}টি** লিখিত প্রশ্ন পাওয়া গেছে "
         f"(SO: {str(kinds['SO']).translate(BN)}, Officer: {str(kinds['Officer']).translate(BN)}, BB AD: {str(kinds['BB AD']).translate(BN)})। "
         f"গণিতের বইয়ে ট্যাগসহ প্রশ্ন: **{str(len(m)).translate(BN)}টি**।\n",
         "> সীমাবদ্ধতা: বইগুলোর বেশিরভাগ প্রশ্ন ২০১২–২০১৯ সালের, আর OCR-এর কারণে কিছু লাইন ভাঙা। ২০২২–২০২৬-এর প্রশ্ন রিপোতে প্রায় নেই। "
         "সেগুলো যোগ করতে হবে, দেখুন [১০ · যা নেই](10_gap_analysis.md)।\n",
         "## থিম অনুযায়ী (কোন ধরনের বিষয় বেশি আসে)\n", "| থিম | সব পরীক্ষা | শুধু SO |\n|---|---|---|"]
    for k, v in th.most_common():
        o.append(f"| {names.get(k, k)} | {str(v).translate(BN)} | {str(th_so.get(k, 0)).translate(BN)} |")
    o.append("\n**শিক্ষা:** ব্যাংকিং ও অর্থনীতি মিলিয়ে সবচেয়ে বেশি প্রশ্ন এসেছে। তাই টপিক ব্যাংকের ১০টির মধ্যে ৭টিই এই দুই থিমের।\n")
    o.append("## বছর অনুযায়ী\n\n" + " · ".join(f"{str(y).translate(BN)}: {str(c).translate(BN)}" for y, c in sorted(yrs.items())) + "\n")
    for kind in ["SO", "Officer", "BB AD", "Cash", "Other"]:
        qs = sorted([q for q in w if q["kind"] == kind], key=lambda q: -(q["year"] or 0))
        if not qs:
            continue
        o.append(f"\n## {kind} পরীক্ষার প্রশ্ন ({str(len(qs)).translate(BN)}টি)\n\n| বছর | প্রশ্ন | পরীক্ষা | থিম | উৎস |\n|---|---|---|---|---|")
        for q in qs:
            t = q["text"].replace("|", "/")
            o.append(f"| {str(q['year'] or '').translate(BN)} | {t} | {q['tag']} | {q['theme']} | {q['source']} p{q['page']} |")
    with open(os.path.join(ROOT, "docs", "12_past_questions.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(o) + "\n")
    print(f"লেখা: {len(w)} লিখিত, {len(m)} গণিত-ট্যাগ → data/past_questions.json, docs/12_past_questions.md")
    print("থিম:", dict(th.most_common()))


if __name__ == "__main__":
    main()
