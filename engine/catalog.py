"""
রিসোর্স ক্যাটালগ — রিপোর ১টি মাত্র সত্য উৎস (single source of truth)।
প্রতিটি PDF: নতুন পাথ, মূল নাম চেনার প্যাটার্ন, বাংলা শিরোনাম, কোন পরীক্ষা-অংশ কাভার করে,
অগ্রাধিকার (1 = সবচেয়ে জরুরি, 3 = সময় থাকলে), এবং ব্যবহারের কৌশল।

section কোড (নতুন ২০০ নম্বরের কাঠামো — নোটিশে মিলিয়ে নিন):
  FW_BN  = ফোকাস রাইটিং বাংলা (৩০)
  FW_EN  = ফোকাস রাইটিং ইংরেজি (৩০)
  ARG    = অ্যানালিটিক্যাল/আর্গুমেন্টেটিভ রাইটিং (৪০)
  TR     = অনুবাদ বাংলা→ইংরেজি (২০)
  MATH   = গণিত (৩০)
  GK     = সাধারণ জ্ঞান + ব্যাংকিং (১০)
  ENG    = ইংরেজি গ্রামার (রচনার ভাষা ঠিক রাখতে)
  META   = প্রশ্ন বিশ্লেষণ / মডেল টেস্ট
"""

M = "materials"
NEW = "📑New Bank Written PDF"

