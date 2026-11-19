#!/usr/bin/env python3
"""
SO Written Intelligence Engine — সিনিয়র অফিসার লিখিত পরীক্ষার প্রস্তুতির কমান্ড-লাইন টুল।

  python3 engine/so.py                    # আজকের কাজ + কাউন্টডাউন (= today)
  python3 engine/so.py plan               # পুরো ৮ দিনের রুটিন
  python3 engine/so.py topic [n]          # সম্ভাব্য টপিক তালিকা / একটি টপিকের পূর্ণ কার্ড (কাঠামো + সংখ্যা + সমাধান + উৎস)
  python3 engine/so.py facts [ট্যাগ]      # রচনায় বসানোর সর্বশেষ সংখ্যা (inflation, npl, external, ldc, energy, digital ...)
  python3 engine/so.py terms [--quiz 15]  # ব্যাংকিং পরিভাষা / ফ্ল্যাশকার্ড কুইজ
  python3 engine/so.py essay [--topic n] [--lang bn|en] [--timer]   # রচনা অনুশীলন (১৮ মিনিট)
  python3 engine/so.py arg [n] [--timer]  # আর্গুমেন্ট প্রম্পট + টেমপ্লেট (২০ মিনিট)
  python3 engine/so.py tr [--all]         # বাংলা→ইংরেজি অনুবাদ ড্রিল
  python3 engine/so.py math [অধ্যায়] [-n 5] [--list]   # বিগত লিখিত গণিত প্রশ্ন থেকে র‍্যান্ডম ড্রিল
  python3 engine/so.py search "শব্দ" [-n 10] # সব PDF-এর টেক্সটে সার্চ (পৃষ্ঠা নম্বরসহ)
  python3 engine/so.py res [অংশ]          # কোন PDF কোন নম্বর কাভার করে (অগ্রাধিকারসহ)
  python3 engine/so.py mock [--writing]   # ২০০ নম্বরের মক প্রশ্নপত্র তৈরি
  python3 engine/so.py timer 18           # শুধু টাইমার
  python3 engine/so.py log MATH 10 "ভুল ২টি"  /  python3 engine/so.py stats   # অগ্রগতি লগ
"""
import argparse, csv, datetime as dt, glob, json, os, random, re, sys, time, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from catalog import CATALOG, SECTION_NAMES  # noqa: E402

DATA = os.path.join(ROOT, "data")
CORPUS = os.path.join(ROOT, "corpus")
LOG = os.path.join(ROOT, "progress", "log.csv")

BN_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
C = {"h": "\033[1;36m", "y": "\033[1;33m", "g": "\033[1;32m", "r": "\033[1;31m", "d": "\033[2m", "x": "\033[0m"}
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    C = {k: "" for k in C}


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def bn(n):
    return str(n).translate(BN_DIGITS)


def hr(title=""):
    print(f"\n{C['h']}━━ {title} {'━' * max(0, 60 - len(title))}{C['x']}")


def norm(s):
    return unicodedata.normalize("NFC", s).lower()


# ───────────────────────── today / plan ─────────────────────────
def days_left(plan, today):
    exam = dt.date.fromisoformat(plan["exam"]["date"])
    return (exam - today).days, exam


