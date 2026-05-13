const pptxgen = require('pptxgenjs');
const fs = require('fs');

if (process.argv.length < 4) {
  console.error("Usage: node build_ppt_v2.js <input_json> <output_pptx>");
  process.exit(1);
}

const dataFile = process.argv[2];
const outFile = process.argv[3];
let data;
try {
  data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
} catch (e) {
  console.error("Failed to read or parse input JSON:", e);
  process.exit(1);
}

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
const F = 'TencentSans W3';       // 正文字体：腾讯体 W3
const F_BOLD = 'TencentSans W7';  // 标题/重点字体：腾讯体 W7
const BLUE = '1A50D6';
const GREEN = '00A45D';
const DARK = '1D2129';
const GRAY = '4E5969';
const LIGHT_GRAY = '86909C';
const BG_LIGHT = 'F7F9FC';
const CARD_BORDER = 'E5EBF5';
const ACCENT_BG = 'EDF2FF';
const WHITE = 'FFFFFF';
const WARN_RED = 'E8553A';
const SUCCESS_GREEN = '00875A';

// ==================== QA QUALITY CONTROL ====================
function estimateLines(text, boxWidthInch, fontSize) {
  if (!text) return 0;
  let chineseCount = (text.match(/[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/g) || []).length;
  let otherCount = text.length - chineseCount;
  let oneInch = fontSize / 72;
  let avgCharW = oneInch * 1.05;
  let avgOtherW = oneInch * 0.55;
  let totalTextWidth = chineseCount * avgCharW + otherCount * avgOtherW;
  return Math.ceil(totalTextWidth / boxWidthInch);
}

function adaptFontSize(text, boxWidthInch, boxHeightInch, baseFontSize, baseLineSpacing) {
  let fs = baseFontSize;
  let ls = baseLineSpacing;
  let minFs = Math.max(7, baseFontSize - 4);
  while (fs >= minFs) {
    let lines = estimateLines(text, boxWidthInch, fs);
    let lineHeightInch = fs / 72 * ls * 1.35;
    let totalHeight = lines * lineHeightInch;
    if (totalHeight <= boxHeightInch) {
      let fillRatio = totalHeight / boxHeightInch;
      if (fillRatio < 0.55 && ls < 2.0) {
        ls = Math.min(2.0, ls + 0.2);
        continue;
      }
      return { fontSize: fs, lineSpacing: ls };
    }
    fs -= 0.5;
    ls = baseLineSpacing;
  }
  return { fontSize: minFs, lineSpacing: baseLineSpacing };
}

function qaCheckSlides(slidesData) {
  let qaReport = [];
  slidesData.forEach((sd, idx) => {
    let issues = [];
    if (sd.type === 'solution_steps' && sd.steps) {
      sd.steps.forEach((step, si) => {
        if (step.desc && step.desc.length > 120) {
          issues.push('Step ' + (si+1) + ' desc (' + step.desc.length + ' chars) may overflow');
        }
      });
    }
    if (sd.type === 'summary' && sd.points) {
      sd.points.forEach((p, pi) => {
        if (p.desc && p.desc.length > 120) {
          issues.push('Point ' + (pi+1) + ' desc (' + p.desc.length + ' chars) may overflow');
        }
      });
    }
    if ((sd.type === 'cards' || !sd.type) && sd.cards) {
      sd.cards.forEach((c, ci) => {
        if (c.desc && c.desc.length > 150) {
          issues.push('Card ' + (ci+1) + ' desc (' + c.desc.length + ' chars) may overflow');
        }
      });
    }
    if (issues.length > 0) {
      qaReport.push({ slide: idx + 1, type: sd.type, issues: issues });
    }
  });
  if (qaReport.length > 0) {
    console.log('[QA] Detected potential issues (auto-adapting font size):');
    qaReport.forEach(r => {
      console.log('  Slide ' + r.slide + ' (' + r.type + '): ' + r.issues.join('; '));
    });
  } else {
    console.log('[QA] All slides passed quality check.');
  }
  return qaReport;
}

// ==================== HELPER FUNCTIONS ====================

function addHeaderBar(slide) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 0.25, w: 1.2, h: 0.07, fill: { color: BLUE }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 1.7, y: 0.25, w: 0.8, h: 0.07, fill: { color: GREEN }
  });
  slide.addText("\u817E\u8BAF\u667A\u6167\u96F6\u552E\u4E0E\u751F\u6D3B\u4EA7\u4E1A", {
    x: 6.5, y: 0.15, w: 3, h: 0.3,
    fontFace: F, fontSize: 9, color: LIGHT_GRAY, align: 'right'
  });
}

