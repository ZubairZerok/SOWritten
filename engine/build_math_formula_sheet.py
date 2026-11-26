#!/usr/bin/env python3
"""পরীক্ষার দিন সকালের গণিত সূত্র-শিট (বাংলা): প্রতিটি অধ্যায়ের সূত্র/নিয়ম + সবচেয়ে ছোট উদাহরণ, অগ্রাধিকার ক্রমে.
Output: final_pdfs/SO_Math_Formula_Sheet_Bangla.pdf"""
import html, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "final_pdfs", "SO_Math_Formula_Sheet_Bangla.pdf")
FONT_BN = os.path.join(ROOT, "answer_book", "fonts", "TiroBangla-400.ttf")
e = html.escape

# (অধ্যায়, ইংরেজি শব্দ, অগ্রাধিকার, [(নিয়ম, সূত্র, উদাহরণ)])
CH = [
("গতি · ট্রেন · নৌকা-স্রোত", "Speed, Train, Boat & Stream (downstream, upstream, km/h)", "★★★", [
 ("মূল সূত্র", "দূরত্ব = গতি × সময় · km/h → m/s: × 5/18 · m/s → km/h: × 18/5", "72 km/h = 72 × 5/18 = 20 m/s"),
 ("গড় গতি (সমান দূরত্ব যাওয়া-আসা)", "গড় গতি = 2xy / (x + y)", "যায় 40, আসে 60 km/h → 2·40·60/100 = 48 km/h"),
 ("আপেক্ষিক গতি", "বিপরীত দিকে = s₁ + s₂ · একই দিকে = s₁ − s₂ · মুখোমুখি মিলিত হতে সময় = দূরত্ব/(s₁ + s₂)", "300 km দূরে, 70 ও 80 km/h মুখোমুখি → 300/150 = 2 ঘণ্টা"),
 ("ট্রেন খুঁটি/মানুষ অতিক্রম", "সময় = ট্রেনের দৈর্ঘ্য ÷ গতি", "200 m ট্রেন, 20 m/s → 10 সেকেন্ড"),
 ("ট্রেন প্ল্যাটফর্ম/সেতু অতিক্রম", "সময় = (ট্রেন + প্ল্যাটফর্ম) ÷ গতি", "150 m ট্রেন, 300 m প্ল্যাটফর্ম, 54 km/h (=15 m/s) → 450/15 = 30 s"),
 ("দুই ট্রেন পরস্পরকে অতিক্রম", "সময় = (L₁ + L₂) ÷ (s₁ ± s₂) — বিপরীতে যোগ, একই দিকে বিয়োগ", "100 m ও 120 m, 40 ও 50 km/h বিপরীতে → 90 km/h = 25 m/s → 220/25 = 8.8 s"),
 ("নৌকা-স্রোত", "অনুকূলে (downstream) = u + v · প্রতিকূলে (upstream) = u − v · নৌকা u = (অনু + প্রতি)/2 · স্রোত v = (অনু − প্রতি)/2", "অনুকূলে 15, প্রতিকূলে 9 km/h → নৌকা 12, স্রোত 3 km/h"),
 ("দেরি/আগে পৌঁছানো", "দূরত্ব = s₁s₂/(s₂ − s₁) × সময়ের পার্থক্য (ঘণ্টায়)", "4 km/h-এ 10 মিনিট দেরি, 5 km/h-এ 5 মিনিট আগে → পার্থক্য ¼ ঘণ্টা → 20 × ¼ = 5 km"),
]),
("সময় ও কাজ · নল-চৌবাচ্চা", "Time & Work, Pipes & Cistern", "★★★", [
 ("এক দিনের কাজ", "A একা n দিনে করলে ১ দিনে করে 1/n অংশ", "8 দিনে করে → প্রতিদিন ⅛ অংশ"),
 ("দুজন একসঙ্গে", "সময় = ab / (a + b) · তিনজন: 1 ÷ (1/a + 1/b + 1/c)", "A 10, B 15 দিন → 150/25 = 6 দিন"),
 ("একজনের সময় বের করা", "একসঙ্গে x দিন, A একা a দিন → B = ax / (a − x)", "একসঙ্গে 12, A 20 → 240/8 = 30 দিন"),
 ("লোক-দিন-ঘণ্টা", "M₁D₁H₁ / W₁ = M₂D₂H₂ / W₂", "12 জন 10 দিনে করে → 15 জন: 12·10/15 = 8 দিন"),
 ("নল-চৌবাচ্চা", "ভরে (+), খালি করে (−) · নিট = 1/a − 1/b", "A 6 ঘণ্টায় ভরে, B 8 ঘণ্টায় খালি → 1/6 − 1/8 = 1/24 → 24 ঘণ্টা"),
 ("মজুরি ভাগ", "মজুরি কাজের অনুপাতে (১ দিনের কাজের অনুপাতে)", "A 10, B 15 দিন → কাজের অনুপাত 3:2; 500 টাকা → 300 ও 200"),
]),
("বীজগণিত ও সমীকরণ গঠন", "Algebra, Forming Equations", "★★★", [
 ("বর্গ সূত্র", "(a+b)² = a² + 2ab + b² · (a−b)² = a² − 2ab + b² · a² − b² = (a+b)(a−b) · a² + b² = (a+b)² − 2ab · 4ab = (a+b)² − (a−b)²", "a+b = 7, ab = 12 → a² + b² = 49 − 24 = 25"),
 ("ঘন সূত্র", "(a+b)³ = a³ + b³ + 3ab(a+b) · a³ + b³ = (a+b)(a² − ab + b²) · a³ − b³ = (a−b)(a² + ab + b²)", "a+b = 5, ab = 6 → a³ + b³ = 125 − 90 = 35"),
 ("x + 1/x = k হলে", "x² + 1/x² = k² − 2 · x³ + 1/x³ = k³ − 3k", "k = 3 → 7 এবং 27 − 9 = 18"),
 ("দ্বিঘাত সমীকরণ ax² + bx + c = 0", "x = [−b ± √(b² − 4ac)] / 2a · মূলের যোগফল = −b/a, গুণফল = c/a", "x² − 5x + 6 = 0 → (x−2)(x−3) = 0 → x = 2, 3"),
 ("যোগফল ও পার্থক্য", "বড় = (S + D)/2 · ছোট = (S − D)/2", "যোগফল 50, পার্থক্য 10 → 30 ও 20"),
 ("দুই অঙ্কের সংখ্যা", "সংখ্যা = 10x + y · উল্টালে 10y + x · পার্থক্য = 9(x − y)", "অঙ্কের যোগফল 9, উল্টালে 27 কমে → x − y = 3 → 63"),
 ("সমীকরণ গঠনের নিয়ম", "অজানাকে x ধরুন → 'বেশি' = +, 'কম' = −, 'গুণ' = ×, 'হয়' = '=' → সমাধান → যাচাই", "একটি সংখ্যার 3 গুণের সঙ্গে 5 যোগ করলে 20 → 3x + 5 = 20 → x = 5"),
]),
("লাভ-ক্ষতি", "Profit & Loss (CP, SP, MP, discount)", "★★★", [
 ("লাভ/ক্ষতির হার", "লাভ% = লাভ/ক্রয়মূল্য × 100 (সবসময় ক্রয়মূল্যের ওপর)", "ক্রয় 800, বিক্রয় 920 → 120/800 × 100 = 15%"),
 ("বিক্রয়মূল্য ↔ ক্রয়মূল্য", "SP = CP × (100 ± p)/100 · CP = SP × 100/(100 ± p)", "20% লাভে বিক্রি 600 → CP = 600 × 100/120 = 500"),
 ("ছাড় (Discount)", "SP = MP × (100 − d)/100", "MP 500, ছাড় 10% → 450; CP 400 হলে লাভ 50/400 = 12.5%"),
 ("পরপর দুই ছাড় a%, b%", "মোট ছাড় = a + b − ab/100", "20% ও 10% → 20 + 10 − 2 = 28%"),
 ("একই দামে দুই পণ্য: x% লাভ ও x% ক্ষতি", "সবসময় ক্ষতি = x²/100 %", "10% লাভ ও 10% ক্ষতি → 1% ক্ষতি"),
 ("কম ওজন দেওয়া দোকানদার", "লাভ% = কম দেওয়া / প্রকৃত দেওয়া × 100", "1 kg-এর বদলে 900 g → 100/900 × 100 = 11.11%"),
]),
("শতকরা", "Percentage", "★★★", [
 ("মূল সূত্র", "y-এর x% = xy/100 · শতকরা = অংশ/মোট × 100", "500-এর 12% = 60"),
 ("বৃদ্ধি পরে হ্রাস", "নিট পরিবর্তন = x − y − xy/100 (ঋণাত্মক হলে হ্রাস)", "20% বৃদ্ধি, পরে 10% হ্রাস → 20 − 10 − 2 = 8% বৃদ্ধি"),
 ("দাম বাড়লে খরচ ঠিক রাখতে", "ব্যবহার কমাতে হবে x/(100 + x) × 100 %", "দাম 25% বাড়ল → 25/125 × 100 = 20% কম ব্যবহার"),
 ("দাম কমলে", "ব্যবহার বাড়ানো যায় x/(100 − x) × 100 %", "দাম 20% কমল → 20/80 × 100 = 25% বেশি"),
 ("A, B-এর চেয়ে x% বেশি", "B, A-এর চেয়ে x/(100 + x) × 100 % কম", "25% বেশি → 20% কম"),
 ("জনসংখ্যা/মূল্য বৃদ্ধি", "P(1 + r/100)ⁿ · হ্রাস হলে P(1 − r/100)ⁿ", "10,000, বছরে 10%, 2 বছর → 12,100"),
 ("পাস-ফেল", "পাস% = 100 − (a + b − উভয়ে ফেল)", "বাংলায় ফেল 30%, ইংরেজিতে 25%, উভয়ে 10% → 100 − 45 = 55%"),
]),
("মিশ্রণ", "Mixture & Alligation (alloy, solution, milk-water)", "★★", [
 ("অ্যালিগেশন", "সস্তা : দামি = (দামি − গড়) : (গড় − সস্তা)", "60 ও 90 টাকার চাল মিশিয়ে 70 টাকা → (90−70):(70−60) = 2:1"),
 ("বারবার তুলে পানি দেওয়া", "বাকি খাঁটি = মোট × (1 − তোলা/মোট)ⁿ", "40 L দুধ, প্রতিবার 4 L তুলে পানি, 2 বার → 40 × 0.9² = 32.4 L"),
 ("অনুপাত বদলাতে যোগ", "যেটা বদলায় না সেটি স্থির রেখে সমীকরণ", "60 L-এ দুধ:পানি 2:1 (40:20) → 1:1 করতে আরও 20 L পানি"),
 ("দুই মিশ্রণ একত্র করা", "প্রতিটি উপাদান আলাদা হিসাব করে যোগ, তারপর অনুপাত", "A-তে 10 L দুধ + 5 L পানি, B-তে 6 + 9 → মোট 16:14 = 8:7"),
]),
("জ্যামিতি ও পরিমিতি", "Geometry & Mensuration (area, perimeter, volume)", "★★", [
 ("আয়তক্ষেত্র", "ক্ষেত্রফল = lb · পরিসীমা = 2(l + b) · কর্ণ = √(l² + b²)", "8 × 6 → 48 বর্গমি, 28 মি, কর্ণ 10 মি"),
 ("বর্গক্ষেত্র", "a² · 4a · কর্ণ = a√2 · ক্ষেত্রফল = কর্ণ²/2", "কর্ণ 10 → ক্ষেত্রফল 50"),
 ("ত্রিভুজ", "½ × ভূমি × উচ্চতা · হেরন: √[s(s−a)(s−b)(s−c)], s = (a+b+c)/2 · সমবাহু = (√3/4)a²", "বাহু 3, 4, 5 → s = 6 → √(6·3·2·1) = 6"),
 ("পিথাগোরাস", "অতিভুজ² = ভূমি² + লম্ব² · চেনা ত্রয়ী: 3-4-5, 5-12-13, 8-15-17", "ভূমি 5, লম্ব 12 → অতিভুজ 13"),
 ("বৃত্ত (π = 22/7)", "ক্ষেত্রফল πr² · পরিধি 2πr · অর্ধবৃত্তের পরিসীমা πr + 2r", "r = 7 → 154 বর্গসেমি, 44 সেমি"),
 ("ঘনবস্তু", "ঘনক a³ (তল 6a²) · আয়তঘন lbh (তল 2(lb+bh+hl)) · বেলন πr²h (বক্রতল 2πrh) · কোণক ⅓πr²h · গোলক 4/3 πr³ (তল 4πr²)", "বেলন r = 7, h = 10 → 22/7 × 49 × 10 = 1540"),
 ("ভেতরে চারপাশে রাস্তা", "রাস্তার ক্ষেত্রফল = 2w(l + b − 2w)", "20 × 10 মাঠে 1 মি রাস্তা → 2(28) = 56 বর্গমি"),
 ("দৈর্ঘ্য-প্রস্থ x% বাড়লে", "ক্ষেত্রফল বাড়ে 2x + x²/100 %", "10% → 21%"),
 ("কোণ", "ত্রিভুজের কোণের সমষ্টি 180° · n বাহুর বহুভুজ (n − 2) × 180° · পূরক 90°, সম্পূরক 180°", "ষড়ভুজ: 4 × 180 = 720°"),
]),
("সরল ও চক্রবৃদ্ধি সুদ", "Simple & Compound Interest (per annum, compounded)", "★★", [
 ("সরল সুদ", "I = Pnr/100 · A = P + I", "5000 টাকা, 8%, 3 বছর → 1200 টাকা"),
 ("চক্রবৃদ্ধি", "A = P(1 + r/100)ⁿ · CI = A − P", "10,000, 10%, 2 বছর → 12,100; CI = 2100"),
 ("ষাণ্মাসিক / ত্রৈমাসিক", "ষাণ্মাসিক: r/2, 2n · ত্রৈমাসিক: r/4, 4n", "10% বার্ষিক, ষাণ্মাসিক, 1 বছর → 5% করে 2 বার"),
 ("CI − SI", "2 বছর: P(r/100)² · 3 বছর: P(r/100)²(3 + r/100)", "10,000, 10% → 2 বছরে 100 টাকা"),
 ("সরল সুদে দ্বিগুণ", "r = 100/n (n বছরে দ্বিগুণ)", "8 বছরে দ্বিগুণ → 12.5%"),
 ("Rule of 72", "চক্রবৃদ্ধিতে দ্বিগুণ হওয়ার বছর ≈ 72 ÷ r", "8% → প্রায় 9 বছর"),
]),
("অনুপাত · অংশীদারি · বয়স", "Ratio, Partnership, Age", "★★", [
 ("অনুপাত যুক্ত করা", "a:b ও b:c → মাঝের পদ সমান করে a:b:c", "2:3 ও 4:5 → 8:12:15"),
 ("অনুপাতে ভাগ", "অংশ = মোট × a/(a + b)", "600 টাকা 2:3-এ → 240 ও 360"),
 ("অংশীদারি", "লাভের ভাগ ∝ মূলধন × সময় · সক্রিয় অংশীদারের বেতন আগে বাদ", "A 5000 × 12 মাস, B 6000 × 8 মাস → 60000:48000 = 5:4"),
 ("বয়স", "বর্তমান বয়স 7x, 2x ধরে সমীকরণ", "বাবা:ছেলে 7:2, 5 বছর পর 8:3 → 3(7x+5) = 8(2x+5) → x = 5 → 35 ও 10"),
]),
("গড়", "Average", "★", [
 ("মূল সূত্র", "গড় = যোগফল ÷ সংখ্যা · ক্রমিক সংখ্যার গড় = (প্রথম + শেষ)/2", "1 থেকে 9-এর গড় = 5"),
 ("নতুন সদস্য যোগ", "নতুন সদস্যের মান = (n + 1) × নতুন গড় − n × পুরোনো গড়", "10 জনের গড় 20, একজন এলে গড় 21 → 231 − 200 = 31"),
]),
("ধারা", "Series / Progression (AP, GP)", "★", [
 ("সমান্তর (AP)", "tₙ = a + (n−1)d · Sₙ = n/2 [2a + (n−1)d] = n/2 (a + l) · পদসংখ্যা n = (l − a)/d + 1", "2, 5, 8 … → 10ম পদ 29; S₁₀ = 5(2 + 29) = 155"),
 ("গুণোত্তর (GP)", "tₙ = arⁿ⁻¹ · Sₙ = a(rⁿ − 1)/(r − 1) · অসীম যোগফল a/(1 − r), |r| < 1", "3, 6, 12 … → 5ম পদ 48; S₅ = 3 × 31 = 93"),
 ("বিশেষ যোগফল", "1 + 2 + … + n = n(n+1)/2 · বর্গের যোগফল n(n+1)(2n+1)/6 · ঘনের যোগফল [n(n+1)/2]² · প্রথম n বিজোড় = n²", "1 থেকে 50 = 50 × 51/2 = 1275"),
]),
("সম্ভাবনা · বিন্যাস · সমাবেশ", "Probability, Permutation, Combination", "★", [
 ("সম্ভাবনা", "P = অনুকূল ÷ মোট · না ঘটার সম্ভাবনা = 1 − P · স্বাধীন ঘটনা: P(A ও B) = P(A) × P(B)", "দুটি ছক্কায় যোগফল 7 → 6/36 = 1/6"),
 ("অন্তত একটি", "1 − কোনোটিই না", "3টি মুদ্রায় অন্তত একটি হেড → 1 − 1/8 = 7/8"),
 ("বিন্যাস ও সমাবেশ", "ⁿPᵣ = n!/(n − r)! · ⁿCᵣ = n!/[r!(n − r)!] · ক্রম গুরুত্বপূর্ণ হলে P, না হলে C", "⁵P₂ = 20 · ⁵C₂ = 10 · ⁶C₃ = 20"),
 ("একই অক্ষর থাকলে", "সাজানোর উপায় = n! ÷ (p! q! …)", "BANANA → 6!/(3! 2!) = 60"),
 ("মনে রাখার সংখ্যা", "এক মুদ্রা 2, দুই মুদ্রা 4, তিন মুদ্রা 8 ফল · দুই ছক্কা 36 · তাস 52: প্রতি রঙে 13, টেক্কা 4, ছবির তাস 12", ""),
]),
("সেট ও ভেনচিত্র", "Set & Venn Diagram", "★", [
 ("দুই সেট", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B) · কোনোটিই না = মোট − n(A ∪ B)", "100 জনে চা 60, কফি 50, দুটোই 20 → 90; কোনোটিই না 10"),
 ("তিন সেট", "n(A∪B∪C) = n(A)+n(B)+n(C) − n(A∩B) − n(B∩C) − n(A∩C) + n(A∩B∩C)", ""),
]),
]