def cmd_today(a):
    plan = load("plan.json")
    today = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    left, exam = days_left(plan, today)
    e = plan["exam"]
    hr("SO লিখিত পরীক্ষা")
    print(f"পরীক্ষা: {bn(exam.isoformat())}  সময় {bn(e['time'])}  ({bn(e['marks'])} নম্বর, {bn(e['duration_min'])} মিনিট)")
    if left > 0:
        print(f"{C['y']}বাকি: {bn(left)} দিন{C['x']}   যাচাই: {e['verify']}")
    elif left == 0:
        print(f"{C['r']}আজই পরীক্ষা! শুভকামনা।{C['x']}")
    else:
        print("পরীক্ষা শেষ।")
    day = next((d for d in plan["days"] if d["date"] == today.isoformat()), None)
    if not day:
        future = [d for d in plan["days"] if d["date"] > today.isoformat()]
        day = future[0] if future else plan["days"][-1]
        print(f"{C['d']}(আজকের জন্য আলাদা রুটিন নেই — পরের দিনেরটা দেখাচ্ছি){C['x']}")
    show_day(day)
    hr("প্রতিদিনের বাধ্যতামূলক")
    for x in plan["daily_core"]:
        print("  •", x)
    hr("এখন কী করবেন? (অগ্রগতি × নম্বর অনুযায়ী)")
    for score, k, cmd, have, tgt in recommend()[:3]:
        print(f"  ▶ {SECTION_NAMES.get(k, k) if k in SECTION_NAMES else k}: {bn(have)}/{bn(tgt)} সম্পন্ন  →  python3 engine/{cmd}")
    done = today_log(today)
    if done:
        hr("আজ লগ করা হয়েছে")
        for k, v in done.items():
            print(f"  {k}: {bn(v)}")
    print(f"\n{C['d']}কাজ শেষে লগ করুন: python3 engine/so.py log MATH 10{C['x']}")


def show_day(day):
    hr(f"{day['title']}  [{bn(day['date'])}]")
    for t, sec, task, ref in day["blocks"]:
        print(f"  {C['g']}{t:>10}{C['x']}  [{sec}] {task}")
        print(f"  {'':>10}  {C['d']}→ {ref}{C['x']}")


def cmd_plan(a):
    plan = load("plan.json")
    for d in plan["days"]:
        show_day(d)


# ───────────────────────── topic / facts ─────────────────────────
def facts_for(tags):
    return [f for f in load("facts.json")["facts"] if f["topic"] in tags]


def cmd_topic(a):
    topics = load("topics.json")["topics"]
    if a.n is None:
        hr("সম্ভাব্য ফোকাস/আর্গুমেন্ট টপিক (অগ্রাধিকার ক্রমে)")
        for t in topics:
            print(f"  {bn(t['n']):>3}. [{t['prob']}] {t['bn']}")
            print(f"       {C['d']}{t['en']}{C['x']}")
        print(f"\n{C['d']}বিস্তারিত: python3 engine/so.py topic 1{C['x']}")
        return
    t = next((x for x in topics if x["n"] == a.n), None)
    if not t:
        sys.exit("এমন টপিক নেই")
    hr(f"টপিক {bn(t['n'])}: {t['bn']}")
    print(f"EN: {t['en']}\nসম্ভাবনা: {t['prob']}")
    print(f"\n{C['y']}প্রশ্ন যেভাবে আসতে পারে:{C['x']}")
    for v in t["variants"]:
        print("  •", v)
    print(f"\n{C['y']}বাংলা কাঠামো (উপশিরোনাম):{C['x']}")
    for i, o in enumerate(t["outline_bn"], 1):
        print(f"  {bn(i)}. {o}")
    print(f"\n{C['y']}English outline:{C['x']}")
    for i, o in enumerate(t["outline_en"], 1):
        print(f"  {i}. {o}")
    print(f"\n{C['y']}কোটেশন:{C['x']} {t['quote']}")
    print(f"\n{C['y']}ডেটা বক্সে বসানোর সংখ্যা:{C['x']}")
    for f in facts_for(t["facts"]):
        print(f"  • {f['bn']}\n    {C['d']}{f['en']}  [{f['src']}]{C['x']}")
    print(f"\n{C['y']}সমাধান/সুপারিশ:{C['x']}")
    for s in t["solutions"]:
        print("  ✓", s)
    print(f"\n{C['y']}রিপোর ভেতরের উৎস:{C['x']}")
    idx = corpus_index()
    for sid in t["sources"]:
        pdf = next((c[2] for c in CATALOG if os.path.splitext(os.path.basename(c[2]))[0] == sid), sid)
        txt = idx.get(sid, {}).get("text", "(টেক্সট এখনো তৈরি হয়নি)")
        print(f"  • {pdf}\n    {C['d']}টেক্সট: {txt}{C['x']}")


