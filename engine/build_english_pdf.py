#!/usr/bin/env python3
"""
English Language Proficiency (20) — "Memorize & Answer" edition → final_pdfs/SO_English_Grammar_Memorize_Edition.pdf
Content = docs/19 (stress-tested) re-organised for memory: one card per syllabus item, trigger → answer tables,
Bangla memory hints, themed group verbs and idioms, self-test with key, last-night sheet.
Run: python3 engine/build_english_pdf.py
"""
import html, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from english_extras import EXTRA, TENSES, IRREG, PRON, MOCKS, PLAN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_HTML = os.path.join(ROOT, "final_pdfs", "SO_English_Grammar_Memorize_Edition.html")
OUT_PDF = os.path.join(ROOT, "final_pdfs", "SO_English_Grammar_Memorize_Edition.pdf")
FONT_BN = os.path.join(ROOT, "answer_book", "fonts", "TiroBangla-400.ttf")
e = html.escape


def b(s):  # **bold** → <b>, keep the rest escaped
    out, parts = [], s.split("**")
    for i, p in enumerate(parts):
        out.append(f"<b>{e(p)}</b>" if i % 2 else e(p))
    import re
    return re.sub(r"\*([^*<>]+)\*", r"<i>\1</i>", "".join(out))


def table(head, rows, cls=""):
    th = "".join(f"<th>{b(h)}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{b(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def hint(bn):
    return f'<div class="hint"><span>মনে রাখুন</span>{b(bn)}</div>'


def trap(items):
    return '<div class="trap"><span>ফাঁদ</span><ul>' + "".join(f"<li>{b(x)}</li>" for x in items) + "</ul></div>"


def qa(items):
    return '<div class="qa">' + "".join(f'<div class="q">{b(q)}</div><div class="a">{b(a)}</div>' for q, a in items) + "</div>"


def learn(bn):
    return f'<div class="learn"><span>শূন্য থেকে বুঝুন</span>{b(bn)}</div>'


def steps(items):
    return '<div class="steps"><span>পরীক্ষায় ধাপে ধাপে</span><ol>' + "".join(f"<li>{b(x)}</li>" for x in items) + "</ol></div>"


def worked(items):
    return '<h3>Worked examples (exactly how to write it)</h3>' + "".join(
        f'<div class="wk"><div class="q">{b(q)}</div><div class="a">{b(a)}</div><div class="why"><span>কেন</span>{b(w)}</div></div>' for q, a, w in items)


def section(num, title, sub, body, stars=""):
    x = EXTRA.get(num, {})
    if x:
        body = (learn(x["learn"]) if "learn" in x else "") + (steps(x["steps"]) if "steps" in x else "") + body + (worked(x["worked"]) if "worked" in x else "")
    return f'<section class="topic"><header><span class="no">{num}</span><div><h2>{e(title)} <i>{stars}</i></h2><p>{b(sub)}</p></div></header>{body}</section>'


# ───────────────────────── content ─────────────────────────
S = []

S.append(section("A", "How the question comes and how to write a 4/4 answer",
    "Q8 · 20 marks · **5 items × 4 marks** · 12–14 minutes. The 5 June 2026 paper asked: group verb, sentence type, idiom, voice, idiom.",
    table(["Item", "Write this for full marks", "Model"], [
        ["Group verb", "rewritten sentence + meaning in brackets", "Over-exercise **told upon** his health. (tell upon = affect adversely)"],
        ["Sentence type", "type + the clauses that prove it", "**Compound-complex**: 2 main clauses (The sun set / the stars appeared) + 1 sub clause (while we sat by the fire)."],
        ["Idiom", "meaning in one line + your own example", "**Hit the nail on the head** = say exactly the right thing. *The governor hit the nail on the head about bad loans.*"],
        ["Voice / narration / transformation", "full new sentence + the rule in 3–4 words", "**The results will be announced tomorrow.** (will + be + V3)"],
        ["Correction / right form / SVA", "whole sentence, changed word in bold + rule", "Each of the officers **has** a laptop. (each of → singular)"],
        ["Finite / clause", "identify + type + function", "'that he is honest' = **noun clause**, object of 'know'."],
    ], "wide") + hint("উত্তরের তিন অংশ: **উত্তর → নিয়ম → উদাহরণ**। শুধু এক শব্দ লিখলে ৪-এর মধ্যে ১–২ নম্বর কাটা যায়।")))

S.append(section("0", "Basics from zero (read this first if English grammar is new)", "Everything else in this booklet uses these four tables.",
    learn("ইংরেজি বাক্যের মূল ছক: **Subject (কে/কী) + Verb (কী করে/হয়) + Object (কাকে/কী)** — *The bank (S) gave (V) him (O) a loan (O).* বাংলায় verb শেষে বসে (আমি ভাত খাই), ইংরেজিতে **subject-এর ঠিক পরে** (I eat rice)। Verb-এর রূপ বদলায় **সময় (tense)** আর **subject (একবচন/বহুবচন)** অনুযায়ী — এই দুটি বুঝলেই প্রশ্ন ৮-এর অর্ধেক সহজ।")
    + '<h3>The 12 tenses (with the Bangla ending to recognise them)</h3>'
    + table(["Tense", "Formula", "Example", "বাংলা"], TENSES, "tense")
    + hint("**be-এর রূপ:** I am · he/she/it is · we/you/they are · was (একবচন) / were (বহুবচন) · been (have/has/had-এর পরে) · be (will/can/must-এর পরে)। **have-এর রূপ:** he/she/it **has**, বাকিরা **have**, অতীতে সবার **had**।")
    + '<h3 style="break-before:page">Irregular verbs: V1 – V2 – V3 (these appear in voice, right form and narration)</h3>'
    + '<div class="irreg">' + "".join(f"<div><b>{e(a)}</b> {e(v2)} · <i>{e(v3)}</i></div>" for a, v2, v3 in IRREG) + "</div>"
    + hint("নিয়মিত verb-এ শুধু **-ed**: work – worked – worked। বাকিগুলো উপরের তালিকা থেকে। **V3 মুখস্থই passive আর perfect tense-এর চাবি।**")
    + '<h3>Pronouns (for voice and narration)</h3>'
    + table(["Subject", "Object (after by / verb)", "Possessive", "In narration it becomes"], PRON)))

S.append(section("1", "Sentence structure", "Count the **finite verbs** → each one = one clause → decide main or sub.",
    table(["Type", "Formula", "Example"], [
        ["Simple", "1 main clause", "Being tired, he **went** to bed early."],
        ["Compound", "2+ main clauses joined by **and, but, or, so, yet, for, nor**", "He **came**, he **saw** and he **conquered**."],
        ["Complex", "1 main + 1 or more sub clauses (**because, although, when, if, who, that**)", "Although he **was** ill, he **attended** the meeting."],
        ["Compound-complex", "2+ main + 1 or more sub", "The sun **set**, and the stars **appeared**, while we **sat** by the fire."],
    ]) + hint("**১ main = Simple · ২ main = Compound · main + sub = Complex · ২ main + sub = Compound-complex**। Sub clause চেনার উপায়: শুরুতে because / although / when / if / who / that।")
    + table(["Pattern", "Example"], [["SV", "Birds fly."], ["SVO", "She signed the cheque."], ["SVC", "He became a manager."], ["SVOO", "The bank gave him a loan."], ["SVOC", "They elected him chairman."]])
    + table(["Inversion (always tested)", "Correct form"], [
        ["No sooner … ", "No sooner **had he arrived than** the meeting started."],
        ["Hardly / Scarcely …", "Hardly **had I reached when** the train left."],
        ["Not only … (at the start)", "Not only **did he** apologise but he also paid."],
        ["Never / Seldom / Only then", "Never **have I** seen … · Seldom **does** he … · Only then **did** she realise …"],
    ]) + trap(["**No sooner → than**, but **Hardly / Scarcely → when** (never 'than').", "A participle phrase (Being tired, …) is **not** a clause — the sentence stays **simple**."])))

S.append(section("2", "Subject-verb agreement", "Find the **real subject**, ignore the words in between.",
    table(["Trigger", "Verb", "Example"], [
        ["each / every / either / neither / one of / many a", "singular", "One of the banks **has** been merged. Many a man **has** tried."],
        ["**a number of**", "plural", "A number of banks **are** in crisis."],
        ["**the number of**", "singular", "The number of defaulters **is** rising."],
        ["neither … nor / either … or / not only … but also", "agrees with the **nearer** subject", "Neither the manager nor the clerks **were** present."],
        ["as well as / along with / with / together with / including", "agrees with the **first** subject", "The chairman, along with the directors, **was** present."],
        ["A and B (two people / things)", "plural", "The secretary and **the** treasurer **are** absent."],
        ["A and B = one person / one idea", "singular", "The secretary and treasurer **is** absent. Bread and butter **is** my breakfast."],
        ["news, economics, physics, measles", "singular", "Economics **is** my favourite subject."],
        ["people, police, cattle, poultry", "plural", "The police **have** arrested him."],
        ["information, advice, furniture, luggage, equipment", "singular, no -s", "The information **is** correct."],
        ["amount / distance / time as a whole", "singular", "Ten thousand taka **is** a big sum."],
        ["the + adjective (people)", "plural", "The rich **are** not always happy."],
        ["more than one + noun", "singular", "More than one officer **was** absent."],
        ["a pair of / one and a half", "singular", "The pair of scissors **is** dull. One and a half hours **is** long."],
        ["there + be", "agrees with the noun after it", "There **are** many reasons."],
        ["one of those who", "plural (who → those)", "He is one of those officers who **work** hard."],
    ]) + hint("**Each-Every-Either-Neither-One of = একবচন।** **Neither…nor = কাছেরটা।** **with / along with / as well as = প্রথমটা।** **A number = বহু, The number = এক।**")
    + trap(["'The quality of the products **is** poor' — the subject is *quality*, not *products*.", "Two *the*s = two people (plural). One *the* = one person with two posts (singular)."])))

S.append(section("3", "Right form of verbs", "Look for the **clue word** → it decides the form.",
    table(["Clue", "Form", "Example"], [
        ["habit · universal truth", "present simple", "The earth **moves** round the sun."],
        ["since / for (up to now)", "present perfect (continuous)", "I **have been working** here since 2020."],
        ["yesterday · ago · last · in 2020", "past simple", "He **went** to Dhaka yesterday."],
        ["two past actions", "earlier = past perfect", "The patient **had died** before the doctor **came**."],
        ["If + present", "will + base", "If it **rains**, we **will** stay."],
        ["If + past (were)", "would + base", "If I **were** rich, I **would** help."],
        ["If + had V3", "would have V3", "If he **had studied**, he **would have passed**."],
        ["wish / as if / as though (present)", "past · were", "He talks as if he **knew** everything."],
        ["wish (past)", "had V3", "I wish I **had seen** it."],
        ["It is (high) time", "past simple", "It is high time we **took** action."],
        ["lest", "should + base", "Walk fast lest you **should miss** the train."],
        ["let / make / see / hear / bid", "base (no to)", "He made me **do** it again."],
        ["had better / would rather", "base", "You **had better go** now."],
        ["avoid, enjoy, finish, mind, deny, admit, postpone, can't help, worth, no use", "V-ing", "He avoided **meeting** me. It's no use **crying**."],
        ["look forward to · be used to · object to · with a view to", "to + V-ing", "I look forward to **hearing** from you."],
        ["want, decide, agree, hope, plan, refuse, afford, manage", "to + base", "She decided **to join** a bank."],
        ["suggest / insist / demand / recommend + that", "(should) + base", "He insisted that the branch **be** closed."],
        ["when / until / as soon as (future meaning)", "present", "I will call you when he **arrives**."],
        ["just · already · yet · ever · never · recently", "present perfect", "He **has just left**."],
        ["know, believe, own, seem, understand", "no -ing form", "I **know** him (not am knowing)."],
    ]) + hint("**শর্তের ১-২-৩:** present → will · past → would · had V3 → would have V3। **High time / wish / as if → past।** **to-এর পরে ing শুধু এই চারটায়:** look forward to · be used to · object to · with a view to।")
    + trap(["**used to** + base = past habit (He used to smoke). **be used to** + V-ing = accustomed (He is used to working late).", "Passive of 'made me do' → I was made **to do** it (the *to* comes back)."])))

S.append(section("4", "Voice (active ↔ passive)", "**Passive = be (in the active verb's tense) + V3**. Object of the active becomes the subject.",
    table(["Tense", "Active", "Passive"], [
        ["Present simple", "They **announce** the results.", "The results **are announced**."],
        ["Present continuous", "They **are announcing** …", "… **are being announced**."],
        ["Present perfect", "They **have announced** …", "… **have been announced**."],
        ["Past simple", "They **announced** …", "… **were announced**."],
        ["Past continuous", "They **were announcing** …", "… **were being announced**."],
        ["Past perfect", "They **had announced** …", "… **had been announced**."],
        ["Future / modal", "They **will announce** … tomorrow.", "… **will be announced** tomorrow."],
        ["Modal", "You **must repay** the loan.", "The loan **must be repaid** (by you)."],
    ]) + table(["Special pattern", "Passive"], [
        ["Did he write the letter?", "**Was** the letter **written** by him?"],
        ["Who wrote this?", "**By whom was** this written?"],
        ["Open the account.", "**Let** the account **be opened**."],
        ["Please help me.", "You **are requested to** help me."],
        ["They laughed at him.", "He **was laughed at**."],
        ["The bank gave him a loan.", "He **was given** a loan by the bank."],
        ["People say that he is honest.", "**It is said that** he is honest. / He **is said to be** honest."],
        ["I know him. · It pleases me.", "He is known **to** me. · I am pleased **with** it."],
    ]) + hint("**be-এর রূপ মুখস্থ:** am/is/are · was/were · being · been · be (modal-এর পরে)। ক্রিয়া সবসময় **V3**। Imperative হলে **Let … be V3**।")
    + trap(["Intransitive verbs (die, go, sleep) have **no** passive.", "Fixed prepositions: known **to**, surprised **at**, pleased **with**, interested **in**, filled **with**, married **to**."])))

S.append(section("5", "Narration (direct ↔ indirect speech)", "**Reporting verb past → move every tense one step back** + change pronouns and time words.",
    table(["Direct", "Indirect", "", "Direct", "Indirect"], [
        ["am / is", "was", "", "now", "then"],
        ["are", "were", "", "today", "that day"],
        ["do / does", "did", "", "tonight", "that night"],
        ["did / have / has", "had / had done", "", "yesterday", "the previous day"],
        ["will / shall", "would / should", "", "tomorrow", "the next day"],
        ["can / may", "could / might", "", "ago", "before"],
        ["must", "had to", "", "this / these / here", "that / those / there"],
    ], "half") + table(["Sentence type", "Reporting verb + link", "Example"], [
        ["Assertive", "told / said + **that**", "He said to me, \"I am busy.\" → He **told me that he was** busy."],
        ["Yes/no question", "asked + **if / whether**", "\"Have you submitted the form?\" → He **asked me if I had submitted** the form."],
        ["Wh-question", "asked + wh-word (no 'that')", "\"Where do you live?\" → He asked me **where I lived**."],
        ["Command / request", "ordered / requested + **to**", "\"Please sign here.\" → He **requested me to sign** there."],
        ["Negative command", "told / advised + **not to**", "\"Don't disclose the PIN.\" → He **advised me not to disclose** the PIN."],
        ["Let us", "proposed / suggested + that + **should**", "\"Let us go home.\" → She **proposed that they should go** home."],
        ["Wish / prayer", "wished / prayed + that + **might**", "\"May you prosper!\" → He **prayed that I might** prosper."],
        ["Exclamation", "exclaimed with joy / sorrow + that", "\"What a fine day!\" → He **exclaimed with joy that it was a very fine day**."],
    ]) + hint("**প্রশ্নে 'that' বসে না।** Yes/no প্রশ্নে **if/whether**, Wh-প্রশ্নে সেই wh-শব্দ, তারপর **subject + verb** (প্রশ্নের ক্রম নয়)।")
    + trap(["Universal truth: **no** tense change — The teacher said that the earth **moves** round the sun.", "Reporting verb in the present (He says …) → **no** tense change."])))

S.append(section("6", "Transformation of sentences", "Meaning stays the same, only the structure changes.",
    table(["Simple", "Complex", "Compound"], [
        ["Being ill, he could not attend.", "**As** he was ill, he could not attend.", "He was ill, **and so** he could not attend."],
        ["In spite of being poor, he is honest.", "**Though** he is poor, he is honest.", "He is poor, **but** he is honest."],
        ["Without working hard, you will fail.", "**If you do not** work hard, you will fail.", "Work hard, **or** you will fail."],
        ["He is too weak to walk.", "He is **so** weak **that** he **cannot** walk.", "He is very weak, **and so** he cannot walk."],
        ["On seeing the police, the thief ran away.", "**As soon as** the thief saw the police, he ran away.", "The thief saw the police **and** ran away."],
    ]) + table(["Change", "From → To"], [
        ["Affirmative → Negative", "Only he can solve it → **None but** he can solve it. · Only water → **Nothing but** water · He must obey → He **cannot but** obey · He is always punctual → He is **never** late"],
        ["As soon as → No sooner", "As soon as he came, … → **No sooner had he come than** …"],
        ["Interrogative → Assertive", "Who does not love his country? → **Everybody loves** his country. · What is the use of crying? → **There is no use** crying."],
        ["Exclamatory → Assertive", "What a beautiful bird it is! → It is a **very** beautiful bird. · Alas! He is dead. → **It is a matter of sorrow that** he is dead."],
        ["Degree (superlative)", "Dhaka is the largest city → Dhaka is larger **than any other** city → **No other** city is **as large as** Dhaka."],
        ["Degree ('one of the')", "one of the greatest → greater than **most other** … → **Very few** … are as great as …"],
    ]) + hint("**too … to = so … that … cannot।** **Only (ব্যক্তি) → None but, Only (বস্তু) → Nothing but।** Superlative থেকে comparative-এ **than any other**, positive-এ **No other … as … as**।")))

S.append(section("7", "Finite and non-finite verbs", "**Finite** changes with the subject and tense; **non-finite** never does.",
    table(["Non-finite", "Form", "Example"], [
        ["To-infinitive", "to + base", "He wants **to join** a bank."],
        ["Bare infinitive", "base (after let, make, see)", "Let him **go**."],
        ["Gerund", "V-ing used as a **noun**", "**Saving** money is a good habit. He is fond of **reading**."],
        ["Present participle", "V-ing used as an **adjective**", "a **running** train · **Walking** along the road, I met him."],
        ["Past participle", "V3 used as an adjective", "a **broken** chair · the **approved** loan"],
        ["Perfect participle", "having + V3", "**Having finished** the audit, he left."],
    ]) + hint("**Gerund না participle?** V-ing-এর জায়গায় 'it' বসিয়ে দেখুন: বাক্য ঠিক থাকলে **gerund** (noun), নইলে **participle** (adjective)।")
    + qa([["Identify the finite and non-finite verbs: *Having finished the audit, he wanted to submit the report.*", "Finite: **wanted**. Non-finite: **Having finished** (perfect participle), **to submit** (to-infinitive, object of 'wanted')."]])
    + trap(["Dangling participle is an **error**: 'Walking down the street, a bus hit him' → *While he was walking down the street, a bus hit him.*"])))

S.append(section("8", "Clause and phrase", "**Phrase** = no subject + finite verb. **Clause** = has subject + finite verb.",
    table(["Clause", "Ask this", "Example"], [
        ["Noun clause", "**What?** (subject / object / complement / apposition)", "**What he said** is true. · I know **that he is honest**. · The news **that he resigned** is true."],
        ["Adjective clause", "**Which one?** (who, which, that, whose, where)", "The officer **who approved the loan** was suspended."],
        ["Adverb clause", "**When? Why? How? On what condition?**", "He was promoted **because he worked hard**. · **Although he was ill**, he attended."],
    ]) + hint("**প্রশ্ন-কৌশল:** কী? → noun clause · কোনটা/কে? → adjective clause · কখন/কেন/কীভাবে/কোন শর্তে? → adverb clause। ফাংশনও লিখুন: subject, object বা apposition।")
    + table(["Phrase", "Example"], [["Noun phrase", "**a very honest officer**"], ["Adjective phrase", "a man **of great wealth**"], ["Adverb phrase", "He spoke **in a loud voice**."], ["Prepositional phrase", "**in the morning**"]])
    + trap(["Non-defining clause (with commas) never uses **that**: Sonali Bank, **which** is state-owned, …"])))

GV = [
    ("put", "off = postpone · out = extinguish · up with = tolerate · on = wear · down = suppress / write · forward = propose · aside = save"),
    ("look", "after = take care of · into = investigate · for = search · up = consult (dictionary) · up to = respect · down upon = despise · over = examine · forward to + ing = expect with pleasure"),
    ("give", "up = quit · in = surrender · away = distribute / reveal · out = distribute / be exhausted · off = emit"),
    ("take", "after = resemble · off = remove / leave the ground · up = start (hobby) · over = take control · in = deceive · to = become addicted to · on = employ"),
    ("come", "across = meet by chance · about = happen · off = take place · round = recover · out = be published · of = be born of (family) · by = get"),
    ("bring", "up = rear · about = cause · out = publish · down = reduce · in = introduce"),
    ("call", "off = cancel · on = visit · for = demand / require · in = summon · up = phone"),
    ("break", "down = collapse / stop working · out = start suddenly (war, fire) · in = interrupt · off = stop suddenly · up = close"),
    ("carry", "out = execute · on = continue · off = win (prizes)"),
    ("set", "up = establish · out / off = start (a journey) · in = begin (winter) · aside = reserve · about = begin (work)"),
    ("turn", "down = reject · up = arrive · out = prove to be / expel · in = submit · into = change into"),
    ("run", "into = meet by chance · out of = exhaust (a supply) · over = knock down · after = chase · short of = have too little"),
    ("get", "over = recover / overcome · through = pass · along with = live in harmony · by = manage · at = reach (the truth)"),
    ("make", "out = understand · up = invent / compensate · up for = compensate · off = run away"),
    ("go", "through = examine / suffer · over = review · off = explode / go bad · back on = withdraw (a promise) · in for = take part in"),
    ("keep", "up = maintain · up with = keep pace with · on = continue · back = conceal"),
    ("hold", "up = delay / rob · on = wait · out = endure"),
    ("stand", "by = support · for = represent · out = be prominent · up for = defend"),
    ("fall", "out = quarrel · through = fail · back on = depend on (last resort) · short of = be less than"),
    ("others", "**tell upon** = affect adversely (June 2026) · do away with = abolish · cut down = reduce · pass away = die · see off = say goodbye · bear with = tolerate · die out = become extinct"),
]
REV = [
    ("affect adversely", "tell upon"), ("postpone", "put off"), ("cancel", "call off"), ("investigate", "look into"), ("tolerate", "put up with"),
    ("extinguish", "put out"), ("quit", "give up"), ("establish", "set up"), ("resemble", "take after"), ("rear (a child)", "bring up"),
    ("explode", "blow up"), ("disappoint", "let down"), ("find by chance", "come across"), ("reject", "turn down"), ("visit", "call on"),
    ("recover", "get over"), ("continue", "carry on"), ("execute", "carry out"), ("compensate", "make up for"), ("understand", "make out"),
    ("despise", "look down upon"), ("respect", "look up to"), ("search", "look for"), ("examine", "go through"), ("explain", "account for"),
    ("arrive", "turn up"), ("cause", "bring about"), ("publish", "bring out"), ("reduce", "cut down"), ("surrender", "give in"),
    ("abolish", "do away with"), ("omit", "leave out"), ("demolish", "pull down"), ("represent", "stand for"), ("support", "stand by"),
    ("delay", "hold up"), ("exhaust (a supply)", "run out of"), ("meet by chance", "run into"), ("happen", "come about"), ("die", "pass away"),
    ("propose", "put forward"), ("repay", "pay back"), ("quarrel", "fall out"), ("fail (a plan)", "fall through"), ("discuss", "talk over"),
    ("wait", "hold on"), ("collapse", "break down"), ("start (war / fire)", "break out"), ("take care of", "look after"), ("save (money)", "put aside"),
]
gv_html = '<div class="families">' + "".join(f'<div class="fam"><b>{e(h)}</b> {b(t)}</div>' for h, t in GV) + "</div>"
rev_rows = [[f"{REV[i][0]}", f"**{REV[i][1]}**", f"{REV[i + 25][0]}", f"**{REV[i + 25][1]}**"] for i in range(25)]
S.append(section("9", "Group verbs", "The paper says *\"substitute the single verb with a group verb\"* — so learn the right-hand column of the first table. ★ tell upon was asked in June 2026.",
    table(["Single verb", "Group verb", "Single verb", "Group verb"], rev_rows, "rev")
    + '<h3 style="break-before:page">Families by head verb (for "use in a sentence")</h3>' + gv_html
    + hint("শেখার নিয়ম: দিনে **একটি family** — put, look, give, take … প্রতিটি particle-এর অর্থ মুখে বলুন, তারপর বাঁ কলাম ঢেকে ডান কলাম বলুন।")
    + trap(["**die of** a disease / hunger · **die from** a wound · **die by** accident.", "**made of** (material visible: gold ring) · **made from** (material changed: paper from wood).", "**look forward to / be used to / object to** + V-ing."])))

ID = [
    ("Money & banking", [
        ("in the red", "in debt / making a loss", "লোকসানে"), ("in the black", "in profit", "লাভে"), ("foot the bill", "pay for something", "খরচ বহন করা"),
        ("make both ends meet", "live within one's income", "আয়ে কোনোমতে চলা"), ("from hand to mouth", "with barely enough to live", "দিন আনে দিন খায়"),
        ("on a shoestring", "with very little money", "খুব কম টাকায়"), ("tighten one's belt", "spend less", "খরচ কমানো"),
        ("a white elephant", "a costly but useless possession", "শ্বেতহস্তী"), ("a cash cow", "a steady source of profit", "নিয়মিত লাভের উৎস"),
        ("make a killing", "make a big profit quickly", "দ্রুত বিপুল লাভ"), ("bail out", "rescue financially", "আর্থিকভাবে উদ্ধার"),
        ("save for a rainy day", "save for hard times", "দুর্দিনের জন্য সঞ্চয়"), ("cost an arm and a leg", "be very expensive", "অনেক দামি"),
        ("a drop in the ocean", "a tiny amount compared with the need", "সিন্ধুতে বিন্দু"), ("the lion's share", "the largest part", "সিংহভাগ"),
        ("cut one's coat according to one's cloth", "live within one's means", "আয় বুঝে ব্যয়"),
    ]),
    ("Work & effort", [
        ("burn the midnight oil", "work or study late at night ★", "রাত জেগে পড়া"), ("burn the candle at both ends", "overwork until exhausted", "অতিরিক্ত খাটুনি"),
        ("leave no stone unturned", "try every possible means", "সব রকম চেষ্টা"), ("move heaven and earth", "make every possible effort", "প্রাণপণ চেষ্টা"),
        ("a Herculean task", "a very difficult task", "অতি কঠিন কাজ"), ("a hard nut to crack", "a difficult problem or person", "কঠিন সমস্যা"),
        ("cut corners", "do something cheaply or carelessly", "ফাঁকি দেওয়া"), ("by hook or by crook", "by any means", "যেভাবেই হোক"),
        ("bite the bullet", "face a hard situation bravely", "কষ্ট সহ্য করে মেনে নেওয়া"), ("red tape", "bureaucratic delay", "লাল ফিতার দৌরাত্ম্য"),
        ("back to square one", "back to the start", "আবার শুরুতে"), ("a wild-goose chase", "a hopeless search", "বৃথা খোঁজ"),
    ]),
    ("Speaking & truth", [
        ("hit the nail on the head", "say exactly the right thing ★", "ঠিক কথাটি বলা"), ("call a spade a spade", "speak frankly", "স্পষ্ট কথা বলা"),
        ("beat about the bush", "avoid the main point", "ঘুরিয়ে বলা"), ("spill the beans", "reveal a secret", "গোপন কথা ফাঁস"),
        ("let the cat out of the bag", "reveal a secret by mistake", "অসাবধানে ফাঁস"), ("break the ice", "start talking in an awkward situation", "জড়তা ভাঙা"),
        ("in black and white", "in writing", "লিখিতভাবে"), ("a cock-and-bull story", "an absurd, unbelievable story", "আষাঢ়ে গল্প"),
        ("a white lie", "a harmless lie", "নিরীহ মিথ্যা"), ("pull one's leg", "tease", "ঠাট্টা করা"),
        ("take with a pinch of salt", "doubt slightly", "পুরো বিশ্বাস না করা"), ("Greek to me", "impossible to understand", "দুর্বোধ্য"),
    ]),
    ("Time, speed & place", [
        ("once in a blue moon", "very rarely", "কালেভদ্রে"), ("at the eleventh hour", "at the last moment", "শেষ মুহূর্তে"),
        ("by fits and starts", "irregularly", "অনিয়মিতভাবে"), ("by leaps and bounds", "very rapidly", "দ্রুতগতিতে"),
        ("in the long run", "eventually", "শেষ পর্যন্ত"), ("few and far between", "rare", "বিরল"),
        ("at a stone's throw", "very near", "খুব কাছে"), ("in a nutshell", "in brief", "সংক্ষেপে"),
    ]),
    ("Trouble & danger", [
        ("in hot water", "in trouble", "বিপদে"), ("on the horns of a dilemma", "facing two bad choices", "উভয় সংকটে"),
        ("hang by a thread", "be in great danger", "সুতোয় ঝোলা"), ("at one's wits' end", "completely puzzled", "দিশেহারা"),
        ("at sixes and sevens", "in disorder", "বিশৃঙ্খল"), ("a bolt from the blue", "a sudden shock", "বিনা মেঘে বজ্রপাত"),
        ("face the music", "accept the consequences", "পরিণতি মেনে নেওয়া"), ("go to the dogs", "be ruined", "উচ্ছন্নে যাওয়া"),
        ("the tip of the iceberg", "a small visible part of a big problem", "সমস্যার সামান্য অংশ"), ("nip in the bud", "stop something at the start", "অঙ্কুরে বিনাশ"),
    ]),
    ("People & relations", [
        ("apple of one's eye", "a dearly loved person", "নয়নের মণি"), ("apple of discord", "the cause of a quarrel", "বিবাদের কারণ"),
        ("at daggers drawn", "bitterly hostile", "সাপে-নেউলে"), ("hand in glove", "in close (often bad) partnership", "গলায় গলায় ভাব"),
        ("see eye to eye", "agree fully", "একমত হওয়া"), ("give the cold shoulder", "ignore deliberately", "এড়িয়ে চলা"),
        ("a snake in the grass", "a hidden enemy", "দুধ-কলা দিয়ে কালসাপ"), ("a wet blanket", "a person who spoils fun", "আনন্দ নষ্টকারী"),
        ("a fish out of water", "someone in unfamiliar surroundings", "বেমানান অবস্থায়"), ("a dark horse", "an unexpected winner", "অপ্রত্যাশিত বিজয়ী"),
        ("a man of letters", "a scholar or writer", "বিদ্বান ব্যক্তি"), ("play second fiddle", "take a lesser role", "অধীনস্থ ভূমিকা"),
        ("through thick and thin", "in all circumstances", "সুখে-দুঃখে"), ("sit on the fence", "stay neutral", "নিরপেক্ষ থাকা"),
    ]),
    ("Success, failure & the rest", [
        ("a feather in one's cap", "an achievement to be proud of", "গৌরবের বিষয়"), ("a red-letter day", "a memorable day", "স্মরণীয় দিন"),
        ("steal the show", "attract the most attention", "সবার নজর কাড়া"), ("win hands down", "win easily", "অনায়াসে জেতা"),
        ("a blessing in disguise", "something bad that turns out good", "শাপে বর"), ("Achilles' heel", "a weak point", "দুর্বল জায়গা"),
        ("cry over spilt milk", "regret what cannot be undone", "অতীত নিয়ে আফসোস"), ("kill two birds with one stone", "achieve two aims with one action", "এক ঢিলে দুই পাখি"),
        ("null and void", "invalid", "বাতিল"), ("pros and cons", "advantages and disadvantages", "ভালো-মন্দ দিক"),
        ("out of the question", "impossible", "অসম্ভব"), ("turn a deaf ear", "ignore", "কানে না তোলা"),
        ("smell a rat", "suspect something wrong", "সন্দেহ করা"), ("take to one's heels", "run away", "চম্পট দেওয়া"),
        ("put the cart before the horse", "do things in the wrong order", "উল্টো কাজ"), ("an axe to grind", "a selfish motive", "স্বার্থ হাসিলের মতলব"),
    ]),
]
idiom_html = ""
n_id = 0
for theme, items in ID:
    n_id += len(items)
    idiom_html += f'<h3>{e(theme)} <small>({len(items)})</small></h3><div class="idioms">' + "".join(
        f'<div class="id"><b>{e(i)}</b><span>{b(m)}</span><em>{e(bn)}</em></div>' for i, m, bn in items) + "</div>"
S.append(section("10", f"Idioms ({n_id}, grouped by theme)", "Write: **idiom = meaning** + **one sentence of your own**. ★ = asked on 5 June 2026.",
    idiom_html + hint("থিম ধরে মনে রাখলে দ্রুত মনে আসে। প্রতিটির জন্য **ব্যাংক বা অর্থনীতির** একটা বাক্য বানিয়ে রাখুন, যেমন: *The new airport became **a white elephant**.*")))

PRACTICE = [
    ("Substitute a group verb: The government has **abolished** the old tax.", "The government has **done away with** the old tax. (do away with = abolish)"),
    ("Substitute a group verb: Inflation **affected** the poor **adversely**.", "Inflation **told upon** the poor."),
    ("Substitute a group verb: The meeting was **postponed**.", "The meeting was **put off**."),
    ("Sentence type: Although the bank was profitable, it closed two branches because costs rose.", "**Complex**: 1 main (it closed two branches) + 2 adverb clauses (concession, reason)."),
    ("Sentence type: He worked hard, but he failed because he was ill.", "**Compound-complex**: 2 main clauses + 1 adverb clause (because …)."),
    ("Correct: Neither the chairman nor the directors was present.", "Neither the chairman nor the directors **were** present. (nearer subject)"),
    ("Correct: The number of defaulters are rising.", "The number of defaulters **is** rising. (the number → singular)"),
    ("Correct: Each of the students have a laptop.", "Each of the students **has** a laptop."),
    ("Right form: If he (study) harder, he would have passed.", "If he **had studied** harder … (3rd conditional)"),
    ("Right form: It is high time we (reform) the banking sector.", "… we **reformed** … (high time + past)"),
    ("Right form: I look forward to (hear) from you.", "… to **hearing** … (look forward to + ing)"),
    ("Right form: Walk fast lest you (miss) the train.", "… lest you **should miss** …"),
    ("Voice: Who signed this cheque?", "**By whom was this cheque signed?**"),
    ("Voice: The bank gave him a loan.", "**He was given a loan by the bank.** / A loan was given to him by the bank."),
    ("Voice: Open the account.", "**Let the account be opened.**"),
    ("Voice: They will announce the results tomorrow.", "**The results will be announced (by them) tomorrow.**"),
    ("Narration: He said to me, \"Don't disclose the PIN.\"", "He **advised me not to disclose** the PIN."),
    ("Narration: She said, \"Let us open a savings account.\"", "She **proposed that they should open** a savings account."),
    ("Narration: He said to me, \"Where do you work?\"", "He **asked me where I worked**."),
    ("Narration: The teacher said, \"Honesty is the best policy.\"", "The teacher said that honesty **is** the best policy. (universal truth)"),
    ("Make it complex: In spite of his poverty, he is honest.", "**Though he is poor, he is honest.**"),
    ("Make it negative: Only the governor can approve this.", "**None but** the governor can approve this."),
    ("Make it simple: He is so weak that he cannot walk.", "He is **too weak to walk**."),
    ("Make it comparative: Dhaka is the largest city in Bangladesh.", "Dhaka is larger **than any other** city in Bangladesh."),
    ("Make it assertive: What a beautiful bird it is!", "It is a **very** beautiful bird."),
    ("Finite / non-finite: He wants to open an account.", "Finite: **wants** · Non-finite: **to open** (to-infinitive, object)."),
    ("Gerund or participle: Saving money is a good habit.", "**Saving** = gerund (subject of 'is')."),
    ("Clause: The news **that the bank has collapsed** shocked everyone.", "**Noun clause**, in apposition to 'the news'."),
    ("Clause: The officer **who approved the loan** was suspended.", "**Adjective clause**, qualifies 'officer'."),
    ("Idiom: a blessing in disguise", "Something that seems bad but turns out good. *Losing that job was a blessing in disguise.*"),
]
pq = '<ol class="practice">' + "".join(f"<li>{b(q)}</li>" for q, _ in PRACTICE) + "</ol>"
pk = '<ol class="key">' + "".join(f"<li>{b(a)}</li>" for _, a in PRACTICE) + "</ol>"
mk = "".join(f'<h3>{e(t)} <small>(20 marks · 12 minutes)</small></h3><ol class="mock">' + "".join(f'<li><div class="q">{b(q)}</div><div class="a">{b(a)}</div></li>' for q, a in items) + "</ol>" for t, items in MOCKS)
S.append(section("M", "Three full Question 8 papers with 4/4 model answers", "Cover the green answer, write yours on paper, then compare: answer + rule + example?", mk))
S.append(section("P", "8-step study plan for this booklet (about 6½ hours)", "Do the steps in order; tick each one.",
    table(["ধাপ", "পড়ুন", "সময়", "কীভাবে"], PLAN, "plan")
    + hint("পরীক্ষার হলে **প্রশ্ন ৮-কে ১২–১৪ মিনিট দিন**, এর বেশি নয়। ৫টির মধ্যে যেটা সবচেয়ে সহজ, সেটা আগে।")))
S.append(section("T", f"Self-test ({len(PRACTICE)} items in the exam style)", "Answer on paper in 15 minutes, then check with the key on the next page. Every wrong item → reread its card.", pq))
S.append(section("K", "Answer key", "1 mark off for any missing rule or example.", pk))

LAST = [
    ("Answer", "answer → rule → example · changed word in **bold**"),
    ("Structure", "1 main = simple · 2 main = compound · main + sub = complex · 2 main + sub = compound-complex"),
    ("SVA", "Each/Every/One of = sg · Neither…nor = nearer · with/as well as = first · a number = pl · the number = sg"),
    ("Right form", "If 1-2-3: will / would / would have V3 · high time / wish / as if → past · lest → should · let/make → base · look forward to → ing"),
    ("Voice", "be (same tense) + V3 · imperative → Let … be V3 · Who → By whom · say that → It is said that"),
    ("Narration", "one tense back · now→then, today→that day, tomorrow→the next day · question: if/whether, no 'that' · command: to / not to · Let us → proposed that … should"),
    ("Transformation", "too…to = so…that…cannot · Only → None but / Nothing but · superlative → than any other / No other … as … as"),
    ("Finite", "changes with subject = finite · to + V, V-ing (noun) = gerund, V-ing/V3 (adjective) = participle"),
    ("Clause", "What? = noun · Which one? = adjective · When/Why/How/If? = adverb"),
    ("Group verbs", "tell upon · put off · call off · look into · put up with · give up · bring about · do away with · carry out · come across"),
    ("Idioms", "hit the nail on the head · burn the midnight oil · a blessing in disguise · a white elephant · in the red · the lion's share · once in a blue moon · a bolt from the blue"),
]
S.append(section("!", "Last-night sheet (read twice, then sleep)", "Everything above in 11 lines.",
    table(["Item", "Remember"], [[a, c] for a, c in LAST], "last")))

# ───────────────────────── page ─────────────────────────
CSS = """
@font-face { font-family: "TiroB"; src: url("file://__BN__"); }
@page { size: A4; margin: 13mm 13mm 15mm 13mm; }
:root { --ink:#0f172a; --ink2:#475569; --rule:#dbe3ee; --acc:#2563eb; --accsoft:#eff5ff; --green:#047857; --greensoft:#ecfdf5; --warn:#b45309; --warnsoft:#fff7ed; }
* { box-sizing: border-box; }
body { font-family: "Inter", "TiroB", sans-serif; color: var(--ink); font-size: 10.6pt; line-height: 1.5; margin: 0; }
b { font-weight: 650; }
.cover { height: 268mm; display: flex; flex-direction: column; justify-content: center; padding: 0 6mm; }
.cover .tag { font-size: 9pt; letter-spacing: .14em; text-transform: uppercase; color: var(--acc); font-weight: 700; }
.cover h1 { font-size: 30pt; line-height: 1.08; margin: 6pt 0 8pt; letter-spacing: -.02em; }
.cover .sub { font-size: 12pt; color: var(--ink2); max-width: 150mm; }
.grid9 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 7pt; margin: 18pt 0 12pt; }
.grid9 div { border: 1px solid var(--rule); border-radius: 8pt; padding: 8pt 10pt; background: #fbfcfe; }
.grid9 div b { display: block; font-size: 10.5pt; }
.grid9 div span { color: var(--ink2); font-size: 8.6pt; }
.cover .note { font-size: 8.8pt; color: var(--ink2); border-top: 1px solid var(--rule); padding-top: 8pt; margin-top: 10pt; }
.topic { break-before: page; }
.topic header { display: flex; gap: 10pt; align-items: center; border-bottom: 2px solid var(--ink); padding-bottom: 6pt; margin-bottom: 8pt; }
.topic .no { flex: none; width: 30pt; height: 30pt; border-radius: 8pt; background: var(--ink); color: #fff; display: grid; place-items: center; font-weight: 800; font-size: 14pt; }
.topic h2 { font-size: 15.5pt; margin: 0; letter-spacing: -.01em; }
.topic h2 i { font-style: normal; color: var(--warn); font-size: 11pt; }
.topic header p { margin: 1pt 0 0; color: var(--ink2); font-size: 9.2pt; }
h3 { font-size: 10.5pt; margin: 10pt 0 5pt; color: var(--acc); }
h3 small { color: var(--ink2); font-weight: 500; }
table { width: 100%; border-collapse: collapse; margin: 0 0 9pt; font-size: 10pt; }
th { text-align: left; background: #f1f5f9; color: var(--ink2); font-size: 7.8pt; text-transform: uppercase; letter-spacing: .05em; padding: 4pt 6pt; border-bottom: 1px solid var(--rule); }
td { padding: 4.4pt 6pt; border-bottom: 1px solid var(--rule); vertical-align: top; }
tr { break-inside: avoid; }
table.half td:nth-child(3), table.half th:nth-child(3) { width: 14pt; border: 0; background: transparent; }
table.rev td:nth-child(2), table.rev td:nth-child(4) { color: var(--green); }
table.rev td:nth-child(3), table.rev th:nth-child(3) { border-left: 1px solid var(--rule); }
table.last td:first-child { font-weight: 700; width: 26mm; color: var(--acc); }
.hint { background: var(--greensoft); border-left: 3pt solid var(--green); border-radius: 0 6pt 6pt 0; padding: 6pt 9pt; margin: 6pt 0 8pt; font-family: "TiroB", "Inter", sans-serif; font-size: 11pt; line-height: 1.6; break-inside: avoid; }
.hint span, .trap span { display: inline-block; font-family: "Inter", sans-serif; font-size: 7.6pt; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: var(--green); margin-right: 6pt; }
.trap { background: var(--warnsoft); border-left: 3pt solid var(--warn); border-radius: 0 6pt 6pt 0; padding: 6pt 9pt; margin: 6pt 0 8pt; break-inside: avoid; }
.trap span { color: var(--warn); }
.trap ul { margin: 3pt 0 0; padding-left: 14pt; }
.learn { background: var(--accsoft); border-left: 3pt solid var(--acc); border-radius: 0 6pt 6pt 0; padding: 7pt 10pt; margin: 0 0 8pt; font-family: "TiroB", "Inter", sans-serif; font-size: 11pt; line-height: 1.6; }
.learn span, .steps span, .why span { display: inline-block; font-family: "Inter", sans-serif; font-size: 7.6pt; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: var(--acc); margin-right: 6pt; }
.learn span { font-family: "TiroB", sans-serif; font-size: 9pt; letter-spacing: 0; }
.steps { border: 1px solid var(--rule); border-radius: 6pt; padding: 6pt 10pt; margin: 0 0 9pt; font-family: "TiroB", "Inter", sans-serif; font-size: 10.6pt; line-height: 1.55; break-inside: avoid; }
.steps span { font-family: "TiroB", sans-serif; font-size: 9pt; letter-spacing: 0; color: var(--ink); }
.steps ol { margin: 3pt 0 0; padding-left: 16pt; } .steps li { margin: 1pt 0; }
.wk { border: 1px solid var(--rule); border-radius: 6pt; padding: 6pt 10pt; margin: 0 0 6pt; break-inside: avoid; }
.wk .q { font-weight: 600; } .wk .a { color: var(--green); margin: 2pt 0; }
.why { font-family: "TiroB", "Inter", sans-serif; font-size: 10.2pt; color: var(--ink2); }
.why span { font-family: "TiroB", sans-serif; font-size: 9pt; letter-spacing: 0; color: var(--warn); }
.irreg { columns: 4; column-gap: 10pt; font-size: 9.6pt; margin-bottom: 8pt; } .irreg div { break-inside: avoid; padding: 1.6pt 0; border-bottom: 1px solid var(--rule); } .irreg i { color: var(--green); font-style: normal; font-weight: 600; }
table.tense td:last-child, table.plan td { font-family: "TiroB", "Inter", sans-serif; }
ol.mock li { margin: 0 0 3pt; break-inside: avoid; } ol.mock .q { font-weight: 600; } ol.mock .a { color: var(--green); }
.hint span, .trap span { font-family: "TiroB", sans-serif !important; font-size: 9pt !important; letter-spacing: 0 !important; }
.qa { border: 1px solid var(--rule); border-radius: 6pt; padding: 6pt 9pt; margin: 6pt 0; }
.qa .q { font-weight: 600; } .qa .a { color: var(--green); margin-bottom: 4pt; }
.families { columns: 2; column-gap: 12pt; }
.fam { break-inside: avoid; padding: 3pt 0; border-bottom: 1px dashed var(--rule); font-size: 8.9pt; }
.fam > b:first-child { display: inline-block; min-width: 36pt; color: #fff; background: var(--acc); border-radius: 4pt; padding: 0 4pt; margin-right: 4pt; font-size: 8pt; text-align: center; }
.idioms { display: grid; grid-template-columns: 1fr 1fr; gap: 0 12pt; }
.id { display: grid; grid-template-columns: 38% 1fr; gap: 0 6pt; padding: 2.6pt 0; border-bottom: 1px solid var(--rule); break-inside: avoid; font-size: 8.8pt; }
.id b { grid-row: span 2; } .id em { font-style: normal; font-family: "TiroB", sans-serif; color: var(--ink2); font-size: 8.8pt; }
ol.practice li, ol.key li { margin: 0 0 6pt; padding-left: 2pt; }
ol.practice li { padding-bottom: 14pt; border-bottom: 1px dotted var(--rule); }
ol.key li b { color: var(--green); }
"""
cover = f"""<section class="cover">
<div class="tag">SO Written · 27 November 2026 · Question 8</div>
<h1>English Language Proficiency<br>Memorize &amp; Answer Booklet<br><span style="font-size:15pt;color:#2563eb">Zero-to-20 edition</span></h1>
<div class="sub">From zero to 20/20. Every syllabus item explained in plain Bangla first (শূন্য থেকে বুঝুন), then step-by-step exam method, the rule table, worked examples with the reason (কেন), the trap examiners set and a memory hint. Plus a basics chapter (12 tenses, 68 irregular verbs, pronouns), 50 group verbs, {n_id} idioms by theme, 3 full Question 8 papers with model answers, a {len(PRACTICE)}-item self-test, a 6½-hour study plan and a last-night sheet.</div>
<div class="grid9">
<div><b>0 · Basics</b><span>tenses · V1-V2-V3 · pronouns</span></div>
<div><b>1 · Sentence structure</b><span>simple · compound · complex · compound-complex</span></div>
<div><b>2 · Subject-verb agreement</b><span>16 triggers</span></div>
<div><b>3 · Right form of verbs</b><span>20 clue words</span></div>
<div><b>4 · Voice</b><span>8 tenses + special patterns</span></div>
<div><b>5 · Narration</b><span>tense shift + 8 sentence types</span></div>
<div><b>6 · Transformation</b><span>S/C/C · negative · degree</span></div>
<div><b>7 · Finite / non-finite</b><span>infinitive · gerund · participle</span></div>
<div><b>8 · Clause &amp; phrase</b><span>noun · adjective · adverb</span></div>
<div><b>9–10 · Group verbs &amp; idioms</b><span>50 + {n_id}, themed</span></div>
<div><b>M · 3 mock papers</b><span>15 items, 4/4 answers</span></div>
<div><b>T · Self-test + key</b><span>{len(PRACTICE)} items · last-night sheet</span></div>
</div>
<div class="note">Source: the stress-tested English pack (docs/19, built from the 5 June 2026 paper, Master English Grammar and the NCTB grammar), re-organised for memory. How to use: follow the 8-step plan (page "P") → read the Bangla box → do the worked examples yourself → cover the right column and say it → mocks → self-test → last-night sheet.</div>
</section>"""
html_doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>English Grammar — Memorize &amp; Answer</title>
<style>{CSS.replace("__BN__", FONT_BN)}</style></head><body>{cover}{"".join(S)}</body></html>"""

JS = r"""
const { chromium } = require("playwright");
(async () => {
  const [inp, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto("file://" + inp, { waitUntil: "load" }); await p.evaluate(() => document.fonts.ready);
  await p.emulateMedia({ media: "print" });
  await p.pdf({ path: out, format: "A4", printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: "<span></span>",
    footerTemplate: '<div style="width:100%;text-align:center;font-family:Inter,Arial;font-size:7.5px;color:#64748b">English Language Proficiency (20) · Memorize & Answer · page <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
  await b.close();
})().catch((e) => { console.error(e); process.exit(1); });
"""


def main():
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    open(OUT_HTML, "w", encoding="utf-8").write(html_doc)
    js = os.path.join(os.path.dirname(OUT_HTML), ".mkpdf.js")
    open(js, "w").write(JS)
    try:
        subprocess.run(["node", js, OUT_HTML, OUT_PDF], check=True)
    finally:
        os.remove(js)
    print("PDF:", OUT_PDF)


if __name__ == "__main__":
    main()
