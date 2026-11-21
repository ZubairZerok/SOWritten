#!/usr/bin/env python3
"""
পুরো রিপোর স্বয়ংক্রিয় যাচাই (ডেটা, লিংক, বিল্ড, CLI)।  চালান:  python3 tests/validate_all.py
ব্যর্থ হলে exit code 1। ওয়েব অ্যাপের ব্রাউজার টেস্ট আলাদা: node webapp/tests/stress.test.js
"""
import glob, json, os, re, subprocess, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, "engine")
P = F = 0
FAILS = []


def ok(cond, name, info=""):
    global P, F
    if cond:
        P += 1
    else:
        F += 1
        FAILS.append(f"✗ {name}" + (f" → {info}" if info else ""))


def load(p):
    return json.load(open(p, encoding="utf-8"))


# ── 1. JSON files parse ─────────────────────────────────────────
for p in glob.glob("data/*.json") + ["corpus/index.json"]:
    try:
        load(p); ok(True, p)
    except Exception as e:
        ok(False, "JSON parse " + p, str(e))

# ── 2. quiz ─────────────────────────────────────────────────────
q = load("data/quiz.json")
names = q.get("_tp_names", {})
for kind in ("eng", "bn", "gk"):
    ok(len(q[kind]) >= 20, f"quiz {kind} size", len(q[kind]))
    seen = set()
    for i, it in enumerate(q[kind]):
        tag = f"quiz {kind}[{i}] {it.get('q','')[:40]}"
        ok(isinstance(it.get("q"), str) and it["q"].strip(), tag + " has question")
        ok(isinstance(it.get("o"), list) and 2 <= len(it["o"]) <= 5, tag + " 2–5 options")
        ok(isinstance(it.get("a"), int) and 0 <= it["a"] < len(it["o"]), tag + " answer index valid")
        ok(len(set(o.strip() for o in it["o"])) == len(it["o"]), tag + " options unique", it["o"])
        ok(all(str(o).strip() for o in it["o"]), tag + " no empty option")
        if kind != "gk":
            ok(it.get("tp") in names, tag + " syllabus tag known", it.get("tp"))
        key = (it["q"], tuple(it["o"]))
        ok(key not in seen, tag + " not duplicate"); seen.add(key)
official_eng = {"sva", "rfv", "structure", "speech", "transformation", "finite", "clause", "groupverb", "idiom"}
official_bn = {"banan", "banan_niyom", "shuddhi", "probad", "karok", "somas", "sondhi", "ekkothay", "somoccharito"}
ok(official_eng <= {i.get("tp") for i in q["eng"]}, "all 9 official English sub-topics covered")
ok(official_bn <= {i.get("tp") for i in q["bn"]}, "all 9 official Bangla sub-topics covered")

# ── 3. facts ────────────────────────────────────────────────────
facts = load("data/facts.json")["facts"]
tags = set()
for i, f in enumerate(facts):
    ok(all(f.get(k) for k in ("topic", "bn", "en", "src")), f"fact[{i}] complete", f.get("bn", "")[:40])
    tags.add(f["topic"])
for t in load("data/topics.json")["topics"]:
    for tag in t["facts"]:
        ok(tag in tags, f"topic {t['n']} fact tag '{tag}' has facts")
# stale-figure guard: the current policy rate must be stated as 9.5%
cur = [f for f in facts if f["topic"] == "monetary" and "পলিসি রেট" in f["bn"][:12]]
ok(cur and all("৯.৫" in f["bn"] for f in cur), "policy-rate fact says 9.5%")

# stale-number guard across all human-readable text
for p_ in [x for x in glob.glob("docs/*.md") if not re.search(r"docs/1[56]_", x)] + glob.glob("answers/*.md") + ["README.md", "webapp/app.html"]:  # 15/16 quote old values on purpose
    t_ = open(p_, encoding="utf-8").read()
    for bad in ("৩৫টি সর্বশেষ", "Instant Interoperable", "১৯% পারস্পরিক", "19% IEEPA", "6.07 lakh", "৬.০৭ লাখ", "৩৪.৮৫", "34.85 bn", "জুন ২০২৭"):
        ok(bad not in t_, f"{p_} has no stale figure", bad)
ok(len(facts) >= 77, "facts ≥77", len(facts))
# Fact Pack (20 Nov 2026) corrections stay applied in the data files too
blob = open("data/facts.json", encoding="utf-8").read() + open("data/quiz.json", encoding="utf-8").read() + open("data/terms.json", encoding="utf-8").read()
for bad in ("Instant Interoperable", "১৯% পারস্পরিক", "19% IEEPA", "৩৪.৮৫"):
    ok(bad not in blob, "data has no superseded figure", bad)
for good in ("Inclusive Instant Payment System", "জুলাই ২০২৭", "৩৪.৩৮", "A/81/L.8", "১৪তম গভর্নর", "৩২.১৭%"):
    ok(good in blob, "data has Fact-Pack figure", good)

# ── 4. terms, topics, arguments, translation, plan ─────────────
terms = load("data/terms.json")["terms"]
ok(all(len(t) == 3 and all(x.strip() for x in t) for t in terms), "terms have 3 non-empty fields")
ok(len({t[0] for t in terms}) == len(terms), "term keys unique")
topics = load("data/topics.json")["topics"]
ok([t["n"] for t in topics] == list(range(1, len(topics) + 1)), "topics numbered 1..n")
ids = {d["id"] for d in load("corpus/index.json")}
for t in topics:
    for k in ("bn", "en", "variants", "outline_bn", "outline_en", "facts", "quote", "solutions", "sources"):
        ok(t.get(k), f"topic {t['n']} field {k}")
    for s in t["sources"]:
        ok(s in ids, f"topic {t['n']} source exists in corpus", s)
