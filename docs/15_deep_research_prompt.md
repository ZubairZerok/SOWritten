# ১৫ · Deep Research Prompt (শেষ ফাঁকগুলো পূরণের জন্য)

> নিচের ব্লকটি পুরোটা কপি করে যেকোনো Deep Research টুলে দিন (Claude Research, ChatGPT Deep Research, Gemini Deep Research, Perplexity)। পাওয়া ফলাফল এই রিপোতে দিলে `data/facts.json`, `data/quiz.json` আর `answers/`-এ সরাসরি বসানো যাবে, কারণ আউটপুটের ফরম্যাট রিপোর স্কিমার সাথে মিলিয়ে চাওয়া হয়েছে।

```text
ROLE
You are a meticulous research analyst preparing a candidate for the Bangladesh
combined-bank SENIOR OFFICER (SO) WRITTEN exam on FRIDAY 27 NOVEMBER 2026,
9:30–11:30 am, 200 marks, 2 hours, hand-written, no calculator.
Today is 20 November 2026. The candidate's target is 128/200, they have 7 days,
and they read Bangla fastest. Every fact you give will be MEMORISED and WRITTEN
in an exam, so a wrong number is worse than no number.

NON-NEGOTIABLE RULES
1. Every number, name and date needs >=2 independent sources, at least one
   PRIMARY (Bangladesh Bank, BBS, Finance Division, EPB, BIDA, IMF, World Bank,
   ADB, UN, official gazette). Give the URL and the publication date for each.
2. Prefer the MOST RECENT figure released on or before 26 Nov 2026. State the
   period the figure refers to (e.g. "Oct 2026, y/y") and the release date.
3. If sources disagree, show both, say which is official, and mark CONFLICT.
4. If you cannot verify something, write UNVERIFIED. Never fill gaps from memory.
5. Search in BOTH Bangla and English (e.g. "খেলাপি ঋণ সেপ্টেম্বর ২০২৬" and
   "default loans September 2026 Bangladesh Bank").
6. Window for news: 20 May 2026 – 26 Nov 2026. Older items only if still current.

SOURCES TO SWEEP (minimum)
Bangla: Prothom Alo, Bonik Barta, Samakal, Kaler Kantho, Jugantor, Ittefaq,
  Banglanews24, bdnews24 (Bangla), Dainik Bangla, Desh Rupantor, Ajker Patrika,
  BBC Bangla.
English (BD): The Daily Star, The Financial Express, The Business Standard,
  Dhaka Tribune, New Age, UNB, BSS.
International: Reuters, Bloomberg, Financial Times, The Economist, Nikkei Asia,
  Al Jazeera, IMF (WEO Oct 2026, Article IV/programme reviews), World Bank
  (Bangladesh Development Update), ADB (ADO Sept 2026 + Dec supplement).
Official: bb.org.bd (MPS, press releases, Major Economic Indicators, Financial
  Stability Report, circulars), bbs.gov.bd (CPI, GDP), mof.gov.bd (budget FY27),
  epb.gov.bd (exports), erecruitment.bb.org.bd + Bankers' Selection Committee
  (BSC) notices.

PART A — EXAM LOGISTICS (highest priority; verify, do not assume)
A1. The official notice for the 27 Nov 2026 SO written exam: which banks/FIs,
    number of posts, admit card, venue, exact time, and whether the marks split
    is still: Focus writing Bangla 30 + English 30, Analytical/Argumentative 40,
    Translation 20, Math 30, English language 20, Bangla grammar 10,
    Banking 10, GK 10 (total 200). Quote the notice text and give its link.
A2. Any change in rules: allowed pens, answer-script pages, negative marking,
    whether Bangla/English is optional per question.
A3. Typical written pass/cut-off marks of the last 3 combined SO exams, ONLY if
    an official or widely corroborated source exists; else UNVERIFIED.
A4. Past SO-level written papers from 2024–2026 that I may be missing
    (combined 8–10 banks SO, SO IT, Bangladesh Bank AD/Officer General,
    BDBL/BKB/RAKUB SO, Probashi Kallyan Bank SO). For each: date, exam name,
    every question verbatim, marks per question. Flag the source quality.

PART B — VERIFY THESE FLAGGED ITEMS (yes/no + corrected value + 2 sources)
B1. Bangladesh Bank policy (repo) rate = 9.5% (cut from 10% on 30 Jul 2026,
    effective 2 Aug), SLF 11%, SDF 7.5%. Any change after Oct 2026?
B2. Bangladesh Bank Governor's full name as of Nov 2026.
B3. Point-to-point inflation Oct 2026 = 8.27% (BBS). Food/non-food split.
    Is the Nov 2026 figure out before 27 Nov? (normally early Dec — confirm).
B4. Default (classified) loans: 32.78% (Jun 2026), 32.17% (Sep 2026), amount
    in Tk crore, and the state-owned vs private split.
B5. Gross reserve (BPM6) latest + IMF's NIR, with date.
B6. Remittance FY26 = US$35.59 bn; Jul–Oct FY27 figure and growth.
B7. Exports FY26 (EPB) and Jul–Oct FY27 growth; RMG share.
B8. FY26 GDP growth (BBS provisional/final = 3.68%?), FY27 targets
    (GDP 6.5%, inflation 7.5%), budget size Tk 9.38 lakh crore — confirm.
B9. IMF Oct 2026 WEO forecast for Bangladesh FY27 (3.2%?), World Bank and ADB
    latest forecasts.
B10. LDC graduation new date = 24 Nov 2029 (UNGA resolution?) — exact decision.
B11. US tariff on Bangladeshi goods: 10% Section 301 from 24 Jul 2026 after the
    Supreme Court struck down the 19% reciprocal tariff — confirm details.
B12. Five Shariah banks merged into "Sammilito Islami Bank PLC" — date, capital,
    status of depositor payouts.
B13. Deposit Protection Act 2026: insured limit Tk 2 lakh? Effective date.
B14. Fuel: diesel Tk 135/litre after the Sep 2026 adjustment? Any later change.
B15. Bangla QR, IIPS (target Jun 2027), IFRS 9 ECL (2027) — confirm.
B16. EU GSP+ / new GSP regulation effective 1 Jan 2027 — confirm.
B17. COP31: venue (Antalya, Türkiye?), dates, Bangladesh's key asks.
B18. Bangladesh–Japan EPA: signed? date? first EPA of Bangladesh?
B19. Past-paper GK answers I am unsure of:
     (a) June 2026 SO paper GK (d): is the answer "BSIC"? Give the question.
     (b) "South Asia's first railway overpass for elephants" — Bangladesh,
         Chunati (Dohazari–Cox's Bazar line)? Confirm.
     (c) How many IMF loan programmes has Bangladesh had (13?) — confirm count.
B20. CTR threshold Tk 10 lakh and STR reporting to BFIU — still current?

PART C — FRESH DATA PACKS FOR LIKELY ESSAY/ARGUMENT TOPICS
For each topic give: 5 latest numbers (with period + source), 5 causes,
5 government/BB actions taken in 2026, 5 solutions, 1 quotable line from a
named official/report (2026), and 1 counter-argument. Bangla + English.
C1 Inflation & cost of living          C2 Default loans & banking reform
C3 Bank mergers/resolution & deposit protection
C4 Reserves, exchange rate, remittance  C5 Exports, RMG, US tariff, EU GSP
C6 LDC graduation 2029 preparedness     C7 Digital banking, Bangla QR, MFS, cyber risk
C8 Climate finance & COP31              C9 Youth unemployment & skills
C10 FY27 budget & revenue (tax-GDP)     C11 AI in banking
C12 Rohingya / energy crisis / Fed rate effects (one line each, latest)

PART D — REPLACE OUTDATED STUDY PDFs (what changed since they were written)
For each, give the 2026 reality in 5 bullets with sources:
PDF08 COP27 · PDF24 Smart Bangladesh 2041 (is the term still official
policy after 2024?) · PDF25 IMF loan programme status · PDF26/PDF58 Russia–
Ukraine war impact (now) · PDF28 LDC graduation (2026 → 2029) · PDF38
Karnaphuli tunnel (traffic/revenue reality) · PDF41 Padma Bridge (revenue,
rail link) · PDF43 Universal Pension scheme (status 2026) · PDF52/53 reserve &
dollar crisis (now) · PDF54 mega projects (status/debt) · PDF37 TakaPay
(status) · PDF18 quotations (which political quotes are no longer safe to use
in an exam; give 10 safe, neutral quotations with exact wording and author).

PART E — GRAMMAR FACT-CHECK (Bangla Academy / standard references)
E1. Bangla Academy প্রমিত বানান rules most tested in bank exams (ই-কার in
    foreign/tadbhava words, ণত্ব-ষত্ব, রেফের পর দ্বিত্ব নয়), with 20 examples.
E2. Under the current NCTB 9–10 Bangla grammar, how is সম্প্রদান কারক treated,
    and is "বৃষ্টিতে ফসল নষ্ট হলো" (বৃষ্টিতে) করণ or অপাদান/অধিকরণ? Cite.
E3. 20 most-repeated idioms/phrasal verbs from bank written exams 2022–2026.

OUTPUT FORMAT (exactly this order)
1. A one-page executive summary: what changed vs the figures in PART B.
2. PART A answers.
3. PART B as a table: item | my value | verified value | status
   (CONFIRMED/CORRECTED/CONFLICT/UNVERIFIED) | source 1 (date) | source 2 (date).
4. PART C–E in sections.
5. A JSON array I can paste into my app, one object per verified fact:
   {"topic": "<inflation|banking|reserve|trade|ldc|digital|climate|budget|
    monetary|youth|ai|gk>", "bn": "<Bangla sentence with the number>",
    "en": "<English sentence>", "src": "<SOURCE, date>"}
6. A JSON array of 20 new GK MCQs:
   {"q": "<Bangla question>", "o": ["opt1","opt2","opt3","opt4"],
    "a": <index of correct option, 0-based>, "src": "<source, date>"}
7. A list of everything you could NOT verify.
```

## রিপো থেকে ফলাফল ঢোকানো

1. ধাপ ৫-এর JSON যাবে `data/facts.json`-এর `facts` তালিকায়, আর ধাপ ৬-এর JSON যাবে `data/quiz.json`-এর `gk` তালিকায়।
2. তারপর এই কমান্ডগুলো চালান:
   - `python3 tests/validate_all.py`
   - `python3 webapp/build.py`
   - `node webapp/tests/stress.test.js`
3. PART B-তে যা CORRECTED এসেছে, সেটা `answers/`, `docs/04_topic_bank.md` আর `docs/00_one_page.md`-এ খুঁজে বদলে দিন।
