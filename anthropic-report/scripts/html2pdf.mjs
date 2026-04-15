/**
 * html2pdf.mjs — Convert HTML to PDF using Playwright Chromium
 *
 * Usage:
 *   node html2pdf.mjs <input.html> [output.pdf]
 *
 * If output.pdf is omitted, defaults to <input>.pdf in the same directory.
 *
 * Features:
 *   - Waits for document.fonts.ready to ensure remote fonts load
 *   - A4 format with printBackground: true
 *   - Configurable margins (default: 12mm top/bottom, 8mm left/right)
 *
 * Prerequisites:
 *   npm install playwright
 *   npx playwright install chromium
 */

import { chromium } from 'playwright';
import { resolve } from 'path';

const inputHtml = process.argv[2];
if (!inputHtml) {
  console.error('Usage: node html2pdf.mjs <input.html> [output.pdf]');
  process.exit(1);
}

const htmlPath = resolve(inputHtml);
const pdfPath = process.argv[3]
  ? resolve(process.argv[3])
  : htmlPath.replace(/\.html?$/i, '.pdf');

console.log(`Converting: ${htmlPath}`);
console.log(`Output:     ${pdfPath}`);

const browser = await chromium.launch();
const page = await browser.newPage();

// Load the HTML file
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });

// Wait for all fonts to load (including remote @font-face)
await page.evaluate(() => document.fonts.ready);

// Extra buffer for font rendering to stabilize
await page.waitForTimeout(2000);

// Generate PDF
await page.pdf({
  path: pdfPath,
  format: 'A4',
  printBackground: true,
  margin: {
    top: '12mm',
    bottom: '12mm',
    left: '8mm',
    right: '8mm'
  },
  displayHeaderFooter: false
});

await browser.close();
console.log(`✓ PDF saved to: ${pdfPath}`);