def cmd_facts(a):
    fs = load("facts.json")["facts"]
    tags = sorted({f["topic"] for f in fs})
    if a.tag and a.tag not in tags:
        sys.exit(f"ট্যাগ: {', '.join(tags)}")
    hr("সর্বশেষ সংখ্যা ও তথ্য" + (f" — {a.tag}" if a.tag else ""))
    for f in fs:
        if a.tag and f["topic"] != a.tag:
            continue
        print(f"  [{f['topic']}] {f['bn']}")
        if a.en:
            print(f"      {C['d']}{f['en']}{C['x']}")
    print(f"\n{C['d']}ট্যাগ: {', '.join(tags)} | ইংরেজি বাক্যসহ: --en | উৎস: data/facts.json{C['x']}")


# ───────────────────────── terms ─────────────────────────
def cmd_terms(a):
    terms = load("terms.json")["terms"]
    if a.find:
        q = norm(a.find)
        terms = [t for t in terms if q in norm(" ".join(t))]
    if not a.quiz:
        hr(f"ব্যাংকিং পরিভাষা ({bn(len(terms))}টি)")
        for k, full, d in terms:
            print(f"  {C['g']}{k}{C['x']} — {full}\n      {d}")
        return
    pool = random.sample(terms, min(a.quiz, len(terms)))
    score = 0
    hr(f"কুইজ: {bn(len(pool))}টি — পূর্ণরূপ মনে মনে বলুন, তারপর Enter চাপুন (q = থামুন)")
    for i, (k, full, d) in enumerate(pool, 1):
        ans = input(f"\n{bn(i)}. {C['y']}{k}{C['x']} = ? ")
        if ans.strip().lower() == "q":
            break
        print(f"   → {full}\n   {d}")
        ok = input("   ঠিক হয়েছিল? (y/n) ").strip().lower()
        score += ok.startswith("y")
    print(f"\nস্কোর: {bn(score)}/{bn(len(pool))}")
    append_log("GK_TERMS", len(pool), f"score {score}/{len(pool)}")


# ───────────────────────── timer ─────────────────────────
def run_timer(minutes, label=""):
    total = int(minutes * 60)
    print(f"\n{C['y']}⏱  {bn(minutes)} মিনিট শুরু {label} — থামাতে Ctrl+C{C['x']}")
    start = time.time()
    try:
        while True:
            el = time.time() - start
            rem = total - el
            if rem <= 0:
                break
            m, s = divmod(int(rem), 60)
            print(f"\r   বাকি {bn(f'{m:02d}:{s:02d}')}   ", end="", flush=True)
            time.sleep(1)
        print(f"\n{C['r']}⏰ সময় শেষ! কলম থামান।{C['x']}\a")
        return minutes
    except KeyboardInterrupt:
        used = (time.time() - start) / 60
        print(f"\nথামানো হয়েছে — {bn(round(used, 1))} মিনিট লেগেছে।")
        return used


def cmd_timer(a):
    run_timer(a.minutes)


# ───────────────────────── essay / arg / tr ─────────────────────────
def cmd_essay(a):
    topics = load("topics.json")["topics"]
    t = next((x for x in topics if x["n"] == a.topic), None) if a.topic else random.choice(topics)
    lang = a.lang or random.choice(["bn", "en"])
    title = t["bn"] if lang == "bn" else t["en"]
    if a.variant:
        title = random.choice(t["variants"])
    hr("রচনা অনুশীলন (৩০ নম্বর ≈ ১৮ মিনিট)")
    print(f"{C['y']}প্রশ্ন:{C['x']} {title}")
    print(f"\nচেকলিস্ট: ① শিরোনাম ② কোটেশনসহ ভূমিকা ③ ৫–৭টি উপশিরোনাম ④ ১টি ডেটা বক্স/টেবিল ⑤ সমাধান ⑥ উপসংহার")
    print(f"লক্ষ্য: {('বাংলায়' if lang == 'bn' else 'ইংরেজিতে')} ~২৫০–৩০০ শব্দ / ২.৫–৩ পৃষ্ঠা")
    print(f"{C['d']}কাঠামো ও সংখ্যা দেখতে (লেখার পরে!): python3 engine/so.py topic {t['n']}{C['x']}")
    if a.timer:
        used = run_timer(18, "(রচনা)")
        append_log(f"FW_{lang.upper()}", 1, f"topic {t['n']} {round(used, 1)}m")


