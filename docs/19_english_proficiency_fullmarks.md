# 19 · English Language Proficiency (20 marks): stress-tested full-marks pack

> **Exam:** 27 November 2026 · Question 8 · 20 marks · budget 12–14 minutes
> **Why this file exists:** the 22 Nov audit found that the earlier English prep (doc 09 plus 69 MCQs) had no errors in its rules, but it was too thin to be sure of 20/20. It covered 12 rules, 12 group verbs and 10 idioms, set a target of only 13/20, and practised in MCQ format although the exam is written. This file is now the main source for Q8.

---

## 0. Verdict of the stress test

**The earlier prep would not have secured full marks.** Here is why:

1. **Coverage was too narrow.** The blueprint paper (5 June 2026) asked for a group verb meaning "affect adversely" (*tell upon*), a compound-complex sentence, two idioms and an active→passive change. *Tell upon* was not in the 12-item group-verb list. Neither idiom (*hit the nail on the head*, *burn the midnight oil*) was in the 10-idiom list. The **voice** rules took up one line. With the earlier prep, roughly 8–12 of the 20 marks were safe.
2. **Each item is worth 4 marks, so a one-word answer loses marks.** The paper has 5 items × 4 marks. A full-mark answer gives the answer, then the reason or rule, then an example (see §1). The earlier materials trained one-word MCQ picks.
3. **Quiz tags were wrong**, so topic-wise practice was broken. Six English MCQs were filed under the wrong topic: an article question tagged "right form of verb", a passive item tagged "SVA", an SVA item tagged "speech", a narration item tagged "group verb", and two preposition items tagged "group verb". *(Fixed in `data/quiz.json`.)*
4. **The target was 13/20** (doc 09).

**Now:** this pack covers all 9 syllabus items plus voice (which came up in the blueprint). It also gives the answer format for 4-mark items, about 80 group verbs, about 100 idioms and 3 mock papers with keys. **No preparation can guarantee 20/20.** The paper can name any idiom, and idiom answers are marked somewhat subjectively. With the mocks written out by hand, a realistic score is **18–20**.

---

## 1. The 4-mark answer formula

| Item type | Full-mark answer contains | Model |
|---|---|---|
| Group verb substitution | the rewritten sentence + the group verb's meaning | Over-exercise **told upon** his health. (*tell upon* = affect adversely) |
| Sentence type / structure | the type + the clause breakdown that proves it | **Compound-complex.** Independent: "The sun set", "the stars appeared" (joined by *and*). Dependent: "while we sat by the fire" (adverb clause of time). |
| Idiom meaning | the meaning in one plain line + **your own example sentence** | **To hit the nail on the head** = to say exactly the right thing. *The governor hit the nail on the head when he blamed weak governance for bad loans.* |
| Voice / narration / transformation | the full converted sentence + the rule in a few words | **The results will be announced (by them) tomorrow.** (will + be + V3) |
| Right form / SVA / correction | the whole corrected sentence with the change **bolded** + the rule | Each of the officers **has** a laptop. (*Each of* + plural noun → singular verb) |
| Finite / non-finite, clause / phrase | identify it + name the type + its function | "to join" = non-finite (**to-infinitive**), object of "wants". |

Write in blue or black, underline the changed word, and leave one blank line between items. Examiners skim, so make the answer easy to find.

---

## 2. Sentence structure

**Simple** = one independent clause (*He works in a bank.*). **Compound** = two or more independent clauses joined by *and, but, or, so, yet, for, nor* or a semicolon. **Complex** = one independent clause + one or more dependent clauses (*because, although, when, if, who, which, that*). **Compound-complex** = at least two independent clauses + at least one dependent clause.

**Method:** count the finite verbs, then mark each clause as independent or dependent, then name the type.

**The 5 basic patterns:** SV (*Birds fly*) · SVO (*She signed the cheque*) · SVC (*He became a manager*) · SVOO (*The bank gave him a loan*) · SVOC (*They elected him chairman*).

**Inversion structures (often tested):** *No sooner had he arrived **than** …* · *Hardly / Scarcely had I reached **when** …* · *Not only **did he** apologise but he also …* · *Never **have I** seen …* · *Only then **did** she realise …* · *Seldom **does** he …*

**Articles and prepositions that recur:** an honest / an hour / an MBA / a university / a European / a one-taka coin · senior **to**, junior **to**, superior **to**, prefer A **to** B · comply **with**, abide **by**, prior **to**, independent **of**, dependent **on**, consist **of**, insist **on**, refrain **from**, invest **in**, deal **with**, accused **of**, charged **with**, according **to**, in spite **of**, despite (no *of*), aware **of**, capable **of**, confident **of**, entitled **to**, eligible **for**, responsible **for**.

---

## 3. Subject-verb agreement (20 rules)

