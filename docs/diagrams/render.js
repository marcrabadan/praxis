// Render the lifecycle infographics (*.infographic.html) to PNG with headless Chrome.
//
//   npm i -D puppeteer-core          # or set PUPPETEER_CORE to a checkout
//   CHROME=/path/to/chrome node docs/diagrams/render.js
//
// CHROME defaults to a puppeteer-managed Chrome if present. Output PNGs land
// next to the HTML at 2x device scale.
const path = require('path');
const puppeteer = require(process.env.PUPPETEER_CORE || 'puppeteer-core');

const CHROME =
  process.env.CHROME ||
  process.env.PUPPETEER_EXECUTABLE_PATH ||
  '/root/.cache/puppeteer/chrome/linux-148.0.7778.97/chrome-linux64/chrome';

const dir = __dirname;
const jobs = [
  ['product-developer-life-cycle.infographic.html', 'product-developer-life-cycle.png'],
  ['software-developer-life-cycle.infographic.html', 'software-developer-life-cycle.png'],
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--force-color-profile=srgb'],
  });
  for (const [inFile, outFile] of jobs) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1240, height: 1400, deviceScaleFactor: 2 });
    await page.goto('file://' + path.join(dir, inFile), { waitUntil: 'networkidle0' });
    await new Promise((r) => setTimeout(r, 350)); // let emoji/fonts settle
    await page.screenshot({ path: path.join(dir, outFile), fullPage: true });
    console.log('rendered', outFile);
    await page.close();
  }
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