QUICK = [
 ("72 km/h কত m/s?", "20 m/s"), ("A 12 দিনে, B 24 দিনে — একসঙ্গে?", "8 দিন"), ("ক্রয় 800, বিক্রয় 920 — লাভ%?", "15%"),
 ("30% বৃদ্ধি, পরে 30% হ্রাস — নিট?", "9% হ্রাস"), ("2000 টাকা, 5% সরল সুদে 4 বছর — সুদ?", "400 টাকা"),
 ("10,000 টাকা, 10% চক্রবৃদ্ধি, 2 বছর — CI?", "2100 টাকা"), ("অনুকূলে 18, প্রতিকূলে 12 km/h — স্রোতের বেগ?", "3 km/h"),
 ("r = 14 সেমি বৃত্তের ক্ষেত্রফল?", "616 বর্গসেমি"), ("1 থেকে 50 পর্যন্ত যোগফল?", "1275"), ("⁶C₃ = ?", "20"),
 ("55 ও 85 টাকার চাল মিশিয়ে 65 — অনুপাত?", "2:1"), ("দাম 25% বাড়লে ব্যবহার কত কমাবেন?", "20%"),
]
VOCAB = [("per annum", "বার্ষিক"), ("compounded half-yearly", "ষাণ্মাসিক চক্রবৃদ্ধি"), ("principal", "আসল"), ("downstream / upstream", "স্রোতের অনুকূলে / প্রতিকূলে"),
         ("still water", "স্থির পানি"), ("cistern / tank", "চৌবাচ্চা"), ("alloy", "সংকর ধাতু"), ("cost price / selling price", "ক্রয়মূল্য / বিক্রয়মূল্য"),
         ("marked price", "লিখিত মূল্য"), ("ratio / proportion", "অনুপাত / সমানুপাত"), ("perimeter / circumference", "পরিসীমা / পরিধি"), ("consecutive", "ক্রমিক")]