function addPageNumber(slide, num, total) {
  slide.addText(num + " / " + total, {
    x: 8.5, y: 5.15, w: 1, h: 0.3,
    fontFace: F, fontSize: 9, color: LIGHT_GRAY, align: 'right'
  });
}

// ==================== SLIDE TEMPLATES ====================

// --- TYPE: cover ---
function buildCover(slide, d) {
  slide.background = { color: BLUE };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 0.5, w: 2.5, h: 0.06, fill: { color: GREEN }
  });
  if (d.sceneTag) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: 1.2, w: 2.2, h: 0.4, fill: { color: '2D6AE0' }, rectRadius: 0.05
    });
    slide.addText(d.sceneTag, {
      x: 0.5, y: 1.2, w: 2.2, h: 0.4,
      fontFace: F, fontSize: 12, color: WHITE, align: 'center', valign: 'middle'
    });
  }
  // 封面主标题 → W7
  slide.addText(d.title || "", {
    x: 0.5, y: 1.8, w: 8.5, h: 1.0,
    fontFace: F_BOLD, fontSize: 32, color: WHITE, lineSpacingMultiple: 1.2
  });
  // 封面副标题 → W3
  if (d.subtitle) {
    slide.addText(d.subtitle, {
      x: 0.5, y: 2.9, w: 8.5, h: 0.5,
      fontFace: F, fontSize: 14, color: 'B0C4FF', lineSpacingMultiple: 1.2
    });
  }
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 4.8, w: 10, h: 0.7, fill: { color: '0F3BA8' }
  });
  let bottomParts = [];
  if (d.source) bottomParts.push("\u6848\u4F8B\u6765\u6E90\uFF1A" + d.source);
  if (d.industry) bottomParts.push("\u884C\u4E1A\uFF1A" + d.industry);
  if (d.scale) bottomParts.push("\u89C4\u6A21\uFF1A" + d.scale);
  if (bottomParts.length > 0) {
    slide.addText(bottomParts.join("    |    "), {
      x: 0.5, y: 4.85, w: 9, h: 0.5,
      fontFace: F, fontSize: 10, color: 'A0BCFF', align: 'left', valign: 'middle'
    });
  }
}

