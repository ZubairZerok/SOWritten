#!/usr/bin/env python3
"""
Math Master Booklet: whole original pages (no rewriting), picked by how often each page's questions came in
2015+ / SO exams (data/math_bank.json) plus every chapter's formula page; ordered by chapter priority.
Scanned pages are re-encoded as grey JPEG (small file); text-based Khairul pages are copied as they are.
Output: final_pdfs/SO_Math_Master_Booklet.pdf
"""
import io, os, subprocess, tempfile
from pypdf import PdfReader, PdfWriter
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, "materials", "03_math")
OUT = os.path.join(ROOT, "final_pdfs", "SO_Math_Master_Booklet.pdf")
SRC = {
    "K01": ("khairul/01_Percentage.pdf", False), "K02": ("khairul/02_Algebra.pdf", False), "K03": ("khairul/03_Time_Work.pdf", False),
    "K04": ("khairul/04_Time_Speed.pdf", False), "K05": ("khairul/05_Arithmetic_Progression.pdf", False), "K06": ("khairul/06_Mixture.pdf", False),
    "K07": ("khairul/07_Boat_Stream.pdf", False), "K08": ("khairul/08_Unitary_Method.pdf", False),
    "PL": ("topic_sheets/PDF45_Profit_Loss.pdf", True), "GEO": ("topic_sheets/PDF33_Geometry.pdf", True),
    "CI": ("topic_sheets/PDF14_Compound_Interest.pdf", True), "RAT": ("topic_sheets/PDF30_Ratio_Proportion.pdf", True),
    "PAR": ("topic_sheets/PDF31_Partnership.pdf", True), "PRB": ("topic_sheets/PDF32_Probability.pdf", True),
    "TRN": ("topic_sheets/PDF62_Problem_on_Train.pdf", True), "MIX": ("topic_sheets/PDF60_Mixture.pdf", True),
    "EQ": ("topic_sheets/PDF16_Formation_of_Equation.pdf", True), "BIBM": ("question_bank/BIBM_Previous_All_Written_Math_Solution.pdf", True),
}
# (chapter, Bangla name, priority stars, [(source, [pages])])
CHAPTERS = [
    ("Time, Speed, Train, Boat", "গতি · ট্রেন · নৌকা-স্রোত", "★★★", [("K04", range(1, 10)), ("TRN", [1, 2, 3, 7, 8, 11]), ("K07", range(1, 5))]),
    ("Time & Work, Pipes, Unitary", "সময় ও কাজ · নল-চৌবাচ্চা", "★★★", [("K03", [1, 2, 3, 13, 14, 21, 22, 23, 28, 50, 51, 53, 54]), ("K08", [2, 4])]),
    ("Algebra & Forming Equations", "বীজগণিত ও সমীকরণ", "★★★", [("K02", [1, 2, 35, 44]), ("EQ", [1, 8, 10, 17, 25, 26])]),
    ("Profit & Loss", "লাভ-ক্ষতি", "★★★", [("PL", [1, 7, 13, 20, 22, 33, 38, 42, 43])]),
    ("Percentage", "শতকরা", "★★★", [("K01", range(1, 10))]),
    ("Mixture & Alligation", "মিশ্রণ", "★★", [("K06", range(1, 6)), ("MIX", [20, 21])]),
    ("Geometry & Mensuration", "জ্যামিতি ও ক্ষেত্রফল", "★★", [("GEO", [1, 3, 10, 16, 17, 21])]),
    ("Simple & Compound Interest", "সরল ও চক্রবৃদ্ধি সুদ", "★★", [("CI", [1, 6, 7, 16, 17, 18])]),
    ("Ratio & Partnership", "অনুপাত ও অংশীদারি", "★★", [("RAT", [10, 11]), ("PAR", [1, 17, 18])]),
    ("Probability, Permutation", "সম্ভাবনা · বিন্যাস-সমাবেশ", "★", [("PRB", [1, 2, 8, 13])]),
    ("Series (AP / GP)", "ধারা", "★", [("K05", [1, 3, 7])]),
    ("Recent BIBM papers (solved)", "সাম্প্রতিক BIBM প্রশ্ন ও সমাধান", "★★", [("BIBM", [1, 2, 5, 7, 9, 15, 94])]),
]
FORMULAS = [
    ("শতকরা", "x% বৃদ্ধির পর y% হ্রাস → নিট = x − y − xy/100 · দাম x% বাড়লে খরচ ঠিক রাখতে ব্যবহার কমাতে হবে x/(100+x) × 100%"),
    ("লাভ-ক্ষতি", "লাভ% = লাভ/ক্রয়মূল্য × 100 · SP = CP × (100 ± %)/100 · ছাড়: SP = MP × (100 − ছাড়%)/100"),
    ("সরল সুদ", "I = Pnr/100 · A = P + I"),
    ("চক্রবৃদ্ধি", "A = P(1 + r/100)ⁿ · ষাণ্মাসিক: r/2, 2n · CI − SI (২ বছর) = P(r/100)²"),
    ("অনুপাত/অংশীদারি", "লাভের ভাগ ∝ মূলধন × সময় · a:b ও b:c → মাঝের পদ সমান করে a:b:c"),
    ("সময় ও কাজ", "১ দিনের কাজ = 1/দিন · একসাথে = 1/A + 1/B · নল: ভরে (+), খালি করে (−) · M₁D₁H₁/W₁ = M₂D₂H₂/W₂"),
    ("গতি · ট্রেন", "দূরত্ব = গতি × সময় · km/h → m/s: × 5/18 · গড় গতি (সমান দূরত্ব) = 2xy/(x+y) · ট্রেন অতিক্রম = ট্রেন + প্ল্যাটফর্ম · বিপরীত দিকে আপেক্ষিক গতি = যোগ, একই দিকে = বিয়োগ"),
    ("নৌকা-স্রোত", "অনুকূলে = u + v · প্রতিকূলে = u − v · নৌকা = (অনু + প্রতি)/2 · স্রোত = (অনু − প্রতি)/2"),
    ("মিশ্রণ", "(দামি − গড়) : (গড় − সস্তা) = সস্তা : দামি · বারবার তুলে প্রতিস্থাপন: বাকি = মোট × (1 − x/মোট)ⁿ"),
    ("ধারা", "tₙ = a + (n−1)d · Sₙ = n/2 [2a + (n−1)d] · GP: arⁿ⁻¹, a(rⁿ − 1)/(r − 1)"),
    ("জ্যামিতি", "আয়ত = l×b, 2(l+b) · ত্রিভুজ = ½ × ভূমি × উচ্চতা · সমবাহু = (√3/4)a² · বৃত্ত = πr², 2πr · ঘনক = a³ · বেলন = πr²h · পিথাগোরাস"),
    ("সম্ভাবনা", "P = অনুকূল/মোট · ⁿPᵣ = n!/(n−r)! · ⁿCᵣ = n!/(r!(n−r)!) · অন্তত একটি = 1 − কোনোটিই না"),
]
BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")