# (match_dir, match_substring, new_relative_path, title_bn, sections, priority, lang, strategy)
CATALOG = [
    # ───────────── 01 ফোকাস রাইটিং: বই ─────────────
    (".", "Unique Bank Focus Writing", f"{M}/01_focus_writing/books/Unique_Bank_Focus_Writing_and_Essay.pdf",
     "ইউনিক ব্যাংক ফোকাস রাইটিং ও রচনা (৪২৭ পৃষ্ঠা, স্ক্যান)", ["FW_BN", "FW_EN", "TR"], 2, "bn+en",
     "পুরো বই নয়। engine দিয়ে টপিক সার্চ করে শুধু সম্ভাব্য ৮ টপিকের অধ্যায় পড়ুন।"),
    (".", "Focus Writting A2B", f"{M}/01_focus_writing/books/A2B_Focus_Writing.pdf",
     "A2B পাবলিকেশন্স ফোকাস রাইটিং (২৩৮ পৃষ্ঠা, স্ক্যান)", ["FW_BN", "FW_EN", "TR"], 2, "bn+en",
     "বাংলা-ইংরেজি জোড়া রচনা থাকলে অনুবাদ অনুশীলনে ব্যবহার করুন (বাংলা পড়ে ইংরেজি ঢেকে নিজে লিখুন)।"),
    (NEW, "Mini PDF", f"{M}/01_focus_writing/books/Focus_Writing_Mini_Recent_Merged.pdf",
     "ফোকাস রাইটিং মিনি PDF (সাম্প্রতিক, ১৯১ পৃষ্ঠা) — ১ নম্বর রচনা-উৎস", ["FW_BN", "FW_EN", "TR"], 1, "bn+en",
     "এটাই মূল ফোকাস বই। প্রতিটি টপিক থেকে উপশিরোনাম + ৫টি তথ্য + ৫টি সমাধান নোট করুন।"),
    (NEW, "July Edition", f"{M}/01_focus_writing/books/Focus_Writing_July_Edition.pdf",
     "ফোকাস রাইটিং জুলাই সংস্করণ (২৪ পৃষ্ঠা)", ["FW_EN", "FW_BN"], 2, "bn+en",
     "এক বসায় চোখ বুলিয়ে টপিক তালিকা আর ডেটা বক্স টুকে নিন।"),

    # ───────────── 01 ফোকাস রাইটিং: কৌশল ─────────────
    (NEW, "_PDF_No_02_Informative_Focus", f"{M}/01_focus_writing/technique/PDF02_Informative_Focus_Writing_Technique.pdf",
     "ইনফরমেটিভ ফোকাস ও ফ্রি-হ্যান্ড রাইটিং কৌশল", ["FW_BN", "FW_EN"], 1, "bn",
     "প্রথম দিনেই একবার পুরো পড়ুন: ইন্ট্রো, কোটেশন, ডেটা বক্স, উপশিরোনাম কাঠামো।"),
    (NEW, "_PDF_No_03_Informative_Focus_&_Free_Hand_Writing_Technique_Sheet.pdf", f"{M}/01_focus_writing/technique/PDF03_Informative_Focus_Writing_Technique_v2.pdf",
     "ইনফরমেটিভ ফোকাস কৌশল (সংস্করণ ২)", ["FW_BN", "FW_EN"], 3, "bn",
     "PDF02-এর প্রায় একই; শুধু PDF02 পড়লেই যথেষ্ট।"),
    (NEW, "_PDF_No_18_", f"{M}/01_focus_writing/technique/PDF18_Quotations_for_Focus_Writing.pdf",
     "ফোকাস রাইটিংয়ের জন্য কোটেশন (বাংলা/ইংরেজি)", ["FW_BN", "FW_EN"], 1, "bn+en",
     "১০টি কোটেশন মুখস্থ: ৪টি অর্থনীতি, ২টি ব্যাংকিং, ২টি পরিবেশ, ২টি প্রযুক্তি।"),

    # ───────────── 01 ফোকাস রাইটিং: অর্থনীতি টপিক ─────────────
    (NEW, "_PDF_No_27_", f"{M}/01_focus_writing/topics_economy/PDF27_Inflation_Govt_CentralBank_Role_Bn.pdf",
     "মূল্যস্ফীতি নিয়ন্ত্রণে সরকার ও কেন্দ্রীয় ব্যাংকের ভূমিকা", ["FW_BN", "FW_EN", "ARG"], 1, "bn", "টপিক #১ — অবশ্যই।"),
    (NEW, "_PDF_No_39_", f"{M}/01_focus_writing/topics_economy/PDF39_Price_Hike_Ways_to_Overcome.pdf",
     "দ্রব্যমূল্যের ঊর্ধ্বগতি ও উত্তরণের উপায়", ["FW_BN", "FW_EN"], 1, "bn+en", "মূল্যস্ফীতির সাথে একসাথে পড়ুন।"),
    (NEW, "_PDF_No_28_", f"{M}/01_focus_writing/topics_economy/PDF28_LDC_Graduation_Bn.pdf",
     "এলডিসি উত্তরণ: সমস্যা ও সম্ভাবনা", ["FW_BN", "FW_EN", "ARG"], 1, "bn",
     "টপিক #২। সতর্কতা: PDF-এ সাল ২০২৬ লেখা — সাম্প্রতিক খবর অনুযায়ী আপডেট করে লিখুন (docs দেখুন)।"),
    (NEW, "_PDF_No_52_", f"{M}/01_focus_writing/topics_economy/PDF52_Reserve_Crisis_Bn.pdf",
     "রিজার্ভ সংকটে বাংলাদেশ: কারণ ও উত্তরণ", ["FW_BN", "FW_EN"], 1, "bn", "রেমিট্যান্স/হুন্ডি/ডলার টপিকে কাজে লাগবে।"),
    (NEW, "_PDF_No_53_", f"{M}/01_focus_writing/topics_economy/PDF53_Dollar_Crisis_Bn.pdf",
     "ডলার সংকটে বাংলাদেশ: কারণ ও উত্তরণ", ["FW_BN", "FW_EN"], 2, "bn", "PDF52-এর সাথে মিলিয়ে একটি নোট বানান।"),
    (NEW, "PDF No-40_", f"{M}/01_focus_writing/topics_economy/PDF40_Remittance_Driving_Force_En.pdf",
     "Remittance: The Driving Force of Our Economy", ["FW_EN", "FW_BN"], 1, "en", "টপিক #৬ (রেমিট্যান্স ও হুন্ডি)।"),
    (NEW, "_PDF_No_25_", f"{M}/01_focus_writing/topics_economy/PDF25_Foreign_Debt_IMF_Loan_Bn.pdf",
     "বাংলাদেশের বৈদেশিক ঋণ ও IMF লোন", ["FW_BN", "ARG"], 2, "bn", "আর্গুমেন্টের তথ্য-উৎস।"),
    (NEW, "_PDF_No_51_", f"{M}/01_focus_writing/topics_economy/PDF51_RMG_Sector_Prospects_Challenges.pdf",
     "RMG খাত: সম্ভাবনা ও চ্যালেঞ্জ", ["FW_EN", "FW_BN"], 1, "bn+en", "টপিক #৫ (রপ্তানি বহুমুখীকরণ)।"),
    (NEW, "_PDF_No_23_", f"{M}/01_focus_writing/topics_economy/PDF23_Bottomless_Basket_to_Rising_Economy.pdf",
     "Bangladesh: From Bottomless Basket to Rising Economy", ["FW_EN"], 2, "en", "সাধারণ অর্থনীতি রচনার ইন্ট্রো/ডেটা।"),
    (NEW, "PDF No-57_", f"{M}/01_focus_writing/topics_economy/PDF57_Inclusive_Development_En.pdf",
     "Inclusive Development & Bangladesh", ["FW_EN"], 2, "en", "আর্থিক অন্তর্ভুক্তি টপিকে কাজে লাগে।"),
    (NEW, "_PDF_No_22_", f"{M}/01_focus_writing/topics_economy/PDF22_Rural_Development_Poverty_En.pdf",
     "Rural Development and Poverty Reduction (BB Officer প্রশ্ন)", ["FW_EN"], 2, "en", "আগে প্রশ্ন এসেছে — কাঠামো দেখুন।"),
    (NEW, "_PDF_No_26_", f"{M}/01_focus_writing/topics_economy/PDF26_Ukraine_War_Impact_on_BD_Economy_Bn.pdf",
     "বাংলাদেশের অর্থনীতিতে ইউক্রেন-রাশিয়া যুদ্ধের প্রভাব", ["FW_BN"], 3, "bn", "পুরোনো; শুধু 'বৈশ্বিক সংকট' অংশের তথ্য নিন।"),
    (NEW, "_PDF_No_58_", f"{M}/01_focus_writing/topics_economy/PDF58_Global_Impact_Russia_Ukraine_En.pdf",
     "Global Impact of Russia-Ukraine Conflict", ["FW_EN"], 3, "en", "পুরোনো; জ্বালানি তেলের দাম টপিকে ২-৩টি লাইন।"),
    (NEW, "PDF No-24_", f"{M}/01_focus_writing/topics_economy/PDF24_Smart_Bangladesh_2041_En.pdf",
     "Smart Bangladesh: Vision 2041", ["FW_EN"], 3, "en", "রাজনৈতিক প্রেক্ষাপট বদলেছে; শুধু ডিজিটাল অবকাঠামো তথ্য নিন।"),
    (NEW, "_PDF_No_54_", f"{M}/01_focus_writing/topics_economy/PDF54_Mega_Projects_Bn.pdf",
     "উন্নয়নের অগ্রযাত্রায় মেগাপ্রকল্পসমূহ", ["FW_BN", "GK"], 3, "bn", "GK-এর জন্য প্রকল্পের নাম/ব্যয়/দৈর্ঘ্য।"),
    (NEW, "_PDF_No_41_", f"{M}/01_focus_writing/topics_economy/PDF41_Padma_Bridge_Bn.pdf",
     "অর্থনৈতিক উন্নয়নে পদ্মা সেতুর গুরুত্ব", ["FW_BN", "GK"], 3, "bn", "সময় না থাকলে বাদ।"),
    (NEW, "_PDF_No_38_", f"{M}/01_focus_writing/topics_economy/PDF38_Karnaphuli_Tunnel_En.pdf",
     "Socio-Economic Impacts of Karnaphuli Tunnel", ["FW_EN", "GK"], 3, "en", "সময় না থাকলে বাদ।"),
    (NEW, "_PDF_No_43_", f"{M}/01_focus_writing/topics_economy/PDF43_Universal_Pension_Social_Safety_Bn.pdf",
     "সর্বজনীন পেনশন ও সামাজিক সুরক্ষা", ["FW_BN"], 3, "bn", "সামাজিক সুরক্ষা প্রশ্ন এলে।"),

    # ───────────── 01 ফোকাস রাইটিং: ব্যাংকিং টপিক ─────────────
    (NEW, "_PDF_No_55_", f"{M}/01_focus_writing/topics_banking/PDF55_Default_Loans_Banking_Sector_En.pdf",
     "Default Loans: Cancer for the Banking Sector", ["FW_EN", "FW_BN", "ARG"], 1, "en", "টপিক #৪ (খেলাপি ঋণ ও একীভূতকরণ) — অবশ্যই।"),
    (NEW, "_PDF_No_56_", f"{M}/01_focus_writing/topics_banking/PDF56_Good_Governance_Banking_En.pdf",
     "Good Governance in Banking Sector", ["FW_EN", "ARG"], 1, "en", "খেলাপি ঋণের সাথে জোড়া।"),
    (NEW, "_PDF_No_04_Establishment", f"{M}/01_focus_writing/topics_banking/PDF04_Digital_Bank_Prospects_Challenges_En.pdf",
     "Digital Bank: Prospects & Challenges", ["FW_EN", "FW_BN"], 1, "en", "টপিক #৭ (AI ও ডিজিটাল ব্যাংকিং)।"),
    (NEW, "_PDF_No_10_", f"{M}/01_focus_writing/topics_banking/PDF10_IT_Impact_on_Banking_En.pdf",
     "Impacts of IT on Banking Sector", ["FW_EN"], 2, "en", "ডিজিটাল ব্যাংকিংয়ের সাথে।"),
    (NEW, "_PDF_No_05_", f"{M}/01_focus_writing/topics_banking/PDF05_MFS_Cashless_Financial_Inclusion_En.pdf",
     "MFS to Cashless Society for Financial Inclusion", ["FW_EN", "FW_BN"], 2, "en", "আর্থিক অন্তর্ভুক্তি/ক্যাশলেস।"),
    (NEW, "_PDF_No_37_", f"{M}/01_focus_writing/topics_banking/PDF37_TakaPay_Cashless_Bn.pdf",
     "টাকা পে কার্ড ও ক্যাশলেস বাংলাদেশ", ["FW_BN", "GK"], 3, "bn", "GK: টাকা পে, NPSB।"),

    # ───────────── 01 ফোকাস রাইটিং: পরিবেশ/সামাজিক ─────────────
    (NEW, "_PDF_No_09_", f"{M}/01_focus_writing/topics_environment_social/PDF09_Climate_Change_Bangladesh_Bn.pdf",
     "জলবায়ু পরিবর্তন ও বাংলাদেশ", ["FW_BN", "FW_EN"], 1, "bn", "টপিক #৮ (জলবায়ু অর্থায়ন ও গ্রিন ব্যাংকিং)।"),
    (NEW, "_PDF_No_08_COP_27_BD_&_Global_Environment_পরিবেশ_বিষয়ক_যে_কোন_লেখার.pdf", f"{M}/01_focus_writing/topics_environment_social/PDF08_COP27_Global_Environment.pdf",
     "COP27, বাংলাদেশ ও বৈশ্বিক পরিবেশ", ["FW_EN", "FW_BN"], 2, "bn+en", "COP তথ্য পুরোনো — সর্বশেষ COP হালনাগাদ করুন।"),
    (NEW, "_PDF_No_21_", f"{M}/01_focus_writing/topics_environment_social/PDF21_Women_Empowerment_En.pdf",
     "Women Empowerment and Bangladesh", ["FW_EN"], 2, "en", "নারী উদ্যোক্তা/এসএমই প্রশ্নে।"),

    # ───────────── 02 আর্গুমেন্ট ─────────────
    (NEW, "Argument Writing Technique Sheet-1", f"{M}/02_argument_writing/Argument_Writing_Technique_Sheet_1.pdf",
     "আর্গুমেন্ট রাইটিং কৌশল শিট-১", ["ARG"], 1, "bn+en", "৪০ নম্বরের কাঠামো এখান থেকে। প্রথম দিনেই পড়ুন।"),
    (NEW, "PDF No-48_", f"{M}/02_argument_writing/PDF48_Argumentative_Writing_Technique_2.pdf",
     "আর্গুমেন্টেটিভ রাইটিং কৌশল-২ (নমুনা উত্তরসহ)", ["ARG"], 1, "bn+en", "নমুনা উত্তর থেকে ১০টি transition phrase তুলুন।"),

    # ───────────── 03 গণিত ─────────────
    (".", "Bank Written Math 1986-2021", f"{M}/03_math/question_bank/Bank_Written_Math_1986-2021.pdf",
     "ব্যাংক লিখিত গণিত ১৯৮৬–২০২১ (৫৭৭ পৃষ্ঠা, অধ্যায়ভিত্তিক বিগত প্রশ্ন)", ["MATH"], 1, "en", "গণিতের প্রশ্নব্যাংক। engine `math` কমান্ড দিয়ে অধ্যায় ধরে ড্রিল।"),
    (NEW, "BIBM_Previous_All_Written_Math", f"{M}/03_math/question_bank/BIBM_Previous_All_Written_Math_Solution.pdf",
     "BIBM বিগত সব লিখিত গণিত সমাধান (জাফর ইকবাল আনসারী)", ["MATH"], 1, "en", "সাম্প্রতিক BIBM প্রশ্ন — প্রথমে এগুলো নিজে করুন, পরে মিলান।"),
    ("Khairul bank written", "Percentage", f"{M}/03_math/khairul/01_Percentage.pdf", "খায়রুল: শতকরা", ["MATH"], 1, "en", "অধ্যায় ১ — শতকরা ভিত্তি।"),
    ("Khairul bank written", "Algebra", f"{M}/03_math/khairul/02_Algebra.pdf", "খায়রুল: বীজগণিত/সমীকরণ", ["MATH"], 1, "en", "সমীকরণ গঠন — সবচেয়ে বেশি আসে।"),
    ("Khairul bank written", "Time-Work", f"{M}/03_math/khairul/03_Time_Work.pdf", "খায়রুল: সময় ও কাজ", ["MATH"], 2, "en", ""),
    ("Khairul bank written", "Time & Speed", f"{M}/03_math/khairul/04_Time_Speed.pdf", "খায়রুল: সময় ও গতি", ["MATH"], 2, "en", ""),
    ("Khairul bank written", "Arithmetic-Progression", f"{M}/03_math/khairul/05_Arithmetic_Progression.pdf", "খায়রুল: সমান্তর ধারা", ["MATH"], 1, "en", ""),
    ("Khairul bank written", "Mixture", f"{M}/03_math/khairul/06_Mixture.pdf", "খায়রুল: মিশ্রণ", ["MATH"], 2, "en", ""),
    ("Khairul bank written", "Boat", f"{M}/03_math/khairul/07_Boat_Stream.pdf", "খায়রুল: নৌকা ও স্রোত", ["MATH"], 3, "en", ""),
    ("Khairul bank written", "Unitary", f"{M}/03_math/khairul/08_Unitary_Method.pdf", "খায়রুল: ঐকিক নিয়ম", ["MATH"], 3, "en", ""),
    (NEW, "PDF No-45_", f"{M}/03_math/topic_sheets/PDF45_Profit_Loss.pdf", "লাভ-ক্ষতি (৫১ পৃষ্ঠা)", ["MATH"], 1, "en", ""),
    (NEW, "_PDF No-16_", f"{M}/03_math/topic_sheets/PDF16_Formation_of_Equation.pdf", "সমীকরণ গঠন", ["MATH"], 1, "en", ""),
    (NEW, "_PDF No-14_", f"{M}/03_math/topic_sheets/PDF14_Compound_Interest.pdf", "চক্রবৃদ্ধি মুনাফা", ["MATH"], 1, "en", "ব্যাংক পরীক্ষার প্রিয় — সূত্র মুখস্থ।"),
    (NEW, "PDF No-30_", f"{M}/03_math/topic_sheets/PDF30_Ratio_Proportion.pdf", "অনুপাত-সমানুপাত", ["MATH"], 2, "en", ""),
    (NEW, "PDF No-31_", f"{M}/03_math/topic_sheets/PDF31_Partnership.pdf", "অংশীদারি কারবার", ["MATH"], 2, "en", ""),
    (NEW, "PDF No-32_", f"{M}/03_math/topic_sheets/PDF32_Probability.pdf", "সম্ভাবনা", ["MATH"], 2, "en", ""),
    (NEW, "PDF No-33_", f"{M}/03_math/topic_sheets/PDF33_Geometry.pdf", "জ্যামিতি/ক্ষেত্রফল", ["MATH"], 1, "en", ""),
    (NEW, "PDF No-46_", f"{M}/03_math/topic_sheets/PDF46_Time_Work.pdf", "সময় ও কাজ (৬৪ পৃষ্ঠা)", ["MATH"], 3, "en", "খায়রুলের Time-Work থাকলে এটা বাদ।"),
    (NEW, "PDF No-60_", f"{M}/03_math/topic_sheets/PDF60_Mixture.pdf", "মিশ্রণ", ["MATH"], 3, "en", ""),
    (NEW, "PDF No-61_", f"{M}/03_math/topic_sheets/PDF61_Time_Speed_Distance.pdf", "সময়, গতি ও দূরত্ব", ["MATH"], 3, "en", ""),
    (NEW, "PDF No-62_", f"{M}/03_math/topic_sheets/PDF62_Problem_on_Train.pdf", "ট্রেন সংক্রান্ত অঙ্ক", ["MATH"], 3, "en", ""),

    # ───────────── 04 ইংরেজি ─────────────
    (".", "Class-9-10 English Grammar", f"{M}/04_english/Class_9-10_English_Grammar_NCTB.pdf",
     "NCTB ৯ম-১০ম ইংরেজি গ্রামার", ["ENG", "TR"], 2, "en", "শুধু Right form of verb, Subject-verb agreement, Narration, Transformation।"),
    (NEW, "_PDF_No_34_", f"{M}/04_english/comprehension_legacy/PDF34_Comprehension_Technique.pdf",
     "কম্প্রিহেনশন কৌশল (পুরোনো সিলেবাস)", ["META"], 3, "bn+en", "নতুন কাঠামোয় কম্প্রিহেনশন নেই বলে জানা গেছে — নোটিশে থাকলে তবেই পড়ুন।"),
    (NEW, "_PDF_No_02_Comprehension", f"{M}/04_english/comprehension_legacy/PDF02_Comprehension_Technique_Old.pdf",
     "কম্প্রিহেনশন কৌশল (পুরোনো সংস্করণ)", ["META"], 3, "bn+en", "বাদ।"),

    # ───────────── 05 GK ও ব্যাংকিং ─────────────
    (NEW, "GK Banking Terminologies", f"{M}/05_gk_banking/GK_Banking_Terminologies_1_2.pdf",
     "ব্যাংকিং পরিভাষা ১ ও ২", ["GK"], 1, "bn+en", "প্রতিদিন ১০–১৫টি পরিভাষা: পূর্ণরূপ + ১ লাইনের সংজ্ঞা।"),
    (NEW, "_PDF_No_12_How_to_Face_Written_GK_Previous_All_Bank_Written_GK.pdf", f"{M}/05_gk_banking/PDF12_Previous_All_Bank_Written_GK.pdf",
     "বিগত সব ব্যাংক লিখিত GK + কৌশল", ["GK"], 1, "bn+en", "বিগত লিখিত GK — একবার পড়ে ভুলগুলো টুকে রাখুন।"),
    (NEW, "GK Practice Sheet-1", f"{M}/05_gk_banking/GK_Practice_Sheet_1.pdf", "GK প্র্যাকটিস শিট-১", ["GK"], 2, "bn+en", ""),
    (NEW, "_PDF_No_35_", f"{M}/05_gk_banking/PDF35_Recent_GK.pdf", "সাম্প্রতিক GK (BB AD)", ["GK"], 2, "bn+en", "সাল/তথ্য পুরোনো হতে পারে — যাচাই করুন।"),
    (NEW, "_PDF_No_49_", f"{M}/05_gk_banking/PDF49_Selected_GK.pdf", "নির্বাচিত GK (BB AD)", ["GK"], 3, "bn+en", ""),
    (NEW, "_PDF_No_50_", f"{M}/05_gk_banking/PDF50_Sports_GK.pdf", "খেলাধুলা GK", ["GK"], 3, "bn+en", "বাদ দিলেও ক্ষতি কম।"),

    # ───────────── 06 প্রশ্ন বিশ্লেষণ ও মডেল টেস্ট ─────────────
    (NEW, "_PDF_No_01_Recent_BIBM", f"{M}/06_question_analysis_model_tests/PDF01_BIBM_Question_Analysis.pdf",
     "BIBM বিগত প্রশ্ন বিশ্লেষণ (মার্কস বণ্টন ও টপিক)", ["META"], 1, "bn+en", "প্রথম দিনে পড়ুন — প্রশ্নকর্তার মন বোঝা।"),
    (NEW, "MT-01.pdf", f"{M}/06_question_analysis_model_tests/MT01_Question.pdf", "মডেল টেস্ট-০১ (প্রশ্ন)", ["META"], 1, "en", "মক পরীক্ষা-১ (দিন ৫)।"),
    (NEW, "46 BCS Analysis Report-1", f"{M}/06_question_analysis_model_tests/MT01_Solution_Analysis.pdf", "মডেল টেস্ট-০১ (সমাধান ও বিশ্লেষণ)", ["META"], 1, "bn+en", "মক-১ শেষে মিলান।"),
    (NEW, "BB AD Wtitten MT-02", f"{M}/06_question_analysis_model_tests/MT02_Question.pdf", "মডেল টেস্ট-০২ (প্রশ্ন)", ["META"], 1, "en", "মক পরীক্ষা-২ (দিন ৭)।"),
    (NEW, "BB AD Written Model Test-2", f"{M}/06_question_analysis_model_tests/MT02_Solution_Analysis.pdf", "মডেল টেস্ট-০২ (সমাধান ও বিশ্লেষণ)", ["META"], 1, "bn+en", "মক-২ শেষে মিলান।"),

    # ───────────── 07 অফিসিয়াল রিপোর্ট ─────────────
    (".", "mps_h1fy27", f"{M}/07_official_reports/BB_Monetary_Policy_Statement_H1FY27.pdf",
     "বাংলাদেশ ব্যাংক মুদ্রানীতি বিবৃতি H1 FY27 (সর্বশেষ)", ["FW_BN", "FW_EN", "ARG", "GK"], 1, "en",
     "রচনার সর্বশেষ সংখ্যা এখান থেকে: মূল্যস্ফীতি, পলিসি রেট, রিজার্ভ, ঋণ প্রবৃদ্ধি। engine `facts` কমান্ড দেখুন।"),
]