def cmd_arg(a):
    d = load("arguments.json")
    ps = d["prompts"]
    p = ps[a.n - 1] if a.n else random.choice(ps)
    hr("আর্গুমেন্ট/অ্যানালিটিক্যাল (৪০ নম্বর ≈ ২০–২৪ মিনিট)")
    print(f"{C['y']}Claim:{C['x']} \"{p['claim']}\"")
    print("\nTemplate:")
    for x in d["template_en"]:
        print("  ", x)
    if a.timer:
        used = run_timer(22, "(আর্গুমেন্ট)")
        append_log("ARG", 1, f"{round(used, 1)}m")
    if a.timer or a.hints:
        print(f"\n{C['g']}পক্ষে:{C['x']}", "; ".join(p["pro"]))
        print(f"{C['r']}বিপক্ষে:{C['x']}", "; ".join(p["con"]))
        print(f"{C['y']}সম্ভাব্য অবস্থান:{C['x']}", p["verdict"])
        print(f"\nউপযোগী বাক্যাংশ: {' | '.join(random.sample(d['phrases'], 4))}")
    else:
        print(f"\n{C['d']}লেখার পরে পক্ষে/বিপক্ষে পয়েন্ট দেখতে: --hints{C['x']}")


def cmd_tr(a):
    d = load("translation.json")
    drills = d["drills"] if a.all else random.sample(d["drills"], 3)
    hr("বাংলা → ইংরেজি অনুবাদ (২০ নম্বর ≈ ১২ মিনিট)")
    for i, x in enumerate(drills, 1):
        print(f"\n{bn(i)}. {x['bn']}")
        if not a.all:
            input(f"   {C['d']}খাতায় লিখে Enter চাপুন...{C['x']}")
        print(f"   {C['g']}→ {x['en']}{C['x']}")
    print(f"\n{C['y']}টিপস:{C['x']}")
    for t in d["tips"]:
        print("  •", t)
    if not a.all:
        append_log("TR", len(drills))


# ───────────────────────── corpus search ─────────────────────────
def corpus_index():
    p = os.path.join(CORPUS, "index.json")
    if not os.path.exists(p):
        return {}
    return {d["id"]: d for d in json.load(open(p, encoding="utf-8"))}


def iter_pages():
    for f in sorted(glob.glob(os.path.join(CORPUS, "**", "*.md"), recursive=True)):
        txt = open(f, encoding="utf-8").read()
        title = txt.split("\n", 1)[0].lstrip("# ")
        for m in re.finditer(r"<!-- page (\d+) -->\n(.*?)(?=<!-- page \d+ -->|\Z)", txt, re.S):
            yield f, title, int(m.group(1)), m.group(2)


