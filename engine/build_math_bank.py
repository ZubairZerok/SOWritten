#!/usr/bin/env python3
"""
গণিতের সব PDF-এর টেক্সট (corpus/.cache) থেকে লিখিত প্রশ্ন আলাদা করে data/math_bank.json বানায়:
প্রশ্ন, অধ্যায়, পরীক্ষার ট্যাগ (যেমন [BB AD 2022]), উত্তর (থাকলে), উৎস PDF ও পৃষ্ঠা।
এরপর অধ্যায়ভিত্তিক ফ্রিকোয়েন্সি দিয়ে docs/07_math_playbook.md-এর টেবিল তৈরি হয়।
"""
import collections, glob, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "corpus", ".cache")
BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

# (key, বাংলা নাম, অগ্রাধিকার, keyword regex)
CHAPTERS = [
    ("profit_loss", "লাভ-ক্ষতি", 1, r"profit|loss|cost price|selling price|discount|marked price|commission|sold .* at|bought"),
    ("interest", "সুদ (সরল ও চক্রবৃদ্ধি)", 1, r"interest|compound|principal|per annum|deposit(ed)? in a bank|invest(ed|ment)? .* rate"),
    ("percentage", "শতকরা", 1, r"percent|%"),
    ("ratio", "অনুপাত ও অংশীদারি", 2, r"ratio|proportion|partner|share[sd]? .* (profit|ratio)|divided among"),
    ("work", "সময় ও কাজ / নল-চৌবাচ্চা", 2, r"work|job|pipe|tank|cistern|fill|empty|days to (do|finish|complete)"),
    ("speed", "গতি, ট্রেন, নৌকা-স্রোত", 2, r"speed|km/h|kmph|mph|km ?/ ?hr|train|boat|stream|current|distance|travel|miles|kilomet"),
    ("mixture", "মিশ্রণ", 2, r"mixture|mixed|alloy|solution .* (water|milk|acid|alcohol)|milk and water|concentration|alcohol"),
    ("average", "গড়", 2, r"average|mean"),
    ("age", "বয়স", 2, r"\bage[sd]?\b|years old|older|younger"),
    ("series", "ধারা", 1, r"series|progression|sequence|term of|sum of (the )?first|consecutive"),
    ("geometry", "জ্যামিতি ও ক্ষেত্রফল", 1, r"area|perimeter|triangle|circle|radius|diameter|rectangle|square (field|room|garden|plot)|volume|cube|cylinder|cone|sphere|angle|hypotenuse|rhombus|parallelogram|trapezium|floor|carpet|fence"),
    ("probability", "সম্ভাবনা ও বিন্যাস-সমাবেশ", 2, r"probabilit|chance|dice|die\b|coin|card|permutation|combination|arrange|ways|committee|selected|draw[n]?"),
    ("set", "সেট/ভেন চিত্র", 3, r"\bset\b|venn|both .* and|neither|only .* (english|bangla|tea|coffee)"),
    ("algebra", "বীজগণিত ও সমীকরণ", 1, r"equation|x\s*[+\-=]|value of [xyabpq]|\bx\b|\by\b|sum of two numbers|digit|fraction|number|integer|square root|root"),
]
SOURCE_CHAPTER = {"01_Percentage": "percentage", "02_Algebra": "algebra", "03_Time_Work": "work", "04_Time_Speed": "speed",
                  "05_Arithmetic_Progression": "series", "06_Mixture": "mixture", "07_Boat_Stream": "speed", "08_Unitary_Method": "work",
                  "PDF45_Profit_Loss": "profit_loss", "PDF16_Formation_of_Equation": "algebra", "PDF14_Compound_Interest": "interest",
                  "PDF30_Ratio_Proportion": "ratio", "PDF31_Partnership": "ratio", "PDF32_Probability": "probability",
                  "PDF33_Geometry": "geometry", "PDF46_Time_Work": "work", "PDF60_Mixture": "mixture",
                  "PDF61_Time_Speed_Distance": "speed", "PDF62_Problem_on_Train": "speed"}
BOOKS = ["Bank_Written_Math_1986-2021", "BIBM_Previous_All_Written_Math_Solution"]

QSTART = re.compile(r"^\s*(?:Q\.?\s*)?(\d{1,4})\s*[.)]\s+([A-Z(].{15,})$")
STOP = re.compile(r"^\s*(Solution|Soln|Sol\s*[:.]|Ans(wer)?\s*[:.]|অনুবাদ|সমাধান|Given that|Let\b|Self Task|Shortcut|Explanation)", re.I)
TAGRE = re.compile(r"[\[{]([^\[\]{}]{3,140}?(?:(?:19|20)\d\d|\b\d\d\b)[^\[\]{}]{0,40})(?:[\]}]|$)")
EXAMWORD = re.compile(r"\b(Bank|BB|SO|Officer|AD|PO|MTO|Cash|BIBM|Combined|BCS|HBFC|BHBFC|RAKUB|BKB|BDBL|PKB|ICB|EO|TSO|JO|AEO|Written)\b", re.I)
YR = re.compile(r"\b((?:19|20)\d\d|\d\d)\b")


