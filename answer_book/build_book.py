#!/usr/bin/env python3
"""
answers/*.md → উত্তরপত্রের মতো দেখতে মডেল উত্তর বই
  answer_book/SO_Model_Answer_Book.html   (পূর্ণ HTML, ব্রাউজারে খোলা যায়)
  answer_book/SO_Model_Answer_Book.pdf    (A4, প্রিন্টযোগ্য — Playwright/Chromium দিয়ে)
  answer_book/dist/index.html             (claude.ai Artifact-এর জন্য, fonts/ সহ)
চালান:  python3 answer_book/build_book.py          (PDF বাদ দিতে: --no-pdf)
প্রয়োজন: pip install markdown ; PDF-এর জন্য node + playwright
"""
import html, os, re, subprocess, sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "answers")
B = os.path.join(ROOT, "answer_book")

MD = markdown.Markdown(extensions=["tables", "sane_lists", "nl2br"])


def read(name):
    s = open(os.path.join(A, name), encoding="utf-8").read()
    meta = {}
    if s.startswith("---"):
        _, fm, s = s.split("---", 2)
        for line in fm.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, s.strip()


def md(text):
    MD.reset()
    out = MD.convert(text)
    # pencil notes
    out = re.sub(r"<p>Tip:\s*(.*?)</p>", r'<aside class="pencil"><span class="pmark">✎</span>\1</aside>', out, flags=re.S)
    return out


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "s"


SECTIONS = []  # (id, label)


def script_article(name, sid, label):
    """হাতে লেখা উত্তরপত্রের অংশ"""
    meta, body = read(name)
    h1 = re.search(r"^# (.+)$", body, re.M)
    title = h1.group(1) if h1 else label
    body = re.sub(r"^# .+$", "", body, count=1, flags=re.M)
    content = md(body)
    # each "Ans." heading starts a new answer page
    content = re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h2 class="ans" id="{sid}-{slug(m.group(1))}">{m.group(1)}</h2>', content)
    SECTIONS.append((sid, label))
    paper = meta.get("paper", "")
    return f"""
<article class="sheet script" id="{sid}">
  <header class="strip"><span>ANSWER SCRIPT · Continuation</span><span>{html.escape(paper)}</span></header>
  <h1 class="script-title">{html.escape(title)}</h1>
  {content}
</article>"""


def printed_article(sid, label, inner, cls="printed"):
    SECTIONS.append((sid, label))
    return f'<article class="sheet {cls}" id="{sid}">{inner}</article>'


def qbank_parts():
    _, body = read("00_question_bank.md")
    parts = re.split(r"\n(?=## Paper )", body)
    intro, papers = parts[0], {}
    for p in parts[1:]:
        key = re.match(r"## Paper (\w)", p).group(1)
        papers[key] = p
    return intro, papers


def question_paper(key, text):
    heading = re.match(r"## (.+)", text).group(1)
    rest = text.split("\n", 1)[1]
    return f"""
  <div class="qp-head">
    <div class="qp-org">Combined Bank Recruitment · Senior Officer (General) · Written Test</div>
    <div class="qp-title">QUESTION PAPER</div>
    <div class="qp-sub">{html.escape(re.sub(r"[★]", "", heading))}</div>
    <div class="qp-meta"><span>Time: 2 Hours</span><span>Full Marks: 200</span></div>
    <div class="qp-note">[Answer all questions. Figures in the right margin indicate full marks.]</div>
  </div>
  <div class="qp-body">{md(rest)}</div>"""


