<!-- স্বয়ংক্রিয়ভাবে তৈরি: engine/build_docs.py — সরাসরি এডিট না করে data/*.json বদলান -->

# ০৭ · গণিত প্লেবুক (৩০ নম্বর, সাধারণত ৫টি প্রশ্ন × ৬)

রিপোর গণিতের PDF থেকে **৯৭৮টি লিখিত প্রশ্ন** আলাদা করে অধ্যায়ভিত্তিক ব্যাংক বানানো হয়েছে (`data/math_bank.json`)।
নিচের টেবিলে **২০১৫ বা পরের পরীক্ষায় আসা প্রশ্নের সংখ্যা** অনুযায়ী অধ্যায় সাজানো আছে। এটাই পড়ার ক্রম।

| ক্রম | অধ্যায় | ব্যাংকে মোট | ২০১৫+ পরীক্ষায় | SO ট্যাগ | ড্রিল কমান্ড |
|---|---|---|---|---|---|
| ১ | সময় ও কাজ / নল-চৌবাচ্চা | ১৪১ | ৪৬ | ৮ | `so.py math work` |
| ২ | গতি, ট্রেন, নৌকা-স্রোত | ১১৭ | ৪৩ | ১৪ | `so.py math speed` |
| ৩ | লাভ-ক্ষতি | ১১৭ | ৩৫ | ৬ | `so.py math profit_loss` |
| ৪ | বীজগণিত ও সমীকরণ | ১৩৯ | ৩৩ | ৮ | `so.py math algebra` |
| ৫ | শতকরা | ১১০ | ৩০ | ৬ | `so.py math percentage` |
| ৬ | অনুপাত ও অংশীদারি | ৯৬ | ২১ | ২ | `so.py math ratio` |
| ৭ | মিশ্রণ | ৪০ | ২০ | ১০ | `so.py math mixture` |
| ৮ | জ্যামিতি ও ক্ষেত্রফল | ৭৮ | ১৮ | ৩ | `so.py math geometry` |
| ৯ | সুদ (সরল ও চক্রবৃদ্ধি) | ৭৬ | ১৪ | ১ | `so.py math interest` |
| ১০ | ধারা | ১৯ | ৫ | ০ | `so.py math series` |
| ১১ | সম্ভাবনা ও বিন্যাস-সমাবেশ | ৩৬ | ৩ | ১ | `so.py math probability` |
| ১২ | গড় | ৬ | ৩ | ১ | `so.py math average` |
| ১৩ | বয়স | ৩ | ০ | ০ | `so.py math age` |

> গণনা স্বয়ংক্রিয়, OCR থেকে নেওয়া। পরীক্ষার ট্যাগ পড়া না গেলে প্রশ্নটা "২০১৫+" কলামে গোনা হয়নি। ধারাটা নির্ভরযোগ্য, তবে প্রতিটি সংখ্যা হুবহু ধরে নেবেন না।

## ৭ দিনের গণিত পরিকল্পনা (মোট ৬০টি অঙ্ক)

| দিন | অধ্যায় | উৎস | সংখ্যা |
|---|---|---|---|
| ১ | শতকরা + লাভ-ক্ষতি | `khairul/01_Percentage.pdf`, `topic_sheets/PDF45_Profit_Loss.pdf` | ১০ |
| ২ | বীজগণিত/সমীকরণ + বয়স | `khairul/02_Algebra.pdf`, `topic_sheets/PDF16_Formation_of_Equation.pdf` | ১০ |
| ৩ | সুদ + ধারা | `topic_sheets/PDF14_Compound_Interest.pdf`, `khairul/05_Arithmetic_Progression.pdf` | ১০ |
| ৪ | সময়-কাজ + গতি/ট্রেন + জ্যামিতি | `khairul/03_Time_Work.pdf`, `khairul/04_Time_Speed.pdf`, `topic_sheets/PDF33_Geometry.pdf` | ১০ |
| ৫ | মক + অনুপাত/মিশ্রণ | `topic_sheets/PDF30/31`, `khairul/06_Mixture.pdf` | ৮ |
| ৬ | BIBM সাম্প্রতিক মিশ্র (২০২২–২৩) | `question_bank/BIBM_Previous_All_Written_Math_Solution.pdf` | ১০ |
| ৭ | ভুলের খাতা + সূত্র | নিজের খাতা | ২–৪ |

## নিয়ম
- ক্যালকুলেটর ছাড়া, **প্রতিটি ধাপ লিখে** করবেন।
- ৬ মিনিটে না মিললে সমাধান দেখুন, তারপর পরদিন অঙ্কটা আবার নিজে করুন।
- ২০২৬ থেকে প্রশ্ন ইংরেজিতে আসছে, তাই প্রশ্নের শব্দ (per annum, alloy, cistern, downstream) চিনে রাখুন।
- উত্তর বক্স করুন আর একক লিখুন।

## সূত্র-শিট (পরীক্ষার আগের রাতে শুধু এটা)

| অধ্যায় | সূত্র / কৌশল |
|---|---|
| শতকরা | x% বৃদ্ধির পর y% হ্রাস → নিট পরিবর্তন = x − y − xy/100 · মূল্য x% বাড়লে ব্যবহার কমাতে হবে x/(100+x) × 100% |
| লাভ-ক্ষতি | লাভ% = লাভ/ক্রয়মূল্য × 100 · বিক্রয়মূল্য = ক্রয়মূল্য × (100 ± লাভ/ক্ষতি%)/100 · ছাড়: বিক্রয়মূল্য = লিখিত মূল্য × (100 − ছাড়%)/100 |
| সরল সুদ | I = Pnr/100 · A = P + I |
| চক্রবৃদ্ধি | A = P(1 + r/100)ⁿ · ষাণ্মাসিক হলে r/2, 2n · CI − SI (২ বছর) = P(r/100)² |
| অনুপাত/অংশীদারি | লাভ ভাগ ∝ মূলধন × সময় · a:b ও b:c থেকে a:b:c = ab' : bb' : bc' মিলিয়ে |
| সময় ও কাজ | ১ দিনে কাজ = 1/দিন · একসাথে: 1/A + 1/B · নল: ভরে (+), খালি করে (−) · M₁D₁H₁/W₁ = M₂D₂H₂/W₂ |
| গতি | দূরত্ব = গতি × সময় · km/h → m/s: ×5/18 · গড় গতি (সমান দূরত্ব) = 2xy/(x+y) · ট্রেন: অতিক্রম দূরত্ব = ট্রেন + প্ল্যাটফর্ম · বিপরীত দিকে আপেক্ষিক গতি = যোগফল, একই দিকে = বিয়োগফল |
| নৌকা-স্রোত | স্রোতের অনুকূলে = u + v, প্রতিকূলে = u − v · নৌকার বেগ = (অনুকূল + প্রতিকূল)/2 |
| মিশ্রণ | Alligation: (দামি − গড়) : (গড় − সস্তা) = সস্তা : দামি · বারবার তুলে প্রতিস্থাপন: বাকি = মোট × (1 − x/মোট)ⁿ |
| ধারা | n-তম পদ = a + (n−1)d · যোগফল = n/2 [2a + (n−1)d] · গুণোত্তর: arⁿ⁻¹, a(rⁿ−1)/(r−1) |
| জ্যামিতি | আয়তক্ষেত্র ক্ষেত্রফল = দৈর্ঘ্য × প্রস্থ, পরিসীমা = 2(l+b) · ত্রিভুজ = ½ভূমি×উচ্চতা, সমবাহু = √3/4 a² · বৃত্ত = πr², পরিধি = 2πr · পিথাগোরাস · ঘনক = a³, বেলন = πr²h |
| সম্ভাবনা | P = অনুকূল/মোট · nPr = n!/(n−r)! · nCr = n!/(r!(n−r)!) · "অন্তত একটি" = 1 − কোনোটিই না |
| গড় ও বয়স | গড় = যোগফল/সংখ্যা · নতুন সদস্য যোগ হলে গড়ের পরিবর্তন × মোট সংখ্যা · বয়সের অঙ্ক: বর্তমান বয়স x ধরে "n বছর আগে/পরে" সমীকরণ |


## সাম্প্রতিক (২০১৯+) ট্যাগযুক্ত প্রশ্ন (৪০টি): আগে এগুলো করুন

1. A man engaged a worker on the condition that he would pay him Tk. 30,000 and one uniform after one year of service. He served only for 9 months and got Tk. 22,000 and a uniform. What is the price of the uniform?  
   _[Combined 9 Banks Officer 23)] · work · BIBM_Previous_All_Written_Math_Solution p1_
2. The cost of 3 horses is same as the cost of 5 cows. If total cost of 4 horses and 6 cows is Tk. 1900, find the cost of one horse.  
   _[Combined 9 Banks Officer 23] · algebra · BIBM_Previous_All_Written_Math_Solution p1_
3. A man won a lottery of Tk. 20,00,000. He gave 5 of the amount to his wife and : of the balance to his son. He donated : of the balance amount. How much money was donated?  
   _[Combined 9 Banks Officer 23] · algebra · BIBM_Previous_All_Written_Math_Solution p1_
4. A square and an equilateral triangle have equal perimeters. If the diagonal of the square is 12V2 cm, then what is the area of the triangle?  
   _[Combined 9 Banks Officer 23] · geometry · BIBM_Previous_All_Written_Math_Solution p2_
5. A bag contains coins of Tk. 1, Tk. 2, and Tk. 5 denomination in the ratio 2: 3: 4. If the total amount is Tk. 280, find the number of coins of Tk. 5 denomination in the bag.  
   _[Combined 9 Bunks SO 23] · ratio · BIBM_Previous_All_Written_Math_Solution p2_
6. A father has divided his property between his two sons A and B. A invests the amount at a compound profit of 8% p. a. B invests the amount of 10% p. a. simple profit. At the end of 2 years, the profit received by B is Taka 1336 more than the interest received by A. Find A’s share in the father’s property of Taka 25000. Exam Aid Bank Previous Written Math Solution Page 8  
   _[Midland Bank MTO 15, SIBL PO 13, BB AME 23] · profit_loss · BIBM_Previous_All_Written_Math_Solution p3_
7. The percentage profit earned by selling an article for Tk. 1920 is equal to the percentage loss incurred by selling the same article for Tk. 1280. At what price should the article be sold to make 25% profit?  
   _[South East Bank MTO 13, BB ১017) 15, SJIB MTO 13, IBBL PO 19, BB AME 23] · profit_loss · BIBM_Previous_All_Written_Math_Solution p4_
8. AD is the longest side of the right triangle ABD shown in the figure. What is the length of longest side of AABC?  
   _[SIBL PO 13, BB AME 23)] · geometry · BIBM_Previous_All_Written_Math_Solution p5_
9. Monthly income of two persons are in the ratio 5: 4 and their monthly expenditures are in the ratio 9: 7, If each saves Tk. 500 per month, then what are their monthly incomes?  
   _[68 AD(Research) 23] · ratio · BIBM_Previous_All_Written_Math_Solution p5_
10. One man wanted to fence one side of his garden. If he uses posts 6 feet apart, the ends and start of the side ends with posts. If he buys certain no of posts from market they are 5 less than required. If the posts are 8 feet apart then no of posts brought satisfied the requirements. What is the length of the garden? How many posts were brought?  
   _[Bb AD(Research) 23] · geometry · BIBM_Previous_All_Written_Math_Solution p5_
11. A team of 2 men and 5 women completed 1/4" of a job in 3 days. After that another man joined them and they all complete the next 1/4" of the job in 2days. How many men can complete the whole job in 4 days? / / 8 ?  
   _[BB AD 14, PKSF AM 09, NCC Bank Officer 02, One Bank SCO 18, NRB Bank MTO 19, BB AD(Research) 23] · work · BIBM_Previous_All_Written_Math_Solution p6_
12. If x is an integer and x ++ =~, then value of x - ~?  
   _[BB AP 23] · algebra · BIBM_Previous_All_Written_Math_Solution p7_
13. In the given figure, PTO is an right triangle, then what is the area of square QRST.  
   _[BB AP 23) R  Q 5 Ss P 5 T] · geometry · BIBM_Previous_All_Written_Math_Solution p7_
14. A basketball team has won 15 games and lost 9. If these games represent 165% of the games to be played, then how many more games must the team win to average 75% for the season?  
   _[ONE Bank PO 10, NCC Bank MTO 11, Premier Bank MTO 12, Midland Bank TO 15, BB  AP 23)] · percentage · BIBM_Previous_All_Written_Math_Solution p7_
15. Students of a class are made to stand in rows. If students are extra in each row, then there would be 2 rows less. If four students are less in each row, then there would be 4 more rows. What is the number of students in the class?  
   _[BB AP 23] · algebra · BIBM_Previous_All_Written_Math_Solution p8_
16. Taxi fare is described by the following relationship: Total taxi Fare = Fixed Charge: Tk. A up to 2 km + Tk. B per km run exceeding 2 km + Tk. 60 for per hours waiting A person paid Tk. 432 for running 52 km and 2 hours of waiting charge. The same person paid Tk. 732 for running 102 km and 2 hours of waiting charge. Find the value of A and B.  
   _[S11B MTO 10, BB Officer(Electrical) 23] · algebra · BIBM_Previous_All_Written_Math_Solution p8_
17. A trader bought some mangoes for Tk. 150 per dozen and equal number of apples for Tk. 100 per dozen. If he sells all the fruits Tk. 140 per dozen, what will be his profit/oss in percentage?  
   _[BASIC Bank PO 99, RAKUB SO 14, SIIB MTO 10, BB Officer(Electrical) 23] · profit_loss · BIBM_Previous_All_Written_Math_Solution p9_
18. The figure shows a circular flowerbed, with its center at O having radius of 8 feet. The flowerbed is surrounded by a circular path, which is 3 feet wide. What is the area of the path in square feet?  
   _[BB Officer(Electrical) 23] · geometry · BIBM_Previous_All_Written_Math_Solution p9_
19. Every year Mr. Kalam saves Tk. 5400 which is 15% of his annual income. Mr. Rahim spends Tk. 2800 a month which is 87.5% of his monthly income. Who has more income?  
   _[AB Bank PO 02, BB AD 2022] · percentage · BIBM_Previous_All_Written_Math_Solution p10_
20. Matin visited his cousin Raju during the summer vacation. In the morning, they both would go for swimming. In the evening, they would play tennis. They would engage in at most one activity per day. There were days when they took rest and stayed home all day long. There were 32 mornings when they did nothing, 18 evenings when they stayed at home, and a total of 28 days when they swam or played tennis. What duration of the summer vacation did Matin stay with Raju?  
   _[Same as Uttara Cash 18, BB AD 2022] · ratio · BIBM_Previous_All_Written_Math_Solution p10_
21. The average weight of A, B and C is 40 kgs. Weight of C is 24 kgs more than A's weight and 3kgs less than B's weight. What will be the average weight of A, B, C and D, if D weights 15 kgs less than C?  
   _[BB AD 2022] · average · BIBM_Previous_All_Written_Math_Solution p11_
22. A labor is paid Tk. 100 per hour for working 8 hours in a day as regular pay. His payment is 1; times than the rate of regular pay in excess of 8 hours in a single day as overtime. If the labor received a total of Tk. 1000 for a single day, how long did he work on that day?  
   _[Same as One Bank PO 07, BB Officer 22] · work · BIBM_Previous_All_Written_Math_Solution p11_
23. A, B, and C can do a work on 10, 30 and 60 days respectively. A is assisted by B and C on every alternative days. How many days required to complete the work?  
   _[Modhumot! PO 22] · work · BIBM_Previous_All_Written_Math_Solution p15_
24. X can travel from village to school at 3km/h and return at 2 km/h. Total time taken 5 hours. What is the distance from Village to School?  
   _[Same as BASIC Bank Officer 02, Modhumoti PO 22] · speed · BIBM_Previous_All_Written_Math_Solution p15_
25. A rectangular Field with length 112 m and width 78 m. Inside the garden there is 2.5 m path. Find the area of path and cost for constructing it at Tk. 4 per sq. m.  
   _[Modhumot! PO 22] · geometry · BIBM_Previous_All_Written_Math_Solution p15_
26. An article when sells at Tk. 75 something loss. If it sells at Tk. 96, gain would be double the former loss. Find the Cost price of that article.  
   _[Modhumoti PO 22)] · profit_loss · BIBM_Previous_All_Written_Math_Solution p15_
27. On average, the bottle-nosed dolphin comes up for air once every two minutes; the beluga whale, a close relative, comes up for air on average once every five minutes. The number of times a bottle-nosed dolphin would come up for air in a 24 hour period is approximately what percent greater than the number of times a beluga whale would come up for air in that same period?  
   _[NRBC Bank (PO)-2021 (Written)] · percentage · 01_Percentage p1_ · **Ans: 150%**
28. An employee’s annual salary was increased Tk.15,000. If her new annual salary now equals Tk.90,000, what was the percent increase?  
   _[Dhaka Bank (MTO)-2021(Written)] · percentage · 01_Percentage p3_ · **Ans: 20%**
29. When the price of oranges is lowered by 40%, 4 more oranges can be purchased for $12 than can be purchased for the original price. How many oranges can be purchased for 24 dollars at the original price?  
   _[FSIBL-(PO)-2021(Written)] · percentage · 01_Percentage p5_ · **Ans: 12**
30. A car dealer received a shipment of cars, half of which were black, with the remainder consisting of equal numbers of blue, silver, and white cars. During the next month, 70% of the black cars, 80% of the blue cars, 30% of the silver cars, and 40% of the white cars were sold. What percent of the cars in the shipment were sold during that month? +  
   _[Basic Bank- (AM)-2018-(Written); Dhaka Bank (MTO)-2021(Written)] · percentage · 01_Percentage p5_ · **Ans: 60%**
31. If 2x = 1024 , what is the value of x? (hw` 2x = 1024 nq, Zvn‡j x Gi gvb KZ?) Solution: 2x = 1024  2x = 32  2x = 25 x=5  
   _[Microcredit Regulator Authority (AD)-2021(Written)] · algebra · 02_Algebra p35_ · **Ans: 5**
32. Kamal will complete work in 18 days. If Shaheen is 20% more efficient than kamal. in how many days he can complete the work? A_©: Kvgvj GKwU KvR 18 w`‡b Ki‡Z cv‡i| hw` kvnxb, Kvgv‡ji †_‡K 20% †ewk `ÿ nq Zvn‡j †m KZw`‡b KvRwU †kl Ki‡Z cvi‡e? Solution:  
   _[Microcredit Regulator Authority (AD)- 2021(Written)] · work · 03_Time_Work p14_
33. A train travels at an average speed of 100 km/hr, stopping for 3 minutes after every 75 km. How long did it take to reach its destination 600 km from the starting point? 6 hrs 21 min. (Ans) Self Task:  
   _[Microcredit Regulator Authority (AD)-2021(Written)] · speed · 04_Time_Speed p1_
34. One biker is faster by 5 km/hr than another biker. They go to the opposite direction. What is the rate of each if they go 195 km in 3 hour?  
   _[IFIC Bank – 2021 (Written)] · speed · 04_Time_Speed p2_ · **Ans: 30km/hr & 35km /hr**
35. Train X leaves New York at 10:00 AM and travels East at a constant speed of x miles per hour. If another Train Y leaves New York at 11:30 AM and travels East along the same tracks at speed 4x/3 , then at what time will Train Y catch Train X?⁠  
   _[FSIBL-(PO)- 2021(Written)] · speed · 04_Time_Speed p3_ · **Ans: 4 PM**
36. A, B and C start at the same time in the same direction to run around a circular stadium. A completes a round in 252 seconds, B in 308 seconds and C in 198 seconds, all starting at the same point. After what time will they again at the starting point?  
   _[Microcredit Regulator Authority (AD)-2021] · speed · 04_Time_Speed p4_ · **Ans: 46 min 12 sec**
37. A mixture of 120 liter milk and water contains 40% milk in it.If a certain portion was removed form the mixture and replaced with water then the new mixture have 10% milk in it. What is the value of remove part?  
   _[IFIC Bank (TSO)-2021 (Written)] · mixture · 06_Mixture p4_ · **Ans: 70**
38. Katrina has a wheat business, She, purchases wheat from a local wholesaler at a particular cost per pound. The price of the wheat at her stores is $3 per pound. Her faulty spring balance reads 0.9 pounds for a pound. Also, in the festival season, she gives a 10% discount on the wheat. She found that she made neither a profit nor a loss in the festival season: At what'price did’ Katrina purchase the wheat from the wholesaler? +  
   _[Jamuna Bank Ltd. 2016 (Written); Global Islamic Bank (PO)-2021 (Written)] · profit_loss · PDF45_Profit_Loss p20_
39. The cost price of 10 pen the same as the selling price of n pens. If there is a loss 40% approximately what i is the value of n?/BEZA(AM)-2020(Written)] + : n | % n ? 4#sSolution:  
   _[BSEC(PA)-2021 (Written)] · profit_loss · PDF45_Profit_Loss p22_
40. What will be the percentage of profit if 11 items are bought at Tk. 10 and then 10 of those items are sold at Tk. 11? : ? #sSolution: — Cost price of 11 items = Tk. 10 .-.Cost price 7 1 item = Tk. — 10 Again, Selling price of 10 items =Tk. 11 Selling suite ct of 1 item = Tk. Since Tk. => > Tk. ah here selling price is greater then cost price So, there will be profit of = 1  
   _[AB Bank (PO)-1995 (Written); 11-19 সপ (21119 | 7721 10 11 110 110  So, percentage of profit = ax aX 100=21%] · profit_loss · PDF45_Profit_Loss p26_ · **Ans: 21%**
