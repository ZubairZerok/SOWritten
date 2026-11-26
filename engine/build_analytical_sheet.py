#!/usr/bin/env python3
"""পরীক্ষার দিন সকালের Analytical Reasoning, Critical Thinking ও Argument Writing (৪০ নম্বর) শিট — বাংলায় নিয়ম + ছোট বাস্তব উদাহরণ.
Content: docs/17_analytical_40_marks.md (verified). Output: final_pdfs/SO_Analytical_40_Sheet_Bangla.pdf"""
import html, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_math_formula_sheet import CSS, FONT_BN, ROOT  # noqa: E402

OUT = os.path.join(ROOT, "final_pdfs", "SO_Analytical_40_Sheet_Bangla.pdf")
e = html.escape

CH = [
("প্রশ্নের ধরন ও ২২ মিনিটের পরিকল্পনা", "Question 6: (a) puzzle · (b) critique · (c) assumption · (d) argument", "★★★", [
 ("চার ভাগ (প্রায় ১০ নম্বর করে)", "(a) লজিক পাজল · (b) কারও সিদ্ধান্তের সমালোচনা · (c) অনুমান/দুর্বল/শক্ত/সিদ্ধান্ত · (d) পক্ষে-বিপক্ষে যুক্তি", "জুন ২০২৬: (a) ৫ প্রার্থীর ইন্টারভিউ সূচি · (b) দুই গুদামের তুলনা · (c) আমানত বিমা · (d) পরিবেশ বনাম প্রবৃদ্ধি"),
 ("উত্তরের ক্রম", "(a) → (c) → (b) → (d) — নিশ্চিত নম্বর আগে", "০–১ মিনিট পড়া ও T-chart · ১–৭ পাজল · ৭–১০ অনুমান · ১০–১৫ সমালোচনা · ১৫–২২ আর্গুমেন্ট"),
 ("একটাই বড় প্রশ্ন এলে", "পুরো ২২ মিনিট আর্গুমেন্ট — ৬ অনুচ্ছেদ (নিচে কাঠামো B)", "২০২৫ পর্যন্ত এভাবেই আসত (৩০ নম্বর)"),
 ("পরীক্ষক কী চান", "(a) উত্তর + ধাপ + যাচাই · (b) ৪–৬টি নাম দেওয়া ফাঁক + ভালো বিকল্প · (c) এক বাক্যে অনুমান + কেন · (d) স্পষ্ট অবস্থান + ৩+৩ যুক্তি + বাংলাদেশের সংখ্যা", "শুধু উত্তর লিখলে পাজলে অর্ধেক নম্বর কাটা যায়"),
]),
("(a) লজিক পাজল", "Analytical Reasoning: schedule, seating, floor, ranking, selection", "★★★", [
 ("৬ ধাপের পদ্ধতি", "১ ছক আঁকুন → ২ নিশ্চিত তথ্য বসান → ৩ জোড়া শর্ত ('ঠিক পরে') → ৪ নিষেধ × দিয়ে → ৫ ২–৩টি সম্ভাবনা আলাদা করে চেষ্টা → ৬ প্রতিটি শর্ত ✓ দিয়ে যাচাই", "জুন ২০২৬: C শুক্র, E মঙ্গল (নিশ্চিত) → A, E-র আগে → সোম → B-র ঠিক পরে D → বুধ-বৃহস্পতি → সূচি A, E, B, D, C"),
 ("শব্দের মানে", "before/after = যেকোনো আগে/পরে · immediately before/after = ঠিক পাশের ঘর · not before A = A-র পরে (বা একসঙ্গে)", "'D immediately after B' আর B বুধবার → D অবশ্যই বৃহস্পতিবার; 'D after B' হলে বৃহস্পতি বা শুক্র"),
 ("সারিতে বসা (সোজা লাইন)", "উত্তরমুখী হলে তাদের ডান = আপনার ডান · দক্ষিণমুখী হলে উল্টো · প্রান্ত (end) মানে ১ বা শেষ চেয়ার", "৫ জন উত্তরমুখী; A ঠিক মাঝে (৩ নম্বর), B A-র ঠিক বাঁয়ে → B ২ নম্বর চেয়ারে"),
 ("গোল টেবিল", "কেন্দ্রমুখী হলে ডান = ঘড়ির কাঁটার উল্টো দিক · মুখোমুখি = ঠিক বিপরীত চেয়ার (৬ জনে ৩ ঘর দূরে)", "৬ জন কেন্দ্রমুখী; A-র ঠিক ডানে B → A থেকে ঘড়ির উল্টো দিকে পরের চেয়ারে B"),
 ("তলা (Floor)", "১ = নিচতলা · above/below = যেকোনো ওপরে/নিচে · immediately above = ঠিক ওপরের তলা", "৫ তলা ভবন; P সবার ওপরে (৫), Q P-র ঠিক নিচে → Q ৪ তলায়"),
 ("র‍্যাংক / তুলনা", "চিহ্ন দিয়ে একটি লাইনে সাজান: বড় > ছোট", "A > B, C < B, D > A → D > A > B > C → সবচেয়ে বেশি বেতন D-র"),
 ("দল বাছাই (Selection)", "'A থাকলে B নয়' মানে 'B থাকলে A নয়'ও · 'C ছাড়া D যায় না' মানে D থাকলে C আছে", "৫ জন থেকে ৩ জনের কমিটি: {A, C, D} বৈধ? A আছে B নেই ✓, D আছে C আছে ✓ → বৈধ"),
 ("যদি-তবে (If-then)", "'যদি P তবে Q' → Q না হলে P নয় (সঠিক) · Q হলে P নিশ্চিত নয় (ভুল সিদ্ধান্ত)", "'বৃষ্টি হলে মাঠ ভেজে' → মাঠ শুকনো → বৃষ্টি হয়নি ✓ · মাঠ ভেজা → বৃষ্টি হয়েছে? নিশ্চিত নয় (পানি দেওয়া হতে পারে)"),
 ("উত্তর লেখার ধরন", "ছক → প্রতিটি ধাপ এক লাইনে ('Since C is on Friday…') → শেষে 'Check:' সব শর্ত ✓", "Check: A before C ✓ · B not Mon/Fri ✓ · D right after B ✓ · E not before A ✓"),
]),
("(b) সিদ্ধান্তের সমালোচনা — ১২টি সাধারণ ফাঁক", "Critical Thinking: evaluate a conclusion (name the flaw!)", "★★★", [
 ("৩ ধাপ", "১ দাবি এক লাইনে: 'The CEO concludes X because Y' → ২ নিচের তালিকা থেকে ৪–৬টি ফাঁক, প্রতিটির নাম + ব্যাখ্যা → ৩ ভালো বিকল্প (কোন ডেটা, কোন পাইলট)", "জুন ২০২৬: উত্তর গুদাম গড়ে ২ দিনে, দক্ষিণ ৪ দিনে দেয় → CEO: উত্তর দ্বিগুণ দক্ষ, ৮০% অর্ডার উত্তরে"),
 ("১. Correlation ≠ causation", "একসঙ্গে ঘটেছে বলে একটি অন্যটির কারণ নয়", "যে শাখায় বেশি এটিএম সেখানে আমানত বেশি → এটিএম বসালেই আমানত বাড়বে? না, দুটোই শহুরে এলাকা বলে"),
 ("২. Post hoc (আগে-পরে)", "X-এর পরে Y হয়েছে, তাই X-ই কারণ — ধরে নেওয়া", "নতুন ম্যানেজার আসার পর ঋণ আদায় বাড়ল → তাঁর কৃতিত্ব? একই সময়ে সারা দেশেই আদায় বেড়েছে কি না দেখা হয়নি"),
 ("৩. Unrepresentative sample", "নমুনা ছোট বা একপেশে", "অ্যাপ ব্যবহারকারী ৫০০ জনের ৯০% ডিজিটাল সেবা চান → সব গ্রাহক চান? গ্রামের বয়স্করা জরিপেই নেই"),
 ("৪. Average hides spread", "শুধু গড় দেখা, তারতম্য বাদ", "উত্তর গুদামের গড় ২ দিন — কিন্তু কিছু অর্ডারে ৭ দিনও লাগতে পারে; দূরত্ব ও অর্ডারের ধরন আলাদা"),
 ("৫. Unlike comparison", "যাদের তুলনা, তাদের অবস্থা আলাদা", "ঢাকার শাখা গ্রামের শাখার চেয়ে বেশি লাভ করে → গ্রামের ম্যানেজার দুর্বল? বাজারই তো আলাদা"),
 ("৬. Capacity / scalability", "ছোট পরিসরে কাজ করেছে বলে বড় পরিসরেও করবে", "উত্তর গুদাম ২০% অর্ডারে ২ দিনে দেয় → ৮০% অর্ডার দিলেও কি ২ দিনে দেবে? জনবল ও গাড়ি সীমিত"),
 ("৭. Ignoring cost", "শুধু লাভ দেখা, খরচ ও ঝুঁকি বাদ", "এজেন্ট আউটলেট দ্বিগুণ করলে গ্রাহক বাড়বে → প্রতি গ্রাহকে খরচ কত, প্রতারণার ঝুঁকি কত?"),
 ("৮. Percentage vs absolute", "শতাংশ বড়, ভিত্তি ছোট (বা উল্টো)", "গ্রাহক অভিযোগ ১০০% বেড়েছে → আসলে ২টি থেকে ৪টি"),
 ("৯. Alternative explanation", "অন্য কারণেও একই ফল আসতে পারত", "বিজ্ঞাপনের পর বিক্রি বাড়ল → ঈদের মৌসুমও তো ছিল"),
 ("১০. Diminishing returns", "খরচ তিনগুণ করলে ফলও তিনগুণ — ধরে নেওয়া", "প্রশিক্ষণে ১ লাখ খরচে বিক্রি ১০% বাড়ল → ৩ লাখে ৩০% বাড়বে? না"),
 ("১১. False dichotomy", "মাত্র দুটি বিকল্প ধরা, অথচ আরও আছে", "'হয় শাখা বন্ধ, নয় লোকসান' → একীভূত করা বা এজেন্ট ব্যাংকিংও তো বিকল্প"),
 ("১২. Hasty generalisation", "এক-দুটি উদাহরণ থেকে সবার সম্পর্কে সিদ্ধান্ত", "দুজন তরুণ উদ্যোক্তা খেলাপি → সব তরুণ উদ্যোক্তা ঝুঁকিপূর্ণ? দুটি উদাহরণ যথেষ্ট নয়"),
 ("উত্তরের ছাঁচ (ইংরেজিতে)", "The conclusion is not justified. The CEO assumes that … 1. [flaw name]: … 2. … 3. … 4. … A better approach: collect …, compare like with like, run a pilot, decide on cost per unit of benefit.", "A better approach: compare both warehouses on the same order type and distance, test North at 50% load for one month, then decide."),
]),
("(c) অনুমান · দুর্বল · শক্ত · সিদ্ধান্ত", "Assumption, Weaken, Strengthen, Inference, Flaw", "★★", [
 ("যুক্তির ৩ অংশ", "Premise (তথ্য) + [লুকানো Assumption = সেতু] → Conclusion", "তথ্য: আমানত বিমা আছে · সিদ্ধান্ত: ব্যাংক বেশি দেউলিয়া হয় · সেতু: আমানতকারীর যাচাই-ই ব্যাংককে সাবধান রাখে"),
 ("Assumption খোঁজা", "না বলা অথচ দরকারি কথা · উল্টানোর পরীক্ষা: উল্টে দিলে যুক্তি ভেঙে পড়লে সেটিই অনুমান", "উল্টে দিন: 'আমানতকারী যাচাই না করলেও বাংলাদেশ ব্যাংকের তদারকিই ব্যাংককে সাবধান রাখে' → যুক্তি ভেঙে গেল → এটাই অনুমান"),
 ("Weaken (দুর্বল করা)", "বিকল্প কারণ দেখান বা অনুমানটি মিথ্যা দেখান", "দাবি: 'সুদ বাড়ালেই মূল্যস্ফীতি কমবে' → দুর্বল করে: মূল্যস্ফীতির কারণ আমদানি খরচ ও টাকার অবমূল্যায়ন, ঋণের চাহিদা নয়"),
 ("Strengthen (শক্ত করা)", "অনুমানটি সত্য প্রমাণ করুন বা বিকল্প কারণ বাতিল করুন", "একই দাবি → শক্ত করে: আগেও সুদ বাড়ানোর ৬ মাস পর মূল্যস্ফীতি কমেছিল, অন্য সব কারণ স্থির থাকা অবস্থায়"),
 ("Inference (সিদ্ধান্ত টানা)", "তথ্য থেকে অবশ্যই যা সত্য — নতুন কিছু যোগ নয়", "সব ডিজিটাল ব্যাংকের শাখা নেই; X একটি ডিজিটাল ব্যাংক → 'X-এর শাখা নেই' ✓ · 'X-এর গ্রাহক কম' — বলা যায় না"),
 ("Flaw (ভুলের নাম)", "ওপরের ১২টি ফাঁক থেকে নাম বেছে নিন", "'X-এর পরে Y, তাই X কারণ' → Post hoc"),
 ("উত্তরের ছাঁচ", "এক বাক্যে অনুমান + এক লাইনে কেন দরকার — পুরো যুক্তি আবার লিখবেন না", "The argument assumes that depositors' monitoring is what keeps banks careful. If supervision alone were enough, the conclusion would not follow."),
]),
("(d) পক্ষে-বিপক্ষে যুক্তি ও আর্গুমেন্ট রচনা", "Argumentative Writing: position, for/against, evidence", "★★★", [
 ("অবস্থান বাছাই", "দাবিতে only / always / all / best / more important than থাকলে → partly agree · নীতির প্রশ্নে → 'Yes, but only if …' · ভূমিকা ও উপসংহারে একই অবস্থান", "'Raising the policy rate is the only way to control inflation' → 'only' আছে → partly agree: সুদ দরকার, কিন্তু সরবরাহ ও বাজার তদারকিও লাগবে"),
 ("কাঠামো A — ছোট (৮ মিনিট, ২০০–২৫০ শব্দ)", "ভূমিকা ২ লাইন (বিষয় + ১টি সংখ্যা + 'This answer examines both sides') → পক্ষে ৩ পয়েন্ট → বিপক্ষে ৩ পয়েন্ট → অবস্থান ২–৩ লাইন + শর্ত", "পরিবেশ বনাম প্রবৃদ্ধি: পক্ষে — জলবায়ু ঝুঁকিতে ১৩তম, বন্যায় ১০.২ লাখ মানুষ · বিপক্ষে — ৬.৫% প্রবৃদ্ধি দরকার কর্মসংস্থানে · অবস্থান: সবুজ প্রবৃদ্ধি"),
 ("কাঠামো B — পূর্ণ (২২ মিনিট, ৩৫০–৪৫০ শব্দ, ৬ অনুচ্ছেদ)", "১ ভূমিকা: hook (সংখ্যা) + পটভূমি + thesis · ২–৪ তিনটি যুক্তি, প্রতিটিতে বাংলাদেশের সংখ্যা · ৫ counter-argument + খণ্ডন · ৬ সুপারিশ (৩–৪ বুলেট) + উপসংহার", "Hook: 'Inflation stood at 8.27% in October 2026 even after the policy rate reached 10%.'"),
 ("T-chart (রুক্ষ খসড়া, ১ মিনিট)", "দুই কলাম: Pro | Con — প্রতিটিতে ৩টি শব্দ-সংকেত + পাশে ১টি সংখ্যা", "Pro: জলবায়ু ক্ষতি (১৩তম), বন্যা (১০.২ লাখ) · Con: চাকরি (প্রতি ৩ স্নাতকে ১ বেকার), প্রবৃদ্ধি ৩.৬৮%"),
 ("শুরুর বাক্যাংশ", "It is often argued that … · At first glance, …; however, a closer look reveals …", "It is often argued that digital banking will end branch banking; however, a closer look reveals …"),
 ("যুক্তির বাক্যাংশ", "First and foremost, … · A case in point is … · This is evident from …", "A case in point is the record remittance of USD 35.59 billion in FY26."),
 ("বিপক্ষ খণ্ডনের বাক্যাংশ", "Admittedly, …; nevertheless, … · Critics may contend that …, but … · This argument rests on the assumption that …", "Critics may contend that higher rates hurt investment, but private credit growth was already 4.17% because of weak confidence."),
 ("উপসংহারের বাক্যাংশ", "Taking all these factors into account, … · On balance, the claim is only partially valid. · It would be an oversimplification to claim that …", "On balance, the claim is only partially valid: rate hikes help, but only with supply-side action."),
 ("নিষেধ", "'I think' নয় → 'The evidence shows' · বানানো সংখ্যা নয় · প্রতিপক্ষকে অপমান নয় · উপসংহারে অবস্থান বদলানো নয় · একটা ভাগে ৮ মিনিটের বেশি নয়", ""),
]),
("প্রমাণের ভান্ডার (যাচাই করা সংখ্যা, নভেম্বর ২০২৬)", "Evidence bank: use 1 number per point", "★★", [
 ("মূল্যস্ফীতি ও মজুরি", "8.27% (অক্টোবর ২০২৬; খাদ্য 6.40%, খাদ্যবহির্ভূত 9.89%) · শীর্ষ 11.66% (জুলাই ২০২৪) · মজুরি টানা ৫৭ মাস মূল্যস্ফীতির নিচে", "মূল্যস্ফীতি বা মুদ্রানীতির যুক্তিতে"),
 ("সুদ ও ঋণ", "নীতি সুদহার 9.5% (১০% থেকে কমানো, জুলাই ২০২৬) · বেসরকারি ঋণ প্রবৃদ্ধি 4.17% (রেকর্ড সর্বনিম্ন)", "বিনিয়োগ বা সুদহারের যুক্তিতে"),
 ("খেলাপি ঋণ", "32.17% = 5.97 লাখ কোটি টাকা (সেপ্টেম্বর ২০২৬) · একীভূত ৫ ব্যাংকের ঋণের প্রায় 86% খেলাপি", "ব্যাংক সংস্কার বা সুশাসনের যুক্তিতে"),
 ("প্রবৃদ্ধি", "FY26: 3.68% · FY27 পূর্বাভাস: IMF 3.2%, বিশ্বব্যাংক 3.4%, ADB 4.0% · লক্ষ্য 6.5%", "প্রবৃদ্ধি বনাম অন্য লক্ষ্যের যুক্তিতে"),
 ("বাহ্যিক খাত", "রেমিট্যান্স FY26: 35.59 বিলিয়ন ডলার (রেকর্ড) · রপ্তানির প্রায় 80% পোশাক · যুক্তরাষ্ট্রে 10% শুল্ক · গ্রস রিজার্ভ 34.38 বিলিয়ন ডলার", "রপ্তানি বহুমুখীকরণ বা রেমিট্যান্সের যুক্তিতে"),
 ("এলডিসি · জলবায়ু · সমাজ", "এলডিসি উত্তরণ ২৪ নভেম্বর ২০২৯ · জার্মানওয়াচ ২০২৬: ঝুঁকিতে ১৩তম · জুলাই ২০২৬ বন্যা: ৭ জেলা, 10.2 লাখ মানুষ · দারিদ্র্য 22.5% · প্রতি ৩ স্নাতকে ১ জন বেকার", "পরিবেশ, এলডিসি বা কর্মসংস্থানের যুক্তিতে"),
]),
]

