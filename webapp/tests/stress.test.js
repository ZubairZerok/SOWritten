/*
 * SO Written Sprint — stress test suite (Playwright, headless Chromium)
 * চালান:  node webapp/tests/stress.test.js
 * (আগে python3 webapp/build.py)
 */
const { chromium } = require("playwright");
const path = require("path");
const http = require("http");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const FILE = "file://" + path.join(ROOT, "index.html");
let pass = 0, fail = 0;
const results = [];
function ok(cond, name, extra = "") { if (cond) { pass++; results.push("  ✓ " + name); } else { fail++; results.push("  ✗ " + name + (extra ? "  → " + extra : "")); } }

function serveDist() {
  return new Promise((res) => {
    const srv = http.createServer((req, resp) => {
      const p = path.join(ROOT, "dist", decodeURIComponent(req.url.split("?")[0]).replace(/^\/+/, "") || "index.html");
      fs.readFile(p, (err, buf) => {
        if (err) { resp.writeHead(404); return resp.end(); }
        let body = buf;
        if (p.endsWith("index.html")) body = Buffer.from('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + buf.toString() + "</body></html>");
        resp.writeHead(200, { "content-type": p.endsWith(".json") ? "application/json" : "text/html; charset=utf-8" });
        resp.end(body);
      });
    });
    srv.listen(0, () => res(srv));
  });
}

async function newPage(browser, opts = {}) {
  const ctx = await browser.newContext({ viewport: opts.viewport || { width: 1280, height: 900 }, colorScheme: opts.dark ? "dark" : "light", deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error" && !/fonts\.g|ERR_NAME|net::|Failed to load resource/.test(m.text())) errors.push("console: " + m.text()); });
  if (opts.time) await page.clock.install({ time: new Date(opts.time) });
  if (opts.init) await page.addInitScript(opts.init);
  await page.goto(opts.url || FILE);
  await page.waitForSelector("main#view section");
  return { ctx, page, errors };
}
const appErrorBox = (page) => page.locator("text=এই পাতাটা দেখাতে সমস্যা হয়েছে").count();
const state = (page) => page.evaluate(() => JSON.parse(localStorage.getItem("so-sprint-v1") || "null"));
const noHScroll = (page) => page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1);

(async () => {
  const browser = await chromium.launch();
  const srv = await serveDist();
  const DIST = "http://localhost:" + srv.address().port + "/index.html";

  /* 1. every view renders at desktop/phone × light/dark, no errors, no sideways scroll */
  results.push("১. সব ভিউ · ডেস্কটপ/ফোন · লাইট/ডার্ক");
  for (const vp of [{ width: 1280, height: 900 }, { width: 375, height: 760 }]) for (const dark of [false, true]) {
    const { ctx, page, errors } = await newPage(browser, { viewport: vp, dark, time: "2026-11-21T10:00:00+06:00" });
    const views = ["today", "plan", "practice-essay", "practice-arg", "practice-tr", "practice-math", "practice-terms", "practice-quiz-eng", "practice-quiz-bn", "practice-quiz-gk", "assess", "mock", "library", "backup"];
    let bad = [];
    for (const v of views) {
      await page.evaluate((h) => (location.hash = h), v);
      await page.waitForTimeout(60);
      if (await appErrorBox(page)) bad.push(v + ":errorbox");
      if (!(await noHScroll(page))) bad.push(v + ":hscroll");
    }
    for (const lib of ["topics", "facts", "terms", "hall", "repo"]) {
      await page.evaluate(() => (location.hash = "library"));
      await page.getByRole("button", { name: { topics: "১০ টপিক", facts: "সর্বশেষ সংখ্যা", terms: "পরিভাষা", hall: "হলের চেকলিস্ট", repo: "রিপোর ফাইল" }[lib], exact: true }).click();
      if (await appErrorBox(page)) bad.push("lib-" + lib);
      if (!(await noHScroll(page))) bad.push("lib-" + lib + ":hscroll");
    }
    ok(bad.length === 0 && errors.length === 0, `${vp.width}px ${dark ? "dark" : "light"}: ${views.length + 5}টি ভিউ`, bad.concat(errors).join(", "));
    await ctx.close();
  }

  /* 2. calendar: each date maps to the right day */
  results.push("২. তারিখ → দিন");
  const expect = { "2026-11-19T21:00:00+06:00": "প্রস্তুতি দিন ০", "2026-11-20T07:00:00+06:00": "দিন ১ / ৭", "2026-11-23T23:59:00+06:00": "দিন ৪ / ৭", "2026-11-24T00:05:00+06:00": "দিন ৫ / ৭", "2026-11-26T22:00:00+06:00": "দিন ৭ / ৭", "2026-11-27T08:00:00+06:00": "আজ পরীক্ষা", "2026-11-28T10:00:00+06:00": "পরীক্ষা শেষ" };
  for (const [t, txt] of Object.entries(expect)) {
    const { ctx, page, errors } = await newPage(browser, { time: t });
    const body = await page.locator("main").innerText();
    ok(body.includes(txt) && errors.length === 0, t + " → " + txt, errors.join(",") || body.slice(0, 80));
    await ctx.close();
  }
  { // 1x vs 5x quotas, day 7 = 60%
    const { ctx, page } = await newPage(browser, { time: "2026-11-26T09:00:00+06:00" });
    await page.evaluate(() => (location.hash = "plan"));
    const txt = await page.locator("main").innerText();
    ok(txt.includes("রচনা ৫ · আর্গুমেন্ট ৫ · অনুবাদ ৫ · অঙ্ক ৪৫ · পরিভাষা ৭৫"), "৫× কোটা: ৫ রচনা, ৫ আর্গুমেন্ট, ৫ অনুবাদ, ৪৫ অঙ্ক, ৭৫ পরিভাষা");
    ok(txt.includes("রচনা ৩ · আর্গুমেন্ট ৩ · অনুবাদ ৩ · অঙ্ক ২৭"), "দিন ৭-এ কোটা ৬০%");
    await page.getByRole("button", { name: "১×", exact: true }).click();
    const t1 = await page.locator("main").innerText();
    ok(t1.includes("রচনা ১ · আর্গুমেন্ট ১ · অনুবাদ ১ · অঙ্ক ৯"), "১× কোটায় বদলায়");
    await page.getByRole("button", { name: "৫×", exact: true }).click();
    await ctx.close();
  }

  /* 3. essay timer → rubric → event → quota */
  results.push("৩. রচনা: টাইমার, মূল্যায়ন, লগ");
  {
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-20T08:00:00+06:00" });
    await page.evaluate(() => (location.hash = "practice-essay"));
    await page.getByRole("button", { name: "১৮ মিনিট শুরু করুন" }).click();
    ok(await page.locator("#timerbar").isVisible(), "টাইমার বার দেখা যায়");
    ok(await page.getByRole("button", { name: "১৮ মিনিট শুরু করুন" }).isDisabled(), "টাইমার চলার সময় দ্বিতীয় টাইমার বন্ধ");
    await page.clock.fastForward("09:00");
    const mid = await page.locator("#timerbar .clock").innerText();
    ok(/০৯:০০|০৮:৫৯/.test(mid), "৯ মিনিট পরে ঘড়ি ০৯:০০", mid);
    await page.reload(); await page.waitForSelector("#timerbar:not([hidden])");
    const afterReload = await page.locator("#timerbar .clock").innerText();
    ok(/০৯:০০|০৮:৫৯|০৮:৫৮/.test(afterReload), "রিলোডের পরেও টাইমার চলে", afterReload);
    await page.getByRole("button", { name: "বিরতি" }).click();
    await page.clock.fastForward("05:00");
    const paused = await page.locator("#timerbar .clock").innerText();
    ok(/০৯:০০|০৮:৫৯|০৮:৫৮/.test(paused), "বিরতিতে সময় থেমে থাকে", paused);
    await page.getByRole("button", { name: "চালু" }).click();
    await page.clock.fastForward("09:30");
    ok(await page.locator("#timerbar.over").count() === 1, "সময় শেষে লাল বার");
    await page.getByRole("button", { name: "ফলাফল দিন" }).click();
    for (const i of [0, 1, 2, 3, 5, 6]) await page.locator("#rb" + i).check();
    await page.selectOption("#rb-lang", "1");
    await page.fill("#rb-wc", "270");
    const shown = await page.locator("#modal b.num").innerText();
    ok(shown.startsWith("২২/") || shown.startsWith("২২"), "স্কোর হিসাব ২+৪+৬+৫+৫+২−২ = ২২", shown);
    await page.getByRole("button", { name: "সংরক্ষণ", exact: true }).click();
    const st = await state(page);
    const ev = st.events.filter((e) => e.k === "essay");
    ok(ev.length === 1 && ev[0].raw === 22 && ev[0].wc === 270 && ev[0].d === "2026-11-20", "ইভেন্ট সঠিকভাবে সংরক্ষিত", JSON.stringify(ev));
    ok(st.timer === null, "টাইমার পরিষ্কার");
    await page.evaluate(() => (location.hash = "today"));
    ok((await page.locator("main").innerText()).includes("১/৫"), "আজকের কোটায় রচনা ১/৫");
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    // cancel path
    await page.evaluate(() => (location.hash = "practice-arg"));
    await page.getByRole("button", { name: "২২ মিনিট শুরু করুন" }).click();
    await page.locator("#timerbar").getByRole("button", { name: "বাতিল" }).click();
    await page.getByRole("button", { name: "বাতিল করুন" }).click();
    ok(await page.locator("#timerbar").isHidden() && (await state(page)).events.filter((e) => e.k === "arg").length === 0, "টাইমার বাতিলে কিছু লগ হয় না");
    await ctx.close();
  }

  /* 4. math, terms, quizzes */
  results.push("৪. গণিত, পরিভাষা, MCQ");
  {
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-21T10:00:00+06:00" });
    await page.evaluate(() => (location.hash = "practice-math"));
    const seen = new Set();
    for (let i = 0; i < 8; i++) { seen.add(await page.locator(".qbox .q").innerText()); await page.getByRole("button", { name: i < 5 ? "✓ সঠিক হয়েছে" : "✗ ভুল/পারিনি" }).click(); }
    let st = await state(page);
    const m = st.events.filter((e) => e.k === "math");
    ok(m.length === 8 && m.filter((e) => e.s === 1).length === 5, "৮টি অঙ্ক লগ, ৫টি সঠিক");
    ok(seen.size === 8, "প্রতিবার নতুন প্রশ্ন", String(seen.size));
    ok(m.every((e) => e.ch === "speed"), "দিন ২-এর অধ্যায় (গতি) ডিফল্ট", m.map((e) => e.ch).join(","));
    await page.selectOption("#m-ch", "wrong");
    const opt = await page.locator("#m-ch option:checked").innerText();
    ok(opt.includes("৩"), "'ভুলগুলো আবার'-এ ৩টি", opt);
    for (const ch of ["mixed", "recent", "probability", "age"]) { await page.selectOption("#m-ch", ch); ok((await page.locator(".qbox .q").innerText()).length > 30, "অধ্যায় '" + ch + "'-এ প্রশ্ন আছে"); }
    await page.evaluate(() => (location.hash = "practice-terms"));
    for (let i = 0; i < 20; i++) { await page.getByRole("button", { name: "উত্তর দেখুন" }).click(); await page.getByRole("button", { name: i % 4 ? "জানতাম" : "জানতাম না", exact: true }).click(); }
    st = await state(page);
    const te = st.events.filter((e) => e.k === "terms");
    ok(te.reduce((a, e) => a + e.n, 0) === 20 && te.length <= 2, "২০টি পরিভাষা, এক-দুটি ইভেন্টে জমা", JSON.stringify(te.map((e) => [e.n, e.s])));
    ok(Math.abs(te.reduce((a, e) => a + e.s * e.n, 0) - 15) < 1e-9, "১৫টি জানা গণনা ঠিক");
    for (const k of ["eng", "bn", "gk"]) {
      await page.evaluate((h) => (location.hash = h), "practice-quiz-" + k);
      for (let i = 0; i < 10; i++) { await page.locator("button.opt").first().click(); await page.getByRole("button", { name: i < 9 ? "পরের প্রশ্ন" : "ফলাফল দেখুন" }).click(); }
      const res = await page.locator("main").innerText();
      ok(res.includes("ফলাফল") && /[০-৯]+\/১০/.test(res), k + " MCQ: ১০ প্রশ্ন শেষে ফলাফল");
      const s2 = await state(page); const qe = s2.events.filter((e) => e.k === k);
      ok(qe.reduce((a, e) => a + e.n, 0) === 10, k + ": ১০টি উত্তর লগ");
    }
    // option shuffle sanity: correct answer not always first
    await page.evaluate(() => (location.hash = "practice-quiz-eng"));
    if (await page.getByRole("button", { name: "পরের ১০টি" }).count()) await page.getByRole("button", { name: "পরের ১০টি" }).click();
    let firstRight = 0;
    for (let i = 0; i < 10; i++) { await page.locator("button.opt").first().click(); if (await page.locator("button.opt").first().evaluate((b) => b.classList.contains("right"))) firstRight++; await page.getByRole("button", { name: i < 9 ? "পরের প্রশ্ন" : "ফলাফল দেখুন" }).click(); }
    ok(firstRight < 10, "সঠিক উত্তর সবসময় প্রথমে থাকে না (অপশন এলোমেলো)", String(firstRight));
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    await ctx.close();
  }

  /* 5. mock: validation, save, projection */
  results.push("৫. মক টেস্ট ও মূল্যায়ন");
  {
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-24T09:30:00+06:00" });
    await page.evaluate(() => (location.hash = "mock"));
    await page.getByRole("button", { name: "পূর্ণ মক শুরু (১২০ মি)" }).click();
    ok((await page.locator("main").innerText()).includes("প্রশ্নপত্র: পূর্ণ মক"), "প্রশ্নপত্র তৈরি");
    const paperQs = await page.locator("main ol li").count();
    ok(paperQs === 25, "পত্রে ৫ গণিত + ১০ ইংরেজি + ৫ বাংলা + ৫ GK = ২৫", String(paperQs));
    await page.clock.fastForward("23:00");
    ok((await page.locator("#timerbar").innerText()).includes("আর্গুমেন্ট"), "২৩ মিনিটে বার বলছে: এখন আর্গুমেন্ট");
    await page.clock.fastForward("01:38:00");
    await page.getByRole("button", { name: "ফলাফল দিন" }).click();
    await page.fill("#mk-FW_EN", "31");
    await page.getByRole("button", { name: "সংরক্ষণ", exact: true }).click();
    ok((await page.locator("#modal").innerText()).includes("০ থেকে ৩০"), "সীমার বাইরে নম্বরে ত্রুটি দেখায়");
    const sc = { FW_EN: 18, FW_BN: 19, ARG: 22, TR: 12, MATH: 24, ENG: 13, BN: 7, BANK: 6, GK: 5 };
    for (const [k, v] of Object.entries(sc)) await page.fill("#mk-" + k, String(v));
    await page.getByRole("button", { name: "সংরক্ষণ", exact: true }).click();
    const st = await state(page);
    ok(st.mocks.length === 1 && st.mocks[0].scores.ARG === 22, "মক সংরক্ষিত");
    await page.waitForFunction(() => location.hash === "#assess");
    await page.waitForTimeout(100);
    const txt = await page.locator("main").innerText();
    ok(txt.includes("প্রজেক্টেড:"), "সব অংশের ডেটা থাকায় পূর্ণ প্রজেকশন দেখায়", txt.slice(0, 120));
    const proj = await page.evaluate(() => { const p = projection(); p.rows.forEach((r) => (r.max = SEC[r.sec].max)); return p; });
    ok(proj.total > 80 && proj.total <= 126 && proj.rows.every((r) => r.proj != null && r.proj <= r.max), "প্রজেকশন যুক্তিসঙ্গত (" + Math.round(proj.total) + ")");
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    await ctx.close();
  }

  /* 6. manual log validation, delete, intensity */
  results.push("৬. খাতার কাজ যোগ, মুছে ফেলা");
  {
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-22T10:00:00+06:00" });
    await page.getByRole("button", { name: "খাতায় করা কাজ যোগ করুন" }).click();
    await page.fill("#ml-n", "5"); await page.fill("#ml-ok", "9");
    await page.getByRole("button", { name: "যোগ করুন", exact: true }).click();
    ok(await page.locator("#modal").isVisible() && (await page.locator("#modal").innerText()).includes("সঠিক উত্তর"), "সঠিক > মোট হলে আটকায়");
    await page.fill("#ml-ok", "4"); await page.getByRole("button", { name: "যোগ করুন", exact: true }).click();
    await page.getByRole("button", { name: "খাতায় করা কাজ যোগ করুন" }).click();
    await page.selectOption("#ml-k", "arg"); await page.fill("#ml-s", "50");
    await page.getByRole("button", { name: "যোগ করুন", exact: true }).click();
    ok((await page.locator("#modal").innerText()).includes("৪০"), "আর্গুমেন্টে ৪০-এর বেশি আটকায়");
    await page.fill("#ml-s", "28"); await page.getByRole("button", { name: "যোগ করুন", exact: true }).click();
    let st = await state(page);
    ok(st.events.length === 2 && st.events[0].n === 5 && st.events[1].raw === 28, "দুটো এন্ট্রি সঠিক");
    await page.evaluate(() => (location.hash = "assess"));
    await page.getByRole("button", { name: "মুছুন" }).first().click();
    await page.locator("#modal").getByRole("button", { name: "মুছুন" }).click();
    st = await state(page);
    ok(st.events.length === 1, "এন্ট্রি মুছে ফেলা যায়");
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    await ctx.close();
  }

  /* 7. persistence robustness */
  results.push("৭. সংরক্ষণ: নষ্ট ডেটা, স্টোরেজ বন্ধ, ব্যাকআপ");
  {
    const bads = ["{not json", "null", "[]", JSON.stringify({ events: "x", settings: 5, mocks: {}, timer: { kind: 3 } }), JSON.stringify({ events: [{ k: "math", t: "bad" }, { k: "essay", t: 1795000000000, s: "NaN", n: "x" }], settings: { mult: 99 } })];
    for (const b of bads) {
      const { ctx, page, errors } = await newPage(browser, { time: "2026-11-21T10:00:00+06:00", init: `try{localStorage.setItem("so-sprint-v1", ${JSON.stringify(b)})}catch(e){}` });
      const views = ["today", "plan", "assess", "mock", "practice-essay"]; let bad = 0;
      for (const v of views) { await page.evaluate((h) => (location.hash = h), v); if (await appErrorBox(page)) bad++; }
      ok(bad === 0 && errors.length === 0, "নষ্ট ডেটা সামলায়: " + b.slice(0, 40), errors.join(","));
      await ctx.close();
    }
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-21T10:00:00+06:00", init: `Storage.prototype.setItem=function(){throw new Error("quota")};Storage.prototype.getItem=function(){throw new Error("blocked")};` });
    await page.evaluate(() => (location.hash = "practice-math"));
    await page.getByRole("button", { name: "✓ সঠিক হয়েছে" }).click();
    ok(errors.length === 0 && (await page.locator("#sync").innerText()).includes("ব্যাকআপ"), "স্টোরেজ বন্ধ থাকলেও চলে, সতর্ক করে", await page.locator("#sync").innerText());
    await ctx.close();
  }
  {
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-21T10:00:00+06:00" });
    await page.evaluate(() => (location.hash = "practice-math"));
    for (let i = 0; i < 6; i++) await page.getByRole("button", { name: "✓ সঠিক হয়েছে" }).click();
    await page.evaluate(() => (location.hash = "backup"));
    const dump = await page.locator("#bk-out").inputValue();
    await page.fill("#bk-reset", "reset"); await page.getByRole("button", { name: "সব মুছুন" }).click();
    ok((await state(page)).events.length === 6, "ভুল শব্দে রিসেট হয় না");
    await page.fill("#bk-reset", "RESET"); await page.getByRole("button", { name: "সব মুছুন" }).click();
    ok((await state(page)).events.length === 0, "RESET লিখলে মুছে যায়");
    await page.fill("#bk-in", "garbage"); await page.getByRole("button", { name: "মিলিয়ে নিন (দুটো একসাথে)" }).click();
    ok((await page.locator("main").innerText()).includes("বৈধ ব্যাকআপ নয়"), "ভুল ব্যাকআপে ত্রুটি দেখায়");
    await page.fill("#bk-in", dump); await page.getByRole("button", { name: "মিলিয়ে নিন (দুটো একসাথে)" }).click();
    ok((await state(page)).events.length === 6, "ব্যাকআপ থেকে ৬টি এন্ট্রি ফেরত");
    await page.fill("#bk-in", dump); await page.getByRole("button", { name: "মিলিয়ে নিন (দুটো একসাথে)" }).click();
    ok((await state(page)).events.length === 6, "একই ব্যাকআপ দুবার দিলে ডুপ্লিকেট হয় না");
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    await ctx.close();
  }

  /* 8. cloud sync (simulated claude.ai db) + external data.json */
  results.push("৮. ক্লাউড সিঙ্ক (সিমুলেটেড) ও আলাদা data.json");
  {
    const fake = `
      window.__writes = []; let listener = null; let doc = window.__remote || null;
      window.__pushRemote = (d) => { doc = d; listener && listener({ exists: true, data: () => d, metadata: { fromCache: false, hasPendingWrites: false } }); };
      window.claude = { use: async (n) => {
        if (n === "user") return { id: async () => "u_test" };
        if (n === "db") return { doc: (p) => { window.__path = p; return {
          set: async (d) => { window.__writes.push(JSON.parse(JSON.stringify(d))); doc = d; },
          onSnapshot: (next) => { listener = next; setTimeout(() => next(doc ? { exists: true, data: () => doc, metadata: { fromCache: false } } : { exists: false, metadata: { fromCache: false } }), 50); return () => {}; } }; } };
        return null; } };`;
    const { ctx, page, errors } = await newPage(browser, { url: DIST, init: fake });
    await page.waitForTimeout(300);
    ok((await page.evaluate(() => window.__path)) === "data/users/u_test/so_state", "ব্যক্তিগত পাথে লেখে: data/users/<id>/so_state");
    await page.evaluate(() => (location.hash = "practice-math"));
    await page.getByRole("button", { name: "✓ সঠিক হয়েছে" }).click();
    await page.getByRole("button", { name: "✓ সঠিক হয়েছে" }).click();
    await page.waitForTimeout(1800);
    const w = await page.evaluate(() => window.__writes);
    ok(w.length >= 1 && w[w.length - 1].events.length === 2, "পরিবর্তন ক্লাউডে যায় (debounced, " + w.length + " write)");
    ok((await page.locator("#sync").innerText()).includes("ক্লাউডে"), "স্ট্যাটাস: ক্লাউডে সংরক্ষিত");
    await page.evaluate(() => { const d = JSON.parse(localStorage.getItem("so-sprint-v1")); d.updatedAt = Date.now() + 60000; d.events.push({ id: "remote1", t: Date.now(), d: "2026-11-21", k: "news", n: 1, s: null }); window.__pushRemote(d); });
    await page.waitForTimeout(200);
    ok((await state(page)).events.some((e) => e.id === "remote1"), "অন্য ডিভাইসের নতুন ডেটা নেয়");
    ok((await page.locator("main").innerText()).length > 50 && errors.length === 0, "data.json আলাদা থেকেও লোড হয়, কোনো error নেই", errors.join(","));
    await ctx.close();
  }

  /* 9. monkey test: 400 random clicks */
  results.push("৯. মাঙ্কি টেস্ট (৪০০ র‍্যান্ডম ক্লিক)");
  for (const vp of [{ width: 1280, height: 900 }, { width: 375, height: 760 }]) {
    const { ctx, page, errors } = await newPage(browser, { viewport: vp, time: "2026-11-23T11:00:00+06:00" });
    let clicks = 0, errBoxes = 0;
    for (let i = 0; i < 200; i++) {
      if (i % 15 === 0) await page.evaluate((h) => (location.hash = h), ["today", "plan", "practice-essay", "practice-math", "practice-terms", "practice-quiz-gk", "assess", "mock", "library", "practice-tr", "practice-arg"][i % 11]);
      if (i % 40 === 39) await page.clock.fastForward("25:00");
      const btns = await page.locator("button:visible:not([disabled]), select:visible, input[type=checkbox]:visible").elementHandles();
      const safe = [];
      for (const b of btns) { const t = (await b.innerText().catch(() => "")) || ""; if (!/সব মুছুন|মুছুন|বাতিল করুন/.test(t)) safe.push(b); }
      if (!safe.length) continue;
      const b = safe[Math.floor(Math.random() * safe.length)];
      const tag = await b.evaluate((e) => e.tagName);
      try {
        if (tag === "SELECT") { const n = await b.evaluate((e) => e.options.length); await b.selectOption({ index: Math.floor(Math.random() * n) }); }
        else await b.click({ timeout: 1500 });
        clicks++;
      } catch (e) { /* element re-rendered: fine */ }
      if (await appErrorBox(page)) errBoxes++;
    }
    const st = await state(page);
    ok(errors.length === 0 && errBoxes === 0 && st && Array.isArray(st.events), `${vp.width}px: ${clicks}টি ক্লিক, কোনো ক্র্যাশ নেই, ${st ? st.events.length : 0}টি এন্ট্রি`, errors.slice(0, 3).join(" | "));
    ok(await noHScroll(page), `${vp.width}px: মাঙ্কি টেস্টের পরেও পাশের স্ক্রল নেই`);
    await ctx.close();
  }

  /* 10. heavy data: 1400 events, performance */
  results.push("১০. লোড টেস্ট");
  {
    const init = `(() => { const ev = []; const base = Date.parse("2026-11-20T06:00:00+06:00"); const kinds = ["math","terms","eng","bn","gk","essay","arg","tr","news"];
      for (let i = 0; i < 1500; i++) { const t = base + i * 300000; const k = kinds[i % 9]; ev.push({ id: "e"+i, t, d: new Date(t + 6*3600e3).toISOString().slice(0,10), k, n: k==="terms"?10:1, s: k==="news"?null:Math.random(), lang: i%2?"en":"bn", topic: 1 + i % 10, ch: "speed", raw: 20, max: 30 }); }
      localStorage.setItem("so-sprint-v1", JSON.stringify({ v:1, updatedAt: 1, settings:{mult:5}, events: ev, mocks: [], checks:{}, mathLog:{}, termBox:{}, quizWrong:{}, hall:{} })); })();`;
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-25T10:00:00+06:00", init });
    const t0 = Date.now();
    for (const v of ["today", "assess", "plan", "practice-math", "today"]) { await page.evaluate((h) => (location.hash = h), v); await page.waitForSelector("main section"); }
    const dt = Date.now() - t0;
    const st = await page.evaluate(() => S.events.length);
    ok(st <= 1400, "এন্ট্রি সর্বোচ্চ ১৪০০-তে সীমিত (" + st + ")");
    ok(dt < 4000 && errors.length === 0, "১৪০০ এন্ট্রিতে ৫টি ভিউ " + dt + " ms-এ", errors.join(","));
    await ctx.close();
  }


  /* 11. confirmed syllabus: sub-topic quizzes, coverage, target 128 */
  results.push("১১. অফিসিয়াল সিলেবাস: সাব-টপিক কুইজ, কভারেজ, লক্ষ্য ১২৮");
  {
    const { ctx, page, errors } = await newPage(browser, { time: "2026-11-22T10:00:00+06:00" });
    const data = await page.evaluate(() => ({ eng: [...new Set(D.quiz.eng.map((q) => q.tp))], bn: [...new Set(D.quiz.bn.map((q) => q.tp))], names: D.quiz._tp_names, bad: [...D.quiz.eng, ...D.quiz.bn, ...D.quiz.gk].filter((q) => !(q.a >= 0 && q.a < q.o.length) || new Set(q.o).size !== q.o.length).length }));
    for (const t of ["sva", "rfv", "structure", "speech", "transformation", "finite", "clause", "groupverb", "idiom"]) ok(data.eng.includes(t), "ইংরেজি সিলেবাস অংশ আছে: " + data.names[t]);
    for (const t of ["banan", "banan_niyom", "shuddhi", "probad", "karok", "somas", "sondhi", "ekkothay", "somoccharito"]) ok(data.bn.includes(t), "বাংলা সিলেবাস অংশ আছে: " + data.names[t]);
    ok(data.bad === 0, "সব MCQ-তে উত্তর index বৈধ আর অপশন আলাদা");
    await page.evaluate(() => (location.hash = "practice-quiz-bn"));
    await page.getByRole("button", { name: /^কারক/ }).click();
    let tags = new Set();
    for (let i = 0; i < 5; i++) { tags.add(await page.locator(".eyebrow").last().innerText()); await page.locator("button.opt").first().click(); await page.getByRole("button", { name: i < 4 ? "পরের প্রশ্ন" : "ফলাফল দেখুন" }).click(); }
    ok([...tags].every((t) => t.includes("কারক")), "'কারক' ফিল্টারে শুধু কারকের প্রশ্ন (৫টি)", [...tags].join(" | "));
    await page.evaluate(() => (location.hash = "assess"));
    const at = await page.locator("main").innerText();
    ok(at.includes("ব্যাকরণ সিলেবাস কভারেজ") && /কারক\s+৫\/৫/.test(at), "কভারেজ টেবিলে কারক ৫/৫ দেখা", at.match(/কারক[^\n]*/)?.[0]);
    ok(at.includes("লক্ষ্য ১২৮") && at.includes("লক্ষ্য (১২৮)"), "মূল্যায়নে লক্ষ্য ১২৮");
    await page.evaluate(() => (location.hash = "plan"));
    const pt = await page.locator("main").innerText();
    ok(pt.includes("নিশ্চিত নম্বর বণ্টন") && /মোট\s+২০০\s+১২৮/.test(pt), "প্ল্যানে নিশ্চিত বণ্টন ও লক্ষ্য টেবিল (মোট ২০০ / ১২৮)");
    const sum = await page.evaluate(() => Object.values(TARGET).reduce((a, b) => a + b, 0) === TARGET_TOTAL && Object.keys(TARGET).every((k) => TARGET[k] <= SEC[k].max) && Object.values(SEC).reduce((a, s) => a + s.max, 0) === 200);
    ok(sum, "অংশের লক্ষ্য যোগফল = ১২৮, পূর্ণ নম্বর যোগফল = ২০০");
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    await ctx.close();
  }

  srv.close();
  await browser.close();
  console.log(results.join("\n"));
  console.log(`\nমোট: ${pass} পাস, ${fail} ফেল`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