// --- TYPE: pain_points ---
function buildPainPoints(slide, d) {
  slide.background = { color: WHITE };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.title || "\u4E1A\u52A1\u73B0\u72B6\u4E0E\u6838\u5FC3\u75DB\u70B9", {
    x: 0.5, y: 0.55, w: 8, h: 0.5,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  // 页面副标题 → W3
  if (d.subtitle) {
    slide.addText(d.subtitle, {
      x: 0.5, y: 1.05, w: 8, h: 0.35,
      fontFace: F, fontSize: 11, color: LIGHT_GRAY
    });
  }
  const items = d.items || [];
  const startY = 1.6;
  const itemH = 0.72;
  const gap = 0.12;
  items.forEach((item, i) => {
    let yPos = startY + i * (itemH + gap);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: yPos, w: 0.06, h: itemH, fill: { color: WARN_RED }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.56, y: yPos, w: 8.94, h: itemH,
      fill: { color: 'FFF7F5' }, line: { color: 'FFE0D9', width: 0.5 }
    });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.75, y: yPos + 0.12, w: 0.85, h: 0.28, fill: { color: WARN_RED }, rectRadius: 0.04
    });
    // 痛点标签 → W7
    slide.addText(item.label || ("\u75DB\u70B9" + (i + 1)), {
      x: 0.75, y: yPos + 0.12, w: 0.85, h: 0.28,
      fontFace: F_BOLD, fontSize: 9, color: WHITE, align: 'center', valign: 'middle'
    });
    // 痛点标题 → W7
    slide.addText(item.title || "", {
      x: 1.75, y: yPos + 0.08, w: 7.5, h: 0.3,
      fontFace: F_BOLD, fontSize: 12, color: DARK
    });
    // 痛点描述 → W3
    slide.addText(item.desc || "", {
      x: 1.75, y: yPos + 0.38, w: 7.5, h: 0.3,
      fontFace: F, fontSize: 10, color: GRAY
    });
  });
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// --- TYPE: solution_steps ---
function buildSolutionSteps(slide, d) {
  slide.background = { color: WHITE };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.title || "\u7CFB\u7EDF\u89E3\u6CD5\u4E0E\u5B9E\u65BD\u8DEF\u5F84", {
    x: 0.5, y: 0.55, w: 8, h: 0.5,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  if (d.subtitle) {
    slide.addText(d.subtitle, {
      x: 0.5, y: 1.05, w: 8, h: 0.35,
      fontFace: F, fontSize: 11, color: LIGHT_GRAY
    });
  }
  const steps = d.steps || [];
  const N = steps.length;
  const totalW = 9.0;
  const stepGap = 0.15;
  const stepW = (totalW - (N - 1) * stepGap) / N;
  const stepStartY = 1.6;
  const stepH = 3.5;

  steps.forEach((step, i) => {
    let xPos = 0.5 + i * (stepW + stepGap);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: stepStartY, w: stepW, h: stepH,
      fill: { color: BG_LIGHT }, line: { color: CARD_BORDER, width: 0.5 },
      shadow: { type: 'outer', blur: 6, offset: 2, angle: 45, color: 'E0E6F1', opacity: 0.4 }
    });
    let circleSize = 0.45;
    slide.addShape(pres.shapes.OVAL, {
      x: xPos + (stepW - circleSize) / 2, y: stepStartY + 0.25, w: circleSize, h: circleSize,
      fill: { color: BLUE }
    });
    slide.addText("" + (i + 1), {
      x: xPos + (stepW - circleSize) / 2, y: stepStartY + 0.25, w: circleSize, h: circleSize,
      fontFace: F_BOLD, fontSize: 16, color: WHITE, align: 'center', valign: 'middle'
    });
    // 步骤标题 → W7
    slide.addText(step.title || "", {
      x: xPos + 0.1, y: stepStartY + 0.85, w: stepW - 0.2, h: 0.4,
      fontFace: F_BOLD, fontSize: 12, color: DARK, align: 'center', valign: 'middle'
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos + 0.2, y: stepStartY + 1.3, w: stepW - 0.4, h: 0.02, fill: { color: CARD_BORDER }
    });
    // 步骤描述 → W3
    let descBoxW = stepW - 0.3;
    let descBoxH = stepH - 1.7;
    let descAdapt = adaptFontSize(step.desc || "", descBoxW, descBoxH, 10, 1.5);
    slide.addText(step.desc || "", {
      x: xPos + 0.15, y: stepStartY + 1.4, w: descBoxW, h: descBoxH,
      fontFace: F, fontSize: descAdapt.fontSize, color: GRAY,
      lineSpacingMultiple: descAdapt.lineSpacing, valign: 'top'
    });
    if (i < N - 1) {
      let arrowX = xPos + stepW + stepGap * 0.1;
      slide.addText("\u25B6", {
        x: arrowX, y: stepStartY + stepH / 2 - 0.15, w: stepGap * 0.8, h: 0.3,
        fontFace: 'Arial', fontSize: 12, color: BLUE, align: 'center', valign: 'middle'
      });
    }
  });
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// --- TYPE: pitfalls ---
function buildPitfalls(slide, d) {
  slide.background = { color: WHITE };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.title || "\u843D\u5730\u907F\u5751\u4E0E\u65B9\u6848\u8FED\u4EE3", {
    x: 0.5, y: 0.55, w: 8, h: 0.5,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  if (d.subtitle) {
    slide.addText(d.subtitle, {
      x: 0.5, y: 1.05, w: 8, h: 0.35,
      fontFace: F, fontSize: 11, color: LIGHT_GRAY
    });
  }
  const leftW = 4.3;
  const rightW = 4.3;
  const colGap = 0.4;
  const colStartY = 1.6;
  const colH = 3.6;

  // Left: pitfall column
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: colStartY, w: leftW, h: colH,
    fill: { color: 'FFF7F5' }, line: { color: 'FFE0D9', width: 0.8 },
    shadow: { type: 'outer', blur: 4, offset: 1, angle: 45, color: 'F0E0E0', opacity: 0.3 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: colStartY, w: leftW, h: 0.45, fill: { color: WARN_RED }
  });
  // 列标题 → W7
  slide.addText("\u2718  \u5E38\u89C1\u5751\u70B9 / \u65E9\u671F\u6311\u6218", {
    x: 0.5, y: colStartY, w: leftW, h: 0.45,
    fontFace: F_BOLD, fontSize: 13, color: WHITE, align: 'center', valign: 'middle'
  });
  const pitfalls = d.pitfalls || [];
  pitfalls.forEach((item, i) => {
    let yPos = colStartY + 0.6 + i * 0.72;
    slide.addText("\u26A0", {
      x: 0.7, y: yPos, w: 0.3, h: 0.25,
      fontFace: 'Arial', fontSize: 12, align: 'center', valign: 'middle'
    });
    // 坑点标题 → W7
    slide.addText(item.title || "", {
      x: 1.05, y: yPos, w: leftW - 0.75, h: 0.25,
      fontFace: F_BOLD, fontSize: 11, color: DARK
    });
    // 坑点描述 → W3
    slide.addText(item.desc || "", {
      x: 1.05, y: yPos + 0.28, w: leftW - 0.75, h: 0.35,
      fontFace: F, fontSize: 9, color: GRAY, lineSpacingMultiple: 1.5
    });
  });

  // Right: optimization column
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5 + leftW + colGap, y: colStartY, w: rightW, h: colH,
    fill: { color: 'F0FFF7' }, line: { color: 'B8E6CD', width: 0.8 },
    shadow: { type: 'outer', blur: 4, offset: 1, angle: 45, color: 'D0F0E0', opacity: 0.3 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5 + leftW + colGap, y: colStartY, w: rightW, h: 0.45, fill: { color: SUCCESS_GREEN }
  });
  // 列标题 → W7
  slide.addText("\u2714  \u4F18\u5316\u65B9\u6848 / \u8FED\u4EE3\u7ECF\u9A8C", {
    x: 0.5 + leftW + colGap, y: colStartY, w: rightW, h: 0.45,
    fontFace: F_BOLD, fontSize: 13, color: WHITE, align: 'center', valign: 'middle'
  });
  const fixes = d.fixes || [];
  fixes.forEach((item, i) => {
    let yPos = colStartY + 0.6 + i * 0.72;
    slide.addText("\u2705", {
      x: 0.5 + leftW + colGap + 0.2, y: yPos, w: 0.3, h: 0.25,
      fontFace: 'Arial', fontSize: 12, align: 'center', valign: 'middle'
    });
    // 优化标题 → W7
    slide.addText(item.title || "", {
      x: 0.5 + leftW + colGap + 0.55, y: yPos, w: rightW - 0.75, h: 0.25,
      fontFace: F_BOLD, fontSize: 11, color: DARK
    });
    // 优化描述 → W3
    slide.addText(item.desc || "", {
      x: 0.5 + leftW + colGap + 0.55, y: yPos + 0.28, w: rightW - 0.75, h: 0.35,
      fontFace: F, fontSize: 9, color: GRAY, lineSpacingMultiple: 1.5
    });
  });
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// --- TYPE: results ---
function buildResults(slide, d) {
  slide.background = { color: WHITE };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.title || "\u4E1A\u52A1\u6210\u6548\u4E0E\u4EF7\u503C\u9A8C\u8BC1", {
    x: 0.5, y: 0.55, w: 8, h: 0.5,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  if (d.subtitle) {
    slide.addText(d.subtitle, {
      x: 0.5, y: 1.05, w: 8, h: 0.35,
      fontFace: F, fontSize: 11, color: LIGHT_GRAY
    });
  }
  const metrics = d.metrics || [];
  const N = metrics.length;
  const totalW = 9.0;
  const mGap = 0.2;
  const mW = (totalW - (N - 1) * mGap) / N;
  const mStartY = 1.55;
  const mH = 1.6;

  metrics.forEach((m, i) => {
    let xPos = 0.5 + i * (mW + mGap);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: mStartY, w: mW, h: mH,
      fill: { color: ACCENT_BG }, line: { color: 'D0DBFF', width: 0.8 },
      shadow: { type: 'outer', blur: 6, offset: 2, angle: 45, color: 'D8E2F8', opacity: 0.4 }
    });
    // 大数字 → W7
    slide.addText(m.value || "", {
      x: xPos, y: mStartY + 0.15, w: mW, h: 0.7,
      fontFace: F_BOLD, fontSize: 36, color: BLUE, align: 'center', valign: 'middle'
    });
    // 指标名称 → W7
    slide.addText(m.label || "", {
      x: xPos + 0.1, y: mStartY + 0.9, w: mW - 0.2, h: 0.25,
      fontFace: F_BOLD, fontSize: 12, color: DARK, align: 'center', valign: 'middle'
    });
    // 指标补充 → W3
    if (m.sub) {
      slide.addText(m.sub, {
        x: xPos + 0.1, y: mStartY + 1.18, w: mW - 0.2, h: 0.3,
        fontFace: F, fontSize: 9, color: GRAY, align: 'center', valign: 'top'
      });
    }
  });

  const takeaways = d.takeaways || [];
  if (takeaways.length > 0) {
    let taStartY = mStartY + mH + 0.3;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: taStartY, w: totalW, h: 0.04, fill: { color: CARD_BORDER }
    });
    // "核心结论"标签 → W7
    slide.addText("\u6838\u5FC3\u7ED3\u8BBA", {
      x: 0.5, y: taStartY + 0.15, w: 1.2, h: 0.3,
      fontFace: F_BOLD, fontSize: 11, color: BLUE
    });
    // 结论正文 → W3
    takeaways.forEach((t, i) => {
      slide.addText("\u25CF  " + t, {
        x: 0.5, y: taStartY + 0.5 + i * 0.38, w: totalW, h: 0.35,
        fontFace: F, fontSize: 11, color: DARK, lineSpacingMultiple: 1.2
      });
    });
  }
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// --- TYPE: cards ---
function buildCards(slide, d) {
  slide.background = { color: WHITE };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.mainTitle || d.title || "", {
    x: 0.5, y: 0.55, w: 8, h: 0.45,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  if (d.subTitle || d.subtitle) {
    slide.addText(d.subTitle || d.subtitle, {
      x: 0.5, y: 1.05, w: 8, h: 0.35,
      fontFace: F, fontSize: 11, color: LIGHT_GRAY
    });
  }
  const startY = 1.55;
  const maxW = 9.0;
  const maxH = 3.6;
  const colSpace = 0.18;
  const rowSpace = 0.18;
  const cards = d.cards || [];
  const N = cards.length;
  let cols = N <= 3 ? N : (N <= 4 ? 2 : (N <= 6 ? 3 : 4));
  let rows = Math.ceil(N / cols);
  const colW = (maxW - (cols - 1) * colSpace) / cols;
  const rowH = (maxH - (rows - 1) * rowSpace) / rows;

  cards.forEach((item, i) => {
    let row = Math.floor(i / cols);
    let col = i % cols;
    let xPos = 0.5 + col * (colW + colSpace);
    let yPos = startY + row * (rowH + rowSpace);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: yPos, w: colW, h: rowH,
      fill: { color: WHITE }, line: { color: CARD_BORDER, width: 0.8 },
      shadow: { type: 'outer', blur: 8, offset: 2, angle: 45, color: 'E0E6F1', opacity: 0.5 }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: yPos + 0.25, w: 0.05, h: rowH - 0.5, fill: { color: BLUE }
    });
    let circleSize = 0.35;
    slide.addShape(pres.shapes.OVAL, {
      x: xPos + 0.18, y: yPos + 0.2, w: circleSize, h: circleSize, fill: { color: ACCENT_BG }
    });
    slide.addText("" + (i + 1), {
      x: xPos + 0.18, y: yPos + 0.2, w: circleSize, h: circleSize,
      fontFace: F_BOLD, fontSize: 11, color: BLUE, align: 'center', valign: 'middle'
    });
    if (item.dep) {
      let depW = 0.85;
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: xPos + colW - depW - 0.12, y: yPos + 0.22, w: depW, h: 0.25,
        fill: { color: 'F4F5F7' }, rectRadius: 0.03
      });
      slide.addText(item.dep, {
        x: xPos + colW - depW - 0.12, y: yPos + 0.22, w: depW, h: 0.25,
        fontFace: F, fontSize: 8, color: LIGHT_GRAY, align: 'center', valign: 'middle'
      });
    }
    // 卡片标题 → W7
    slide.addText(item.title || "", {
      x: xPos + 0.6, y: yPos + 0.18, w: colW - 1.7, h: 0.35,
      fontFace: F_BOLD, fontSize: 11, color: DARK, valign: 'middle'
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos + 0.15, y: yPos + 0.6, w: colW - 0.3, h: 0.015, fill: { color: CARD_BORDER }
    });
    // 卡片正文 → W3
    let cardDescW = colW - 0.36;
    let cardDescH = rowH - 0.85;
    let cardAdapt = adaptFontSize(item.desc || "", cardDescW, cardDescH, 9.5, 1.5);
    slide.addText(item.desc || "", {
      x: xPos + 0.18, y: yPos + 0.65, w: cardDescW, h: cardDescH,
      fontFace: F, fontSize: cardAdapt.fontSize, color: GRAY,
      lineSpacingMultiple: cardAdapt.lineSpacing, valign: 'top'
    });
  });
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// --- TYPE: summary ---
function buildSummary(slide, d) {
  slide.background = { color: BG_LIGHT };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.title || "\u6838\u5FC3\u542F\u793A\u4E0E\u8FC1\u79FB\u4EF7\u503C", {
    x: 0.5, y: 0.55, w: 8, h: 0.5,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  const points = d.points || [];
  const totalW = 9.0;
  const pGap = 0.18;
  const pW = (totalW - (points.length - 1) * pGap) / points.length;
  const pStartY = 1.4;
  const pH = 3.5;

  points.forEach((p, i) => {
    let xPos = 0.5 + i * (pW + pGap);
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: pStartY, w: pW, h: pH,
      fill: { color: WHITE }, line: { color: CARD_BORDER, width: 0.8 },
      shadow: { type: 'outer', blur: 6, offset: 2, angle: 45, color: 'D8E2F8', opacity: 0.4 }
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos, y: pStartY, w: pW, h: 0.06, fill: { color: BLUE }
    });
    // 编号 → W7
    slide.addText(p.icon || ("0" + (i + 1)), {
      x: xPos, y: pStartY + 0.25, w: pW, h: 0.5,
      fontFace: F_BOLD, fontSize: 24, color: BLUE, align: 'center', valign: 'middle'
    });
    // 启示标题 → W7
    slide.addText(p.title || "", {
      x: xPos + 0.15, y: pStartY + 0.85, w: pW - 0.3, h: 0.4,
      fontFace: F_BOLD, fontSize: 13, color: DARK, align: 'center', valign: 'middle'
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: xPos + 0.2, y: pStartY + 1.3, w: pW - 0.4, h: 0.02, fill: { color: CARD_BORDER }
    });
    // 启示正文 → W3
    let pointDescW = pW - 0.3;
    let pointDescH = pH - 1.75;
    let pointAdapt = adaptFontSize(p.desc || "", pointDescW, pointDescH, 10, 1.5);
    slide.addText(p.desc || "", {
      x: xPos + 0.15, y: pStartY + 1.45, w: pointDescW, h: pointDescH,
      fontFace: F, fontSize: pointAdapt.fontSize, color: GRAY,
      lineSpacingMultiple: pointAdapt.lineSpacing, valign: 'top'
    });
  });
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// --- TYPE: image_ref ---
function getImageDimensions(filePath) {
  try {
    let buf = fs.readFileSync(filePath);
    if (buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4E && buf[3] === 0x47) {
      let w = buf.readUInt32BE(16);
      let h = buf.readUInt32BE(20);
      return { width: w, height: h };
    }
    if (buf[0] === 0xFF && buf[1] === 0xD8) {
      let offset = 2;
      while (offset < buf.length - 9) {
        if (buf[offset] !== 0xFF) { offset++; continue; }
        let marker = buf[offset + 1];
        if (marker === 0xC0 || marker === 0xC2) {
          let h = buf.readUInt16BE(offset + 5);
          let w = buf.readUInt16BE(offset + 7);
          return { width: w, height: h };
        }
        let segLen = buf.readUInt16BE(offset + 2);
        offset += 2 + segLen;
      }
    }
  } catch (e) { /* ignore */ }
  return null;
}