VOCAB = [("assumption", "অনুমান (না বলা পূর্বধারণা)"), ("premise", "তথ্য/ভিত্তি"), ("conclusion", "সিদ্ধান্ত"), ("infer / inference", "সিদ্ধান্ত টানা"),
         ("undermine / weaken", "দুর্বল করা"), ("bolster / strengthen", "শক্ত করা"), ("flaw / fallacy", "যুক্তির ভুল"), ("immediately after", "ঠিক পরে"),
         ("valid / justified", "যুক্তিসংগত"), ("counter-argument", "বিপক্ষ যুক্তি"), ("on balance", "সব মিলিয়ে"), ("trade-off", "একটি পেতে অন্যটি ছাড়া")]
CHECK = ["পাজলে ছক + ধাপ + 'Check' — শুধু উত্তর নয়", "সমালোচনায় প্রতিটি ফাঁকের নাম ইংরেজিতে", "অনুমান এক বাক্যে, উল্টানোর পরীক্ষা দিয়ে যাচাই",
         "আর্গুমেন্টে প্রথম লাইনেই অবস্থান, শেষে একই অবস্থান", "প্রতিটি পয়েন্টে বাংলাদেশের ১টি সংখ্যা", "সময়: ৬ + ৩ + ৫ + ৮ মিনিট — ঘড়ি দেখে"]