def cmd_search(a):
    q = norm(a.query)
    words = [w for w in re.split(r"\s+", q) if w]
    hits = []
    for f, title, page, body in iter_pages():
        nb = norm(body)
        if not all(w in nb for w in words):
            continue
        score = sum(nb.count(w) for w in words) + (5 if q in nb else 0)
        i = nb.find(words[0])
        snip = re.sub(r"\s+", " ", body[max(0, i - 120): i + 220])
        hits.append((score, f, title, page, snip))
    hits.sort(key=lambda h: -h[0])
    hr(f"'{a.query}' — {bn(len(hits))}টি পৃষ্ঠায় পাওয়া গেছে")
    for score, f, title, page, snip in hits[: a.n]:
        print(f"\n{C['g']}{title}{C['x']}  পৃষ্ঠা {bn(page)}  {C['d']}({os.path.relpath(f, ROOT)}){C['x']}")
        print(f"   …{snip}…")
    if not hits and not os.path.exists(os.path.join(CORPUS, "index.json")):
        print("corpus তৈরি হয়নি — আগে চালান: python3 engine/extract.py")


# ───────────────────────── math ─────────────────────────
def cmd_math(a):
    p = os.path.join(DATA, "math_bank.json")
    if not os.path.exists(p):
        sys.exit("data/math_bank.json নেই — চালান: python3 engine/build_math_bank.py")
    bank = load("math_bank.json")
    chapters = bank["chapters"]
    if a.list or not bank["questions"]:
        hr("গণিত অধ্যায় — বিগত প্রশ্নের সংখ্যা (বেশি = বেশি গুরুত্বপূর্ণ)")
        for ch in chapters:
            print(f"  {ch['key']:<14} {ch['bn']:<22} {bn(ch['count']):>5}টি  অগ্রাধিকার {bn(ch['priority'])}")
        return
    qs = bank["questions"]
    if a.chapter:
        qs = [q for q in qs if a.chapter.lower() in q["chapter"].lower()]
        if not qs:
            sys.exit("এই অধ্যায়ে প্রশ্ন নেই। --list দেখুন।")
    pick = random.sample(qs, min(a.n, len(qs)))
    hr(f"গণিত ড্রিল — {bn(len(pick))}টি (ক্যালকুলেটর ছাড়া, পূর্ণ ধাপসহ খাতায়)")
    for i, q in enumerate(pick, 1):
        print(f"\n{C['y']}{bn(i)}. [{q['chapter']}]{C['x']} {q['text']}")
        print(f"   {C['d']}উৎস: {q['source']} পৃষ্ঠা {bn(q['page'])}{(' | ' + q['exam']) if q.get('exam') else ''}{C['x']}")
    print(f"\n{C['d']}সমাধান মিলাতে উৎস PDF-এর ওই পৃষ্ঠা খুলুন। OCR লেখায় ভুল থাকলে মূল PDF দেখুন।{C['x']}")
    append_log("MATH_DRILL", len(pick), a.chapter or "mixed")


# ───────────────────────── resources ─────────────────────────
def cmd_res(a):
    hr("রিসোর্স ম্যাপ — কোন PDF কোন অংশ (অগ্রাধিকার ১ = আগে)")
    rows = [c for c in CATALOG if not a.section or a.section.upper() in c[4]]
    for prio in (1, 2, 3):
        group = [c for c in rows if c[5] == prio]
        if not group:
            continue
        print(f"\n{C['y']}অগ্রাধিকার {bn(prio)}{C['x']}")
        for _d, _s, path, title, secs, _p, _l, strat in group:
            print(f"  • {title}  {C['d']}[{', '.join(secs)}]{C['x']}\n    {path}")
            if strat:
                print(f"    {C['g']}কৌশল:{C['x']} {strat}")
    print(f"\n{C['d']}অংশ কোড: " + ", ".join(f"{k}={v}" for k, v in SECTION_NAMES.items()) + C["x"])