def exam_years(tag):
    ys = []
    for y in YR.findall(tag or ""):
        y = int(y)
        ys.append(y if y > 100 else (2000 + y if y <= 26 else 1900 + y))
    return ys
ANS = re.compile(r"Ans(?:wer)?\s*[:.]\s*(.{1,60})$", re.I)
ASK = re.compile(r"\?|\b(find|what|how|calculate|determine|show|prove|compute|which|whom|when)\b", re.I)


def classify(text, src):
    if src in SOURCE_CHAPTER:
        return SOURCE_CHAPTER[src]
    t = text.lower()
    order = ["mixture", "interest", "profit_loss", "probability", "speed", "work", "ratio", "average", "age", "series",
             "geometry", "set", "percentage", "algebra"]
    for key, _bn, _p, pat in sorted(CHAPTERS, key=lambda c: order.index(c[0])):
        if re.search(pat, t):
            return key
    return "algebra"


def tidy(s):
    s = re.sub(r"[ঀ-৿]+[ঀ-৿\s,।-]*", " ", s)  # মার্জিনের বাংলা লেবেল/অনুবাদ বাদ
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip(" |_—-")


def parse_file(src, page, raw):
    lines = re.sub(r"<!--method:\w+-->", "", unicodedata.normalize("NFC", raw)).splitlines()
    qs, cur = [], None

    def flush():
        if cur:
            body = " ".join(cur["lines"])
            ans = None
            m = ANS.search(body)
            if m:
                ans = m.group(1).strip()
                body = body[: m.start()]
            body = re.split(r"\s(?:Solution|Soln|Hints?)\s*[:.]|CamScanner", body)[0]
            tags = [t.strip(" +") for t in TAGRE.findall(body) if EXAMWORD.search(t)]
            tags = [re.split(r";\s*Hints?", t)[0] for t in tags if not re.match(r"\s*Hints?", t)]
            if ans and not re.search(r"\d", ans):
                ans = None
            body = TAGRE.sub(" ", body)
            body = re.sub(r"[+/]?\s*\[?\s*/?\b[\w.]+\.(com|in|org|net)\]?", " ", body)
            body = tidy(body)
            if 40 <= len(body) <= 700 and ASK.search(body) and len(re.findall(r"[A-Za-z]", body)) > 0.5 * len(body.replace(" ", "")):
                qs.append({"text": body, "exam": "; ".join(t.strip() for t in tags), "answer": ans,
                           "source": src, "page": page, "chapter": classify(body, src)})

    for ln in lines:
        m = QSTART.match(ln)
        if m:
            flush()
            cur = {"lines": [m.group(2)]}
            continue
        if cur is None:
            continue
        if STOP.match(ln) and not ANS.search(ln):
            flush(); cur = None
            continue
        if not ln.strip():
            if len(cur["lines"]) > 1 and cur["lines"][-1] == "":
                flush(); cur = None
            else:
                cur["lines"].append("")
            continue
        cur["lines"].append(ln.strip())
        if ANS.search(ln):
            flush(); cur = None
    flush()
    return qs


def main():
    srcs = BOOKS + list(SOURCE_CHAPTER)
    allq, seen = [], set()
    for src in srcs:
        for f in sorted(glob.glob(os.path.join(CACHE, src, "p*.txt"))):
            page = int(re.search(r"p(\d+)", os.path.basename(f)).group(1))
            for q in parse_file(src, page, open(f, encoding="utf-8").read()):
                k = re.sub(r"[^a-z0-9]", "", q["text"].lower())[:70]
                if k in seen:
                    continue
                seen.add(k)
                allq.append(q)
    cnt = collections.Counter(q["chapter"] for q in allq)
    for q in allq:
        ys = exam_years(q["exam"])
        q["latest_year"] = max(ys) if ys else None
    recent = collections.Counter(q["chapter"] for q in allq if (q["latest_year"] or 0) >= 2015)
    so = collections.Counter(q["chapter"] for q in allq if re.search(r"\bSO\b|Senior", q["exam"] or ""))
    chapters = [{"key": k, "bn": b, "priority": p, "count": cnt.get(k, 0), "recent_2015plus": recent.get(k, 0), "so_tagged": so.get(k, 0)}
                for k, b, p, _ in CHAPTERS]
    chapters.sort(key=lambda c: (-c["recent_2015plus"], -c["count"]))
    out = {"_note": "OCR/টেক্সট থেকে স্বয়ংক্রিয় — engine/build_math_bank.py। প্রশ্নে OCR ভুল থাকতে পারে; উৎস পৃষ্ঠায় মিলিয়ে নিন।",
           "chapters": chapters, "questions": allq}
    json.dump(out, open(os.path.join(ROOT, "data", "math_bank.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(allq)} প্রশ্ন → data/math_bank.json")
    for c in chapters:
        print(f"  {c['key']:<12} মোট {c['count']:>4}  ২০১৫+ {c['recent_2015plus']:>3}  SO {c['so_tagged']:>3}")
    by_src = collections.Counter(q["source"] for q in allq)
    print(dict(by_src))


if __name__ == "__main__":
    main()