1. **Each / every / either / neither / one of / many a** → singular: *One of the banks **has** been merged. Many a man **has** tried.*
2. **A number of** → plural; **the number of** → singular: *A number of banks **are** … The number of defaulters **is** rising.*
3. **Neither…nor / either…or / not only…but also / or** → the verb agrees with the **nearer** subject: *Neither the manager nor the clerks **were** present.*
4. **As well as, along with, together with, with, including, in addition to, accompanied by** → the verb agrees with the **first** subject: *The chairman, along with the directors, **was** present.*
5. **Two nouns joined by *and*** → plural, *but* singular if they name one person or idea: *The secretary and treasurer **is** absent* (one person). *The secretary and **the** treasurer **are** absent* (two people). *Bread and butter **is** …* *Slow and steady **wins** …*
6. **Each / every + noun and noun** → singular: *Every officer and every clerk **was** informed.*
7. **Collective nouns**: singular when the group acts as one unit, plural when the members act separately: *The committee **has** decided. The committee **are** divided in their opinions.*
8. **Plural in form, singular in sense**: news, economics, physics, mathematics, measles → singular: *Economics **is** …*
9. **Always plural**: people, police, cattle, poultry, gentry, scissors, trousers, spectacles: *The police **have** arrested him.*
10. **Uncountable nouns** (always singular, no *-s*): information, advice, furniture, luggage, equipment, machinery, scenery, poetry: *The information **is** correct.*
11. **An amount, distance or time taken as a whole** → singular: *Ten thousand taka **is** a big sum.*
12. **Relative pronouns** take the number of their antecedent: *He is one of those officers who **work** hard. He is the only one of those officers who **works** hard.*
13. **Titles and country names** → singular: *Gulliver's Travels **is** … The United States **is** …*
14. **There + be** agrees with the noun that follows: *There **is** a reason. There **are** many reasons.*
15. **Indefinite pronouns**: everyone, someone, nobody, anything → singular. Few, many, several, both → plural. All, some, most → follow the noun: *Some of the money **is** … Some of the officers **are** …* With **None**, use *is* in formal writing.
16. **Majority / percentage** follow the noun: *The majority of voters **are** … 40 percent of the loan **is** … 40 percent of the borrowers **are** …*
17. **More than one** + singular noun → singular verb: *More than one officer **was** absent.*
18. **The + adjective** (meaning people) → plural: *The rich **are** …*
19. A **phrase between subject and verb** does not change the verb: *The quality of the products **is** poor.*
20. **Modal + be + V3**: *The loan must **be** repaid.*

**Extra SVA traps (*Master English Grammar*, pp. 436–439, all asked in BCS or university tests):**

