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
    const views = ["today", "plan", "practice-essay", "practice-arg", "practice-tr", "practice-math", "practice-terms", "practice-quiz-eng", "practice-quiz-bn", "practice-quiz-gk", "ai", "ai-history", "ai-settings", "assess", "mock", "library", "backup"];
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
    const nK = Math.min(10, await page.evaluate(() => D.quiz.bn.filter((q) => q.tp === "karok").length));
    for (let i = 0; i < nK; i++) { tags.add(await page.locator(".eyebrow").last().innerText()); await page.locator("button.opt").first().click(); await page.getByRole("button", { name: i < nK - 1 ? "পরের প্রশ্ন" : "ফলাফল দেখুন" }).click(); }
    ok([...tags].every((t) => t.includes("কারক")), "'কারক' ফিল্টারে শুধু কারকের প্রশ্ন (" + nK + "টি)", [...tags].join(" | "));
    await page.evaluate(() => (location.hash = "assess"));
    const at = await page.locator("main").innerText();
    const kTot = await page.evaluate(() => D.quiz.bn.filter((q) => q.tp === "karok").length); const bnD = (x) => String(x).replace(/[0-9]/g, (d) => "০১২৩৪৫৬৭৮৯"[d]);
    ok(at.includes("ব্যাকরণ সিলেবাস কভারেজ") && new RegExp("কারক\\s+" + bnD(nK) + "\\/" + bnD(kTot)).test(at), "কভারেজ টেবিলে কারক " + nK + "/" + kTot + " দেখা", at.match(/কারক[^\n]*/)?.[0]);
    ok(at.includes("লক্ষ্য ১২৮") && at.includes("লক্ষ্য (১২৮)"), "মূল্যায়নে লক্ষ্য ১২৮");
    await page.evaluate(() => (location.hash = "plan"));
    const pt = await page.locator("main").innerText();
    ok(pt.includes("নিশ্চিত নম্বর বণ্টন") && /মোট\s+২০০\s+১২৮/.test(pt), "প্ল্যানে নিশ্চিত বণ্টন ও লক্ষ্য টেবিল (মোট ২০০ / ১২৮)");
    const sum = await page.evaluate(() => Object.values(TARGET).reduce((a, b) => a + b, 0) === TARGET_TOTAL && Object.keys(TARGET).every((k) => TARGET[k] <= SEC[k].max) && Object.values(SEC).reduce((a, s) => a + s.max, 0) === 200);
    ok(sum, "অংশের লক্ষ্য যোগফল = ১২৮, পূর্ণ নম্বর যোগফল = ২০০");
    ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
    await ctx.close();
  }


  /* 12. AI পরীক্ষক: ছবি → ট্রান্সক্রিপশন → ২ পরীক্ষক → কোড-যাচাই; ত্রুটি; নিজের API */
  results.push("১২. AI পরীক্ষক (সিমুলেটেড Claude ও API)");
  {
    const SENT = "মূল্যস্ফীতি নিয়ন্ত্রণে বাংলাদেশ ব্যাংক নীতি সুদহার ৯.৫% রেখেছে এবং বাজার তদারকি জোরদার করতে হবে যাতে সাধারণ মানুষ স্বস্তি পায়।";
    const TRANSCRIPT = "=== পৃষ্ঠা 1 ===\nমূল্যস্ফীতি: কারণ ও প্রতিকার\nভূমিকা\nঅক্টোবর ২০২৬-এ মূল্যস্ফীতি ৮.২৭% যা সাধারণ মানুষের জীবন কঠিন করেছে। মূল্যস্ফিতি এখন বড় সমস্যা।\n" +
      Array.from({ length: 14 }, () => SENT).join(" ") + "\nমজুরি বাড়ছে কম, দাম বাড়ছে বেশি।\n<img src=x onerror=\"window.__xss=1\">\nউপসংহার\nসমন্বিত উদ্যোগেই সমাধান সম্ভব।";
    const makeResp = (p, T) => {
      const task = (p.match(/TASK: (\w+)/) || [])[1];
      if (task === "TRANSCRIBE_HANDWRITTEN_ANSWER") return T + "\nLEGIBILITY: 82";
      if (task === "COACH_REPORT") return "১. এখনকার অবস্থা: ফোকাস বাংলায় ৭৫%। ২. সমস্যা: বানান। ৩. পরিকল্পনা: সকাল ৯টায় GK। ৪. সতর্কতা: সময়।";
      if (p.includes("ITEMS (number")) {
        return JSON.stringify({ items: [
          { n: 1, answer: "৭.৫%", verdict: "correct", award: 2, correct: "৭.৫%", note: "ঠিক" },
          { n: 2, answer: "৩৫.৫৯", verdict: "correct", award: 1, correct: "৩৫.৫৯ বি.", note: "ঠিক" },
          { n: 3, answer: "আহসান মনসুর", verdict: "wrong", award: 2, correct: "মো. মোস্তাকুর রহমান", note: "পুরোনো তথ্য" },
          { n: 4, answer: "৩২%", verdict: "partial", award: 5, correct: "৩২.১৭%", note: "আংশিক" } ],
          errors: [{ type: "fact", wrong: "আহসান মনসুর", right: "মো. মোস্তাকুর রহমান", why: "গভর্নর বদলেছে" }], strengths: ["দ্রুত"], fixes: ["গভর্নরের নাম মুখস্থ"], verdict: "চলনসই", confidence: 0.8, total: 99 });
      }
      const ev = { rel: "মূল্যস্ফীতি: কারণ ও প্রতিকার", intro: "অক্টোবর ২০২৬-এ মূল্যস্ফীতি ৮.২৭%", content: "মজুরি বাড়ছে কম", data: "এই কথাটা উত্তরে কোথাও লেখা হয়নি একদম", struct: "ভূমিকা", sol: "বাজার তদারকি জোরদার করতে হবে", lang: "", concl: "সমন্বিত উদ্যোগেই সমাধান সম্ভব" };
      const mod = task === "MODERATE";
      const aw = { rel: 4, intro: 3, content: mod ? 5 : 9, data: 5, struct: 3, sol: 2, lang: 2, concl: 1 };
      return JSON.stringify({ criteria: Object.keys(aw).map((id) => ({ id, award: aw[id], evidence: ev[id], comment: "মন্তব্য " + id })),
        errors: [{ type: "spelling", wrong: "মূল্যস্ফিতি", right: "মূল্যস্ফীতি", why: "ঈ-কার হবে" }], facts: [{ claim: "মূল্যস্ফীতি ৮.২৭%", status: "correct", fix: "" }],
        strengths: ["সংখ্যা আছে"], fixes: ["ডেটা বক্স দিন", "উপশিরোনাম বাড়ান", "বানান"], improved: "উন্নত ভূমিকা…", verdict: "ভালো, তবে ডেটা বক্স নেই", confidence: 0.7, total: 30,
        moderation: mod ? [{ id: "content", from: 7, to: 5, why: "গভীরতা কম" }] : undefined });
    };
    const fakeClaude = (maxCount) => `
      window.__calls = []; window.__fail = []; window.__delay = 0; const T = ${JSON.stringify(TRANSCRIPT)};
      const makeResp = ${makeResp.toString()};
      const respond = async (input, opts) => {
        const p = typeof input === "string" ? input : input.map((x) => x.content).join("\\n");
        window.__calls.push({ task: (p.match(/TASK: (\\w+)/) || [])[1], len: new TextEncoder().encode(p).length, images: opts && opts.images ? opts.images.length : 0, imgTypes: opts && opts.images ? [...opts.images].map((b) => b.type) : [], tier: opts && opts.modelTier, cache: opts && opts.cache, prompt: p });
        if (window.__delay) await new Promise((res, rej) => { const t = setTimeout(res, window.__delay); opts && opts.signal && opts.signal.addEventListener("abort", () => { clearTimeout(t); rej({ code: "cancelled" }); }); });
        const f = window.__fail.shift(); if (f) throw f;
        return makeResp(p, window.__T || T);
      };
      const sample = async (input, opts) => { const r = await respond(input, opts); opts && opts.onText && opts.onText({ text: r, delta: r }); return { text: r, truncated: false, modelTierApplied: "complex" }; };
      sample.json = async (input, opts) => { const r = await respond(input, opts); opts && opts.onText && opts.onText({ text: r, delta: r }); return JSON.parse(r); };
      sample.limits = async () => ({ maxPromptBytes: 262144, images: { maxCount: ${maxCount}, maxInputBytes: 20e6, mediaTypes: ["image/jpeg", "image/png", "image/webp"] } });
      window.__dbWrites = [];
      window.claude = { use: async (n) => n === "sample" ? sample : n === "user" ? { id: async () => "u_ai" } : n === "db" ? { doc: () => ({ set: async (d) => { window.__dbWrites.push(JSON.stringify(d).length); }, onSnapshot: (next) => { setTimeout(() => next({ exists: false, metadata: { fromCache: false } }), 30); return () => {}; } }) } : null };`;
    const tall = await (async () => { const { ctx, page } = await newPage(browser, { viewport: { width: 400, height: 900 } }); const b = await page.screenshot({ clip: { x: 0, y: 0, width: 300, height: 620 } }); await ctx.close(); return b; })();
    const wide = await (async () => { const { ctx, page } = await newPage(browser, { viewport: { width: 900, height: 600 } }); const b = await page.screenshot({ clip: { x: 0, y: 0, width: 640, height: 300 } }); await ctx.close(); return b; })();
    const focusBtn = (page, name) => page.locator(".qbox", { hasText: name }).getByRole("button", { name: "প্রশ্ন তৈরি করুন" });

    /* A. ছবি → পড়া → ২ পরীক্ষক → ফল (ফোনের মাপে) */
    {
      const { ctx, page, errors } = await newPage(browser, { url: DIST, init: fakeClaude(4), viewport: { width: 390, height: 820 }, time: "2026-11-21T10:00:00+06:00" });
      await page.evaluate(() => (location.hash = "ai"));
      await page.waitForSelector("text=মূল্যায়ক: Claude");
      ok(await page.locator(".qbox", { hasText: "ফোকাস রাইটিং (বাংলা)" }).count() === 1 && await page.locator(".qbox", { hasText: "সাধারণ জ্ঞান" }).count() >= 1, "আজকের ফোকাস কার্ড: GK, ব্যাংকিং, বাংলা, অনুবাদ, ফোকাস বাংলা");
      const fc = await page.evaluate(() => [...document.querySelectorAll("main .qbox b")].map((b) => b.textContent));
      ok(["সাধারণ জ্ঞান", "ব্যাংকিং ও আর্থিক জ্ঞান", "বাংলা ব্যাকরণ", "বাংলা→ইংরেজি অনুবাদ", "ফোকাস রাইটিং (বাংলা)"].every((x) => fc.includes(x)), "৫টি ফোকাস অংশই আছে", fc.join(","));
      await focusBtn(page, "ফোকাস রাইটিং (বাংলা)").click();
      ok(await page.locator("text=৩০ নম্বর · ১৮ মিনিট").count() === 1, "প্রশ্ন: ৩০ নম্বর · ১৮ মিনিট");
      await page.setInputFiles("#ai-files", [{ name: "p1.png", mimeType: "image/png", buffer: tall }, { name: "p2.png", mimeType: "image/png", buffer: wide }, { name: "note.pdf", mimeType: "application/pdf", buffer: Buffer.from("%PDF-1.4") }]);
      ok(await page.locator(".thumb").count() === 2, "২টি ছবি নেয়, PDF বাদ দেয়");
      await page.locator(".thumb").nth(1).getByRole("button", { name: "ঘোরান" }).click();
      await page.locator(".thumb").nth(1).getByRole("button", { name: "আগে নিন" }).click();
      ok((await page.locator(".thumb img").first().getAttribute("style")).includes("rotate(90deg)"), "ঘোরানো ও ক্রম বদল কাজ করে");
      ok(await noHScroll(page), "ফোনে ছবির তালিকায় পাশে স্ক্রল নেই");
      await page.getByRole("button", { name: "১. হাতের লেখা পড়ান" }).click();
      await page.waitForSelector("#ai-tr");
      const c0 = (await page.evaluate(() => window.__calls))[0];
      ok(c0.task === "TRANSCRIBE_HANDWRITTEN_ANSWER" && c0.images === 4 && c0.tier === "complex" && c0.imgTypes.every((t) => t === "image/jpeg"), "ট্রান্সক্রিপশন: লম্বা পৃষ্ঠা দুই ভাগ, ঘোরানো পৃষ্ঠাও ভাগ → ৪টি JPEG, complex মডেল", JSON.stringify({ i: c0.images, t: c0.tier, ty: c0.imgTypes }));
      ok(c0.prompt.includes("Do NOT correct spelling") && c0.prompt.includes("[অস্পষ্ট]") && c0.prompt.includes("top half"), "ট্রান্সক্রিপশন নির্দেশ: ভুল শুধরাবে না, অস্পষ্ট চিহ্ন, অর্ধেক পৃষ্ঠা");
      ok(await page.locator("text=হাতের লেখা পড়ার সুবিধা ৮২/১০০").count() === 1, "হাতের লেখার মান (৮২) দেখায়");
      await page.locator("#ai-tr").fill(TRANSCRIPT.replace("=== পৃষ্ঠা 1 ===\n", "=== পৃষ্ঠা 1 ===\n") + "\nশেষ।");
      ok((await state(page)).aiDraft.transcript.endsWith("শেষ।"), "পড়ার ভুল ঠিক করলে সংরক্ষিত হয় (রিলোডেও থাকবে)");
      await page.getByRole("button", { name: /২\. নম্বর দিন \(২ জন পরীক্ষক\)/ }).click();
      await page.waitForSelector("text=মানদণ্ড অনুযায়ী নম্বর");
      const calls = await page.evaluate(() => window.__calls);
      const g1 = calls.find((c) => c.task === "GRADE_V1"), g2 = calls.find((c) => c.task === "MODERATE");
      ok(g1 && g2 && g1.tier === "complex" && g2.tier === "complex", "২ জন পরীক্ষক: GRADE_V1 → MODERATE");
      ok(["MARKING SCHEME", 'id "data" (max 5)', "VERIFIED FACTS AS OF 20 NOVEMBER 2026", "SECURITY:", "<<<ANSWER", "মজুরি বাড়ছে কম", "গুরুচণ্ডালী", "computed word count", "MODEL OUTLINE"].every((x) => g1.prompt.includes(x)), "গ্রেডিং প্রম্পটে রুব্রিক, যাচাই করা তথ্য, নিরাপত্তা, মডেল আউটলাইন, শব্দসংখ্যা");
      ok(g2.prompt.includes("EXAMINER 1'S MARKING") && g2.prompt.includes("Lower an award"), "মডারেশন প্রম্পটে পরীক্ষক ১-এর নম্বর ও যাচাইয়ের নির্দেশ");
      ok(g1.len < 262144 && g2.len < 262144, "প্রম্পট ২৫৬ KB সীমার নিচে (" + Math.round(g2.len / 1024) + " KB)");
      const ev = (await state(page)).evals[0];
      ok(ev && ev.total === 22.5 && ev.first === 24.5 && ev.max === 30, "কোডে যোগফল: অতিরিক্ত নম্বর কাটা, প্রমাণহীন নম্বর অর্ধেক, মডারেশন → ২২.৫ (পরীক্ষক ১: ২৪.৫)", JSON.stringify(ev && { t: ev.total, f: ev.first }));
      ok(ev.criteria.find((c) => c.id === "content").award === 5 && ev.criteria.find((c) => c.id === "data").award === 2.5 && ev.criteria.find((c) => c.id === "data").unproven, "AI-র দেওয়া মোট (৩০) উপেক্ষা; প্রমাণ না মেলায় ডেটা ৫ → ২.৫");
      const evt = (await state(page)).events.slice(-1)[0];
      ok(evt.k === "essay" && evt.lang === "bn" && evt.ai && evt.s === 0.75 && evt.evalId === ev.id, "লগ: রচনা (বাংলা), AI, ৭৫% → প্রজেকশনে যোগ হয়");
      const body = await page.locator("main").innerText();
      ok(body.includes("২২.৫/৩০") && body.includes("পরীক্ষক ১: ২৪.৫") && body.includes("প্রমাণ মেলেনি") && body.includes("ডেটা বক্স দিন"), "ফলাফলে নম্বর, পরীক্ষক ১ বনাম চূড়ান্ত, প্রমাণ-সতর্কতা, ৩টি করণীয়");
      await page.getByText("আপনার খাতা (ভুল চিহ্নিত)").click();
      ok(await page.locator(".transcript mark.err").count() >= 1, "খাতার লেখায় ভুল শব্দ লাল দাগে চিহ্নিত");
      ok(await page.evaluate(() => !window.__xss && !document.querySelector(".transcript img")), "খাতার লেখায় HTML/স্ক্রিপ্ট চলে না (XSS নিরাপদ)");
      ok(await noHScroll(page), "ফোনে ফলাফল পাতায় পাশে স্ক্রল নেই");
      await page.evaluate(() => (location.hash = "assess"));
      ok((await page.locator("main").innerText()).includes("AI পরীক্ষকের নম্বর"), "মূল্যায়ন ট্যাবে AI নম্বরের সারাংশ");
      /* B. GK টাইপ করা উত্তর, প্রশ্নভিত্তিক */
      await page.evaluate(() => (location.hash = "ai"));
      await focusBtn(page, "সাধারণ জ্ঞান").click();
      await page.getByRole("button", { name: "⌨️ টাইপ করা উত্তর" }).click();
      await page.locator("#ai-typed").fill("১. ৭.৫%\n২. ৩৫.৫৯\n৩. আহসান মনসুর\n৪. ৩২%");
      await page.getByRole("button", { name: /নম্বর দিন/ }).click();
      await page.waitForSelector("text=প্রশ্নভিত্তিক নম্বর");
      const gk = (await state(page)).evals.slice(-1)[0];
      ok(gk.sec === "GK" && gk.total === 5.5 && gk.items.length === 5 && gk.items[1].award === 2 && gk.items[2].award === 0 && gk.items[3].award === 1.5 && gk.items[4].verdict === "blank", "GK: সঠিক=পূর্ণ, ভুল=০, আংশিক সীমিত, বাদ পড়া=খালি → ৫.৫/১০", JSON.stringify(gk.items.map((i) => i.award)));
      ok(gk.flags.some((f) => f.includes("সব প্রশ্নের ফল দেয়নি")), "AI কোনো প্রশ্ন বাদ দিলে সতর্কতা");
      const gkEv = (await state(page)).events.slice(-1)[0];
      ok(gkEv.k === "gk" && gkEv.n === 5 && Math.abs(gkEv.s - 0.55) < 1e-9, "লগ: GK ৫টি প্রশ্ন, ৫৫%");
      /* C. ইতিহাস, স্পার্কলাইন, বারবার ভুল, কোচ */
      await page.evaluate(() => (location.hash = "ai-history"));
      const ht = await page.locator("main").innerText();
      ok(ht.includes("AI নম্বরের হিসাব") && ht.includes("মূল্যস্ফিতি → মূল্যস্ফীতি") && await page.locator("svg.spark polyline").count() >= 2, "ইতিহাস: অংশভিত্তিক টেবিল, ধারা-রেখা, বারবার ভুলের তালিকা");
      await page.getByRole("button", { name: "রিপোর্ট তৈরি করুন" }).click();
      await page.waitForSelector("text=এখনকার অবস্থা");
      const cc = (await page.evaluate(() => window.__calls)).find((c) => c.task === "COACH_REPORT");
      ok(cc && cc.cache === false && cc.prompt.includes("ফোকাস বাংলা") === false && cc.prompt.includes("AI-MARKED PRACTICE SCRIPTS"), "কোচ রিপোর্ট: সব নম্বর পাঠিয়ে নতুন রিপোর্ট (ক্যাশ ছাড়া)");
      ok((await state(page)).coach && (await state(page)).coach.text.includes("পরিকল্পনা"), "কোচ রিপোর্ট সংরক্ষিত");
      /* D. আবার মূল্যায়ন ও মুছুন */
      await page.getByRole("button", { name: "দেখুন" }).last().click();
      await page.waitForSelector("text=মানদণ্ড অনুযায়ী নম্বর");
      const nCalls = (await page.evaluate(() => window.__calls)).length;
      await page.getByRole("button", { name: "আবার মূল্যায়ন" }).click();
      await page.getByRole("button", { name: "আবার মূল্যায়ন" }).last().click();
      await page.waitForFunction((n) => window.__calls.length >= n + 2 && location.hash === "#ai-result", nCalls);
      await page.waitForTimeout(150);
      const st2 = await state(page);
      const re = (await page.evaluate(() => window.__calls)).slice(nCalls);
      ok(st2.evals.length === 2 && st2.evals.filter((e) => e.sec === "FW_BN").length === 1 && re.every((c) => c.cache === false), "আবার মূল্যায়ন: নতুন করে (ক্যাশ ছাড়া), পুরোনোটি প্রতিস্থাপিত");
      ok(st2.events.filter((e) => e.ai).length === 2, "আগের মূল্যায়নের লগ মুছে নতুন লগ");
      await page.getByRole("button", { name: "মুছুন" }).first().click();
      await page.getByRole("button", { name: "মুছুন" }).last().click();
      await page.waitForTimeout(100);
      const st3 = await state(page);
      ok(st3.evals.length === 1 && st3.events.filter((e) => e.ai).length === 1, "মূল্যায়ন মুছলে তার নম্বরও লগ থেকে মোছে");
      ok(!JSON.stringify(st3).includes("sk-"), "অ্যাপের ডেটায় কোনো key নেই");
      ok(errors.length === 0, "পুরো ফ্লোতে কোনো JS error নেই", errors.join(","));
      await ctx.close();
    }

    /* E. ব্যাচ: প্রতি বারে ২টি ছবি সীমা → ২ বার পড়া, লেখা জোড়া লাগে */
    {
      const { ctx, page, errors } = await newPage(browser, { url: DIST, init: fakeClaude(2), time: "2026-11-21T10:00:00+06:00" });
      await page.evaluate(() => (location.hash = "ai")); await page.waitForSelector("text=মূল্যায়ক: Claude");
      await focusBtn(page, "বাংলা→ইংরেজি অনুবাদ").click();
      await page.setInputFiles("#ai-files", [{ name: "a.png", mimeType: "image/png", buffer: tall }, { name: "b.png", mimeType: "image/png", buffer: tall }]);
      await page.getByRole("button", { name: "১. হাতের লেখা পড়ান" }).click();
      await page.waitForSelector("#ai-tr");
      const cs = await page.evaluate(() => window.__calls);
      ok(cs.length === 2 && cs.every((c) => c.images === 2) && cs[1].prompt.includes("page 2 (top half)"), "সীমা ২ হলে ২ ব্যাচে পড়ে, এক পৃষ্ঠার দুই ভাগ একসাথে থাকে", JSON.stringify(cs.map((c) => c.images)));
      ok((await page.locator("#ai-tr").inputValue()).split("=== পৃষ্ঠা").length - 1 === 2, "২ ব্যাচের লেখা জোড়া লাগে");
      /* ত্রুটি: rate_limited, invalid_json, stop */
      await page.evaluate(() => { window.__fail = [{ code: "rate_limited", message: "x" }]; });
      await page.getByRole("button", { name: /নম্বর দিন/ }).click();
      await page.waitForSelector("text=ব্যবহারসীমা");
      ok((await state(page)).evals.length === 0 && await page.getByRole("button", { name: /নম্বর দিন/ }).isEnabled(), "rate_limited: বার্তা দেখায়, কিছু সংরক্ষণ করে না, আবার চেষ্টা করা যায়");
      await page.evaluate(() => { window.__fail = [{ code: "invalid_json", message: "x", text: "আমি JSON দিতে পারছি না" }]; });
      await page.getByRole("button", { name: /নম্বর দিন/ }).click();
      await page.waitForSelector("text=ঠিক ফরম্যাটে আসেনি");
      ok(await page.locator("text=AI-এর কাঁচা উত্তর").count() === 1, "invalid_json: বার্তা ও কাঁচা উত্তর দেখায়");
      await page.evaluate(() => { window.__delay = 4000; });
      await page.getByRole("button", { name: /নম্বর দিন/ }).click();
      await page.getByRole("button", { name: "থামান" }).click();
      await page.waitForSelector("text=থামানো হয়েছে");
      ok((await state(page)).evals.length === 0 && await page.getByRole("button", { name: /নম্বর দিন/ }).isEnabled(), "থামান: চলমান মূল্যায়ন বাতিল, কিছু সংরক্ষণ হয় না");
      await page.evaluate(() => { window.__delay = 0; window.__fail = [{ code: "not_granted", message: "no" }]; });
      await page.getByRole("button", { name: /নম্বর দিন/ }).click();
      await page.waitForSelector("text=অনুমতি দেননি");
      ok(await page.locator("text=AI মূল্যায়ক চালু নেই").count() >= 1, "not_granted: AI বন্ধ দেখায়, আর অনুরোধ পাঠায় না");
      ok(errors.length === 0, "ত্রুটির পথেও কোনো JS error নেই", errors.join(","));
      await ctx.close();
    }

    /* F. টাইমার → AI, মক প্রশ্নপত্র → AI, রুব্রিক থেকে AI, আজকের কার্ড */
    {
      const { ctx, page, errors } = await newPage(browser, { url: DIST, init: fakeClaude(4), time: "2026-11-21T10:00:00+06:00" });
      ok((await page.locator("main").innerText()).includes("খাতা লিখে AI দিয়ে দেখান"), "আজ ট্যাবে AI কার্ড ও ফোকাস বোতাম");
      await page.evaluate(() => (location.hash = "ai")); await page.waitForSelector("text=মূল্যায়ক: Claude");
      await focusBtn(page, "ব্যাংকিং ও আর্থিক জ্ঞান").click();
      await page.getByRole("button", { name: /৫ মিনিট টাইমার/ }).click();
      await page.clock.fastForward("05:30");
      await page.getByRole("button", { name: "ফলাফল দিন" }).click();
      await page.waitForTimeout(150);
      ok((await page.evaluate(() => location.hash)) === "#ai" && (await state(page)).aiDraft.minutes > 5, "টাইমার শেষে AI পাতায় ফেরে, সময় লেখা থাকে");
      await page.getByRole("button", { name: "বাতিল", exact: true }).click(); await page.getByRole("button", { name: "বাতিল করুন" }).click();
      await page.evaluate(() => (location.hash = "mock"));
      await page.getByRole("button", { name: "পূর্ণ মক শুরু (১২০ মি)" }).click();
      const mockGk = await page.evaluate(() => S.timer.ctx.paper.gk);
      await page.getByRole("button", { name: "📷 GK" }).click();
      const set = (await state(page)).aiDraft.set;
      ok(set.sec === "GK" && set.items.length === 5 && set.items.every((it, i) => it.ref === "gk:" + mockGk[i]), "মক প্রশ্নপত্রের GK খাতা হুবহু একই প্রশ্নে AI-তে যায়");
      await page.evaluate(() => { cancelTimer(); location.hash = "practice-essay"; });
      await page.getByRole("button", { name: "টাইমার ছাড়া লিখেছি: মূল্যায়ন" }).click();
      await page.getByRole("button", { name: "📷 AI দিয়ে দেখান" }).click();
      const s2 = (await state(page)).aiDraft.set;
      ok(s2.sec === "FW_BN" || s2.sec === "FW_EN", "রুব্রিক থেকে এক ক্লিকে AI খাতা দেখা (রচনা)");
      for (const v of ["practice-arg", "practice-tr"]) { await page.evaluate((x) => (location.hash = x), v); ok(await page.getByRole("button", { name: "📷 AI দিয়ে খাতা দেখান" }).count() === 1, v + ": AI বোতাম আছে"); }
      await page.evaluate(() => (location.hash = "ai"));
      await page.getByRole("button", { name: "বাতিল", exact: true }).click(); await page.getByRole("button", { name: "বাতিল করুন" }).click();
      await page.getByText("নিজের প্রশ্ন (বই, মডেল টেস্ট বা বিগত প্রশ্ন থেকে)").click();
      await page.selectOption("#ai-csec", "BN");
      await page.locator("#ai-cq").fill("সন্ধি বিচ্ছেদ করুন: বিদ্যালয়\nশুদ্ধ করুন: সরকারী\nসমাস নির্ণয়: দশানন");
      await page.getByRole("button", { name: "এই প্রশ্নে খাতা দেখান" }).click();
      const cs = (await state(page)).aiDraft.set;
      ok(cs.custom && cs.items.length === 3 && Math.abs(cs.max - 10) < 0.05, "নিজের প্রশ্ন: ৩টি প্রশ্ন, মোট ১০ নম্বর ভাগ");
      await page.evaluate(() => (location.hash = "ai-settings"));
      await page.locator("#ai-strict").uncheck();
      await page.evaluate(() => (location.hash = "ai"));
      ok(await page.getByRole("button", { name: /নম্বর দিন \(দ্রুত\)/ }).count() === 1 && (await state(page)).settings.aiStrict === false, "দ্রুত মোড (১ পরীক্ষক) বেছে নেওয়া যায়");
      ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
      await ctx.close();
    }

    /* G. ক্লাউড আকার সীমা: ৩০টি বড় মূল্যায়ন */
    {
      const big = "ক".repeat(9000);
      const init = fakeClaude(4) + `;(() => { const ev = []; for (let i = 0; i < 34; i++) ev.push({ id: "v" + i, t: Date.now() - i * 1e5, sec: "FW_BN", total: 15, max: 30, transcript: "${big}", improved: "${big.slice(0, 3000)}", question: "q", criteria: [], items: [], errors: [] });
        localStorage.setItem("so-sprint-v1", JSON.stringify({ v: 1, updatedAt: 5, settings: { mult: 5 }, events: [], evals: ev })); })();`;
      const { ctx, page, errors } = await newPage(browser, { url: DIST, init, time: "2026-11-21T10:00:00+06:00" });
      await page.waitForTimeout(400);
      const n = await page.evaluate(() => S.evals.length);
      await page.evaluate(() => { logEvent("news", { n: 1 }); save(); });
      await page.waitForTimeout(1800);
      const w = await page.evaluate(() => window.__dbWrites);
      ok(n === 30, "সর্বোচ্চ ৩০টি মূল্যায়ন রাখে (" + n + ")");
      ok(w.length >= 1 && w[w.length - 1] <= 240000, "ক্লাউডে লেখার আকার ২৪০ KB-এর নিচে (" + Math.round(w[w.length - 1] / 1024) + " KB)");
      ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
      await ctx.close();
    }

    /* H. নিজের API (OpenAI-compatible), claude.ai-র বাইরে */
    {
      const { ctx, page, errors } = await newPage(browser, { time: "2026-11-21T10:00:00+06:00" });
      const reqs = [];
      await page.route("https://router.test/v1/**", async (route) => {
        const req = route.request(); const url = req.url();
        reqs.push({ url, auth: req.headers()["authorization"], body: req.postData() });
        if (url.endsWith("/models")) return route.fulfill({ json: { data: [{ id: "vision-x" }, { id: "grader-y" }] } });
        const b = JSON.parse(req.postData()); const c = b.messages[0].content; const p = typeof c === "string" ? c : c[0].text;
        if (page.__mode === "401") return route.fulfill({ status: 401, json: { error: "bad key" } });
        if (page.__mode === "abort") return route.abort();
        if (page.__mode === "html") return route.fulfill({ status: 200, contentType: "text/html", body: "<html>captcha</html>" });
        const text = p.startsWith("Reply with only this JSON") ? '{"ok":true}' : "<think>ভাবছি</think>```json\n" + makeResp(p, TRANSCRIPT) + "\n```";
        return route.fulfill({ json: { choices: [{ message: { content: makeResp(p, TRANSCRIPT).startsWith("{") ? text : makeResp(p, TRANSCRIPT) }, finish_reason: "stop" }] } });
      });
      await page.evaluate(() => (location.hash = "ai-settings"));
      await page.locator("#ai-base").fill("https://router.test/v1");
      await page.locator("#ai-key").fill("sk-secret-123");
      await page.getByRole("button", { name: "মডেল তালিকা আনুন" }).click();
      await page.waitForSelector("text=২টি মডেল পাওয়া গেছে");
      ok(reqs[0].auth === "Bearer sk-secret-123", "মডেল তালিকা: key Authorization হেডারে যায়");
      await page.locator("#ai-vmodel").fill("vision-x"); await page.locator("#ai-gmodel").fill("grader-y");
      await page.getByRole("button", { name: "সংরক্ষণ" }).click();
      await page.getByRole("button", { name: "সংযোগ পরীক্ষা" }).click();
      await page.waitForSelector("text=সংযোগ ঠিক আছে");
      const cfg = await page.evaluate(() => JSON.parse(localStorage.getItem("so-ai-cfg")));
      ok(cfg.key === "sk-secret-123" && cfg.gradeModel === "grader-y", "key শুধু এই ব্রাউজারের আলাদা জায়গায় (so-ai-cfg)");
      await page.evaluate(() => (location.hash = "ai"));
      await page.waitForSelector("text=মূল্যায়ক: API · grader-y");
      await focusBtn(page, "সাধারণ জ্ঞান").click();
      await page.getByRole("button", { name: "⌨️ টাইপ করা উত্তর" }).click();
      await page.locator("#ai-typed").fill("১. ৭.৫%\n২. ৩৫.৫৯");
      await page.getByRole("button", { name: /নম্বর দিন/ }).click();
      await page.waitForSelector("text=প্রশ্নভিত্তিক নম্বর");
      const chat = reqs.filter((r) => r.url.endsWith("/chat/completions"));
      const b0 = JSON.parse(chat[chat.length - 1].body);
      ok(b0.model === "grader-y" && b0.temperature === 0 && (await state(page)).evals[0].total === 5.5, "নিজের API দিয়ে GK মূল্যায়ন: temperature 0, <think> ও ``` বাদ দিয়ে JSON পড়ে → ৫.৫");
      await page.evaluate(() => (location.hash = "ai"));
      await focusBtn(page, "ফোকাস রাইটিং (বাংলা)").click();
      await page.getByRole("button", { name: "📷 খাতার ছবি" }).click();
      await page.setInputFiles("#ai-files", [{ name: "p.png", mimeType: "image/png", buffer: wide }]);
      await page.getByRole("button", { name: "১. হাতের লেখা পড়ান" }).click();
      await page.waitForSelector("#ai-tr");
      const vb = JSON.parse(reqs.filter((r) => r.url.endsWith("/chat/completions")).slice(-1)[0].body);
      ok(vb.model === "vision-x" && Array.isArray(vb.messages[0].content) && vb.messages[0].content[1].image_url.url.startsWith("data:image/jpeg;base64,"), "ছবি পড়তে ভিশন মডেল, ছবি data URL হিসেবে যায়");
      page.__mode = "401"; await page.getByRole("button", { name: /নম্বর দিন/ }).click(); await page.waitForSelector("text=API key ভুল");
      ok(true, "401: 'API key ভুল' বার্তা");
      page.__mode = "html"; await page.getByRole("button", { name: /নম্বর দিন/ }).click(); await page.waitForSelector("text=ফায়ারওয়াল/ক্যাপচা");
      ok(true, "HTML/ক্যাপচা পেজ এলে স্পষ্ট বার্তা");
      page.__mode = "abort"; await page.getByRole("button", { name: /নম্বর দিন/ }).click(); await page.waitForSelector("text=API-তে পৌঁছানো যায়নি");
      ok(true, "নেটওয়ার্ক/CORS ব্লক হলে স্পষ্ট বার্তা");
      const st = await state(page);
      await page.evaluate(() => (location.hash = "backup"));
      const bk = await page.locator("#bk-out").inputValue();
      ok(!JSON.stringify(st).includes("sk-secret-123") && !bk.includes("sk-secret-123"), "key অ্যাপের ডেটা, ক্লাউড বা ব্যাকআপে যায় না");
      await page.evaluate(() => (location.hash = "ai-settings"));
      await page.getByRole("button", { name: "key মুছুন" }).click(); await page.getByRole("button", { name: "মুছুন", exact: true }).click();
      ok(await page.evaluate(() => localStorage.getItem("so-ai-cfg")) === null, "key মুছে ফেলা যায়");
      ok(errors.length === 0, "কোনো JS error নেই", errors.join(","));
      await ctx.close();
    }
  }

  srv.close();
  await browser.close();
  console.log(results.join("\n"));
  console.log(`\nমোট: ${pass} পাস, ${fail} ফেল`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
