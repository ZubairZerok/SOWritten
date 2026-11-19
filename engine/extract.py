#!/usr/bin/env python3
"""
সব PDF থেকে সার্চযোগ্য টেক্সট বের করে corpus/ ফোল্ডারে রাখে।

নিয়ম (প্রতি পৃষ্ঠা):
  - টেক্সট লেয়ার আছে এবং বাংলা নেই  → pdftotext (দ্রুত, নিখুঁত)
  - বাংলা আছে (এই PDF-গুলোর বাংলা টেক্সট লেয়ার ভাঙা) বা টেক্সট নেই (স্ক্যান) → Tesseract OCR (ben+eng)
প্রতিটি পৃষ্ঠার ফল corpus/.cache-এ জমা থাকে, তাই মাঝপথে থামলেও আবার চালালে আগের কাজ নষ্ট হয় না।

ব্যবহার:
  python3 engine/extract.py                 # সব PDF
  python3 engine/extract.py --only Math     # নামের অংশ মিললে শুধু সেগুলো
  python3 engine/extract.py --workers 4
প্রয়োজন: poppler-utils (pdftotext, pdftoppm, pdfinfo), tesseract-ocr + tesseract-ocr-ben
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, time
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
from catalog import CATALOG  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus")
CACHE = os.path.join(CORPUS, ".cache")
BN = re.compile("[ঀ-৿]")
# স্ক্যান করা PDF-এ শুধু ওয়াটারমার্কের টেক্সট লেয়ার থাকে — সেগুলো বাদ দিয়ে আসল টেক্সট মাপা হয়
WATERMARK = re.compile(r"(?im)^.*(wondershare|pdfelement|remove\s*watermark|^\s*watermark\s*$|^\s*updates\s*$|"
                       r"like our page|join fb group|boimate|bdniyog|exambd|page \d+ of \d+|www\.[\w.]+).*$")


# Tesseract-এর পরিচিত বাংলা OCR ভুল সংশোধন (ঋ প্রায়ই খ/ঝ হয়ে যায়)
OCR_FIXES = [
    (re.compile("(?<![\u0980-\u09FF])[খঝ]ণ(?!\u09CD)"), "ঋণ"),
    (re.compile("(?<![\u0980-\u09FF])খতু"), "ঋতু"),
    (re.compile("মুদ্রাক্ষীতি"), "মুদ্রাস্ফীতি"),
]


def fix_ocr(t):
    for pat, rep in OCR_FIXES:
        t = pat.sub(rep, t)
    return t


def real_text(t):
    return re.sub(r"\s+", "", WATERMARK.sub("", t))


def doc_id(path):
    return os.path.splitext(os.path.basename(path))[0]


def npages(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


def text_layer(pdf, p):
    return subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), pdf, "-"],
                          capture_output=True, text=True).stdout


def ocr(pdf, p, lang):
    with tempfile.TemporaryDirectory() as td:
        base = os.path.join(td, "pg")
        subprocess.run(["pdftoppm", "-r", "220", "-gray", "-png", "-f", str(p), "-l", str(p), "-singlefile", pdf, base],
                       capture_output=True)
        img = base + ".png"
        if not os.path.exists(img):
            return ""
        env = dict(os.environ, OMP_THREAD_LIMIT="1")
        r = subprocess.run(["tesseract", img, "stdout", "-l", lang, "--psm", "3"],
                           capture_output=True, text=True, env=env)
        return r.stdout


def work(pdf, p, lang, cache_file):
    if os.path.exists(cache_file):
        return cache_file, "cached"
    t = text_layer(pdf, p)
    stripped = real_text(t)
    if len(stripped) >= 150 and not BN.search(t):
        method, out = "text", t
    else:
        method, out = "ocr", ocr(pdf, p, lang)
        if len(re.sub(r"\s+", "", out)) < 20 and len(stripped) > 20:
            method, out = "text", t  # OCR ব্যর্থ হলে টেক্সট লেয়ারই ভালো
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    tmp = cache_file + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(f"<!--method:{method}-->\n" + out)
    os.replace(tmp, cache_file)
    return cache_file, method


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    a = ap.parse_args()

    docs = []
    for _d, _s, path, title, sections, prio, lang, _strat in CATALOG:
        full = os.path.join(ROOT, path)
        if a.only and a.only.lower() not in path.lower():
            continue
        if not os.path.exists(full) or os.path.getsize(full) < 10_000:
            print(f"!! অনুপস্থিত/LFS pointer: {path} (git lfs pull চালান)")
            continue
        tess_lang = "eng" if lang == "en" and "Grammar" in path else "ben+eng"
        docs.append((prio, path, full, title, sections, tess_lang))
    docs.sort(key=lambda d: (d[0], npages(d[2])))  # জরুরি ও ছোটগুলো আগে

    tasks = []
    for prio, path, full, title, sections, lang in docs:
        n = npages(full)
        for p in range(1, n + 1):
            cf = os.path.join(CACHE, doc_id(path), f"p{p:04d}.txt")
            tasks.append((full, p, lang, cf))
    todo = [t for t in tasks if not os.path.exists(t[3])]
    print(f"{len(docs)} PDF, {len(tasks)} পৃষ্ঠা, বাকি {len(todo)}", flush=True)

    t0, done = time.time(), 0
    with ProcessPoolExecutor(a.workers) as ex:
        futs = [ex.submit(work, *t) for t in todo]
        for f in as_completed(futs):
            f.result()
            done += 1
            if done % 25 == 0 or done == len(todo):
                el = time.time() - t0
                print(f"  {done}/{len(todo)}  {el/60:.1f} মিনিট, বাকি ~{el/done*(len(todo)-done)/60:.1f} মিনিট", flush=True)

    assemble(docs)


def assemble(docs):
    index = []
    for prio, path, full, title, sections, lang in docs:
        did = doc_id(path)
        cdir = os.path.join(CACHE, did)
        n = npages(full)
        parts, methods = [], {}
        for p in range(1, n + 1):
            cf = os.path.join(cdir, f"p{p:04d}.txt")
            if not os.path.exists(cf):
                continue
            raw = open(cf, encoding="utf-8").read()
            m = re.match(r"<!--method:(\w+)-->\n", raw)
            meth = m.group(1) if m else "?"
            methods[meth] = methods.get(meth, 0) + 1
            body = raw[m.end():] if m else raw
            body = re.sub(r"\n{3,}", "\n\n", body).strip()
            if meth == "ocr":
                body = fix_ocr(body)
            parts.append(f"\n\n<!-- page {p} -->\n## পৃষ্ঠা {p}\n\n{body}")
        if not parts:
            continue
        rel = os.path.relpath(os.path.dirname(path), "materials")
        out = os.path.join(CORPUS, rel, did + ".md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n- উৎস PDF: `{path}`\n- পৃষ্ঠা: {n} (টেক্সট বের হয়েছে {len(parts)})\n"
                    f"- পদ্ধতি: {methods}\n- অংশ: {', '.join(sections)}\n"
                    f"\n> স্বয়ংক্রিয় OCR — বানান/সংখ্যায় ভুল থাকতে পারে, সন্দেহ হলে মূল PDF দেখুন।\n")
            f.write("".join(parts) + "\n")
        index.append({"id": did, "pdf": path, "text": os.path.relpath(out, ROOT), "title": title,
                      "sections": sections, "priority": prio, "pages": n, "pages_extracted": len(parts),
                      "methods": methods})
    old = {}
    ip = os.path.join(CORPUS, "index.json")
    if os.path.exists(ip):
        old = {d["id"]: d for d in json.load(open(ip, encoding="utf-8"))}
    for d in index:
        old[d["id"]] = d
    json.dump(sorted(old.values(), key=lambda d: d["text"]), open(ip, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"corpus তৈরি: {len(index)} ফাইল → corpus/")


if __name__ == "__main__":
    if "--assemble" in sys.argv:
        sys.argv.remove("--assemble")
        docs = []
        for _d, _s, path, title, sections, prio, lang, _ in CATALOG:
            full = os.path.join(ROOT, path)
            if os.path.exists(full):
                docs.append((prio, path, full, title, sections, lang))
        assemble(docs)
    else:
        main()