def cover():
    marks = [("1", "Focus Writing (English)", 30), ("2", "Focus Writing (Bangla)", 30), ("3", "General Knowledge", 10),
             ("4", "Mathematics", 30), ("5", "Translation (B→E)", 20), ("6", "Analytical / Argumentative", 40),
             ("7", "বাংলা ব্যাকরণ", 10), ("8", "English Proficiency", 20), ("9", "Banking Knowledge", 10)]
    rows = "".join(f"<tr><td>{n}</td><td class='l'>{t}</td><td>{m}</td><td></td><td></td></tr>" for n, t, m in marks)
    roll = "".join("<span class='box'></span>" for _ in range(8))
    SECTIONS.append(("cover", "Cover page"))
    return f"""
<article class="sheet cover" id="cover">
  <div class="cv-top">
    <div class="stamp">PRACTICE COPY · MODEL ANSWERS<br><small>not an official document</small></div>
    <div class="code-box"><div>Code No.</div><div class="code-blank"></div><small>(for office use — candidate will not write here)</small></div>
  </div>
  <div class="cv-head">
    <div class="cv-1">Combined Bank Recruitment Examination</div>
    <div class="cv-2">Senior Officer (General) — Written Test</div>
    <div class="cv-3">ANSWER SCRIPT</div>
    <div class="cv-4">উত্তরপত্র</div>
  </div>
  <table class="fields">
    <tr><th>Name of the Candidate</th><td><span class="hand">Model Answer Book</span></td></tr>
    <tr><th>Father's Name</th><td></td></tr>
    <tr><th>Mother's Name</th><td></td></tr>
    <tr><th>Roll No.</th><td><div class="roll">{roll}</div></td></tr>
    <tr><th>Name of the Post</th><td><span class="hand">Senior Officer (General)</span></td></tr>
    <tr><th>Date of Examination</th><td><span class="hand">27 / 11 / 2026 &nbsp;·&nbsp; 9:30 a.m. – 11:30 a.m.</span></td></tr>
    <tr><th>Signature of the Candidate</th><td><span class="hand sig">Model</span></td></tr>
    <tr><th>Signature of the Invigilator</th><td></td></tr>
  </table>
  <div class="cv-grid">
    <div class="instr">
      <div class="box-h">Instructions to the Candidate</div>
      <ol>
        <li>Write your name, roll number and signature only in the spaces provided on this page. Do not write your name anywhere inside the script.</li>
        <li>Use a black ink ball-point pen only. Pencil may be used only for graphs and drawings.</li>
        <li>Use of correction fluid anywhere in the answer script is strictly prohibited.</li>
        <li>Write the question number clearly at the start of every answer, and begin each answer on a new page.</li>
        <li>Use the last page for rough work and cross it out.</li>
        <li>No additional sheet will be supplied; plan the space before you write.</li>
      </ol>
    </div>
    <div class="exam">
      <div class="box-h">For Examiner's Use Only</div>
      <table class="marks"><thead><tr><th>Q.</th><th>Section</th><th>FM</th><th>Obt.</th><th>Sign</th></tr></thead>
      <tbody>{rows}<tr class="tot"><td colspan="2">Total</td><td>200</td><td></td><td></td></tr></tbody></table>
      <div class="target hand">Target: 128 / 200</div>
    </div>
  </div>
</article>"""


def contents():
    inner = """
  <h1>How to use this answer book</h1>
  <p>This book has three layers, in the order you should study them:</p>
  <ol>
    <li><b>The blueprint paper (5 June 2026)</b> — the only Senior Officer paper already set on the confirmed 200-mark syllabus. Its question paper is followed by a complete model answer script.</li>
    <li><b>Predicted topics for 27 November 2026</b> — eight full focus-writing answers and a complete practice set in the June 2026 format (Analytical 40, Translation, Grammar, Banking, GK, Math).</li>
    <li><b>Earlier papers (Dec 2025, Jun 2025, 2021–2024)</b> — more practice with full or pointer answers.</li>
  </ol>
  <p>Answers are written the way a strong script looks in the hall: black ink, headings underlined in blue, one data box with its source, recommendations and a short conclusion. <span class="pencil-inline">Pencil notes</span> are coaching tips, not part of the answer.</p>
  <p><b>Language:</b> all model answers are in English, as requested. Questions that must be answered in Bangla in the exam carry a pencil note with the Bangla sub-headings to use.</p>
  <p><b>Figures</b> are current to 19–20 November 2026 and carry their sources. Key ones: policy rate 9.5% (cut on 30 July 2026); inflation 8.27% (Oct 2026); default loans 32.17% (Sept 2026); remittance USD 35.59 bn in FY26 (record); LDC graduation 24 Nov 2029; US tariff 10% (Section 301).</p>
  <p class="cv-foot"><b>About the layout:</b> Layout reconstructed from candidates' published descriptions of bank written-test answer scripts (cover fields, office code, black ink, self-drawn margins); no official specimen is publicly available. Contents prepared from the SOWritten repository, past papers (Satt Academy) and 15+ news sources, 19–20 November 2026.</p>
  <h2>Contents</h2>
  <ul class="toc-list">__TOC__</ul>"""
    return printed_article("contents", "How to use · Contents", inner)


