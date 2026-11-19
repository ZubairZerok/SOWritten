#!/usr/bin/env python3
"""data/*.json + catalog থেকে docs/-এর স্বয়ংক্রিয় ফাইলগুলো তৈরি করে।
data/ ফাইল বদলালে আবার চালান:  python3 engine/build_docs.py
(হাতে লেখা ফাইল — 01, 02, 07, 09, 10, 11 — এটি স্পর্শ করে না)"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from catalog import CATALOG, SECTION_NAMES  # noqa: E402

D = os.path.join(ROOT, "docs")
BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
AUTO = "<!-- স্বয়ংক্রিয়ভাবে তৈরি: engine/build_docs.py — সরাসরি এডিট না করে data/*.json বদলান -->\n\n"


def load(n):
    return json.load(open(os.path.join(ROOT, "data", n), encoding="utf-8"))


def write(name, text):
    with open(os.path.join(D, name), "w", encoding="utf-8") as f:
        f.write(AUTO + text.strip() + "\n")
    print("লেখা হলো:", "docs/" + name)


def plan_doc():
    p = load("plan.json")
    e = p["exam"]
    out = [f"# ০৩ · ৮ দিনের রুটিন (আজ থেকে পরীক্ষা পর্যন্ত)\n",
           f"**পরীক্ষা:** {e['date'].translate(BN)}, {e['time'].translate(BN)}, {str(e['marks']).translate(BN)} নম্বর। যাচাই: {e['verify']}\n",
           "প্রতিদিন সকালে `python3 engine/so.py` চালান। সেদিনের কাজ আর কত দিন বাকি, দুটোই দেখাবে।\n",
           "## প্রতিদিনের বাধ্যতামূলক কাজ (যে দিনই হোক)\n"]
    out += [f"- {x}" for x in p["daily_core"]]
    for d in p["days"]:
        out.append(f"\n## {d['title']} — {d['date'].translate(BN)}\n")
        out.append("| সময় | অংশ | কাজ | কোথা থেকে |\n|---|---|---|---|")
        for t, s, task, ref in d["blocks"]:
            out.append(f"| {t} | {s} | {task} | `{ref}` |")
    out.append("\n## নিয়ম\n- পড়ার চেয়ে **লেখা** বেশি করবেন: প্রতিটি সেশনের অন্তত অর্ধেক সময় হাতে লিখবেন।\n"
               "- রাত ১২টার পর পড়বেন না, কারণ পরীক্ষা সকাল ৯:৩০-এ। শরীরের ঘড়ি সকালের জন্য তৈরি রাখুন।\n"
               "- প্রতিটি কাজ শেষে লগ করুন (`so.py log ARG 1`), আর রাতে `so.py stats` দেখে নিন।")
    write("03_8_day_plan.md", "\n".join(out))


def topic_doc():
    t = load("topics.json")["topics"]
    facts = load("facts.json")["facts"]
    out = ["# ০৪ · টপিক ব্যাংক: সম্ভাব্য ১০টি ফোকাস/আর্গুমেন্ট বিষয়\n",
           "প্রতিটি কার্ডে আছে: প্রশ্ন যেভাবে আসতে পারে, বাংলা ও ইংরেজি উপশিরোনাম, ডেটা বক্সের সংখ্যা, সমাধান আর রিপোর ভেতরের উৎস।",
           "টার্মিনালে দেখতে: `python3 engine/so.py topic N`\n",
           "| # | টপিক | সম্ভাবনা |\n|---|---|---|"]
    out += [f"| {str(x['n']).translate(BN)} | {x['bn']} | {x['prob']} |" for x in t]
    for x in t:
        out.append(f"\n---\n\n## {str(x['n']).translate(BN)}. {x['bn']}\n\n*{x['en']}* · সম্ভাবনা: **{x['prob']}**\n")
        out.append("**প্রশ্ন যেভাবে আসতে পারে:** " + " · ".join(x["variants"]) + "\n")
        out.append("| বাংলা উপশিরোনাম | English sub-heading |\n|---|---|")
        bn_, en_ = x["outline_bn"], x["outline_en"]
        for i in range(max(len(bn_), len(en_))):
            out.append(f"| {bn_[i] if i < len(bn_) else ''} | {en_[i] if i < len(en_) else ''} |")
        out.append(f"\n**কোটেশন:** {x['quote']}\n\n**ডেটা বক্স:**\n")
        for f in facts:
            if f["topic"] in x["facts"]:
                out.append(f"- {f['bn']}  \n  _{f['en']}_ `[{f['src']}]`")
        out.append("\n**সমাধান/সুপারিশ:**\n")
        out += [f"- {s}" for s in x["solutions"]]
        out.append("\n**রিপোর উৎস:**\n")
        for sid in x["sources"]:
            pdf = next((c[2] for c in CATALOG if os.path.splitext(os.path.basename(c[2]))[0] == sid), sid)
            out.append(f"- `{pdf}`")
    write("04_topic_bank.md", "\n".join(out))


def arg_doc():
    a = load("arguments.json")
    out = ["# ০৫ · আর্গুমেন্ট প্লেবুক (৪০ নম্বর)\n",
           "## কাঠামো (প্রতিবার এটাই)\n"]
    out += [f"{x}" for x in a["template_en"]]
    out.append("\n**শব্দসীমা:** ৩৫০–৪৫০ শব্দ, সময় ২০–২২ মিনিট। প্রতিটি যুক্তির শুরুতে একটি **বোল্ড টপিক সেন্টেন্স** দিন, কারণ পরীক্ষক স্ক্যান করে পড়েন।\n")
    out.append("## অবস্থান বাছাইয়ের নিয়ম\n- \"only\", \"always\", \"best\", \"all\" জাতীয় চরম দাবি এলে বেশিরভাগ ক্ষেত্রে **partly agree** নিন, কারণ এতে দুই পক্ষ দেখিয়ে বেশি নম্বর পাওয়া যায়।\n"
               "- নীতিগত প্রশ্নে (যেমন subsidy, merger) **শর্তসাপেক্ষ সমর্থন** নিন: \"Yes, but only if ...\"\n"
               "- অবস্থান ভূমিকাতেই স্পষ্ট লিখবেন, আর উপসংহারে তা থেকে সরবেন না।\n")
    out.append("## উপযোগী বাক্যাংশ\n")
    out += [f"- {p}" for p in a["phrases"]]
    out.append("\n## অনুশীলনের প্রম্পট (`so.py arg N --timer`)\n")
    for i, p in enumerate(a["prompts"], 1):
        out.append(f"### {i}. \"{p['claim']}\"\n- **পক্ষে:** {'; '.join(p['pro'])}\n- **বিপক্ষে:** {'; '.join(p['con'])}\n- **সম্ভাব্য অবস্থান:** {p['verdict']}\n")
    out.append("## রিপোর উৎস\n- `materials/02_argument_writing/Argument_Writing_Technique_Sheet_1.pdf`\n"
               "- `materials/02_argument_writing/PDF48_Argumentative_Writing_Technique_2.pdf` (পূর্ণ নমুনা উত্তর)")
    write("05_argument_playbook.md", "\n".join(out))


def tr_doc():
    t = load("translation.json")
    out = ["# ০৬ · বাংলা → ইংরেজি অনুবাদ (২০ নম্বর)\n", "## কৌশল\n"]
    out += [f"- {x}" for x in t["tips"]]
    out.append("\n## পরিভাষা (মুখস্থ)\n\n| বাংলা | English |\n|---|---|")
    out += [f"| {b} | {e} |" for b, e in t["glossary"]]
    out.append("\n## ড্রিল: আগে নিজে লিখুন, তারপর মিলান (`so.py tr`)\n")
    for i, d in enumerate(t["drills"], 1):
        out.append(f"{i}. {d['bn']}\n   <details><summary>উত্তর</summary>{d['en']}</details>\n")
    out.append("\n**বাড়তি অনুশীলন:** নিজের লেখা বাংলা ফোকাসের ২টি অনুচ্ছেদ প্রতিদিন ইংরেজিতে অনুবাদ করবেন।")
    write("06_translation.md", "\n".join(out))


def terms_doc():
    t = load("terms.json")["terms"]
    f = load("facts.json")["facts"]
    out = ["# ০৮ · ব্যাংকিং পরিভাষা ও সাম্প্রতিক তথ্য (ব্যাংকিং ১০ + GK ১০)\n",
           f"মোট {str(len(t)).translate(BN)}টি পরিভাষা। কুইজ: `python3 engine/so.py terms --quiz 15`\n",
           "| সংক্ষেপ | পূর্ণরূপ | এক লাইনে |\n|---|---|---|"]
    out += [f"| **{k}** | {full} | {d} |" for k, full, d in t]
    out.append("\n## সাম্প্রতিক তথ্য (GK + রচনার ডেটা বক্স)\n\n| ট্যাগ | তথ্য | উৎস |\n|---|---|---|")
    out += [f"| {x['topic']} | {x['bn']} | {x['src']} |" for x in f]
    write("08_banking_terms.md", "\n".join(out))


def resource_doc():
    idx = {}
    ip = os.path.join(ROOT, "corpus", "index.json")
    if os.path.exists(ip):
        idx = {d["pdf"]: d for d in json.load(open(ip, encoding="utf-8"))}
    out = ["# ১৩ · রিসোর্স ইনডেক্স: রিপোর প্রতিটি PDF\n",
           "অগ্রাধিকার: **১** = অবশ্যই · **২** = সময় থাকলে · **৩** = বাদ দিলেও চলে। সার্চযোগ্য টেক্সট পাবেন `corpus/`-এ।\n",
           "অংশ কোড: " + ", ".join(f"`{k}` {v}" for k, v in SECTION_NAMES.items()) + "\n"]
    folder = None
    for _d, _s, path, title, secs, prio, lang, strat in sorted(CATALOG, key=lambda c: (os.path.dirname(c[2]), c[5])):
        fd = os.path.dirname(path)
        if fd != folder:
            folder = fd
            out.append(f"\n## `{fd}/`\n\n| অগ্রা. | ফাইল | অংশ | পৃষ্ঠা | কৌশল |\n|---|---|---|---|---|")
        pg = idx.get(path, {}).get("pages", "")
        txt = idx.get(path, {}).get("text")
        name = f"[{os.path.basename(path)}](../{path})" + (f" · [টেক্সট](../{txt})" if txt else "")
        out.append(f"| {str(prio).translate(BN)} | {title}<br>{name} | {', '.join(secs)} | {str(pg).translate(BN)} | {strat} |")
    write("13_resource_index.md", "\n".join(out))


FORMULAS = """
## সূত্র-শিট (পরীক্ষার আগের রাতে শুধু এটা)

