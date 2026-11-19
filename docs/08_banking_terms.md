<!-- স্বয়ংক্রিয়ভাবে তৈরি: engine/build_docs.py — সরাসরি এডিট না করে data/*.json বদলান -->

# ০৮ · ব্যাংকিং পরিভাষা ও সাম্প্রতিক তথ্য (ব্যাংকিং ১০ + GK ১০)

মোট ৮৬টি পরিভাষা। কুইজ: `python3 engine/so.py terms --quiz 15`

| সংক্ষেপ | পূর্ণরূপ | এক লাইনে |
|---|---|---|
| **CRR** | Cash Reserve Ratio | আমানতের যে অংশ ব্যাংককে নগদে বাংলাদেশ ব্যাংকে জমা রাখতে হয়; বাড়ালে বাজারে টাকা কমে। |
| **SLR** | Statutory Liquidity Ratio | আমানতের যে অংশ নগদ/সরকারি বন্ড/অনুমোদিত তরল সম্পদে রাখতে হয়। |
| **Repo** | Repurchase Agreement | কেন্দ্রীয় ব্যাংক বন্ড জামানত নিয়ে ব্যাংককে স্বল্পমেয়াদি ঋণ দেয়; এটাই পলিসি রেট (এখন ১০%)। |
| **Reverse Repo** | Reverse Repurchase Agreement | ব্যাংক কেন্দ্রীয় ব্যাংকে টাকা রাখে; বাজার থেকে অতিরিক্ত তারল্য তুলে নেওয়ার হাতিয়ার। |
| **SLF** | Standing Lending Facility | জরুরি প্রয়োজনে ব্যাংক BB থেকে ঋণ নেয় — সুদ-করিডরের ঊর্ধ্বসীমা (১১.৫%)। |
| **SDF** | Standing Deposit Facility | ব্যাংক উদ্বৃত্ত টাকা BB-তে রাখে — সুদ-করিডরের নিম্নসীমা (৭.৫%)। |
| **IRC** | Interest Rate Corridor | SDF ও SLF-এর মাঝের সুদহার কাঠামো; মাঝখানে পলিসি রেট। |
| **OMO** | Open Market Operations | সরকারি বিল/বন্ড কেনাবেচা করে কেন্দ্রীয় ব্যাংকের তারল্য নিয়ন্ত্রণ। |
| **Bank Rate** | Bank Rate | যে হারে কেন্দ্রীয় ব্যাংক বাণিজ্যিক ব্যাংকের বিল পুনঃবাট্টা করে। |
| **NPL** | Non-Performing Loan | নির্ধারিত সময়ে (সাধারণত ৯০ দিন) কিস্তি না আসা ঋণ — খেলাপি ঋণ; মার্চ ২০২৬-এ ৩২.২৬%। |
| **SMA** | Special Mention Account | খেলাপি হওয়ার ঝুঁকিতে থাকা ঋণ হিসাব (প্রাথমিক সতর্কসংকেত)। |
| **CAR / CRAR** | Capital to Risk-weighted Asset Ratio | ঝুঁকিভিত্তিক সম্পদের বিপরীতে মূলধনের অনুপাত; Basel III-এ ন্যূনতম ১০% + ২.৫% বাফার। |
| **Basel III** | Basel Accord III | ব্যাংকের মূলধন, তারল্য (LCR, NSFR) ও লিভারেজ নিয়ে আন্তর্জাতিক মানদণ্ড। |
| **LCR** | Liquidity Coverage Ratio | ৩০ দিনের চাপে টিকে থাকার মতো উচ্চমানের তরল সম্পদ (≥১০০%)। |
| **NSFR** | Net Stable Funding Ratio | দীর্ঘমেয়াদি স্থিতিশীল তহবিলের অনুপাত (>১০০%)। |
| **ADR** | Advance-Deposit Ratio | মোট আমানতের কত অংশ ঋণ দেওয়া হয়েছে। |
| **ECL** | Expected Credit Loss | IFRS 9 অনুযায়ী ভবিষ্যৎ সম্ভাব্য ঋণক্ষতির বিপরীতে আগাম প্রভিশন; লক্ষ্য ২০২৭। |
| **IFRS 9** | International Financial Reporting Standard 9 | আর্থিক উপকরণের হিসাবমান; ECL পদ্ধতি এর অংশ। |
| **AQR** | Asset Quality Review | ব্যাংকের ঋণ/সম্পদের প্রকৃত মান যাচাই (৬টি শরিয়াহ ব্যাংকে হয়েছে)। |
| **RBS** | Risk-Based Supervision | ঝুঁকির মাত্রা অনুযায়ী ব্যাংক তদারকি। |
| **Bank Resolution** | Bank Resolution Act 2026 | দুর্বল ব্যাংক একীভূত/পুনর্গঠন/অবসায়নের আইনি কাঠামো। |
| **Deposit Insurance** | Deposit Protection Act 2026 | ব্যাংক বন্ধ হলে আমানতকারী সর্বোচ্চ ২ লাখ টাকা ফেরত পাবেন (আগে ১ লাখ)। |
| **BRRF** | Bank Restructuring and Resolution Fund | ব্যাংক পুনর্গঠন ও রেজল্যুশনের জন্য তহবিল। |
| **ELA** | Emergency Liquidity Assistance | সংকটে পড়া সচ্ছল ব্যাংককে কেন্দ্রীয় ব্যাংকের জরুরি তারল্য। |
| **DAMA** | Distressed Asset Management Act | খেলাপি সম্পদ আলাদা কোম্পানিতে সরিয়ে ব্যবস্থাপনার প্রস্তাবিত আইন (ব্যাড ব্যাংক ধারণা)। |
| **Artha Rin Adalat** | Money Loan Court | অর্থঋণ আদালত — খেলাপি ঋণ আদায়ের বিশেষ আদালত। |
| **KYC** | Know Your Customer | গ্রাহকের পরিচয় ও লেনদেন প্রোফাইল যাচাই। |
| **e-KYC** | Electronic KYC | NID ও ছবি দিয়ে ডিজিটালি হিসাব খোলা। |
| **AML** | Anti-Money Laundering | অর্থপাচার প্রতিরোধ ব্যবস্থা। |
| **CFT** | Combating Financing of Terrorism | সন্ত্রাসে অর্থায়ন প্রতিরোধ। |
| **BFIU** | Bangladesh Financial Intelligence Unit | অর্থপাচার/সন্দেহজনক লেনদেন (STR) বিশ্লেষণকারী সংস্থা, BB-র অধীনে। |
| **STR / SAR** | Suspicious Transaction / Activity Report | সন্দেহজনক লেনদেন বা কার্যক্রমের রিপোর্ট BFIU-তে। |
| **CTR** | Cash Transaction Report | নির্দিষ্ট সীমার (১০ লাখ টাকা) বেশি নগদ লেনদেনের রিপোর্ট। |
| **Hundi** | Hundi (informal transfer) | অবৈধ অনানুষ্ঠানিক টাকা পাঠানোর পথ; রেমিট্যান্স ও রিজার্ভের ক্ষতি। |
| **RTGS** | Real Time Gross Settlement | বড় অঙ্কের তাৎক্ষণিক আন্তঃব্যাংক লেনদেন (১ লাখ টাকার বেশি)। |
| **BEFTN** | Bangladesh Electronic Funds Transfer Network | ব্যাচভিত্তিক ইলেকট্রনিক আন্তঃব্যাংক লেনদেন (বেতন, ডিভিডেন্ড)। |
| **NPSB** | National Payment Switch Bangladesh | কার্ড/ইন্টারনেট ব্যাংকিংয়ে আন্তঃব্যাংক তাৎক্ষণিক লেনদেনের সুইচ। |
| **BACH** | Bangladesh Automated Clearing House | চেক (BACPS) ও BEFTN-এর স্বয়ংক্রিয় ক্লিয়ারিং ব্যবস্থা। |
| **Bangla QR** | Bangla QR | জাতীয় ইন্টারঅপারেবল QR পেমেন্ট মান; ব্যাংক-MFS সব অ্যাপে চলে। |
| **Taka Pay** | Taka Pay | দেশীয় কার্ড স্কিম (NPSB-ভিত্তিক), ভিসা/মাস্টারকার্ড নির্ভরতা কমাতে। |
| **IIPS** | Instant Interoperable Payment System | সব ব্যাংক-MFS-এর মধ্যে তাৎক্ষণিক লেনদেন ব্যবস্থা; লক্ষ্য জুন ২০২৭। |
| **MFS** | Mobile Financial Service | মোবাইলভিত্তিক আর্থিক সেবা (বিকাশ, নগদ, রকেট)। |
| **CBDC** | Central Bank Digital Currency | কেন্দ্রীয় ব্যাংক ইস্যুকৃত ডিজিটাল মুদ্রা। |
| **Digital Bank** | Digital Bank | শাখাবিহীন, সম্পূর্ণ অনলাইনভিত্তিক ব্যাংক (BB নীতিমালা ২০২৩)। |
| **Agent Banking** | Agent Banking | এজেন্টের মাধ্যমে শাখার বাইরে সীমিত ব্যাংকিং সেবা। |
| **Financial Inclusion** | Financial Inclusion | সব মানুষকে সাশ্রয়ী আনুষ্ঠানিক আর্থিক সেবার আওতায় আনা। |
| **CMSME** | Cottage, Micro, Small & Medium Enterprises | কুটির, অতি ক্ষুদ্র, ক্ষুদ্র ও মাঝারি শিল্প। |
| **Refinance** | Refinance Scheme | ব্যাংক যে ঋণ দেয় তার অর্থ BB কম সুদে ব্যাংককে ফেরত দেয়। |
| **LC** | Letter of Credit | আমদানিকারকের পক্ষে ব্যাংকের পরিশোধ নিশ্চয়তাপত্র। |
| **UCP 600** | Uniform Customs & Practice for Documentary Credits | LC-এর আন্তর্জাতিক নিয়মাবলি (ICC)। |
| **Incoterms** | International Commercial Terms | FOB, CIF ইত্যাদি বাণিজ্যিক শর্ত (ICC, সর্বশেষ ২০২০)। |
| **SWIFT** | Society for Worldwide Interbank Financial Telecommunication | আন্তর্জাতিক ব্যাংক বার্তা নেটওয়ার্ক। |
| **SOFR** | Secured Overnight Financing Rate | LIBOR-এর বদলে ডলার ঋণের রেফারেন্স রেট। |
| **ACU** | Asian Clearing Union | আঞ্চলিক আমদানি দায় নিষ্পত্তি ব্যবস্থা; প্রতি দুই মাসে পরিশোধে রিজার্ভ কমে। |
| **BPM6** | Balance of Payments Manual 6 | IMF-এর রিজার্ভ/লেনদেন ভারসাম্য হিসাবের মান। |
| **BoP** | Balance of Payments | চলতি + মূলধন + আর্থিক হিসাবের সমষ্টি। |
| **CAB** | Current Account Balance | পণ্য, সেবা, আয় ও রেমিট্যান্সের নিট হিসাব। |
| **Broad Money (M2)** | Broad Money | নগদ + চাহিদা ও মেয়াদি আমানত; FY27 লক্ষ্য ১৩%। |
| **Reserve Money** | Reserve Money / High-powered money | প্রচলিত মুদ্রা + ব্যাংকের BB-তে রাখা রিজার্ভ। |
| **Money Multiplier** | Money Multiplier | M2 ÷ Reserve Money (~৫.২)। |
| **Stagflation** | Stagflation | উচ্চ মূল্যস্ফীতি + নিম্ন প্রবৃদ্ধি + বেকারত্ব একসাথে। |
| **Core Inflation** | Core Inflation | খাদ্য ও জ্বালানি বাদ দিয়ে মূল্যস্ফীতি। |
| **Crowding Out** | Crowding Out | সরকার ব্যাংক থেকে বেশি ঋণ নিলে বেসরকারি খাত ঋণ কম পায়। |
| **Fiscal Policy** | Fiscal Policy | সরকারের কর ও ব্যয় নীতি (অর্থ মন্ত্রণালয়)। |
| **Monetary Policy** | Monetary Policy | সুদহার ও অর্থ সরবরাহ নীতি (বাংলাদেশ ব্যাংক)। |
| **Sukuk** | Sukuk | শরিয়াহসম্মত সম্পদভিত্তিক বন্ড। |
| **Green Banking** | Green Banking | পরিবেশবান্ধব প্রকল্পে অর্থায়ন ও কাগজবিহীন ব্যাংকিং। |
| **Sustainable Finance** | Sustainable Finance | ESG বিবেচনায় অর্থায়ন; BB-র Sustainable Finance Department। |
| **ESG** | Environmental, Social, Governance | পরিবেশ, সামাজিক ও সুশাসন মানদণ্ড। |
| **CSR** | Corporate Social Responsibility | প্রতিষ্ঠানের সামাজিক দায়বদ্ধতা। |
| **LDC** | Least Developed Country | স্বল্পোন্নত দেশ; বাংলাদেশের উত্তরণ ২৪ নভেম্বর ২০২৯। |
| **GSP / EBA** | Generalised Scheme of Preferences / Everything But Arms | EU-তে এলডিসি হিসেবে শুল্কমুক্ত রপ্তানি সুবিধা। |
| **GSP+** | GSP Plus | এলডিসি-পরবর্তী EU সুবিধা, শ্রম-মানবাধিকারসহ ২৭টি কনভেনশন মানতে হয়। |
| **FDI** | Foreign Direct Investment | বিদেশি প্রত্যক্ষ বিনিয়োগ। |
| **CIB** | Credit Information Bureau | ঋণগ্রহীতার ঋণ-ইতিহাস তথ্যভান্ডার (BB)। |
| **Wilful Defaulter** | Wilful Defaulter | সামর্থ্য থাকা সত্ত্বেও ইচ্ছাকৃত খেলাপি। |
| **Write-off** | Loan Write-off | আদায় অনিশ্চিত খেলাপি ঋণ ব্যালান্সশিট থেকে বাদ (আদায় চেষ্টা চলবে)। |
| **Mudaraba** | Mudaraba | ইসলামী ব্যাংকিংয়ে লাভ-ক্ষতি ভাগাভাগি চুক্তি। |
| **Murabaha** | Murabaha | খরচ+লাভে কিস্তিতে বিক্রয় চুক্তি (ইসলামী ব্যাংকিং)। |
| **Hire Purchase** | Hire Purchase | কিস্তিতে মূল্য পরিশোধ শেষে মালিকানা হস্তান্তর। |
| **Overdraft** | Overdraft | হিসাবে জমার চেয়ে বেশি টাকা তোলার সুবিধা। |
| **Cheque Crossing** | Crossed Cheque | চেকের কোণে দুটি সমান্তরাল রেখা — নগদ নয়, শুধু হিসাবে জমা হবে। |
| **Negotiable Instrument** | Negotiable Instruments Act 1881 | চেক, বিল অব এক্সচেঞ্জ, প্রমিসরি নোট। |
| **Bancassurance** | Bancassurance | ব্যাংকের মাধ্যমে বিমা পণ্য বিক্রি। |
| **Fintech** | Financial Technology | প্রযুক্তিনির্ভর আর্থিক সেবা। |
| **Regtech** | Regulatory Technology | প্রযুক্তি দিয়ে নিয়ন্ত্রক তদারকি/কমপ্লায়েন্স। |

## সাম্প্রতিক তথ্য (GK + রচনার ডেটা বক্স)

| ট্যাগ | তথ্য | উৎস |
|---|---|---|
| inflation | পয়েন্ট-টু-পয়েন্ট মূল্যস্ফীতি অক্টোবর ২০২৬: ৮.২৭% (সেপ্টেম্বর ৮.৩৪%) | NEWS: BBS via Financial Express/Daily Sun, Nov 2026 |
| inflation | খাদ্য মূল্যস্ফীতি ৬.৪০% (৫৪ মাসে সর্বনিম্ন), খাদ্যবহির্ভূত ৯.৮৯% (৪১ মাসে সর্বোচ্চ) — অক্টোবর ২০২৬ | NEWS: BBS, Nov 2026 |
| inflation | ১২ মাসের গড় মূল্যস্ফীতি ৮.৬৬% (নভে ২০২৫–অক্টো ২০২৬); মজুরি প্রবৃদ্ধি ৭.৬৩% — প্রকৃত আয় কমছে | NEWS: BBS, Nov 2026 |
| inflation | মূল্যস্ফীতির শীর্ষ: জুলাই ২০২৪-এ ১১.৬৬%; খাদ্য মূল্যস্ফীতি তখন ১৪.১০% | MPS H1FY27, p.4 |
| inflation | FY27 বাজেট লক্ষ্য: GDP প্রবৃদ্ধি ৬.৫%, মূল্যস্ফীতি সীমা ৭.৫% | MPS H1FY27, Executive Summary |
| monetary | পলিসি রেট ১০% (অক্টোবর ২০২৪ থেকে অপরিবর্তিত); SLF ১১.৫%, SDF ৭.৫% — সংকোচনমূলক মুদ্রানীতি বহাল | MPS H1FY27 |
| monetary | বেসরকারি খাতে ঋণ প্রবৃদ্ধি মে ২০২৬-এ মাত্র ৫.০%; FY27 লক্ষ্য ৮.০% | MPS H1FY27 |
| monetary | সরকারি খাতে ঋণ প্রবৃদ্ধি জুন ২০২৬: ২৫.৯% — সরকার ব্যাংক থেকে বেশি ধার নিচ্ছে (crowding out) | MPS H1FY27, Table 4 |
| monetary | ব্যাংকিং খাতে উদ্বৃত্ত তারল্য ৩,২৭,৮৭৭ কোটি টাকা (মে ২০২৬) — অথচ বেসরকারি ঋণ কম | MPS H1FY27 |
| stimulus | ৬০,০০০ কোটি টাকার প্রণোদনা প্যাকেজ: ৪১,০০০ কোটি (ব্যাংকের উদ্বৃত্ত তারল্য) + ১৯,০০০ কোটি (BB-র নিজস্ব); ~২৫ লাখ কর্মসংস্থান লক্ষ্য | MPS H1FY27 |
| growth | প্রকৃত GDP প্রবৃদ্ধি: FY25 ৩.৪৯%, FY26 ৪.১৪% (সাময়িক); BB পূর্বাভাস FY27 ৬.১% | MPS H1FY27 (BBS) |
| npl | মোট খেলাপি ঋণের হার: ডিসেম্বর ২০২৪ ২০.২০% → সেপ্টেম্বর ২০২৫ ৩৫.৭৩% (শীর্ষ) → মার্চ ২০২৬ ৩২.২৬% | MPS H1FY27, Sec 4.2 |
| npl | নিট খেলাপি ঋণ মার্চ ২০২৬: ১৫.০১%; ঋণ পুনঃতফসিল সর্বোচ্চ ১০ বছর (২ বছর গ্রেস) | MPS H1FY27 |
| npl | IFRS 9-এর অধীনে ECL (Expected Credit Loss) পদ্ধতি পূর্ণ বাস্তবায়ন লক্ষ্য ২০২৭ | MPS H1FY27 |
| merger | ৫টি শরিয়াহভিত্তিক ব্যাংক একীভূত হয়ে রাষ্ট্রায়ত্ত 'সম্মিলিত ইসলামী ব্যাংক পিএলসি'; সরকারি মূলধন ২০,০০০ কোটি, মোট পরিশোধিত মূলধন ৩৫,০০০ কোটি টাকা | MPS H1FY27, Sec 4.3 |
| merger | ব্যাংক রেজল্যুশন অ্যাক্ট ২০২৬ ও আমানত সুরক্ষা অ্যাক্ট ২০২৬; আমানত বিমা সীমা ১ লাখ থেকে ২ লাখ টাকা | MPS H1FY27 |
| merger | ৩৫টি NBFI-এর মধ্যে ২০টি আর্থিক চাপে; ৯টির মূলধন ঘাটতি তীব্র — রেজল্যুশন প্রক্রিয়া শুরু | MPS H1FY27 |
| external | রেমিট্যান্স জুলাই–মে FY26: ৩২.৭৫ বিলিয়ন ডলার (+১৯.০৭%) | MPS H1FY27 |
| external | FY27-এ (জুলাই–১৬ নভেম্বর ২০২৬) রেমিট্যান্স ১৩.৪৩ বিলিয়ন ডলার (+১৩.৪%) | NEWS: Bangladesh Bank data via UNB, Nov 2026 |
| external | রপ্তানি আয় জুলাই–মে FY26: ৩৯.৮ বিলিয়ন ডলার (−১.৬৭%); RMG ≈ ৮০% রপ্তানি, কমেছে ২.৬১% | MPS H1FY27 |
| external | আমদানি ব্যয় জুলাই–এপ্রিল FY26: ৬১.৬২ বিলিয়ন ডলার (+৫.৯২%); এপ্রিলে +২১.৪২% (জ্বালানি, LNG, সার) | MPS H1FY27 |
| external | গ্রস রিজার্ভ (BPM6) ২৮ জুন ২০২৬: ৩১.৭৪ বিলিয়ন ডলার (জুন ২০২৫: ২৬.৭৪); নভেম্বরের শুরুতে ACU পরিশোধের পর ৩০ বিলিয়নের নিচে | MPS H1FY27 + NEWS Nov 2026 |
| external | BB FY26-এ নিলামে বাজার থেকে নিট ৬.৪৩ বিলিয়ন ডলার কিনেছে; বিনিময় হার ~১২৩ টাকা/ডলার (স্থিতিশীল) | MPS H1FY27 |
| external | চলতি হিসাবের ঘাটতি জুলাই–এপ্রিল FY26: ১.০৭ বিলিয়ন ডলার; সামগ্রিক BoP উদ্বৃত্ত ৩.৭৪ বিলিয়ন | MPS H1FY27 |
| ldc | জাতিসংঘ সাধারণ পরিষদ বাংলাদেশের এলডিসি উত্তরণ ৩ বছর পিছিয়ে ২৪ নভেম্বর ২০২৯ করেছে (প্রস্তাব গৃহীত অক্টোবর ২০২৬; নেপালও একই সুবিধা) | NEWS: bdnews24 30 Oct 2026; Prothom Alo English |
| ldc | উত্তরণের পর বছরে ১৭.৫ বিলিয়ন ডলারের বেশি রপ্তানি ঝুঁকিতে পড়তে পারে (জাতিসংঘের মূল্যায়ন) | NEWS |
| energy | ২০২৬-এ ডিজেলের দাম: এপ্রিলে ১০০→১১৫, সেপ্টেম্বরে ১১৫→১৩৫ টাকা/লিটার (পেট্রোল ১৬০); কারণ মধ্যপ্রাচ্য যুদ্ধ, হরমুজ প্রণালীতে বিঘ্ন | NEWS: Dhaka Tribune/bdnews24/Reuters, Sep–Oct 2026 |
| energy | ডিজেল মোট জ্বালানি তেল ব্যবহারের ~৬৬%; কৃষি সেচ ও পরিবহন খরচে সরাসরি প্রভাব | NEWS |
| digital | 'বাংলা QR' — জাতীয় ইন্টারঅপারেবল QR মান; সব ক্লোজড-লুপ QR ৩০ জুন ২০২৬-এর মধ্যে বাংলা QR-এ রূপান্তর বাধ্যতামূলক | MPS H1FY27, Sec 4.6 |
| digital | গেটস ফাউন্ডেশনের সাথে MoU: Instant Interoperable Payment System (IIPS) চালু লক্ষ্য জুন ২০২৭; CBDC পর্যবেক্ষণে | MPS H1FY27 |
| digital | স্টুডেন্ট ব্যাংকিং নীতিমালা ফেব্রুয়ারি ২০২৬ (২৫ বছর পর্যন্ত); ডিজিটাল ন্যানো লোন স্কিম জুন ২০২৮ পর্যন্ত | MPS H1FY27 |
| inclusion | ২০২৫-এ ৫,৫৩১টি আর্থিক সাক্ষরতা প্রশিক্ষণ, ২.৮৫ লাখ মানুষ; ২০২৬ লক্ষ্য ৫,৮১৮টি | MPS H1FY27 |
| social | সামাজিক সুরক্ষায় 'ফ্যামিলি কার্ড' ও 'কৃষক কার্ড' চালু | MPS H1FY27, Foreword |
| policy | সরকারের '৩R কৌশল': Recovery & Stabilization, Restoration, Reconstruction for Acceleration (FY27 বাজেট) | MPS H1FY27, Sec 2.2 |
| global | IMF (এপ্রিল ২০২৬): বৈশ্বিক প্রবৃদ্ধি ২০২৫-এ ৩.৪%, ২০২৬-এ ৩.১%; বৈশ্বিক মূল্যস্ফীতি ৪.৪% (২০২৬) | MPS H1FY27, Sec 3 |
