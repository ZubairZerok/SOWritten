// HTML → A4 PDF (Chromium via Playwright). Usage: node make_pdf.js in.html out.pdf
const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(inp), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: out, format: "A4", printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: "<span></span>",
    footerTemplate: '<div style="width:100%;text-align:center;font-family:Times New Roman,serif;font-size:8px;color:#555">Page <span class="pageNumber"></span> of <span class="totalPages"></span> · SO Model Answer Script (practice copy)</div>',
  });
  await browser.close();
  console.log("PDF:", out);
})().catch((e) => { console.error(e); process.exit(1); });