# ───────────────────────── mock ─────────────────────────
def cmd_mock(a):
    topics = load("topics.json")["topics"]
    args = load("arguments.json")["prompts"]
    tr = load("translation.json")["drills"]
    t_bn, t_en = random.sample(topics, 2)
    hr("মক প্রশ্নপত্র — সিনিয়র অফিসার লিখিত (মোট ২০০, সময় ২ ঘণ্টা)")
    sec = [
        ("১. Focus Writing (English) — ৩০", t_en["en"], "১৮ মি"),
        ("২. ফোকাস রাইটিং (বাংলা) — ৩০", t_bn["bn"], "১৮ মি"),
        ("৩. Analytical/Argumentative Writing — ৪০", f"\"{random.choice(args)['claim']}\" — Do you agree? Justify.", "২২ মি"),
        ("৪. Translate into English — ২০", " ".join(x["bn"] for x in random.sample(tr, 3)), "১২ মি"),
    ]
    if not a.writing:
        mq = []
        p = os.path.join(DATA, "math_bank.json")
        if os.path.exists(p):
            qs = load("math_bank.json")["questions"]
            mq = [q["text"] for q in random.sample(qs, min(5, len(qs)))]
        sec += [
            ("৫. Mathematics — ৩০ (৫×৬)", "\n      ".join(f"({bn(i)}) {q}" for i, q in enumerate(mq, 1)) or "so.py math -n 5 থেকে ৫টি নিন", "২২ মি"),
            ("৬. English Language Proficiency — ২০", "Right form of verbs / correction / transformation / narration (docs/09_grammar_quick.md থেকে ১০টি)", "১০ মি"),
            ("৭. বাংলা ব্যাকরণ — ১০", "বানান/বাক্যশুদ্ধি/সমাস/প্রবাদ (docs/09_grammar_quick.md)", "৫ মি"),
            ("৮. Banking & Financial Knowledge — ১০", "Write short notes: " + ", ".join(t[0] for t in random.sample(load("terms.json")["terms"], 5)), "৫ মি"),
            ("৯. General Knowledge — ১০", "সাম্প্রতিক বিষয় থেকে ৫টি ছোট প্রশ্ন (data/facts.json)", "৫ মি"),
        ]
    for h, q, tm in sec:
        print(f"\n{C['y']}{h}{C['x']}  {C['d']}(সময়: {tm}){C['x']}\n   {q}")
    print(f"\n{C['d']}শুরু করতে: python3 engine/so.py timer {90 if a.writing else 120}{C['x']}")


# ───────────────────────── progress log ─────────────────────────
def append_log(section, qty, note=""):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["datetime", "section", "qty", "note"])
        w.writerow([dt.datetime.now().isoformat(timespec="minutes"), section, qty, note])