def main():
    head = '<div class="r head"><span>নিয়ম</span><span>কী করবেন</span><span>বাস্তব উদাহরণ (ছোট)</span></div>'
    body = ""
    for name, en, st, rows in CH:
        body += f'<div class="ch"><h2>{e(name)}<small>{e(en)}</small><i>{st}</i></h2>{head}' + "".join(
            f'<div class="r"><b>{e(a)}</b><span class="f">{e(b)}</span><span>{"<span class=x>" + e(c) + "</span>" if c else ""}</span></div>' for a, b, c in rows) + "</div>"
    vocab = "".join(f"<div><span>{e(a)}</span> = {e(b)}</div>" for a, b in VOCAB)
    check = "".join(f"<li>{e(x)}</li>" for x in CHECK)
    doc = f"""<!doctype html><html lang="bn"><head><meta charset="utf-8"><title>Analytical 40 Sheet</title><style>{CSS.replace("__BN__", FONT_BN)}</style></head><body>
<div class="top"><div><div class="tag">SO Written · 27 Nov 2026 · Analytical Reasoning, Critical Thinking &amp; Argumentative Writing (40 marks) · exam-morning sheet</div><h1>অ্যানালিটিক্যাল ৪০ — সব নিয়ম + বাস্তব উদাহরণ</h1></div></div>
<div class="how"><b>পরীক্ষার হলে:</b> উত্তর <b>ইংরেজিতে</b>। ক্রম (a) পাজল → (c) অনুমান → (b) সমালোচনা → (d) আর্গুমেন্ট। শুরুতেই (d)-র জন্য ১ মিনিটে T-chart। পাজলে ধাপ ও যাচাই, সমালোচনায় ফাঁকের নাম, আর্গুমেন্টে স্পষ্ট অবস্থান ও সংখ্যা — এই তিনটিতেই নম্বর।</div>
{body}
<div class="grid2"><div class="box"><h3>শেষ মুহূর্তের চেকলিস্ট</h3><ol>{check}</ol></div>
<div class="box"><h3>প্রশ্নের ইংরেজি শব্দ</h3><div class="v">{vocab}</div></div></div>
</body></html>"""
    hp = OUT.replace(".pdf", ".html"); open(hp, "w", encoding="utf-8").write(doc)
    js = os.path.join(ROOT, "final_pdfs", ".mkan.js")
    open(js, "w").write(r"""const { chromium } = require("playwright");
(async () => { const [inp, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
 await p.goto("file://" + inp); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
  footerTemplate: '<div style="width:100%;text-align:center;font-family:Inter,Arial;font-size:7.5px;color:#64748b">Analytical 40 Sheet (Bangla) · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
 await b.close(); })().catch((e) => { console.error(e); process.exit(1); });""")
    try:
        subprocess.run(["node", js, hp, OUT], check=True, cwd=ROOT)
    finally:
        os.remove(js); os.remove(hp)
    print("PDF:", OUT)


if __name__ == "__main__":
    main()
