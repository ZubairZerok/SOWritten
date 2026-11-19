#!/usr/bin/env python3
"""
ওয়েব অ্যাপ বিল্ড: data/*.json + webapp/app.html →
  webapp/index.html        (সব ডেটা ভেতরে — ইন্টারনেট ছাড়াই ব্রাউজারে খোলা যায়)
  webapp/dist/index.html   (claude.ai Artifact-এর জন্য, ডেটা আলাদা)
  webapp/dist/data.json
চালান:  python3 webapp/build.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "webapp")


def load(n):
    with open(os.path.join(ROOT, "data", n), encoding="utf-8") as f:
        return json.load(f)


def good_math(x):
    t = x["text"]
    if not (50 <= len(t) <= 450):
        return False
    junk = len(re.findall(r"[^A-Za-z0-9 .,?%:;()'\"/+\-=×÷&]", t))
    if junk / len(t) >= 0.03:
        return False
    return "?" in t or re.search(r"\b(find|what|how|calculate|determine)\b", t, re.I)


def bundle():
    mb = load("math_bank.json")
    math = [{"id": i, "t": q["text"], "c": q["chapter"], "e": q.get("exam") or "", "a": q.get("answer") or "",
             "s": q["source"], "p": q["page"], "y": q.get("latest_year") or 0}
            for i, q in enumerate(mb["questions"]) if good_math(q)]
    return {
        "version": 1,
        "plan": load("plan.json")["exam"],
        "topics": load("topics.json")["topics"],
        "facts": load("facts.json")["facts"],
        "terms": load("terms.json")["terms"],
        "arguments": load("arguments.json"),
        "translation": load("translation.json"),
        "quiz": {k: v for k, v in load("quiz.json").items() if k != "_note"},
        "mathChapters": mb["chapters"],
        "math": math,
    }


HEAD = ('<!doctype html><html lang="bn"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>\n')


def main():
    src = open(os.path.join(W, "app.html"), encoding="utf-8").read()
    data = json.dumps(bundle(), ensure_ascii=False, separators=(",", ":"))
    data_safe = data.replace("</", "<\\/")
    assert "__SO_DATA__" in src
    full = HEAD + src.replace("__SO_DATA__", data_safe) + "\n</body></html>\n"
    open(os.path.join(W, "index.html"), "w", encoding="utf-8").write(full)
    os.makedirs(os.path.join(W, "dist"), exist_ok=True)
    open(os.path.join(W, "dist", "index.html"), "w", encoding="utf-8").write(src.replace("__SO_DATA__", ""))
    open(os.path.join(W, "dist", "data.json"), "w", encoding="utf-8").write(data)
    print(f"index.html {len(full)//1024} KB · dist/data.json {len(data)//1024} KB · math {len(json.loads(data)['math'])}")


if __name__ == "__main__":
    main()