CSS = """
@font-face { font-family: "TiroB"; src: url("file://__BN__"); }
@page { size: A4; margin: 10mm 10mm 12mm 10mm; }
* { box-sizing: border-box; }
body { font-family: "TiroB", "Inter", sans-serif; color: #0f172a; font-size: 10.2pt; line-height: 1.42; margin: 0; }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #0f172a; padding-bottom: 4pt; margin-bottom: 6pt; }
h1 { font-size: 19pt; margin: 0; } .tag { font-family: Inter; font-size: 8pt; color: #2563eb; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
.how { background: #ecfdf5; border-left: 3pt solid #047857; padding: 5pt 9pt; margin: 0 0 7pt; font-size: 10pt; }
.ch { margin: 0 0 7pt; break-inside: auto; }
.ch h2 { font-size: 12.4pt; margin: 4pt 0 2pt; padding: 2pt 7pt; background: #0f172a; color: #fff; border-radius: 4pt; break-after: avoid; }
.ch h2 small { font-family: Inter; font-weight: 500; font-size: 8pt; color: #cbd5e1; margin-left: 6pt; } .ch h2 i { float: right; color: #fbbf24; font-style: normal; }
.r { display: grid; grid-template-columns: minmax(0,21fr) minmax(0,43fr) minmax(0,36fr); gap: 0 7pt; padding: 2.6pt 3pt; border-bottom: 1px solid #e5eaf1; break-inside: avoid; }
.r b { color: #1e293b; } .r .f { font-family: "Inter", "TiroB"; font-size: 9.3pt; color: #1d4ed8; } .r span { overflow-wrap: anywhere; } .r .x { box-decoration-break: clone; -webkit-box-decoration-break: clone; background: #fef9c3; border-radius: 3pt; padding: 0 4pt; font-size: 9.6pt; }
.head { font-family: Inter; font-size: 7.6pt; color: #64748b; text-transform: uppercase; letter-spacing: .06em; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8pt; break-inside: avoid; }
.box { border: 1px solid #dbe3ee; border-radius: 6pt; padding: 5pt 8pt; } .box h3 { margin: 0 0 3pt; font-size: 11pt; color: #2563eb; }
.box ol { margin: 0; padding-left: 15pt; } .box li { margin: 1pt 0; } .ans { color: #047857; font-family: Inter; font-size: 9pt; }
.v { display: grid; grid-template-columns: 1fr 1fr; gap: 0 8pt; font-size: 9.6pt; } .v span { font-family: Inter; color: #1d4ed8; }
"""