| অধ্যায় | সূত্র / কৌশল |
|---|---|
| শতকরা | x% বৃদ্ধির পর y% হ্রাস → নিট পরিবর্তন = x − y − xy/100 · মূল্য x% বাড়লে ব্যবহার কমাতে হবে x/(100+x) × 100% |
| লাভ-ক্ষতি | লাভ% = লাভ/ক্রয়মূল্য × 100 · বিক্রয়মূল্য = ক্রয়মূল্য × (100 ± লাভ/ক্ষতি%)/100 · ছাড়: বিক্রয়মূল্য = লিখিত মূল্য × (100 − ছাড়%)/100 |
| সরল সুদ | I = Pnr/100 · A = P + I |
| চক্রবৃদ্ধি | A = P(1 + r/100)ⁿ · ষাণ্মাসিক হলে r/2, 2n · CI − SI (২ বছর) = P(r/100)² |
| অনুপাত/অংশীদারি | লাভ ভাগ ∝ মূলধন × সময় · a:b ও b:c থেকে a:b:c = ab' : bb' : bc' মিলিয়ে |
| সময় ও কাজ | ১ দিনে কাজ = 1/দিন · একসাথে: 1/A + 1/B · নল: ভরে (+), খালি করে (−) · M₁D₁H₁/W₁ = M₂D₂H₂/W₂ |
| গতি | দূরত্ব = গতি × সময় · km/h → m/s: ×5/18 · গড় গতি (সমান দূরত্ব) = 2xy/(x+y) · ট্রেন: অতিক্রম দূরত্ব = ট্রেন + প্ল্যাটফর্ম · বিপরীত দিকে আপেক্ষিক গতি = যোগফল, একই দিকে = বিয়োগফল |
| নৌকা-স্রোত | স্রোতের অনুকূলে = u + v, প্রতিকূলে = u − v · নৌকার বেগ = (অনুকূল + প্রতিকূল)/2 |
| মিশ্রণ | Alligation: (দামি − গড়) : (গড় − সস্তা) = সস্তা : দামি · বারবার তুলে প্রতিস্থাপন: বাকি = মোট × (1 − x/মোট)ⁿ |
| ধারা | n-তম পদ = a + (n−1)d · যোগফল = n/2 [2a + (n−1)d] · গুণোত্তর: arⁿ⁻¹, a(rⁿ−1)/(r−1) |
| জ্যামিতি | আয়তক্ষেত্র ক্ষেত্রফল = দৈর্ঘ্য × প্রস্থ, পরিসীমা = 2(l+b) · ত্রিভুজ = ½ভূমি×উচ্চতা, সমবাহু = √3/4 a² · বৃত্ত = πr², পরিধি = 2πr · পিথাগোরাস · ঘনক = a³, বেলন = πr²h |
| সম্ভাবনা | P = অনুকূল/মোট · nPr = n!/(n−r)! · nCr = n!/(r!(n−r)!) · "অন্তত একটি" = 1 − কোনোটিই না |
| গড় ও বয়স | গড় = যোগফল/সংখ্যা · নতুন সদস্য যোগ হলে গড়ের পরিবর্তন × মোট সংখ্যা · বয়সের অঙ্ক: বর্তমান বয়স x ধরে "n বছর আগে/পরে" সমীকরণ |
"""


def math_doc():
    p = os.path.join(ROOT, "data", "math_bank.json")
    if not os.path.exists(p):
        return
    mb = json.load(open(p, encoding="utf-8"))
    ch, qs = mb["chapters"], mb["questions"]
    out = ["# ০৭ · গণিত প্লেবুক (৩০ নম্বর, সাধারণত ৫টি প্রশ্ন × ৬)\n",
           f"রিপোর গণিতের PDF থেকে **{str(len(qs)).translate(BN)}টি লিখিত প্রশ্ন** আলাদা করে অধ্যায়ভিত্তিক ব্যাংক বানানো হয়েছে (`data/math_bank.json`)।",
           "নিচের টেবিলে **২০১৫ বা পরের পরীক্ষায় আসা প্রশ্নের সংখ্যা** অনুযায়ী অধ্যায় সাজানো আছে। এটাই পড়ার ক্রম।\n",
           "| ক্রম | অধ্যায় | ব্যাংকে মোট | ২০১৫+ পরীক্ষায় | SO ট্যাগ | ড্রিল কমান্ড |\n|---|---|---|---|---|---|"]
    for i, c in enumerate([c for c in ch if c["count"]], 1):
        out.append(f"| {str(i).translate(BN)} | {c['bn']} | {str(c['count']).translate(BN)} | {str(c['recent_2015plus']).translate(BN)} | "
                   f"{str(c['so_tagged']).translate(BN)} | `so.py math {c['key']}` |")
    out.append("\n> গণনা স্বয়ংক্রিয়, OCR থেকে নেওয়া। পরীক্ষার ট্যাগ পড়া না গেলে প্রশ্নটা \"২০১৫+\" কলামে গোনা হয়নি। ধারাটা নির্ভরযোগ্য, তবে প্রতিটি সংখ্যা হুবহু ধরে নেবেন না।\n")
    out.append("## ৭ দিনের গণিত পরিকল্পনা (মোট ৬০টি অঙ্ক)\n\n| দিন | অধ্যায় | উৎস | সংখ্যা |\n|---|---|---|---|\n"
               "| ১ | শতকরা + লাভ-ক্ষতি | `khairul/01_Percentage.pdf`, `topic_sheets/PDF45_Profit_Loss.pdf` | ১০ |\n"
               "| ২ | বীজগণিত/সমীকরণ + বয়স | `khairul/02_Algebra.pdf`, `topic_sheets/PDF16_Formation_of_Equation.pdf` | ১০ |\n"
               "| ৩ | সুদ + ধারা | `topic_sheets/PDF14_Compound_Interest.pdf`, `khairul/05_Arithmetic_Progression.pdf` | ১০ |\n"
               "| ৪ | সময়-কাজ + গতি/ট্রেন + জ্যামিতি | `khairul/03_Time_Work.pdf`, `khairul/04_Time_Speed.pdf`, `topic_sheets/PDF33_Geometry.pdf` | ১০ |\n"
               "| ৫ | মক + অনুপাত/মিশ্রণ | `topic_sheets/PDF30/31`, `khairul/06_Mixture.pdf` | ৮ |\n"
               "| ৬ | BIBM সাম্প্রতিক মিশ্র (২০২২–২৩) | `question_bank/BIBM_Previous_All_Written_Math_Solution.pdf` | ১০ |\n"
               "| ৭ | ভুলের খাতা + সূত্র | নিজের খাতা | ২–৪ |\n")
    out.append("## নিয়ম\n- ক্যালকুলেটর ছাড়া, **প্রতিটি ধাপ লিখে** করবেন।\n- ৬ মিনিটে না মিললে সমাধান দেখুন, তারপর পরদিন অঙ্কটা আবার নিজে করুন।\n"
               "- ২০২৬ থেকে প্রশ্ন ইংরেজিতে আসছে, তাই প্রশ্নের শব্দ (per annum, alloy, cistern, downstream) চিনে রাখুন।\n"
               "- উত্তর বক্স করুন আর একক লিখুন।")
    out.append(FORMULAS)
    recent = sorted([q for q in qs if (q.get("latest_year") or 0) >= 2019], key=lambda q: -(q["latest_year"] or 0))[:40]
    out.append(f"\n## সাম্প্রতিক (২০১৯+) ট্যাগযুক্ত প্রশ্ন ({str(len(recent)).translate(BN)}টি): আগে এগুলো করুন\n")
    for i, q in enumerate(recent, 1):
        out.append(f"{i}. {q['text']}  \n   _[{q['exam']}] · {q['chapter']} · {q['source']} p{q['page']}_" + (f" · **Ans: {q['answer']}**" if q.get("answer") else ""))
    write("07_math_playbook.md", "\n".join(out))


if __name__ == "__main__":
    os.makedirs(D, exist_ok=True)
    plan_doc(); topic_doc(); arg_doc(); tr_doc(); terms_doc(); resource_doc(); math_doc()