# পাঠ্যগতভাবে হুবহু ডুপ্লিকেট (টেক্সট হ্যাশ মিলেছে) — রিপো থেকে সরানো হয়েছে
DUPLICATES = [
    (NEW, "_PDF_No_03_Informative_Focus_&_Free_Hand_Writing_Technique_Sheet (1).pdf"),
    (NEW, "_PDF_No_12_How_to_Face_Written_GK_Previous_All_Bank_Written_GK (1).pdf"),
    (NEW, "_PDF_No_04_How_to_Face_Written_GK_Previous_All_Bank_Written_GK.pdf"),
    (NEW, "_PDF_No_08_COP_27_BD_&_Global_Environment_পরিবেশ_বিষয়ক_যে_কোন_লেখার (1).pdf"),
]

SECTION_NAMES = {
    "FW_BN": "ফোকাস রাইটিং (বাংলা)", "FW_EN": "ফোকাস রাইটিং (ইংরেজি)", "ARG": "আর্গুমেন্ট/অ্যানালিটিক্যাল",
    "TR": "অনুবাদ (বাংলা→ইংরেজি)", "MATH": "গণিত", "GK": "সাধারণ জ্ঞান ও ব্যাংকিং", "ENG": "ইংরেজি গ্রামার",
    "META": "প্রশ্ন বিশ্লেষণ/মডেল টেস্ট",
}