function buildImageRef(slide, d) {
  slide.background = { color: WHITE };
  addHeaderBar(slide);
  // 页面标题 → W7
  slide.addText(d.title || "", {
    x: 0.5, y: 0.55, w: 8, h: 0.5,
    fontFace: F_BOLD, fontSize: 22, color: DARK
  });
  if (d.subtitle) {
    slide.addText(d.subtitle, {
      x: 0.5, y: 1.05, w: 8, h: 0.35,
      fontFace: F, fontSize: 11, color: LIGHT_GRAY
    });
  }
  let imgPath = d.imagePath || "";
  let imgStartY = d.subtitle ? 1.55 : 1.3;
  let maxImgH = 3.7;
  let maxImgW = 9.0;
  let sourceY = imgStartY + maxImgH + 0.05;

  if (imgPath && fs.existsSync(imgPath)) {
    let dims = getImageDimensions(imgPath);
    let finalW = maxImgW;
    let finalH = maxImgH;
    let finalX = 0.5;
    let finalY = imgStartY;

    if (dims && dims.width > 0 && dims.height > 0) {
      let ratio = dims.width / dims.height;
      let fitByWidth_W = maxImgW;
      let fitByWidth_H = maxImgW / ratio;
      let fitByHeight_H = maxImgH;
      let fitByHeight_W = maxImgH * ratio;
      if (fitByWidth_H <= maxImgH) {
        finalW = fitByWidth_W;
        finalH = fitByWidth_H;
      } else {
        finalW = fitByHeight_W;
        finalH = fitByHeight_H;
      }
      finalX = 0.5 + (maxImgW - finalW) / 2;
      finalY = imgStartY + (maxImgH - finalH) / 2;
    }

    slide.addShape(pres.shapes.RECTANGLE, {
      x: finalX - 0.05, y: finalY - 0.05, w: finalW + 0.1, h: finalH + 0.1,
      fill: { color: BG_LIGHT }, line: { color: CARD_BORDER, width: 0.5 },
      shadow: { type: 'outer', blur: 4, offset: 1, angle: 45, color: 'E0E6F1', opacity: 0.3 }
    });
    slide.addImage({
      path: imgPath,
      x: finalX, y: finalY, w: finalW, h: finalH
    });
    sourceY = finalY + finalH + 0.08;
  } else {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: imgStartY, w: maxImgW, h: maxImgH,
      fill: { color: BG_LIGHT }, line: { color: CARD_BORDER, width: 1, dashType: 'dash' }
    });
    slide.addText("[" + (imgPath ? "\u56FE\u7247\u672A\u627E\u5230: " + imgPath : "\u672A\u6307\u5B9A\u56FE\u7247\u8DEF\u5F84") + "]", {
      x: 0.5, y: imgStartY, w: maxImgW, h: maxImgH,
      fontFace: F, fontSize: 12, color: LIGHT_GRAY, align: 'center', valign: 'middle'
    });
  }
  if (d.source) {
    slide.addText("\u56FE\u7247\u6765\u6E90\uFF1A" + d.source, {
      x: 0.5, y: sourceY, w: maxImgW, h: 0.25,
      fontFace: F, fontSize: 8, color: LIGHT_GRAY, italic: true
    });
  }
  addPageNumber(slide, d._pageNum || '', d._totalPages || '');
}

// ==================== MAIN BUILDER ====================

qaCheckSlides(data.slides);

const totalPages = data.slides.length;
data.slides.forEach((sd, idx) => {
  let slide = pres.addSlide();
  sd._pageNum = idx + 1;
  sd._totalPages = totalPages;

  switch (sd.type) {
    case 'cover':       buildCover(slide, sd); break;
    case 'pain_points': buildPainPoints(slide, sd); break;
    case 'solution_steps': buildSolutionSteps(slide, sd); break;
    case 'pitfalls':    buildPitfalls(slide, sd); break;
    case 'results':     buildResults(slide, sd); break;
    case 'summary':     buildSummary(slide, sd); break;
    case 'image_ref':   buildImageRef(slide, sd); break;
    case 'cards':       buildCards(slide, sd); break;
    default:            buildCards(slide, sd); break;
  }
});

pres.writeFile({ fileName: outFile }).then(() => {
  console.log('PPT generated successfully at ' + outFile);
}).catch(err => {
  console.error('Error generating PPT:', err);
  process.exit(1);
});