def read_log():
    if not os.path.exists(LOG):
        return []
    with open(LOG, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def today_log(day):
    out = {}
    for r in read_log():
        if r["datetime"].startswith(day.isoformat()):
            out[r["section"]] = out.get(r["section"], 0) + int(r["qty"])
    return out


def cmd_log(a):
    append_log(a.section.upper(), a.qty, a.note or "")
    print(f"লগ হয়েছে: {a.section.upper()} +{bn(a.qty)}")


TARGETS = {"FW_BN": 7, "FW_EN": 7, "ARG": 8, "TR": 30, "MATH": 60, "MATH_DRILL": 60, "GK_TERMS": 90}
# অংশ → (নম্বর, লক্ষ্য, পরামর্শের কমান্ড)
WEIGHTS = {"ARG": (40, 8, "so.py arg --timer"), "FW_EN": (30, 7, "so.py essay --lang en --timer"),
           "FW_BN": (30, 7, "so.py essay --lang bn --timer"), "MATH": (30, 60, "so.py math -n 8"),
           "TR": (20, 30, "so.py tr"), "GK_TERMS": (20, 90, "so.py terms --quiz 15")}


def recommend():
    """যে অংশে (নম্বর × বাকি কাজের অনুপাত) সবচেয়ে বেশি, সেটাই এখন করার পরামর্শ।"""
    tot = {}
    for r in read_log():
        k = "MATH" if r["section"].startswith("MATH") else r["section"]
        tot[k] = tot.get(k, 0) + int(r["qty"])
    scored = []
    for k, (marks, tgt, cmd) in WEIGHTS.items():
        gap = max(0.0, 1 - tot.get(k, 0) / tgt)
        scored.append((marks * gap, k, cmd, tot.get(k, 0), tgt))
    scored.sort(reverse=True)
    return scored


def cmd_stats(a):
    rows = read_log()
    tot, days = {}, {}
    for r in rows:
        tot[r["section"]] = tot.get(r["section"], 0) + int(r["qty"])
        days.setdefault(r["datetime"][:10], {}).setdefault(r["section"], 0)
        days[r["datetime"][:10]][r["section"]] += int(r["qty"])
    hr("অগ্রগতি (লক্ষ্য = পরীক্ষার আগে মোট)")
    for k in sorted(set(TARGETS) | set(tot)):
        v, tgt = tot.get(k, 0), TARGETS.get(k)
        bar = ""
        if tgt:
            n = min(20, int(20 * v / tgt))
            bar = f"[{'█' * n}{'·' * (20 - n)}] {bn(v)}/{bn(tgt)}"
        else:
            bar = bn(v)
        print(f"  {k:<11} {bar}")
    if days:
        hr("দিনভিত্তিক")
        for d in sorted(days):
            print(f"  {bn(d)}: " + ", ".join(f"{k} {bn(v)}" for k, v in days[d].items()))
    print(f"\n{C['d']}MATH ও MATH_DRILL একসাথে ৬০টি অঙ্ক লক্ষ্য; ফাইল: progress/log.csv{C['x']}")


# ───────────────────────── main ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="SO Written Intelligence Engine", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__)
    sp = ap.add_subparsers(dest="cmd")
    p = sp.add_parser("today"); p.add_argument("--date"); p.set_defaults(f=cmd_today)
    sp.add_parser("plan").set_defaults(f=cmd_plan)
    p = sp.add_parser("topic"); p.add_argument("n", type=int, nargs="?"); p.set_defaults(f=cmd_topic)
    p = sp.add_parser("facts"); p.add_argument("tag", nargs="?"); p.add_argument("--en", action="store_true"); p.set_defaults(f=cmd_facts)
    p = sp.add_parser("terms"); p.add_argument("--quiz", type=int, default=0); p.add_argument("--find"); p.set_defaults(f=cmd_terms)
    p = sp.add_parser("essay"); p.add_argument("--topic", type=int); p.add_argument("--lang", choices=["bn", "en"])
    p.add_argument("--variant", action="store_true"); p.add_argument("--timer", action="store_true"); p.set_defaults(f=cmd_essay)
    p = sp.add_parser("arg"); p.add_argument("n", type=int, nargs="?"); p.add_argument("--timer", action="store_true")
    p.add_argument("--hints", action="store_true"); p.set_defaults(f=cmd_arg)
    p = sp.add_parser("tr"); p.add_argument("--all", action="store_true"); p.set_defaults(f=cmd_tr)
    p = sp.add_parser("math"); p.add_argument("chapter", nargs="?"); p.add_argument("-n", type=int, default=5)
    p.add_argument("--list", action="store_true"); p.set_defaults(f=cmd_math)
    p = sp.add_parser("search"); p.add_argument("query"); p.add_argument("-n", type=int, default=10); p.set_defaults(f=cmd_search)
    p = sp.add_parser("res"); p.add_argument("section", nargs="?"); p.set_defaults(f=cmd_res)
    p = sp.add_parser("mock"); p.add_argument("--writing", action="store_true"); p.set_defaults(f=cmd_mock)
    p = sp.add_parser("timer"); p.add_argument("minutes", type=float); p.set_defaults(f=cmd_timer)
    p = sp.add_parser("log"); p.add_argument("section"); p.add_argument("qty", type=int); p.add_argument("note", nargs="?")
    p.set_defaults(f=cmd_log)
    sp.add_parser("stats").set_defaults(f=cmd_stats)
    a = ap.parse_args()
    if not a.cmd:
        a = ap.parse_args(["today"])
    a.f(a)


if __name__ == "__main__":
    main()