- An adjective cannot be a subject; it agrees with the noun after it: "Sweet **are** the uses of adversity." "Loud **were** the cries of the victim."
- One and a half + plural noun + **singular** verb: "One and a half hours **is** a long time."
- A pair of + **singular**: "The pair of scissors **is** dull."
- Names of books, countries or subjects are singular: "The United States **is** a rich country." "Gulliver's Travels **is** wonderful." "The Arabian Nights **is** still a great favourite."
- Two nouns joined by *and* that make one idea or dish are singular: "Bread and butter **is** a popular breakfast." "The horse and carriage **is** at the door." "The rise and fall of the tide **is** due to the moon."
- One person holding two posts gets one *the* and a singular verb: "The poet and novelist **is** dead." Two people get two *the*s and a plural verb: "The Headmaster and the Principal **were** present."
- *each / every / no* … *and* … takes a singular verb: "Every man, woman and child **has suffered**." "No boy and no girl **performs** well."
- Subject names (physics, economics, politics, ethics) are singular, but with a determiner the noun takes a plural verb: "Politics **is** popular here." "His politics **are** not practical." "His mathematics **are** weak." (This is the book's answer, following Thomson & Martinet. It means his mathematical ability.)
- Scissors and trousers are plural on their own, but *a pair of* makes them singular (see above).
- The + adjective is a plural noun: "The poor **live** from hand to mouth." "The virtuous **are** blessed."
- *If / wish* + **were** for every person: "If I **were** a king."

---

## 4. Right forms of verbs (30 rules)

| # | Clue | Form | Example |
|---|---|---|---|
| 1 | habit, universal truth | present simple | *The earth **moves** round the sun.* |
| 2 | since / for | present perfect (continuous) | *I **have been working** here since 2020.* |
| 3 | yesterday, ago, last, in 2020 | past simple (never present perfect) | *He **went** to Dhaka yesterday.* |
| 4 | two past actions | the earlier one in past perfect | *The patient **had died** before the doctor **came**.* |
| 5 | after + earlier action | past perfect … past simple | *After he **had finished**, he **left**.* |
| 6 | 1st conditional | If + present, will + base | *If it **rains**, we **will** stay.* |
| 7 | 2nd conditional | If + past (were), would + base | *If I **were** rich, I **would** help.* |
| 8 | 3rd conditional | If + had V3, would have V3 | *If he **had studied**, he **would have passed**.* |
| 9 | inverted conditional | Had / Were / Should + subject | ***Had** I known, I would have come.* |
| 10 | wish / as if / as though / would that / if only (present) | past (were) | *He talks **as if** he **knew** everything.* |
| 11 | wish (past) | past perfect | *I wish I **had seen** it.* |
| 12 | it is (high / about) time | past simple | *It is high time we **took** action.* |
| 13 | lest | should + base | *Walk fast **lest** you **should miss** the train.* |
| 14 | let, make, see, hear, watch, feel, bid | bare infinitive (active) | *He made me **do** it.* → passive: *I was made **to do** it.* |
| 15 | had better / would rather | base | *You **had better go**.* |
| 16 | avoid, enjoy, finish, mind, deny, admit, consider, risk, postpone, suggest, can't help, it's no use, worth, busy | gerund | *He **avoided meeting** me. It's no use **crying**.* |
| 17 | look forward to, be used to, object to, with a view to, accustomed to, addicted to | to + V-ing | *I look forward to **hearing** from you.* |
| 18 | want, decide, agree, hope, expect, plan, refuse, afford, manage, promise | to-infinitive | *She **decided to join** a bank.* |
| 19 | used to (past habit) vs be used to (accustomed) | base vs V-ing | *He **used to smoke**. He **is used to working** late.* |
| 20 | suggest / recommend / insist / demand / propose + that | (should) + base | *The auditor recommended that the branch **be** closed.* |
| 21 | when / until / before / as soon as / if referring to the future | present for future | *I will call you when he **arrives**.* |
| 22 | while (an ongoing past action) | past continuous | *While I **was reading**, the light went out.* |
| 23 | stative verbs (know, believe, own, belong, seem, understand) | no continuous form | *I **know** him* (not *am knowing*). |
| 24 | just, already, yet, ever, never, recently, lately | present perfect | *He **has just left**.* |
| 25 | It is / has been … since + past | past simple after *since* | *It is two years since he **died**.* |
| 26 | need (passive meaning) | needs + V-ing / needs to be V3 | *The form **needs signing**.* |
| 27 | have / get + object + V3 (causative) | V3 | *I **had** my account **updated**.* |
| 28 | would you mind / how about / what about | V-ing | *Would you mind **closing** the door?* |
| 29 | modal + perfect (a deduction about the past) | must / may / can't have V3 | *He **must have forgotten**.* |
| 30 | to (infinitive marker) | base | *I want **to go*** (not *to went*). |

**Extra right-form patterns (*Master English Grammar*, pp. 461–464):**

- *when* + *when* for a habit or universal truth: both present indefinite. "When water **freezes**, its density decreases."
- *now / at present / at this moment / look! / listen!* → present continuous. "Look! A car **is coming**."
- A near future that is already planned → present continuous. "We **are taking** the car to Sylhet next month."
- *for / since* + a stative verb (be, have, know, see) → present perfect, not perfect continuous. "I **have known** him for five years." "She **has been** ill since Monday."
- Present tense + *while* → present indefinite or continuous. "Do not make a noise while your father **is sleeping**."
- Present perfect with *yet* (negative), *already* (affirmative), *just*, *ever*, *never*, *so far*, *up to now*. "I **have not finished** my letter yet."

---

## 5. Finite and non-finite verbs

**A finite verb** changes with the subject's person, number and tense, and makes a clause: *He **works**. They **worked**.*
**Non-finite verbs** do not change with the subject:

- **Infinitive.** *To*-infinitive (*He wants **to join***), bare infinitive (*Let him **go***), perfect infinitive (*He seems **to have left***).
- **Gerund** = V-ing used as a **noun**: ***Saving** money is a good habit* (subject). *He is fond of **reading*** (object of a preposition).
- **Present participle** = V-ing used as an **adjective** or to make a phrase: *a **running** train*, ***Walking** along the road, I met him.*
- **Past participle** = V3 used as an adjective: *a **broken** chair*, *the **approved** loan.*
- **Absolute participle**: ***The sun having set**, we went home.*
- **Dangling participle (an error)**: ~~*Walking down the street, a bus hit him.*~~ → *While he was walking down the street, a bus hit him.*

**Gerund or participle?** Replace the V-ing with a noun such as *it* or *this*. If the sentence still works, it is a gerund.
**Exam model:** "Identify the finite and non-finite verbs: *He wants to open an account.*" → finite: **wants**; non-finite: **to open** (to-infinitive, object of *wants*).

---

## 6. Clause and phrase

**Phrase** = a group of words with no subject + finite verb: *in the morning*, *to save money*, *a very honest officer*. Types: noun phrase, adjective phrase, adverb phrase, prepositional phrase.
**Clause** = a group of words with a subject + finite verb.

| Clause | Function / signal | Example |
|---|---|---|
| **Noun clause** | subject, object, complement, object of a preposition, apposition | ***What he said** is true.* · *I know **that he is honest**.* · *The news **that he has resigned** is true* (apposition). |
| **Adjective (relative) clause** | describes a noun; who / which / that / whose / where / when | *The officer **who approved the loan** was suspended.* |
| **Adverb clause** | time (when, while, after), place (where), reason (because, since, as), purpose (so that), condition (if, unless), concession (though, although), result (so…that), comparison (than, as), manner (as if) | *He was promoted **because he worked hard**.* |

**Defining vs non-defining relative clauses:** *The bank **that** lent us money …* (defining, no commas) vs *Sonali Bank, **which** is state-owned, …* (non-defining, with commas; never *that*).

---

## 7. Transformation of sentences

### 7.1 Simple ↔ Complex ↔ Compound

| Simple | Complex | Compound |
|---|---|---|
| *Being ill, he could not attend.* | *As he was ill, he could not attend.* | *He was ill, **and so** he could not attend.* |
| *In spite of being poor, he is honest.* | *Though he is poor, he is honest.* | *He is poor, **but** he is honest.* |
| *He worked hard to pass.* | *He worked hard **so that he might pass**.* | *He wanted to pass, **so** he worked hard.* |
| *Without working hard, you will fail.* | ***If you do not** work hard, you will fail.* | *Work hard, **or** you will fail.* |
| *He is too weak to walk.* | *He is **so** weak **that** he **cannot** walk.* | *He is very weak, **and so** he cannot walk.* |
| *I know the man's address.* | *I know **where** the man lives.* | — |
| *On seeing the police, the thief ran away.* | ***As soon as** the thief saw the police, he ran away.* | *The thief saw the police **and** (immediately) ran away.* |

### 7.2 Affirmative ↔ Negative

- *Only he can do it* → ***None but** he can do it.* (a person) · *Only water …* → ***Nothing but** water …* (a thing) · *only ten* → ***not more than** ten*
- *He must obey* → *He **cannot but** obey / cannot help obeying.*
- *He is always punctual* → *He is **never** late / never fails to be punctual.*
- *As soon as he came, …* → ***No sooner** had he come **than** …*
- *Both A and B* → ***Not only** A **but also** B*
- *Every mother loves her child* → ***There is no mother but** loves her child.*
- *I was doubtful* → *I was **not sure**.* · *He is honest* → *He is **not dishonest**.*

### 7.3 Interrogative ↔ Assertive

- *Who does not love his country?* → ***Everybody** loves his country.*
- *Is there anyone who can help?* → ***There is no one** who can help.*
- *What is the use of crying?* → ***There is no use** crying.*
- *Did he not help you?* → *He **helped** you.* · *Was he not honest?* → *He was honest.*

### 7.4 Exclamatory ↔ Assertive

- *What a beautiful bird it is!* → *It is a **very** beautiful bird.*
- *How kind he is!* → *He is **very** kind.*
- *Alas! He is dead.* → ***It is a matter of sorrow that** he is dead.*
- *Hurrah! We have won.* → ***It is a matter of great joy that** we have won.*
- *Would that I were rich!* → ***I wish** I were rich.*

### 7.5 Degree of comparison

- *Dhaka is the largest city in Bangladesh* → comparative: *Dhaka is larger **than any other** city in Bangladesh* → positive: ***No other** city in Bangladesh is **as large as** Dhaka.*
- *Shakespeare is one of the greatest poets* → comparative: *Shakespeare is greater than **most other** poets* → positive: ***Very few** poets are as great as Shakespeare.*
- *Karim is taller than Rahim* → *Rahim is **not as (so) tall as** Karim.*

### 7.6 Voice (in the blueprint, so learn every pattern)

| Active | Passive |
|---|---|
| They **announce** the results. | The results **are announced** (by them). |
| They **are announcing** … | … **are being announced** … |
| They **have announced** … | … **have been announced** … |
| They **announced** … | … **were announced** … |
| They **were announcing** … | … **were being announced** … |
| They **had announced** … | … **had been announced** … |
| They **will announce** … tomorrow. | … **will be announced** (by them) tomorrow. |
| You **must repay** the loan. | The loan **must be repaid** (by you). |
| **Did** he write the letter? | **Was** the letter **written** by him? |
| **Who** wrote this? | **By whom was** this written? |
| **Why** did he sign it? | Why **was** it **signed** by him? |
| **Open** the account. | **Let** the account **be opened**. |
| **Please help** me. | You **are requested to** help me. |
| They **laughed at** him. | He **was laughed at** (by them). |
| The bank **gave** him a loan. | He **was given** a loan by the bank. / A loan **was given** to him by the bank. |
| They **made** him **sign**. | He **was made to sign**. |
| People **say** that he is honest. | **It is said that** he is honest. / He **is said to be** honest. |
| I **know** him. | He **is known to** me. |

**Fixed prepositions in the passive:** known **to**, surprised **at**, pleased **with**, satisfied **with**, interested **in**, filled **with**, covered **with**, married **to**, made **of** (material that does not change) / made **from** (material that changes).

### 7.7 Narration (speech)

**Tense backshift** (when the reporting verb is past): am / is → was · are → were · do / does → did · did → had done · have / has → had · will → would · can → could · may → might · shall → should · must → had to (an obligation) or stays *must* (a general truth).
**Time and place words:** now → then · today → that day · tonight → that night · yesterday → the previous day · tomorrow → the next day · ago → before · this → that · these → those · here → there · last night → the previous night.
**No backshift** for universal truths and habitual facts, or when the reporting verb is in the present tense.

| Type | Reporting verb | Example |
|---|---|---|
| Assertive | said / told + object | *He said to me, "I am busy."* → *He **told me that he was** busy.* |
| Yes/no question | asked / enquired + **if / whether** | *He said to me, "Have you submitted the form?"* → *He **asked me if I had submitted** the form.* |
| Wh-question | asked + wh-word + subject + verb | *"Where do you live?"* → *He asked me **where I lived**.* |
| Imperative | ordered / requested / advised / told + **to** | *"Please sign here."* → *He **requested** me **to sign** there.* |
| Negative imperative | told / advised + **not to**, or forbade | *"Don't lie."* → *He told me **not to** lie.* |
| Let us (a proposal) | proposed / suggested + that + we/they + should | *"Let us go."* → *She **proposed that they should go**.* |
| Optative | wished / prayed + that + may | *"May you prosper!"* → *He **prayed that I might** prosper.* |
| Exclamatory | exclaimed with joy / sorrow / wonder + that | *"What a fine day!"* → *He **exclaimed with joy that it was a very fine day**.* |
| Courtesy | thanked / wished / bade | *"Thank you."* → *He **thanked** me.* · *"Good morning, sir."* → *He **wished** me good morning **respectfully**.* |
| Yes / No | replied in the affirmative / negative | *He said, "No."* → *He **replied in the negative**.* |

---

## 8. Group verbs: single verb → group verb (80)

The blueprint asked: "substitute the single verb with a group verb." Learn this list in that direction.

| Single verb | Group verb | | Single verb | Group verb |
|---|---|---|---|---|
| affect adversely | **tell upon** | | postpone | put off |
| cancel | call off | | investigate | look into / inquire into |
| tolerate | put up with | | extinguish | put out |
| quit | give up | | establish | set up |
| resemble | take after | | raise (a child) | bring up |
| explode | blow up | | disappoint | let down |
| find by chance | come across | | reject | turn down |
| visit | call on | | recover (from illness) | get over |
| continue | carry on / go on | | execute | carry out |
| compensate | make up for | | understand | make out |
| despise | look down upon | | respect | look up to |
| search | look for | | examine | go through |
| consult (a book) | look up | | explain | account for |
| start (a journey) | set out / set off | | arrive | turn up |
| cause | bring about | | publish | bring out |
| reduce | cut down (on) | | surrender | give in |
| distribute | give away / hand out | | reveal (a secret) | give away |
| escape | get away | | review | go over |
| abolish | do away with | | omit | leave out |
| demolish | pull down | | represent | stand for |
| support | stand by / back up | | endure | hold out |
| delay | hold up | | exhaust (a supply) | run out of |
| meet by chance | run into | | increase | go up |
| decrease | come down | | happen | come about / take place |
| invent (a story) | make up | | reconcile | make up |
| wear | put on | | remove (clothes) / succeed suddenly | take off |
| employ | take on | | undertake / start (a hobby) | take up |
| participate | take part in | | faint | pass out |
| die | pass away | | ask about (health) | ask after |
| write down / suppress | put down | | accommodate | put up |
| propose (an idea) | put forward / come up with | | repay | pay back |
| settle (a debt) | pay off | | save | set aside / put aside |
| withdraw (from a promise) | back out | | overlook | pass over |
| eliminate | weed out / root out | | quarrel | fall out |
| fail (a plan) | fall through | | depend on | rely on / count on |
| discuss | talk over | | wait | hang on / hold on |
| check (the facts) | find out | | conclude | wind up |
| close (a business) | shut down / wind up | | collapse | break down |
| begin (war or fire) | break out | | interrupt | break in |
| stop (a habit) | leave off | | take care of | look after |

### 8.1 Group verbs by head verb (from *Master English Grammar*, pp. 338–365, the exam-tagged ones)

Examiners also ask the other way round: "Use *put off* in a sentence" or "fill in the gap: The meeting was put ___". So learn each head verb with all its particles. ★ = asked in BCS or bank papers.

| Head verb | Particle → meaning (example) |
|---|---|
| **act** | act **upon/on** = follow (act upon my advice) · act **for** = represent · act **up** = behave badly · act **up to** = live up to |
| **bear** | bear **out** = confirm · bear **with** = tolerate ★ · bear **up** = endure · bear **down** = overpower |
| **blow** | blow **up** = explode · blow **out** = extinguish · blow **over** = pass away (the storm blew over) |
| **break** | break **down** = collapse / stop working ★ · break **out** = start suddenly (war, fire) ★ · break **in/into** = interrupt / enter by force · break **off** = stop suddenly · break **up** = close (school broke up) · break **with** = quarrel with |
| **bring** | bring **up** = rear ★ · bring **about** = cause ★ · bring **out** = publish · bring **forth** = produce · bring **round/through** = cure · bring **in** = yield / introduce · bring **down** = reduce |
| **call** | call **off** = cancel ★ · call **on** = visit ★ · call **for** = demand / require ★ · call **at** = visit (a place) · call **up** = phone / recall · call **in** = summon · call **over** = take the roll call ★ · call **out** = order to come out |
| **carry** | carry **out** = execute / obey ★ · carry **on** = continue ★ · carry **off** = win (prizes) / cause death · carry **away** = remove · carry **over** = take forward (an amount) · carry **through** = bring success |
| **come** | come **across** = meet by chance ★ · come **about** = happen ★ · come **off** = take place ★ · come **round** = recover ★ · come **out** = be published ★ · come **of** = be born of (a family) ★ · come **from** = belong to (a place) · come **by** = get · come **down** = decrease · come **down with** = fall ill with ★ · come **down on** = criticise strongly · come **up** = appear · come **up to** = equal (expectation) · come **over** = influence · come **to** = amount to · come **at** = attack |
| **cut** | cut **down** = fell / reduce ★ · cut **down on** = consume less ★ · cut **off** = die young / disconnect / isolate ★ · cut **in** = interrupt ★ · cut **up** = grieve · cut **out** = remove |
| **die** | die **of** a disease / hunger ★ · die **from** a wound / overwork ★ · die **by** an accident / the sword ★ · die **for** one's country ★ · die **in** battle / poverty · die **out** = become extinct ★ · die **away** = fade (the sound died away) ★ · die **down** = become weaker ★ · die **off** = die one by one ★ |
| **do** | do **away with** = abolish ★ · do **up** = repair or decorate · do **without** = manage without |
| **fall** | fall **out** = quarrel ★ · fall **through** = fail ★ · fall **off** = decline · fall **back on** = depend on (as a last resort) ★ · fall **in with** = agree with ★ · fall **on** = attack ★ · fall **among** = come among · fall **behind** = be late (with payments) ★ · fall **flat** = have no effect ★ · fall **short of** = be less than |
| **get** | get **over** = overcome / recover ★ · get **through** = pass (an exam) ★ · get **on** = board (a bus) ★ · get **off** = get down / escape ★ · get **along with** = live in harmony ★ · get **on with** = have a good relationship ★ · get **by** = manage (on money) ★ · get **at** = reach (the truth) ★ · get **away** = escape · get **up** = rise · get **back** = recover (a stolen thing) ★ |
| **give** | give **up** = abandon / quit ★ · give **in** = surrender / yield ★ · give **away** = distribute / reveal ★ · give **out** = distribute / be exhausted ★ · give **over** = stop · give **off** = emit |
| **go** | go **through** = read / examine / suffer ★ · go **over** = examine / review ★ · go **off** = explode / go bad ★ · go **out** = be extinguished ★ · go **on** = continue · go **back on** = withdraw (a promise) ★ · go **by** = follow (the rules) · go **in for** = take part in / adopt ★ · go **with** = agree with · go **without** = live without ★ · go **after** = pursue ★ · go **against** = oppose · go **beyond** = exceed · go **up** = increase |
| **hold** | hold **up** = delay / rob ★ · hold **on** = wait · hold **out** = endure / offer ★ · hold **over** = postpone ★ · hold **off on** = delay (a decision) ★ |
| **keep** | keep **up** = maintain ★ · keep **up with** = keep pace with ★ · keep **on** = continue ★ · keep **back** = conceal ★ · keep **down** = suppress · keep **off** = keep away ★ · keep **out** = prevent from entering |
| **look** | look **after** = take care of ★ · look **into** = investigate ★ · look **for** = search ★ · look **up** = consult (a dictionary) / improve ★ · look **up to** = respect ★ · look **down upon** = despise ★ · look **over** = examine ★ · look **out** = be careful ★ · look **forward to** + -ing = expect with pleasure · look **to** = attend to ★ · look **on** = watch · look **like** = resemble |
| **make** | make **out** = understand ★ · make **up** = compensate / invent / complete ★ · make **up for** = compensate ★ · make **up one's mind** = decide ★ · make **off** = run away ★ · make **for** = move towards · make **after** = chase · made **of / from** = material / raw material ★ · made **up of** = composed of ★ |
| **pass** | pass **away** = die ★ · pass **off as** = pretend to be ★ · pass **out** = faint / graduate · pass **over** = overlook · pass **by** = ignore |
| **put** | put **off** = postpone ★ · put **out** = extinguish ★ · put **up with** = tolerate ★ · put **up** = stay (for a time) ★ · put **on** = wear / pretend ★ · put **down** = suppress / write down ★ · put **aside / by** = save ★ · put **away** = give up / store · put **forward** = propose |
| **run** | run **into** = meet by chance / fall into (debt) ★ · run **over** = knock down (with a vehicle) ★ · run **out of** = exhaust (a supply) ★ · run **after** = chase ★ · run **away** = flee · run **down** = criticise · run **short of** = have too little ★ · run **across** = meet by chance |
| **see** | see **off** = say goodbye (at a station) ★ · see **through** = understand (a trick) / continue to the end ★ · see **to** = attend to ★ · see **to it that** = make sure ★ |
| **set** | set **up** = establish ★ · set **out / off** = start (a journey) ★ · set **in** = begin (winter, rains) ★ · set **about** = begin (work) ★ · set **aside** = reserve / ignore ★ · set **down** = write down ★ · set **upon / on** = attack ★ · set **back** = delay · set **forth** = start / explain |
| **stand** | stand **by** = support ★ · stand **for** = represent / contest ★ · stand **out** = be prominent · stand **against** = oppose · stand **up for** = defend · stand **over** = be postponed · stand **to reason** = be logical |
| **take** | take **after** = resemble ★ · take **off** = remove / leave the ground ★ · take **up** = start (a hobby) / occupy (time) ★ · take **over** = take control ★ · take **in** = deceive ★ · take **for** = mistake for ★ · take **to** = become addicted to ★ · take **on** = employ · take **back** = withdraw (words) · take **away** = remove |
| **tell** | tell **upon** = affect adversely ★★ (blueprint, June 2026) |
| **turn** | turn **down** = reject ★ · turn **up** = arrive ★ · turn **out** = expel / prove to be ★ · turn **on / off** = switch on/off ★ · turn **in** = submit ★ · turn **into** = change into · turn **over** = overturn ★ · turn **aside** = deviate · turn **against** = become hostile · turn **to** = take up (a study) |

**Traps the book flags most:**

- **die of / from / by.** Disease or hunger: *of*. Wound, overwork or overeating: *from*. Accident: *by* (also *in* an accident). "He died ___ hunger" → *of* (or *from*, but if *of* is not among the options, *from* is right).
- **come of / come from.** Family: *of* ("He comes of a noble family"). Place: *from*.
- **take to.** After it, use verb + ing: "He took to drinking." **hope to** takes the base form: "hoping to lose weight."
- **made of / from.** *Of*: the material stays visible (a ring made of gold). *From*: the material is changed (paper is made from wood).
- **look forward to / be used to / object to / with a view to** all take verb + ing: "I look forward to **hearing** from you."

---

## 9. Idioms (100, with the blueprint ones first)

**Blueprint and banking:** hit the nail on the head = say exactly the right thing · burn the midnight oil = work or study late at night · burn the candle at both ends = overwork oneself until exhausted · a blessing in disguise = something that seems bad but turns out good · foot the bill = pay for something · in the red = in debt or making a loss · in the black = in profit · bail out = rescue (a firm) financially · tighten one's belt = spend less · make both ends meet = live within one's income · from hand to mouth = with barely enough to live on · on a shoestring = with very little money · a white elephant = a costly but useless possession · a drop in the ocean = a very small amount compared with what is needed · the tip of the iceberg = a small visible part of a large problem · cut one's coat according to one's cloth = live within one's means · red tape = bureaucratic delay · the lion's share = the largest part · a ballpark figure = a rough estimate · back to square one = back to the start · cut corners = do something cheaply or carelessly · a cash cow = a steady source of profit · make a killing = make a large profit quickly · save for a rainy day = save money for hard times

**Most frequently set:** a bolt from the blue = a sudden shock · at a stone's throw = very near · once in a blue moon = very rarely · break the ice = start a conversation in an awkward situation · in black and white = in writing · call a spade a spade = speak frankly · a red-letter day = a memorable day · at sixes and sevens = in disorder · at daggers drawn = bitterly hostile · at one's wits' end = completely puzzled · at the eleventh hour = at the last moment · apple of discord = the cause of a quarrel · apple of one's eye = a dearly loved person · Achilles' heel = a weak point · an axe to grind = a selfish motive · beat about the bush = avoid the main point · bear the brunt = take the worst part · bring to book = punish, call to account · by fits and starts = irregularly · by hook or by crook = by any means · by leaps and bounds = very rapidly · cry over spilt milk = regret what cannot be undone · cut a sorry figure = make a poor impression · few and far between = rare · get into hot water = get into trouble · give the cold shoulder = ignore deliberately · Greek to me = incomprehensible · hand in glove = in close (often bad) partnership · hang by a thread = be in great danger · in a nutshell = in brief · in cold blood = deliberately and cruelly · in the long run = eventually · ins and outs = full details · keep one's fingers crossed = hope for success · kill two birds with one stone = achieve two aims with one action · leave no stone unturned = try every possible means · nip in the bud = stop something at the start · null and void = invalid · on the horns of a dilemma = facing two bad choices · out of the question = impossible · pros and cons = advantages and disadvantages · pull one's leg = tease · put the cart before the horse = do things in the wrong order · rain cats and dogs = rain heavily · see eye to eye = agree fully · sit on the fence = stay neutral · spill the beans = reveal a secret · take to one's heels = run away · through thick and thin = in all circumstances · turn a deaf ear = ignore · up to the mark = of the expected standard · a wet blanket = a person who spoils others' fun · bite the bullet = face a hard situation bravely · a feather in one's cap = an achievement to be proud of · cost an arm and a leg = be very expensive · hit below the belt = act unfairly · the ball is in your court = it is your turn to act · a bed of roses = an easy, comfortable situation · a bird's eye view = a general overview · a cock-and-bull story = an absurd, unbelievable story · a far cry = very different · a fish out of water = someone in an unfamiliar situation · a hard nut to crack = a difficult problem or person · a Herculean task = a very difficult task · a man of letters = a scholar or writer · a man of straw = a person of no substance · a snake in the grass = a hidden enemy · a wild-goose chase = a hopeless search · a white lie = a harmless lie · a dark horse = an unexpected winner · blue blood = aristocratic birth · break the news = reveal bad news gently · come to light = become known · face the music = accept the consequences · get the sack = be dismissed from a job · go to the dogs = be ruined · in hot water = in trouble · keep body and soul together = barely survive · let the cat out of the bag = reveal a secret by mistake · lose heart = become discouraged · move heaven and earth = make every possible effort · of no avail = useless · play second fiddle = take a subordinate role · put one's foot down = take a firm stand · smell a rat = suspect something wrong · steal the show = attract the most attention · take with a pinch of salt = doubt slightly · to the backbone = thoroughly · under one's thumb = under one's control · win hands down = win easily

---

## 10. Three mock papers (5 June 2026 format, 5 × 4 marks)

**Rule:** write each one by hand in 13 minutes, then mark it against the key and the §1 formula. Take 1 mark off for every missing "rule" or "example".

### Mock 1
(a) Substitute the single verb with a group verb: "The government has **abolished** the old tax." (b) What type of sentence is this? "Although the bank was profitable, it closed two branches because costs rose." (c) Explain the idiom *a white elephant* and use it in a sentence. (d) Change the voice: "Who signed this cheque?" (e) Change the narration: He said to me, "Don't disclose the PIN to anyone."

### Mock 2
(a) Correct the sentence: "Neither the chairman nor the directors was present." (b) Give the right form of the verbs: "If he (study) harder, he would have passed. It is high time we (reform) the banking sector." (c) Identify the finite and non-finite verbs: "Having finished the audit, he wanted to submit the report." (d) Make it complex: "In spite of his poverty, he is honest." (e) Explain the idiom *to burn the candle at both ends* with an example.

### Mock 3
(a) Identify the clause and its function: "The news **that the bank has collapsed** shocked everyone." (b) Substitute a group verb: "Inflation **affected** the poor **adversely**." (c) Change the narration: She said, "Let us open a savings account." (d) Make it negative without changing the meaning: "Only the governor can approve this." (e) Change the voice: "The bank gave him a loan."

### Answer key
**Mock 1:** (a) The government has **done away with** the old tax. (*do away with* = abolish) (b) **Complex**: one independent clause ("it closed two branches") + two dependent adverb clauses ("Although the bank was profitable" – concession; "because costs rose" – reason). (c) A white elephant = a costly possession that is of no use. *The unused airport became a white elephant for the government.* (d) **By whom was this cheque signed?** (e) He **told / advised me not to disclose** the PIN to anyone.
**Mock 2:** (a) Neither the chairman nor the directors **were** present. (The verb agrees with the nearer subject.) (b) **had studied** (3rd conditional); **reformed** (It is high time + past). (c) Finite: **wanted**. Non-finite: **Having finished** (perfect participle), **to submit** (to-infinitive). (d) **Though he is poor, he is honest.** (e) To burn the candle at both ends = to exhaust oneself by working from early morning till late night. *Working two jobs, he burned the candle at both ends and fell ill.*
**Mock 3:** (a) **Noun clause**, in apposition to "the news". (b) Inflation **told upon** the poor. (c) She **proposed that they should open** a savings account. (d) **None but** the governor can approve this. (e) He **was given a loan by the bank.** / A loan **was given to him by the bank.**

---

## 11. 5-day schedule (22–26 Nov, 40 minutes a day)

| Day | Work |
|---|---|
| 22 Nov | §1 formula · §7.6 voice table (write all 18 rows from memory) · Mock 1 |
| 23 Nov | §3 SVA · §4 right forms (cover the right-hand column and recall it) · Mock 2 |
| 24 Nov | §8 group verbs (cover the right-hand column) · §9 the first 50 idioms, with one sentence each for 10 of them |
| 25 Nov | §5 finite / non-finite · §6 clauses · §7.1–7.5 transformation · §7.7 narration · Mock 3 |
| 26 Nov | §9 the remaining idioms · redo every mistake from the three mocks · web app English MCQs once |

---

## 12. Correction log (22 Nov 2026)

| Where | Problem | Fix |
|---|---|---|
| `data/quiz.json` eng[12] | an article question tagged *right form of verb* | retagged → structure |
| `data/quiz.json` eng[13] | a passive (modal + be) item tagged *SVA* | retagged → voice |
| `data/quiz.json` eng[15] | *Each of … has* tagged *speech* | retagged → sva |
| `data/quiz.json` eng[16] | a narration item tagged *group verb* | retagged → speech |
| `data/quiz.json` eng[17–18] | *comply with / accused of* tagged *group verb* | retagged → structure (preposition) |
| doc 09 | target of 13/20; 12 group verbs, 10 idioms; voice in one line | pointer added to this file; full lists here |
| blueprint gap | *tell upon*, *hit the nail on the head* and *burn the midnight oil* were missing from every list | added (§8, §9) |

**23 Nov 2026:** added §8.1 (group verbs by head verb), the extra SVA traps after §3 and the extra right-form patterns after §4, all read from *Master English Grammar*. The English PDF in `final_pdfs/` is built from this file.