def scan_page(path, p, tmp):
    base = os.path.join(tmp, "pg")
    subprocess.run(["pdftoppm", "-r", "120", "-gray", "-jpeg", "-jpegopt", "quality=55", "-f", str(p), "-l", str(p), "-singlefile", path, base], check=True)
    im = Image.open(base + ".jpg")
    buf = io.BytesIO()
    im.save(buf, "PDF", resolution=120)
    return PdfReader(io.BytesIO(buf.getvalue())).pages[0]


def front_matter(index_rows, total):
    rows = "".join(f"<tr><td>{i + 1}</td><td><b>{en}</b><br><span>{bn}</span></td><td class='st'>{st}</td><td>{a}–{z}</td><td>{n}</td></tr>"
                   for i, (en, bn, st, a, z, n) in enumerate(index_rows))
    frm = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in FORMULAS)
    font = os.path.join(ROOT, "answer_book", "fonts", "TiroBangla-400.ttf")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:TiroB;src:url("file://{font}")}}
@page{{size:A4;margin:14mm}} body{{font-family:Inter,TiroB,sans-serif;color:#0f172a;font-size:10pt;margin:0}}
.tag{{color:#2563eb;font-weight:700;letter-spacing:.12em;font-size:9pt;text-transform:uppercase}}
h1{{font-size:26pt;margin:4pt 0 4pt;letter-spacing:-.02em}} .sub{{color:#475569;font-family:TiroB,Inter;font-size:11pt;margin-bottom:12pt}}
table{{width:100%;border-collapse:collapse}} th{{text-align:left;background:#f1f5f9;font-size:8pt;text-transform:uppercase;color:#475569;padding:4pt 6pt}}
td{{padding:4pt 6pt;border-bottom:1px solid #dbe3ee;vertical-align:top}} td span{{font-family:TiroB;color:#475569}} .st{{color:#b45309}}
.f td{{font-family:TiroB,Inter;font-size:10.5pt;line-height:1.5}} .f td:first-child{{width:28mm;color:#2563eb}}
.box{{font-family:TiroB,Inter;background:#ecfdf5;border-left:3pt solid #047857;padding:7pt 10pt;margin:10pt 0;font-size:10.5pt;line-height:1.55}}
.pb{{break-before:page}} h2{{font-size:15pt;margin:0 0 6pt}}
</style></head><body>
<div class="tag">SO Written · 27 November 2026 · Mathematics (30 marks)</div>
<h1>Math Master Booklet</h1>
<div class="sub">মূল বইয়ের পাতা হুবহু (Khairul's Bank Written Math, টপিক শিট, BIBM সমাধান) — ১১০০+ পাতা থেকে শুধু সূত্রের পাতা আর ২০১৫-পরবর্তী ও SO পরীক্ষায় বারবার আসা প্রশ্নের পাতা, অধ্যায়ের অগ্রাধিকার অনুযায়ী সাজানো। মোট {total} পাতা।</div>
<table><thead><tr><th>#</th><th>Chapter</th><th>Priority</th><th>Booklet pages</th><th>Pages</th></tr></thead><tbody>{rows}</tbody></table>
<div class="box"><b>কীভাবে পড়বেন:</b> ★★★ অধ্যায় আগে। প্রতিটি অধ্যায়ের প্রথম পাতা = সূত্র ও মূল ধারণা; তারপর পরীক্ষায় আসা প্রশ্ন (ব্র্যাকেটে ব্যাংক ও সাল)। প্রতিটি অঙ্ক আগে নিজে করুন (৬ মিনিট), না মিললে সমাধান দেখুন, পরদিন আবার করুন। পরীক্ষায় প্রতিটি ধাপ লিখুন, উত্তর বক্স করুন, একক লিখুন।</div>
<div class="pb"></div><h2>Formula sheet (পরীক্ষার আগের রাতে শুধু এটা)</h2>
<table class="f"><tbody>{frm}</tbody></table>
</body></html>"""
    with tempfile.TemporaryDirectory() as t:
        hp, pp, js = os.path.join(t, "f.html"), os.path.join(t, "f.pdf"), os.path.join(t, "m.js")
        open(hp, "w", encoding="utf-8").write(html)
        open(js, "w").write('const {chromium}=require("playwright");(async()=>{const b=await chromium.launch();const p=await b.newPage();'
                            f'await p.goto("file://{hp}");await p.evaluate(()=>document.fonts.ready);'
                            f'await p.pdf({{path:"{pp}",format:"A4",printBackground:true,preferCSSPageSize:true}});await b.close();}})();')
        subprocess.run(["node", js], check=True, cwd=ROOT)
        return [pg for pg in PdfReader(io.BytesIO(open(pp, "rb").read())).pages]


def main():
    FRONT = 2
    index_rows, cur = [], FRONT + 1
    for en, bn, st, parts in CHAPTERS:
        n = sum(len(list(p)) for _, p in parts)
        index_rows.append((en, bn, st, cur, cur + n - 1, n))
        cur += n
    total = cur - 1
    w = PdfWriter()
    front = front_matter(index_rows, total)
    assert len(front) == FRONT, len(front)
    for pg in front:
        w.add_page(pg)
    readers = {}
    with tempfile.TemporaryDirectory() as tmp:
        for en, bn, st, parts in CHAPTERS:
            first = len(w.pages)
            for key, pages in parts:
                rel, scanned = SRC[key]
                path = os.path.join(M, rel)
                for p in pages:
                    if scanned:
                        w.add_page(scan_page(path, p, tmp))
                    else:
                        r = readers.setdefault(key, PdfReader(path))
                        w.add_page(r.pages[p - 1])
            w.add_outline_item(f"{en} ({bn})", first)
    for pg in w.pages:
        pg.compress_content_streams()
    w.compress_identical_objects(remove_identicals=True, remove_unreferenced=True)
    with open(OUT, "wb") as f:
        w.write(f)
    print("PDF:", OUT, len(w.pages), "pages", round(os.path.getsize(OUT) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
