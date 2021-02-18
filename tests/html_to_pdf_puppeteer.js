const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('file://C:/Users/ljtal/Documents/CV_Maker/CV.html', {
    waitUntil: 'networkidle2',
  });
  await page.pdf({ path: 'CV_from_js.pdf', format: 'a4' });

  await browser.close();
})();