args = load("data/arguments.json")
for i, p in enumerate(args["prompts"]):
    ok(p.get("claim") and p.get("pro") and p.get("con") and p.get("verdict"), f"argument[{i}] complete")
tr = load("data/translation.json")
ok(all(d.get("bn") and d.get("en") for d in tr["drills"]), "translation drills complete")
plan = load("data/plan.json")
ds = [d["date"] for d in plan["days"]]
ok(ds == sorted(ds) and len(ds) == 9, "plan has 9 ordered dates (19–27 Nov)", ds)
ok(plan["exam"]["date"] == "2026-11-27" and ds[-1] == "2026-11-27", "exam date 27 Nov 2026")
for d in ds:
    date.fromisoformat(d)

# ── 5. math bank ────────────────────────────────────────────────
mb = load("data/math_bank.json")
ok(len(mb["questions"]) >= 1000, "math bank ≥1000 questions", len(mb["questions"]))
ok(all(q_.get("text") and q_.get("chapter") and q_.get("source") and q_.get("page") for q_ in mb["questions"]), "math items complete")
chs = {c["key"] for c in mb["chapters"]}
ok(all(q_["chapter"] in chs for q_ in mb["questions"]), "math chapters valid")

# ── 6. catalog & files ─────────────────────────────────────────
from catalog import CATALOG  # noqa: E402
for c in CATALOG:
    ok(os.path.exists(c[2]) and os.path.getsize(c[2]) > 10_000, "catalog file exists", c[2])
ok(len({c[2] for c in CATALOG}) == len(CATALOG), "catalog paths unique")

# ── 7. Markdown links in docs/README resolve ───────────────────
for md in glob.glob("docs/*.md") + ["README.md"]:
    text = open(md, encoding="utf-8").read()
    for link in re.findall(r"\]\(([^)#]+?)\)", text):
        if link.startswith("http"):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(md), link))
        ok(os.path.exists(target), f"link in {md}", link)
    for path in re.findall(r"`((?:materials|docs|data|engine|webapp|answers|answer_book)/[^`*?<> ]+)`", text):
        if any(ch in path for ch in "<>{}") or path.endswith("/"):
            continue
        ok(os.path.exists(path) or glob.glob(path), f"path mentioned in {md} exists", path)

# ── 8. answers: verified math results present ──────────────────
ans = {p: open(p, encoding="utf-8").read() for p in glob.glob("answers/*.md")}
checks = {
    "answers/01_SO_2026-06-05.md": ["11,600", "50/19", "25 staff", "53.**", "5 pieces", "A | E | B | D | C"],
    "answers/02_SO_2025-12-24.md": ["7 p.m.", "20 persons", "90,000", "47/66", "24 cm"],
    "answers/03_SO_2025-06-20.md": ["**55**", "**45**", "T = 200", "**70**", "x = 2/11", "360 units", "240 units", "**50 cm**"],
    "answers/06_predicted_other_sections.md": ["2:15 p.m.", "21 litres", "n = 4 years", "68 extra men", "60 days", "R | P | S | T | Q | U", "1 Nila, 2 Tanvir, 3 Omar, 4 Rafi, 5 Sumi"],
    "answers/07_older_papers.md": ["72 oranges", "17,411.32", "**36**", "132.75", "42.59"],
}
for p, needles in checks.items():
    for n in needles:
        ok(n in ans.get(p, ""), f"{p} contains verified result", n)
for p, t in ans.items():
    ok(t.count("**") % 2 == 0, f"{p} balanced bold markers")
    ok("✗ — check" not in t, f"{p} no leftover working note")

# ── 9. CLI smoke ───────────────────────────────────────────────
for args_ in (["today"], ["plan"], ["topic"], ["topic", "10"], ["facts"], ["terms"], ["arg", "1", "--hints"], ["tr", "--all"],
              ["math", "--list"], ["math", "speed", "-n", "2"], ["search", "ঋণ", "-n", "1"], ["res"], ["mock"], ["stats"]):
    r = subprocess.run([sys.executable, "engine/so.py", *args_], capture_output=True, text=True, env=dict(os.environ, NO_COLOR="1"))
    ok(r.returncode == 0, "so.py " + " ".join(args_), r.stderr[-200:])
if os.path.exists("progress/log.csv"):
    os.remove("progress/log.csv")  # smoke runs must not leave a fake log

# ── 10. builds are reproducible ────────────────────────────────
for cmd in (["engine/build_docs.py"], ["webapp/build.py"], ["answer_book/build_book.py", "--no-pdf"]):
    r = subprocess.run([sys.executable, *cmd], capture_output=True, text=True)
    ok(r.returncode == 0, "build " + cmd[0], r.stderr[-300:])
html = open("answer_book/SO_Model_Answer_Book.html", encoding="utf-8").read()
for sid in re.findall(r'href="#([\w-]+)"', html):
    ok(f'id="{sid}"' in html, "answer-book anchor exists", sid)
ok(len(re.findall(r'class="ans"', html)) >= 40, "answer book has ≥40 answer sections", len(re.findall(r'class="ans"', html)))

# ── 11. no API key / secret is ever committed ─────────────────
tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
for f_ in tracked + [x for x in glob.glob("webapp/**/*.html", recursive=True)]:
    if not f_.endswith((".md", ".json", ".html", ".js", ".py", ".css", ".txt", ".csv")) or not os.path.exists(f_):
        continue
    t_ = open(f_, encoding="utf-8", errors="ignore").read()
    ok(not re.search(r"\bsk-[A-Za-z0-9]{24,}", t_), "no API key in " + f_)

print("\n".join(FAILS[:60]))
print(f"\nমোট: {P} পাস, {F} ফেল")
sys.exit(1 if F else 0)