def main():
    head = '<div class="r head"><span>নিয়ম</span><span>সূত্র</span><span>সবচেয়ে ছোট উদাহরণ</span></div>'
    body = ""
    for name, en, st, rows in CH:
        body += f'<div class="ch"><h2>{e(name)}<small>{e(en)}</small><i>{st}</i></h2>{head}' + "".join(
            f'<div class="r"><b>{e(a)}</b><span class="f">{e(b)}</span><span>{"<span class=x>" + e(c) + "</span>" if c else ""}</span></div>' for a, b, c in rows) + "</div>"
    quick = "".join(f"<li>{e(q)} <span class='ans'>→ {e(a)}</span></li>" for q, a in QUICK)
    vocab = "".join(f"<div><span>{e(a)}</span> = {e(b)}</div>" for a, b in VOCAB)
    doc = f"""<!doctype html><html lang="bn"><head><meta charset="utf-8"><title>Math Formula Sheet</title><style>{CSS.replace("__BN__", FONT_BN)}</style></head><body>
<div class="top"><div><div class="tag">SO Written · 27 Nov 2026 · Math (30 marks) · exam-morning sheet</div><h1>গণিত সূত্র-শিট — সব সূত্র + ছোট উদাহরণ</h1></div></div>
<div class="how"><b>পরীক্ষার হলে:</b> প্রতিটি অঙ্কে <b>"Let …" দিয়ে শুরু</b> → সূত্র লিখুন → প্রতিটি ধাপ → উত্তর <b>বক্স</b> করুন, <b>একক</b> লিখুন। একটি অঙ্কে ৬ মিনিটের বেশি নয় — আটকালে পরেরটায় যান। ক্রম: ★★★ অধ্যায় সবচেয়ে বেশি আসে (২০১৫-এর পরের পরীক্ষা অনুযায়ী)।</div>
{body}
<div class="grid2"><div class="box"><h3>দ্রুত অনুশীলন (২ মিনিট)</h3><ol>{quick}</ol></div>
<div class="box"><h3>প্রশ্নের ইংরেজি শব্দ</h3><div class="v">{vocab}</div></div></div>
</body></html>"""
    hp = OUT.replace(".pdf", ".html"); open(hp, "w", encoding="utf-8").write(doc)
    js = os.path.join(ROOT, "final_pdfs", ".mkmf.js")
    open(js, "w").write(r"""const { chromium } = require("playwright");
(async () => { const [inp, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
 await p.goto("file://" + inp); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;text-align:center;font-family:Inter,Arial;font-size:7.5px;color:#64748b">Math Formula Sheet (Bangla) · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
 await b.close(); })().catch((e) => { console.error(e); process.exit(1); });""")
    try:
        subprocess.run(["node", js, hp, OUT], check=True, cwd=ROOT)
    finally:
        os.remove(js); os.remove(hp)
    print("PDF:", OUT)


if __name__ == "__main__":
    main()