def wrap_printed(name, sid, label):
    _, body = read(name)
    return printed_article(sid, label, md(body), "printed analysis")


def build():
    intro, papers = qbank_parts()
    parts = [cover(), contents(), wrap_printed("04_topic_prediction.md", "prediction", "Topic prediction for 27 Nov 2026")]
    plan = [("A", "01_SO_2026-06-05.md", "paperA", "Paper A · 5 June 2026 (blueprint)"),
            ("B", "02_SO_2025-12-24.md", "paperB", "Paper B · 24 December 2025"),
            ("C", "03_SO_2025-06-20.md", "paperC", "Paper C · 20 June 2025")]
    # blueprint first, then predicted, then older practice
    k, f, sid, lab = plan[0]
    parts.append(printed_article(sid + "-q", lab + " — question paper", question_paper(k, papers[k]), "printed qpaper"))
    parts.append(script_article(f, sid, lab + " — model answers"))
    parts.append(script_article("05_predicted_focus.md", "predfocus", "Predicted focus writing — model answers"))
    parts.append(script_article("06_predicted_other_sections.md", "predother", "Practice set (Analytical, Translation, Grammar, Banking, GK, Math)"))
    for k, f, sid, lab in plan[1:]:
        parts.append(printed_article(sid + "-q", lab + " — question paper", question_paper(k, papers[k]), "printed qpaper"))
        parts.append(script_article(f, sid, lab + " — model answers"))
    parts.append(script_article("07_older_papers.md", "older", "2021–2024 papers — answer pointers"))
    rest = intro + "\n\n" + "\n\n".join(papers[k] for k in sorted(papers) if k not in "ABC")
    parts.append(printed_article("qbank", "Appendix · Question bank 2014–2026", md(rest), "printed analysis"))
    toc = "".join(f'<li><a href="#{sid}">{html.escape(lab)}</a></li>' for sid, lab in SECTIONS if sid not in ("cover", "contents"))
    body = "\n".join(parts).replace("__TOC__", toc)
    opts = "".join(f'<option value="{sid}">{html.escape(lab)}</option>' for sid, lab in SECTIONS)
    css = open(os.path.join(B, "book.css"), encoding="utf-8").read()
    page = f"""<title>SO Model Answer Script</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>{css}</style>
<nav class="bar" aria-label="Sections">
  <b>SO Model Answer Script</b>
  <label class="sr" for="jump">Go to section</label>
  <select id="jump" onchange="if(this.value)location.hash=this.value">{opts}</select>
</nav>
<main class="desk">
{body}
</main>
<script>
(function () {{
  var sel = document.getElementById("jump");
  function sync() {{ var h = location.hash.slice(1); if (h && sel.querySelector('option[value="' + h + '"]')) sel.value = h; }}
  window.addEventListener("hashchange", sync); sync();
}})();
</script>"""
    os.makedirs(os.path.join(B, "dist"), exist_ok=True)
    open(os.path.join(B, "dist", "index.html"), "w", encoding="utf-8").write(page)
    full = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
            + page + "</body></html>")
    out = os.path.join(B, "SO_Model_Answer_Book.html")
    open(out, "w", encoding="utf-8").write(full)
    print("HTML:", out, len(full) // 1024, "KB ·", len(SECTIONS), "sections")
    return out


def pdf(html_path):
    js = os.path.join(B, "make_pdf.js")
    r = subprocess.run(["node", js, html_path, os.path.join(B, "SO_Model_Answer_Book.pdf")], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())


if __name__ == "__main__":
    p = build()
    if "--no-pdf" not in sys.argv:
        pdf(p)
