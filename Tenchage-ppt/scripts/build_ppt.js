/**
 * Tenchage-ppt v2.0 — 多布局 PPT 生成引擎
 * 腾讯智慧零售与生活产业路演风格
 *
 * 支持布局：cards | summary | table | compare | phases | kpi | hierarchy
 *
 * 用法：node build_ppt.js <input_json> <output_pptx>
 */

const pptxgen = require('pptxgenjs');
const fs = require('fs');

// ── 参数校验 ──────────────────────────────────────────────────
if (process.argv.length < 4) {
  console.error('Usage: node build_ppt.js <input_json> <output_pptx>');
  process.exit(1);
}

const dataFile = process.argv[2];
const outFile  = process.argv[3];
let data;

try {
  data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
} catch (e) {
  console.error('Failed to read or parse input JSON:', e);
  process.exit(1);
}

// ── 常量 ──────────────────────────────────────────────────────
const FONT_W3 = '腾讯体 W3';
const FONT_W7 = '腾讯体 W7';
const M    = 0.5;   // 左边距
const CW   = 9.0;   // 内容区宽

const CLR = {
  blue:      '1A50D6',  // 腾讯蓝
  green:     '00A45D',  // 腾讯绿
  dark:      '1D2129',  // 深黑
  body:      '4E5969',  // 中灰正文
  note:      '86909C',  // 浅灰注释
  border:    'E5EBF5',  // 卡片边框
  shadow:    'E0E6F1',  // 卡片阴影
  lightBlue: 'EDF2FF',  // 极浅蓝
  lightGray: 'F4F5F7',  // 极浅灰
  white:     'FFFFFF',
  risk:      'C62828',  // 深红
  medBlue:   '4E82C5',  // 中蓝（流程中期）
  ltBlue:    '7CB3E0',  // 浅蓝（流程长期）
};

// ── 主题覆写（在 CLR 之后执行）────────────────────────────
if (data && data.theme === 'red') {
  CLR.blue    = 'C62828';   // 深红（主色）
  CLR.green   = 'B71C1C';   // 极深红（替代绿色元素）
  CLR.medBlue = 'D32F2F';   // 中红
  CLR.ltBlue  = 'E53935';   // 浅红
  CLR.lightBlue = 'FFCDD2'; // 极浅红底
}

if (data && data.theme === 'orange') {
  CLR.blue    = 'E65100';   // 深橙（主色）
  CLR.green   = 'FF8F00';   // 琥珀橙（替代绿色元素）
  CLR.medBlue = 'FF7A2E';   // 中橙
  CLR.ltBlue  = 'FFAB40';   // 浅橙
  CLR.lightBlue = 'FFF3E0'; // 极浅橙底
}

// ── 创建演示文稿 ──────────────────────────────────────────────
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const startPage  = data.startPage || 1;

// ── 通用工具函数 ──────────────────────────────────────────────

/** 添加文字 */
function t(s, text, x, y, w, h, opts) {
  let fontFace = FONT_W3;
  if (opts && opts.bold) {
    fontFace = FONT_W7;
  }
  if (opts && opts.fontFace) {
    fontFace = opts.fontFace;
  }
  s.addText(String(text), { x, y, w, h, fontFace: fontFace, ...opts });
}

/** 添加矩形 */
function box(s, x, y, w, h, fill, borderColor, borderW) {
  const shapeOpts = { x, y, w, h };
  if (fill) shapeOpts.fill = { color: fill };
  if (borderColor) shapeOpts.line = { color: borderColor, width: borderW || 0.5 };
  s.addShape(pres.shapes.RECTANGLE, shapeOpts);
}

/** 添加水平线 */
function hln(s, x, y, w, color, pw) {
  s.addShape(pres.shapes.LINE, {
    x, y, w, h: 0,
    line: { color: color || CLR.border, width: pw || 0.5 },
  });
}

/** 添加卡片阴影矩形 */
function cardBox(s, x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: CLR.white },
    line: { color: CLR.border, width: 1 },
    shadow: { type: 'outer', blur: 10, offset: 3, angle: 45, color: CLR.shadow, opacity: 0.6 },
  });
}

// ── 页面公共元素 ──────────────────────────────────────────────

function renderPageCommon(slide, slideData, idx) {
  // 白色背景
  slide.background = { color: CLR.white };

  // 标题由各布局渲染器自行处理（quad_loop 等布局有特殊需求，不走公共标题）
  if (slideData.skipCommonTitle) {
    // 页码
    t(slide, '-' + (startPage + idx) + '-', 8.5, 5.2, 1, 0.3, {
      fontSize: 10, color: CLR.body, bold: true, align: 'right',
    });
    return;
  }

  // 主标题
  t(slide, slideData.mainTitle || '主标题', M, 0.45, 8, 0.4, {
    fontSize: 24, color: CLR.dark, bold: true,
  });

  // 副标题（可选）
  if (slideData.actionTitle) {
    t(slide, slideData.actionTitle, M, 1.05, CW, 0.3, {
      fontSize: 12, color: CLR.blue, bold: true,
    });
  } else if (slideData.subTitle) {
    t(slide, '\u89E3\u51B3\u201C' + slideData.subTitle + '\u201D', M, 1.05, 8, 0.3, {
      fontSize: 12, color: CLR.body, bold: true,
    });
  }

  // 页码
  t(slide, '-' + (startPage + idx) + '-', 8.5, 5.2, 1, 0.3, {
    fontSize: 10, color: CLR.body, bold: true, align: 'right',
  });
}

/** 简单矩形（不带阴影边框） */
function s_rect(slide, x, y, w, h, fill) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill },
  });
}

// ══════════════════════════════════════════════════════════════
//  布局渲染器
// ══════════════════════════════════════════════════════════════

// ── 1. cards — 模块化卡片 ────────────────────────────────────
function renderCards(slide, d) {
  const cards = d.cards || [];
  if (!cards.length) return;

  const startY = 1.8, maxW = 9.0, maxH = 3.4;
  const colSpace = 0.2, rowSpace = 0.2;
  const N = cards.length;

  let cols, rows;
  if (N <= 3)      { cols = N; rows = 1; }
  else if (N <= 4) { cols = 2; rows = 2; }
  else if (N <= 6) { cols = 3; rows = 2; }
  else             { cols = 4; rows = 2; }

  const colW = (maxW - (cols - 1) * colSpace) / cols;
  const rowH = (maxH - (rows - 1) * rowSpace) / rows;

  cards.forEach((item, i) => {
    const row = Math.floor(i / cols);
    const col = i % cols;
    const xPos = M + col * (colW + colSpace);
    const yPos = startY + row * (rowH + rowSpace);

    // 卡片背景+阴影
    cardBox(slide, xPos, yPos, colW, rowH);

    // 左侧蓝色竖条
    s_rect(slide, xPos, yPos + 0.3, 0.06, rowH - 0.6, CLR.blue);

    // 编号圆形
    slide.addShape(pres.shapes.OVAL, {
      x: xPos + 0.2, y: yPos + 0.25, w: 0.35, h: 0.35,
      fill: { color: CLR.lightBlue },
    });
    t(slide, String(i + 1), xPos + 0.2, yPos + 0.25, 0.35, 0.35, {
      fontFace: 'Arial', fontSize: 12, color: CLR.blue,
      bold: true, align: 'center', valign: 'middle',
    });

    // 依赖标签（可选）
    let depW = 0;
    if (item.dep) {
      depW = Math.min(1.0, colW * 0.3);
      s_rect(slide, xPos + colW - depW - 0.1, yPos + 0.28, depW, 0.25, CLR.lightGray);
      t(slide, item.dep, xPos + colW - depW - 0.1, yPos + 0.28, depW, 0.25, {
        fontSize: 8, color: CLR.note, align: 'center', valign: 'middle',
      });
    }

    // 卡片标题
    const titleW = colW - 0.65 - depW;
    t(slide, item.title || '', xPos + 0.6, yPos + 0.2, titleW, 0.4, {
      fontSize: 12, color: CLR.dark, valign: 'middle',
    });

    // tagline 大字标签（可选，放在标题与正文之间）
    let descYOffset = 0.65;
    if (item.tagline) {
      t(slide, item.tagline, xPos + 0.2, yPos + 0.6, colW - 0.4, 0.45, {
        fontSize: 18, color: CLR.blue, bold: true, valign: 'middle',
      });
      descYOffset = 1.05;
    }

    // 描述正文
    t(slide, item.desc || '', xPos + 0.2, yPos + descYOffset, colW - 0.4, rowH - descYOffset - 0.15, {
      fontSize: 10, color: CLR.body, align: 'left', valign: 'top',
      lineSpacingMultiple: 1.2,
    });
  });
}

// ── 2. summary — 执行摘要 ────────────────────────────────────
function renderSummary(slide, d) {
  const bodyY = 1.7;

  // 结论段
  if (d.conclusion) {
    t(slide, d.conclusion, M, bodyY, CW, 0.5, {
      fontSize: 13, color: CLR.dark, bold: true, valign: 'top',
      lineSpacingMultiple: 1.3,
    });
  }

  // 分项要点
  const points = d.points || [];
  const pStartY = d.conclusion ? bodyY + 0.6 : bodyY;
  const pHeight = 0.55;

  points.forEach((pt, i) => {
    const y = pStartY + i * pHeight;

    // 蓝色方块 bullet
    s_rect(slide, M, y + 0.08, 0.1, 0.1, CLR.blue);

    // 粗体标签
    t(slide, pt.label || '', M + 0.2, y, 1.5, 0.3, {
      fontSize: 11.5, color: CLR.blue, bold: true, valign: 'middle',
    });

    // 正文描述
    t(slide, pt.text || '', M + 1.7, y, CW - 1.7, 0.3, {
      fontSize: 11, color: CLR.body, valign: 'middle',
      lineSpacingMultiple: 1.2,
    });

    // 分隔线（最后一项不加）
    if (i < points.length - 1) {
      hln(slide, M, y + pHeight - 0.05, CW, CLR.border, 0.5);
    }
  });
}

// ── 3. table — 比较表格 ──────────────────────────────────────
function renderTable(slide, d) {
  const columns = d.columns || [];
  const rows    = d.rows    || [];
  if (!columns.length) return;

  const tableY = 1.7;
  const colCount = columns.length;
  const colW = CW / colCount;
  const headerH = 0.4;
  const rowH = 0.5;

  // 表头
  columns.forEach((col, i) => {
    s_rect(slide, M + i * colW, tableY, colW, headerH, CLR.blue);
    t(slide, col, M + i * colW, tableY, colW, headerH, {
      fontSize: 11, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });
  });

  // 数据行
  rows.forEach((row, ri) => {
    const y = tableY + headerH + ri * rowH;
    const bgColor = ri % 2 === 0 ? CLR.lightGray : CLR.white;

    row.forEach((cell, ci) => {
      // 行底色
      s_rect(slide, M + ci * colW, y, colW, rowH, bgColor);
      // 边框
      slide.addShape(pres.shapes.RECTANGLE, {
        x: M + ci * colW, y, w: colW, h: rowH,
        fill: { type: 'none' },
        line: { color: CLR.border, width: 0.5 },
      });
      // 文字
      t(slide, cell || '', M + ci * colW + 0.1, y, colW - 0.2, rowH, {
        fontSize: 10, color: ci === 0 ? CLR.dark : CLR.body,
        bold: ci === 0, valign: 'middle',
        lineSpacingMultiple: 1.1,
      });
    });
  });

  // 底部评论条
  if (d.commentary) {
    const commY = tableY + headerH + rows.length * rowH + 0.1;
    s_rect(slide, M, commY, CW, 0.35, CLR.lightBlue);
    s_rect(slide, M, commY, 0.06, 0.35, CLR.blue);
    t(slide, d.commentary, M + 0.15, commY, CW - 0.25, 0.35, {
      fontSize: 9, color: CLR.body, valign: 'middle',
    });
  }
}

// ── 4. compare — 双栏对比 ────────────────────────────────────
function renderCompare(slide, d) {
  const gap = 0.3;
  const halfW = (CW - gap) / 2;
  const bodyY = 1.7;
  const headerH = 0.4;
  const itemH = 0.55;

  // 左栏表头（腾讯蓝）
  s_rect(slide, M, bodyY, halfW, headerH, CLR.blue);
  t(slide, d.leftTitle || '对比项A', M, bodyY, halfW, headerH, {
    fontSize: 13, color: CLR.white, bold: true, align: 'center', valign: 'middle',
  });

  // 右栏表头（腾讯绿，差异化）
  const rightX = M + halfW + gap;
  s_rect(slide, rightX, bodyY, halfW, headerH, CLR.green);
  t(slide, d.rightTitle || '对比项B', rightX, bodyY, halfW, headerH, {
    fontSize: 13, color: CLR.white, bold: true, align: 'center', valign: 'middle',
  });

  // 中间竖虚线
  slide.addShape(pres.shapes.LINE, {
    x: M + halfW + gap / 2, y: bodyY + headerH, w: 0, h: Math.max((d.leftItems || []).length, (d.rightItems || []).length) * itemH,
    line: { color: CLR.border, width: 1, dashType: 'dash' },
  });

  // 左栏条目
  (d.leftItems || []).forEach((item, i) => {
    const y = bodyY + headerH + i * itemH;
    const bgColor = i % 2 === 0 ? CLR.lightGray : CLR.white;
    s_rect(slide, M, y, halfW, itemH, bgColor);
    s_rect(slide, M, y, 0.06, itemH, CLR.blue);

    // 序号圆
    slide.addShape(pres.shapes.OVAL, {
      x: M + 0.15, y: y + 0.12, w: 0.28, h: 0.28,
      fill: { color: CLR.blue },
    });
    t(slide, String(i + 1), M + 0.15, y + 0.12, 0.28, 0.28, {
      fontFace: 'Arial', fontSize: 10, color: CLR.white,
      bold: true, align: 'center', valign: 'middle',
    });

    t(slide, item, M + 0.55, y, halfW - 0.65, itemH, {
      fontSize: 10, color: CLR.body, valign: 'middle',
      lineSpacingMultiple: 1.15,
    });
  });

  // 右栏条目
  (d.rightItems || []).forEach((item, i) => {
    const y = bodyY + headerH + i * itemH;
    const bgColor = i % 2 === 0 ? CLR.lightGray : CLR.white;
    s_rect(slide, rightX, y, halfW, itemH, bgColor);
    s_rect(slide, rightX, y, 0.06, itemH, CLR.green);

    // 序号圆
    slide.addShape(pres.shapes.OVAL, {
      x: rightX + 0.15, y: y + 0.12, w: 0.28, h: 0.28,
      fill: { color: CLR.green },
    });
    t(slide, String(i + 1), rightX + 0.15, y + 0.12, 0.28, 0.28, {
      fontFace: 'Arial', fontSize: 10, color: CLR.white,
      bold: true, align: 'center', valign: 'middle',
    });

    t(slide, item, rightX + 0.55, y, halfW - 0.65, itemH, {
      fontSize: 10, color: CLR.body, valign: 'middle',
      lineSpacingMultiple: 1.15,
    });
  });
}

// ── 5. phases — 三阶段流程 ───────────────────────────────────
function renderPhases(slide, d) {
  const phases = d.phases || [];
  if (!phases.length) return;

  const bodyY = 1.7;
  const gap = 0.1;
  const colCount = phases.length;
  const colW = (CW - (colCount - 1) * gap) / colCount;
  const headerH = 0.42;
  const itemH = 0.55;

  const colorMap = {
    dark:   CLR.blue,
    medium: CLR.medBlue,
    light:  CLR.ltBlue,
  };

  phases.forEach((phase, pi) => {
    const x = M + pi * (colW + gap);
    const phaseColor = colorMap[phase.color] || CLR.blue;

    // 阶段标题块
    s_rect(slide, x, bodyY, colW, headerH, phaseColor);
    t(slide, phase.name || 'Phase ' + (pi + 1), x, bodyY, colW, headerH, {
      fontSize: 12, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });

    // 行动项
    (phase.items || []).forEach((item, ii) => {
      const y = bodyY + headerH + ii * itemH;
      const bgColor = ii % 2 === 0 ? CLR.lightGray : CLR.white;

      s_rect(slide, x, y, colW, itemH, bgColor);
      s_rect(slide, x, y, 0.06, itemH, phaseColor);

      t(slide, item, x + 0.15, y, colW - 0.25, itemH, {
        fontSize: 10, color: CLR.body, valign: 'middle',
        lineSpacingMultiple: 1.15,
      });
    });
  });

  // 底部时间轴箭头
  const maxItems = Math.max(...phases.map(p => (p.items || []).length));
  const arrowY = bodyY + headerH + maxItems * itemH + 0.15;

  slide.addShape(pres.shapes.LINE, {
    x: M, y: arrowY, w: CW, h: 0,
    line: { color: CLR.blue, width: 1.5, endArrowType: 'arrow' },
  });

  // 时间轴刻度
  phases.forEach((phase, pi) => {
    const x = M + pi * (colW + gap) + colW / 2;
    slide.addShape(pres.shapes.LINE, {
      x, y: arrowY - 0.06, w: 0, h: 0.12,
      line: { color: CLR.blue, width: 1 },
    });
  });
}

// ── 6. kpi — KPI 大数字 ──────────────────────────────────────
function renderKpi(slide, d) {
  const metrics = d.metrics || [];
  if (!metrics.length) return;

  const bodyY = 1.8;
  const barH = 1.8;
  const n = metrics.length;
  const gap = 0.15;
  const itemW = (CW - (n - 1) * gap) / n;

  metrics.forEach((metric, i) => {
    const x = M + i * (itemW + gap);
    const isHl = metric.highlight;

    // 背景色块
    s_rect(slide, x, bodyY, itemW, barH, isHl ? CLR.blue : CLR.lightBlue);

    // 白色竖线分隔（非第一个）
    if (i > 0) {
      slide.addShape(pres.shapes.LINE, {
        x: x - gap / 2, y: bodyY + 0.2, w: 0, h: barH - 0.4,
        line: { color: CLR.border, width: 0.75 },
      });
    }

    // 大数字
    t(slide, metric.value || '0', x, bodyY + 0.2, itemW, barH * 0.55, {
      fontSize: 36, bold: true,
      color: isHl ? CLR.white : CLR.blue,
      align: 'center', valign: 'middle',
    });

    // 标签
    t(slide, metric.label || '', x, bodyY + barH * 0.6, itemW, barH * 0.35, {
      fontSize: 11,
      color: isHl ? 'B8D4E8' : CLR.body,
      align: 'center', valign: 'middle',
    });
  });

  // 底部装饰线
  hln(slide, M, bodyY + barH + 0.15, CW, CLR.blue, 1.5);
}

// ── 7. hierarchy — 架构/层级 ─────────────────────────────────
function renderHierarchy(slide, d) {
  const layers = d.layers || [];
  if (!layers.length) return;

  const bodyY = 1.7;

  // 中心标题块
  if (d.centerTitle) {
    const centerW = 3.2;
    const centerX = M + (CW - centerW) / 2;
    s_rect(slide, centerX, bodyY, centerW, 0.5, CLR.blue);
    t(slide, d.centerTitle, centerX, bodyY, centerW, 0.5, {
      fontSize: 14, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });
  }

  // 层级渐变颜色
  const layerColors = [CLR.blue, CLR.medBlue, CLR.ltBlue, 'B8D4E8'];
  const layerStartY = d.centerTitle ? bodyY + 0.65 : bodyY;
  const layerH = 0.7;
  const layerGap = 0.08;

  layers.forEach((layer, li) => {
    const y = layerStartY + li * (layerH + layerGap);
    const color = layerColors[li % layerColors.length];

    // 层标题（左侧竖条+标签）
    s_rect(slide, M, y, 0.06, layerH, color);
    t(slide, layer.title || '', M + 0.15, y, 1.5, 0.3, {
      fontSize: 11, color: CLR.dark, bold: true, valign: 'middle',
    });

    // 层内 items 横排小卡片
    const items = layer.items || [];
    const itemStartX = M + 1.7;
    const itemAreaW = CW - 1.7;
    const itemGap = 0.12;
    const itemW = items.length > 0 ? (itemAreaW - (items.length - 1) * itemGap) / items.length : itemAreaW;

    items.forEach((item, ii) => {
      const ix = itemStartX + ii * (itemW + itemGap);
      // 小卡片背景
      cardBox(slide, ix, y + 0.05, itemW, layerH - 0.1);
      // 顶部色条
      s_rect(slide, ix, y + 0.05, itemW, 0.05, color);
      // 文字
      t(slide, item, ix + 0.08, y + 0.12, itemW - 0.16, layerH - 0.22, {
        fontSize: 9.5, color: CLR.body, align: 'center', valign: 'middle',
      });
    });
  });
}

// ── 8. split_1_2 — 左1右2(上下)拆分 ────────────────────────────
function renderSplit12(slide, d) {
  const gap = 0.2;
  const startY = 1.7;
  const maxH = 3.6;
  
  // Left: 1/3, Right: 2/3
  const leftW = CW * 0.35 - gap / 2; 
  const rightW = CW * 0.65 - gap / 2;
  const rightX = M + leftW + gap;
  
  // -- 左侧宽卡片 (深色背景定调) --
  const leftH = maxH;
  s_rect(slide, M, startY, leftW, leftH, CLR.dark); // 深黑底色
  if (d.leftCard) {
    t(slide, d.leftCard.title || '', M + 0.25, startY + 0.2, leftW - 0.5, 0.35, {
      fontSize: 13, color: CLR.white, bold: true, align: 'left',
    });
    // 渲染段落
    const desc = d.leftCard.desc || '';
    t(slide, desc, M + 0.25, startY + 0.6, leftW - 0.5, leftH - 0.7, {
      fontSize: 9.5, color: CLR.white, lineSpacingMultiple: 1.25, valign: 'top'
    });
  }
  
  // -- 右侧上卡片 --
  const rightCardH = (maxH - gap) / 2;
  if (d.rightTopCard) {
    cardBox(slide, rightX, startY, rightW, rightCardH);
    s_rect(slide, rightX, startY, 0.06, rightCardH, CLR.blue);
    
    t(slide, d.rightTopCard.title || '', rightX + 0.2, startY + 0.15, rightW - 0.4, 0.3, {
      fontSize: 14, color: CLR.dark, bold: true
    });
    t(slide, d.rightTopCard.subTitle || '', rightX + 0.2, startY + 0.45, rightW - 0.4, 0.25, {
      fontSize: 11, color: CLR.blue, bold: true
    });
    
    const rtItems = d.rightTopCard.items || [];
    if (rtItems.length > 0) {
      t(slide, rtItems.join('\n'), rightX + 0.2, startY + 0.75, rightW - 0.4, rightCardH - 0.85, {
        fontSize: 10, color: CLR.body, lineSpacingMultiple: 1.3, bullet: { type: 'bullet' }, valign: 'top'
      });
    }
  }
  
  // -- 右侧下卡片 --
  const rbY = startY + rightCardH + gap;
  if (d.rightBottomCard) {
    cardBox(slide, rightX, rbY, rightW, rightCardH);
    s_rect(slide, rightX, rbY, 0.06, rightCardH, CLR.green);
    
    t(slide, d.rightBottomCard.title || '', rightX + 0.2, rbY + 0.15, rightW - 0.4, 0.3, {
      fontSize: 14, color: CLR.dark, bold: true
    });
    t(slide, d.rightBottomCard.subTitle || '', rightX + 0.2, rbY + 0.45, rightW - 0.4, 0.25, {
      fontSize: 11, color: CLR.green, bold: true
    });
    
    const rbItems = d.rightBottomCard.items || [];
    if (rbItems.length > 0) {
      t(slide, rbItems.join('\n'), rightX + 0.2, rbY + 0.75, rightW - 0.4, rightCardH - 0.85, {
        fontSize: 10, color: CLR.body, lineSpacingMultiple: 1.3, bullet: { type: 'bullet' }, valign: 'top'
      });
    }
  }
}

// ── 8.5 split_1_4 — 左1右4(2x2)拆分 ────────────────────────────
function renderSplit14(slide, d) {
  const gap = 0.2;
  const startY = 1.7;
  const maxH = 3.6;
  
  // Left: 1/3, Right: 2/3
  const leftW = CW * 0.32; 
  const rightAreaW = CW - leftW - gap;
  const rightX = M + leftW + gap;
  
  // -- 左侧大卡片 (痛点) --
  const leftH = maxH;
  s_rect(slide, M, startY, leftW, leftH, CLR.lightGray); // 浅灰底色
  s_rect(slide, M, startY, 0.06, leftH, CLR.risk);       // 深红警示色竖条
  if (d.leftCard) {
    t(slide, d.leftCard.title || '', M + 0.25, startY + 0.15, leftW - 0.4, 0.4, {
      fontSize: 16, color: CLR.risk, bold: true, align: 'left',
    });
    
    // 渲染段落
    const desc = d.leftCard.desc || [];
    t(slide, desc.join('\n'), M + 0.25, startY + 0.7, leftW - 0.4, leftH - 0.8, {
      fontSize: 11, color: CLR.body, lineSpacingMultiple: 1.35, valign: 'top'
    });
  }
  
  // -- 右侧 4 卡片 (2x2) --
  const rightCards = d.rightCards || [];
  const rCols = 2;
  const rRows = 2;
  const rColW = (rightAreaW - gap) / 2;
  const rRowH = (maxH - gap) / 2;
  
  rightCards.forEach((item, i) => {
    if (i >= 4) return;
    const row = Math.floor(i / rCols);
    const col = i % rCols;
    const cx = rightX + col * (rColW + gap);
    const cy = startY + row * (rRowH + gap);
    
    cardBox(slide, cx, cy, rColW, rRowH);
    s_rect(slide, cx, cy, 0.06, rRowH, CLR.blue);
    
    // 标题
    t(slide, item.title || '', cx + 0.2, cy + 0.1, rColW - 0.3, 0.35, {
      fontSize: 13, color: CLR.dark, bold: true
    });
    
    // 标签
    if (item.tag) {
      s_rect(slide, cx + rColW - 0.9, cy + 0.15, 0.8, 0.25, CLR.blue);
      t(slide, item.tag, cx + rColW - 0.9, cy + 0.15, 0.8, 0.25, {
        fontSize: 9, color: CLR.white, bold: true, align: 'center', valign: 'middle'
      });
    }
    
    // 内容
    const itemsText = Array.isArray(item.desc) ? item.desc.join('\n') : (item.desc || '');
    t(slide, itemsText, cx + 0.2, cy + 0.55, rColW - 0.4, rRowH - 0.65, {
      fontSize: 10, color: CLR.body, lineSpacingMultiple: 1.3, bullet: { type: 'bullet' }, valign: 'top'
    });
  });
  
  // -- 中间引出箭头 --
  slide.addShape(pres.shapes.RIGHT_ARROW, {
    x: M + leftW - 0.05, y: startY + maxH / 2 - 0.15, w: gap + 0.1, h: 0.3,
    fill: { color: CLR.blue },
    line: { type: 'none' }
  });
}

// ── 9. cards_outlined — 描边卡片（6 卡模板） ──────────────────────────────
// 图片参考：3 列 × 2 行，编号+粗体标题在卡片框外上方，标题旁蓝色渐变标签，
// 内容区为浅灰描边圆角矩形（白色填充、无弥散阴影），内部 bullet 列表。
function renderCardsOutlined(slide, d) {
  const cards = d.cards || [];
  if (!cards.length) return;

  // ── intro 正文段（主标题下方的描述性文字，可选） ──
  let startY = 1.15;
  if (d.intro) {
    t(slide, d.intro, M, startY, CW, 0.45, {
      fontSize: 10.5, color: CLR.body, align: 'left', valign: 'top',
      lineSpacingMultiple: 1.3,
    });
    startY += 0.55;
  } else {
    startY = 1.7;
  }

  const N = cards.length;
  const maxW = 9.0;
  // 有 footerBar 时为卡片区预留更少高度
  const maxH = d.footerBar ? 3.1 : 3.5;
  const colSpace = 0.25;
  const rowSpace = 0.25;

  // 自适应行列（与 cards 类似但优化 5-6 张为 3 列）
  let cols, rows;
  if (N <= 3)      { cols = N; rows = 1; }
  else if (N <= 4) { cols = 2; rows = 2; }
  else if (N <= 6) { cols = 3; rows = 2; }
  else             { cols = 4; rows = 2; }

  const colW = (maxW - (cols - 1) * colSpace) / cols;
  const rowH = (maxH - (rows - 1) * rowSpace) / rows;

  // 标题行高度（编号+标题+标签在卡片框外上方）
  const headerRowH = 0.35;
  // 内容框高度
  const contentH = rowH - headerRowH - 0.08;

  // 标签颜色方案（蓝色渐变系列）
  const tagColors = [
    { fill: CLR.blue,    text: CLR.white },
    { fill: CLR.blue,    text: CLR.white },
    { fill: CLR.blue,    text: CLR.white },
    { fill: CLR.medBlue, text: CLR.white },
    { fill: CLR.medBlue, text: CLR.white },
    { fill: CLR.ltBlue,  text: CLR.white },
    { fill: CLR.ltBlue,  text: CLR.white },
    { fill: 'B8D4E8',   text: CLR.dark  },
  ];

  cards.forEach((item, i) => {
    const row = Math.floor(i / cols);
    const col = i % cols;
    const xPos = M + col * (colW + colSpace);
    const yPos = startY + row * (rowH + rowSpace);

    // ── 1. 编号 + 标题（卡片外上方）──
    const numStr = String(i + 1).padStart(2, '0');
    const titleText = numStr + '  ' + (item.title || '');
    t(slide, titleText, xPos, yPos, colW * 0.6, headerRowH, {
      fontSize: 13, color: CLR.dark, bold: true, valign: 'bottom',
    });

    // ── 2. 右侧标签色块（蓝色纯色填充 + 圆角） ──
    if (item.tag) {
      const tagW = Math.min(1.2, colW * 0.4);
      const tagH = 0.22;
      const tagX = xPos + colW - tagW;
      const tagY = yPos + (headerRowH - tagH) / 2 + 0.04;
      const tagStyle = tagColors[i % tagColors.length];

      // 纯色标签背景（pptxgenjs shape 不支持渐变，用纯色替代）
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: tagX, y: tagY, w: tagW, h: tagH,
        rectRadius: 0.04,
        fill: { color: tagStyle.fill },
        line: { type: 'none' },
      });
      t(slide, item.tag, tagX, tagY, tagW, tagH, {
        fontSize: 8.5, color: tagStyle.text, bold: true,
        align: 'center', valign: 'middle',
      });
    }

    // ── 3. 内容区描边圆角矩形（浅灰边框、白色填充、无阴影） ──
    const contentY = yPos + headerRowH + 0.05;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: xPos, y: contentY, w: colW, h: contentH,
      rectRadius: 0.08,
      fill: { color: CLR.white },
      line: { color: CLR.border, width: 1.0 },
      // 无 shadow 属性 → 没有弥散阴影
    });

    // ── 4. 内容文字（bullet 列表，"·" 前缀风格，支持 <b> 富文本高亮） ──
    // desc 可以是字符串（换行分隔）或数组
    let descLines = [];
    if (Array.isArray(item.desc)) {
      descLines = item.desc;
    } else if (typeof item.desc === 'string') {
      descLines = item.desc.split('\n').filter(Boolean);
    }

    // 构造富文本 runs，支持 <b>xxx</b> 蓝色加粗高亮
    const runs = [];
    descLines.forEach((line, li) => {
      if (li > 0) {
        runs.push({ text: '\n', options: { fontSize: 10, fontFace: FONT_W3 } });
      }
      // 空行：仅换行
      const trimmed = String(line).replace(/^[\s·\-•]+/, '').trim();
      if (!trimmed) return;
      // bullet 前缀
      runs.push({
        text: '\u00B7 ',
        options: { fontSize: 10, color: CLR.body, fontFace: FONT_W3 },
      });
      // 识别 <b>xxx</b>
      const parts = trimmed.split(/(<b>[^<]+<\/b>)/);
      parts.forEach((p) => {
        if (!p) return;
        const m = p.match(/^<b>([^<]+)<\/b>$/);
        if (m) {
          runs.push({
            text: m[1],
            options: { fontSize: 10, color: CLR.blue, bold: true, fontFace: FONT_W7 },
          });
        } else {
          runs.push({
            text: p,
            options: { fontSize: 10, color: CLR.body, fontFace: FONT_W3 },
          });
        }
      });
    });

    slide.addText(runs, {
      x: xPos + 0.15, y: contentY + 0.1, w: colW - 0.3, h: contentH - 0.2,
      align: 'left', valign: 'top',
      lineSpacingMultiple: 1.35,
    });
  });

  // ── footerBar：底部蓝色横条（类似原图底部的核心价值条） ──
  if (d.footerBar) {
    const barH = 0.35;
    const barY = 5.625 - 0.45 - barH; // 页面底部上方留空
    const barW = CW;
    // 蓝色圆角条
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: barY, w: barW, h: barH,
      rectRadius: 0.05,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });
    t(slide, d.footerBar, M, barY, barW, barH, {
      fontSize: 9.5, color: CLR.white, bold: true,
      align: 'center', valign: 'middle',
    });
  }
}

// ══════════════════════════════════════════════════════════════
//  trinity_pillars — 三位一体·三支柱版（每柱 3 子卡）
//  用途：顶层方案、战略总览这类"3 × 3"信息密度页面
//  自渲染标题（skipCommonTitle=true）
// ══════════════════════════════════════════════════════════════
function _runsFromText(str, baseSize, baseColor, hlColor) {
  const runs = [];
  const parts = String(str || '').split(/(<b>[^<]+<\/b>)/);
  parts.forEach((p) => {
    if (!p) return;
    const m = p.match(/^<b>([^<]+)<\/b>$/);
    if (m) {
      runs.push({ text: m[1], options: { fontSize: baseSize, color: hlColor, bold: true, fontFace: FONT_W7 } });
    } else {
      runs.push({ text: p, options: { fontSize: baseSize, color: baseColor, fontFace: FONT_W3 } });
    }
  });
  return runs;
}

function renderTrinityPillars(slide, d) {
  // ── 2026-04-20 v7 同款瘦身：徽章与主标题同行、主标题 20pt、顶部整体压缩 ──
  let cursorY = 0.28;

  // ── 1. 徽章与主标题同行 ──
  const bt = d.topBadge ? String(d.topBadge) : '';
  const bw = bt ? Math.max(1.4, bt.length * 0.18 + 0.5) : 0;
  const rowH = 0.42;

  if (bt) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: cursorY + 0.05, w: bw, h: 0.32,
      rectRadius: 0.05,
      fill: { color: CLR.lightBlue },
      line: { color: CLR.blue, width: 0.75 },
    });
    t(slide, bt, M, cursorY + 0.05, bw, 0.32, {
      fontSize: 10, color: CLR.blue, bold: true,
      align: 'center', valign: 'middle',
    });
  }

  // 主标题（含 <b> 高亮，20pt，与徽章同一行）
  const titleStr = d.mainTitle || '三位一体打法';
  const titleParts = String(titleStr).split(/(<b>[^<]+<\/b>)/);
  const titleRuns = [];
  titleParts.forEach((p) => {
    if (!p) return;
    const m = p.match(/^<b>([^<]+)<\/b>$/);
    if (m) {
      titleRuns.push({ text: m[1], options: { fontSize: 20, color: CLR.blue, bold: true, fontFace: FONT_W7 } });
    } else {
      titleRuns.push({ text: p, options: { fontSize: 20, color: CLR.dark, bold: true, fontFace: FONT_W7 } });
    }
  });
  const titleX = bt ? (M + bw + 0.18) : M;
  const titleW = bt ? (CW - bw - 0.18) : CW;
  slide.addText(titleRuns, {
    x: titleX, y: cursorY, w: titleW, h: rowH,
    align: 'left', valign: 'middle',
  });
  cursorY += rowH + 0.04;

  // ── 2. 副标题（可选） ──
  if (d.subTitle) {
    t(slide, d.subTitle, M, cursorY, CW, 0.28, {
      fontSize: 11, color: CLR.note, align: 'left', valign: 'middle',
    });
    cursorY += 0.3;
  }

  // ── 4. 三支柱 ──
  const pillars = d.pillars || [];
  if (!pillars.length) return;
  const N = Math.min(3, pillars.length);
  const gap = 0.2;
  const colW = (CW - (N - 1) * gap) / N;

  const hasFooter = !!d.footerBar;
  const footerH = hasFooter ? 0.5 : 0;
  const pillarY = cursorY + 0.08;
  const pillarH = 5.2 - pillarY - footerH - 0.05;

  pillars.slice(0, N).forEach((pillar, pIdx) => {
    const px = M + pIdx * (colW + gap);

    // 柱体底板
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: px, y: pillarY, w: colW, h: pillarH,
      rectRadius: 0.06,
      fill: { color: CLR.lightBlue },
      line: { color: CLR.border, width: 0.5 },
    });

    // ── 头部区（固定约 1/4 柱高）──
    // 包含：蓝底白字徽章 + 柱主标题
    const headerH = Math.min(0.95, pillarH * 0.22);
    let headerY = pillarY + 0.14;

    // 头部徽章（蓝底白字胶囊，更醒目）
    const badgeStr = pillar.badge || '';
    if (badgeStr) {
      const bw = Math.max(1.0, badgeStr.length * 0.22 + 0.3);
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: px + 0.2, y: headerY, w: bw, h: 0.3,
        rectRadius: 0.15,
        fill: { color: CLR.blue },
        line: { type: 'none' },
      });
      t(slide, badgeStr, px + 0.2, headerY, bw, 0.3, {
        fontSize: 10, color: CLR.white, bold: true,
        align: 'center', valign: 'middle',
      });
      headerY += 0.4;
    }

    // 柱主标题（含 <b> 高亮）
    const ptStr = pillar.title || '';
    const ptParts = String(ptStr).split(/(<b>[^<]+<\/b>)/);
    const ptRuns = [];
    ptParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        ptRuns.push({ text: m[1], options: { fontSize: 15, color: CLR.blue, bold: true, fontFace: FONT_W7 } });
      } else {
        ptRuns.push({ text: p, options: { fontSize: 15, color: CLR.dark, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(ptRuns, {
      x: px + 0.2, y: headerY, w: colW - 0.4, h: 0.38,
      align: 'left', valign: 'middle',
    });

    // ── 子卡区（剩余约 3/4）──
    const items = pillar.items || [];
    if (!items.length) return;
    const subAreaY = pillarY + 0.14 + headerH + 0.1;
    const subAreaH = pillarY + pillarH - subAreaY - 0.15;
    const subGap = 0.12;
    const subH = (subAreaH - (items.length - 1) * subGap) / items.length;

    items.forEach((it, iIdx) => {
      const sy = subAreaY + iIdx * (subH + subGap);
      const sx = px + 0.2;
      const sw = colW - 0.4;

      // 白底子卡
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: sx, y: sy, w: sw, h: subH,
        rectRadius: 0.05,
        fill: { color: CLR.white },
        line: { type: 'none' },
      });
      // 左侧蓝色竖条
      slide.addShape(pres.shapes.RECTANGLE, {
        x: sx, y: sy, w: 0.07, h: subH,
        fill: { color: CLR.blue },
        line: { type: 'none' },
      });

      // 布局：上半部分标题（1行），下半部分描述（1行）
      const titleH = subH * 0.45;
      const descH = subH * 0.45;
      const padX = 0.2;

      // 子卡标题（统一 bold）
      const stRuns = _runsFromText(it.title, 12, CLR.dark, CLR.blue).map(r => ({
        text: r.text,
        options: { ...r.options, bold: true, fontFace: FONT_W7 },
      }));
      slide.addText(stRuns, {
        x: sx + padX, y: sy + subH * 0.08, w: sw - padX - 0.1, h: titleH,
        align: 'left', valign: 'middle',
      });

      // 子卡描述（一行，不换行）
      if (it.desc) {
        const sdRuns = _runsFromText(it.desc, 9, CLR.body, CLR.blue);
        slide.addText(sdRuns, {
          x: sx + padX, y: sy + subH * 0.5, w: sw - padX - 0.1, h: descH,
          align: 'left', valign: 'middle',
          wrap: false,
        });
      }
    });
  });

  // ── 5. 底部结论条（带左侧标签胶囊 + 高亮文字） ──
  if (d.footerBar) {
    const barH = 0.4;
    const barY = 5.625 - 0.45 - barH;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: barY, w: CW, h: barH,
      rectRadius: 0.05,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });

    // 左侧白底胶囊标签
    const lblStr = d.footerLabel || '三位一体 · 落地';
    const lblW = Math.max(1.4, lblStr.length * 0.18 + 0.4);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M + 0.12, y: barY + 0.07, w: lblW, h: barH - 0.14,
      rectRadius: 0.04,
      fill: { color: CLR.white },
      line: { type: 'none' },
    });
    t(slide, lblStr, M + 0.12, barY + 0.07, lblW, barH - 0.14, {
      fontSize: 9.5, color: CLR.blue, bold: true,
      align: 'center', valign: 'middle',
    });

    // 右侧主结论（支持 <b> 高亮成更亮的浅蓝/白）
    const fbStr = d.footerBar;
    const fbParts = String(fbStr).split(/(<b>[^<]+<\/b>)/);
    const fbRuns = [];
    fbParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        fbRuns.push({ text: m[1], options: { fontSize: 11, color: 'FFE082', bold: true, fontFace: FONT_W7 } });
      } else {
        fbRuns.push({ text: p, options: { fontSize: 10.5, color: CLR.white, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(fbRuns, {
      x: M + lblW + 0.3, y: barY, w: CW - lblW - 0.42, h: barH,
      align: 'left', valign: 'middle',
    });
  }
}

// ══════════════════════════════════════════════════════════════
//  breakthrough_trio — 破局三栏对比（痛点 / 资产 / 机会）
//  用途：战略拐点类开篇页，3 栏递进色（橙/蓝/绿）
//  每栏包含：头部徽章（中文） + 单行标题 + 强化框 + 要点列表
//  ⛔ 禁止：英文装饰字 enNote / 右上角 01 02 03 数字水印
//  ✅ 顶部区压缩到 ≤1.4"，给下面子卡片留充足空间
//  自渲染标题（skipCommonTitle=true）
// ══════════════════════════════════════════════════════════════
function renderBreakthroughTrio(slide, d) {
  // 三色配色主题（橙/蓝/绿）
  const THEMES = [
    { main: 'FF7A2E', light: 'FFF4ED', watermark: 'FFD9C2', name: 'orange' },
    { main: '2F6BFF', light: 'EAF1FF', watermark: 'C2D4FB', name: 'blue' },
    { main: '16A37A', light: 'E8F6EF', watermark: 'BEE5D5', name: 'green' },
  ];

  let cursorY = 0.32;

  // ── 1. 顶部章节徽章 + 主标题（同一行，压缩高度）──
  const bt = d.topBadge ? String(d.topBadge) : '';
  const titleStr = d.mainTitle || '';
  const titleH = 0.52;

  let titleX = M;
  if (bt) {
    const bw = Math.max(1.6, bt.length * 0.2 + 0.5);
    const bh = 0.34;
    const by = cursorY + (titleH - bh) / 2;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: by, w: bw, h: bh,
      rectRadius: 0.05,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });
    t(slide, bt, M, by, bw, bh, {
      fontSize: 10.5, color: CLR.white, bold: true,
      align: 'center', valign: 'middle',
    });
    titleX = M + bw + 0.2;
  }

  // 主标题（支持 <b> 蓝色高亮）— 字号压缩到 20
  const titleParts = String(titleStr).split(/(<b>[^<]+<\/b>)/);
  const titleRuns = [];
  titleParts.forEach((p) => {
    if (!p) return;
    const m = p.match(/^<b>([^<]+)<\/b>$/);
    if (m) {
      titleRuns.push({ text: m[1], options: { fontSize: 20, color: CLR.blue, bold: true, fontFace: FONT_W7 } });
    } else {
      titleRuns.push({ text: p, options: { fontSize: 20, color: CLR.dark, bold: true, fontFace: FONT_W7 } });
    }
  });
  slide.addText(titleRuns, {
    x: titleX, y: cursorY, w: M + CW - titleX, h: titleH,
    align: 'left', valign: 'middle',
  });
  cursorY += titleH + 0.08;

  // ── 2. 副标题条（左侧蓝竖条 + 一句话点题，压缩高度）──
  if (d.subTitle) {
    const subH = 0.34;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: M, y: cursorY, w: 0.06, h: subH,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });
    const subRuns = _runsFromText(d.subTitle, 11, CLR.dark, CLR.blue);
    slide.addText(subRuns, {
      x: M + 0.16, y: cursorY, w: CW - 0.16, h: subH,
      align: 'left', valign: 'middle',
    });
    cursorY += subH + 0.12;
  }

  // ── 3. 三栏卡片（扩大可用空间）──
  const cols = (d.columns || []).slice(0, 3);
  if (!cols.length) return;
  const N = cols.length;
  const gap = 0.22;
  const colW = (CW - (N - 1) * gap) / N;

  const hasFooter = !!d.footerBar;
  const footerH = hasFooter ? 0.52 : 0;
  const bottomMargin = 0.42;
  const cardY = cursorY + 0.02;
  const cardH = 5.625 - cardY - footerH - bottomMargin - (hasFooter ? 0.1 : 0);

  cols.forEach((col, cIdx) => {
    const theme = THEMES[cIdx] || THEMES[1];
    const cx = M + cIdx * (colW + gap);

    // 卡片底板（浅色底）
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: cardY, w: colW, h: cardH,
      rectRadius: 0.08,
      fill: { color: theme.light },
      line: { type: 'none' },
    });

    // ── 头部徽章（彩色底 + 白字，贴近顶部）──
    let innerY = cardY + 0.12;
    const badgeStr = col.badge || '';
    if (badgeStr) {
      const bw = Math.max(1.3, badgeStr.length * 0.24 + 0.5);
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.22, y: innerY, w: bw, h: 0.3,
        rectRadius: 0.15,
        fill: { color: theme.main },
        line: { type: 'none' },
      });
      t(slide, badgeStr, cx + 0.22, innerY, bw, 0.3, {
        fontSize: 10.5, color: CLR.white, bold: true,
        align: 'center', valign: 'middle',
      });
      innerY += 0.38;
    }

    // ── 主标题（单行，紧跟徽章）──
    if (col.title) {
      const tRuns = _runsFromText(col.title, 14, CLR.dark, theme.main).map(r => ({
        text: r.text,
        options: { ...r.options, bold: true, fontFace: FONT_W7 },
      }));
      slide.addText(tRuns, {
        x: cx + 0.22, y: innerY, w: colW - 0.44, h: 0.38,
        align: 'left', valign: 'middle',
        lineSpacingMultiple: 1.15,
      });
      innerY += 0.44;
    }

    // ── 中段强化框（数据 / 标语 / 勾选图，压缩高度）──
    if (col.highlight) {
      const hl = col.highlight;
      const hlH = 0.58;
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.22, y: innerY, w: colW - 0.44, h: hlH,
        rectRadius: 0.04,
        fill: { color: CLR.white },
        line: { type: 'none' },
      });

      if (hl.kind === 'data' && hl.number) {
        // 数据型：大数字 + 下方说明
        t(slide, hl.number, cx + 0.32, innerY + 0.02, colW - 0.64, 0.32, {
          fontSize: 20, color: theme.main, bold: true,
          align: 'left', valign: 'middle', fontFace: FONT_W7,
        });
        if (hl.note) {
          t(slide, hl.note, cx + 0.32, innerY + 0.32, colW - 0.64, 0.22, {
            fontSize: 8.5, color: CLR.body,
            align: 'left', valign: 'middle',
          });
        }
      } else if (hl.kind === 'slogan' && hl.text) {
        // 标语型：大号彩色粗体
        const slRuns = _runsFromText(hl.text, 15, theme.main, theme.main).map(r => ({
          text: r.text,
          options: { ...r.options, bold: true, fontFace: FONT_W7, color: theme.main },
        }));
        slide.addText(slRuns, {
          x: cx + 0.32, y: innerY + 0.02, w: colW - 0.64, h: 0.32,
          align: 'left', valign: 'middle',
        });
        if (hl.note) {
          t(slide, hl.note, cx + 0.32, innerY + 0.32, colW - 0.64, 0.22, {
            fontSize: 8.5, color: CLR.body,
            align: 'left', valign: 'middle',
          });
        }
      } else if (hl.kind === 'checks') {
        // 勾选型：✓✓✓ 三个大勾 + 下方说明
        t(slide, '✓ ✓ ✓', cx + 0.32, innerY, colW - 0.64, 0.34, {
          fontSize: 20, color: theme.main, bold: true,
          align: 'left', valign: 'middle',
        });
        if (hl.note) {
          t(slide, hl.note, cx + 0.32, innerY + 0.32, colW - 0.64, 0.22, {
            fontSize: 8.5, color: CLR.body,
            align: 'left', valign: 'middle',
          });
        }
      }
      innerY += hlH + 0.16;
    }

    // ── 要点列表（彩色圆点 + 短句，支持 <b> 高亮）──
    const bullets = col.bullets || [];
    const listH = cardY + cardH - innerY - 0.18;
    if (bullets.length && listH > 0.3) {
      const lineH = Math.min(0.42, listH / bullets.length);
      bullets.forEach((b, bi) => {
        const by = innerY + bi * lineH;
        // 圆点
        slide.addShape(pres.shapes.OVAL, {
          x: cx + 0.26, y: by + lineH / 2 - 0.05, w: 0.1, h: 0.1,
          fill: { color: theme.main },
          line: { type: 'none' },
        });
        // 文字（带蓝色高亮）
        const bRuns = _runsFromText(b, 10.5, CLR.dark, theme.main);
        slide.addText(bRuns, {
          x: cx + 0.44, y: by, w: colW - 0.64, h: lineH,
          align: 'left', valign: 'middle',
          wrap: false,
        });
      });
    }
  });

  // ── 5. 底部结论条（深蓝 banner + 双引号装饰）──
  if (hasFooter) {
    const barH = 0.52;
    const barY = 5.625 - 0.42 - barH;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: barY, w: CW, h: barH,
      rectRadius: 0.06,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });

    // 左右双引号装饰
    t(slide, '\u201C', M + 0.18, barY - 0.02, 0.4, barH, {
      fontSize: 22, color: '6B8EE8', bold: true,
      align: 'center', valign: 'middle',
    });
    t(slide, '\u201D', M + CW - 0.52, barY - 0.02, 0.4, barH, {
      fontSize: 22, color: '6B8EE8', bold: true,
      align: 'center', valign: 'middle',
    });

    // 主文案（支持 <b> 高亮成金黄色）
    const fbStr = d.footerBar;
    const fbParts = String(fbStr).split(/(<b>[^<]+<\/b>)/);
    const fbRuns = [];
    fbParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        fbRuns.push({ text: m[1], options: { fontSize: 13, color: 'FFE082', bold: true, fontFace: FONT_W7 } });
      } else {
        fbRuns.push({ text: p, options: { fontSize: 12.5, color: CLR.white, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(fbRuns, {
      x: M + 0.6, y: barY, w: CW - 1.2, h: barH,
      align: 'center', valign: 'middle',
    });
  }
}

// ══════════════════════════════════════════════════════════════
//  hub_dual_cards — 中枢+左右双卡（数据反哺类页面）
//  用途：闭环最后一步 "数据回流 → 双向反哺" 这种"中心辐射"型信息
//  自渲染标题（skipCommonTitle=true）
//  2026-04-20 深夜为哈哥的伊利液奶第五步"数据反哺"定制固化
// ══════════════════════════════════════════════════════════════
function renderHubDualCards(slide, d) {
  // 左右卡主题（蓝 / 绿），与腾讯智慧零售配色统一
  const THEMES = [
    { main: '1A50D6', light: 'EAF1FF', dark: '0E3AA8', name: 'blue'  },  // 左：电商
    { main: '00A45D', light: 'E6F5EE', dark: '007A45', name: 'green' },  // 右：媒介
  ];

  let cursorY = 0.32;

  // ── 1. 顶部徽章 + 主标题（同一行）──
  const bt = d.topBadge ? String(d.topBadge) : '';
  const titleStr = d.mainTitle || '';
  const titleH = 0.52;

  let titleX = M;
  if (bt) {
    const bw = Math.max(1.4, bt.length * 0.2 + 0.5);
    const bh = 0.34;
    const by = cursorY + (titleH - bh) / 2;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: by, w: bw, h: bh,
      rectRadius: 0.05,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });
    t(slide, bt, M, by, bw, bh, {
      fontSize: 10.5, color: CLR.white, bold: true,
      align: 'center', valign: 'middle',
    });
    titleX = M + bw + 0.2;
  }

  // 主标题（支持 <b> 蓝色高亮，20pt）
  const titleParts = String(titleStr).split(/(<b>[^<]+<\/b>)/);
  const titleRuns = [];
  titleParts.forEach((p) => {
    if (!p) return;
    const m = p.match(/^<b>([^<]+)<\/b>$/);
    if (m) {
      titleRuns.push({ text: m[1], options: { fontSize: 20, color: CLR.blue, bold: true, fontFace: FONT_W7 } });
    } else {
      titleRuns.push({ text: p, options: { fontSize: 20, color: CLR.dark, bold: true, fontFace: FONT_W7 } });
    }
  });
  slide.addText(titleRuns, {
    x: titleX, y: cursorY, w: M + CW - titleX, h: titleH,
    align: 'left', valign: 'middle',
  });
  cursorY += titleH + 0.06;

  // ── 2. 副标题（一句话领读，支持金黄高亮）──
  if (d.subTitle) {
    const subH = 0.32;
    const subRuns = [];
    const subParts = String(d.subTitle).split(/(<b>[^<]+<\/b>)/);
    subParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        // 金黄底 + 深色字 的 highlight 片段
        subRuns.push({ text: m[1], options: { fontSize: 11, color: CLR.dark, bold: true, fontFace: FONT_W7, highlight: 'FFE082' } });
      } else {
        subRuns.push({ text: p, options: { fontSize: 11, color: CLR.body, fontFace: FONT_W3 } });
      }
    });
    slide.addText(subRuns, {
      x: M, y: cursorY, w: CW, h: subH,
      align: 'left', valign: 'middle',
    });
    cursorY += subH + 0.14;
  }

  // ── 3. 主体：左卡 + 中央圆盘 + 右卡 ──
  const hasFooter = !!d.footerBar;
  const footerH = hasFooter ? 0.52 : 0;
  const bottomMargin = 0.4;
  const bodyY = cursorY;
  const bodyH = 5.625 - bodyY - footerH - bottomMargin - (hasFooter ? 0.1 : 0);

  // 圆盘放正中间，卡片各占一侧并为圆盘留出空隙
  const hubDiameter = Math.min(2.1, bodyH - 0.4);
  const hubX = M + (CW - hubDiameter) / 2;
  const hubY = bodyY + (bodyH - hubDiameter) / 2;
  const hubGap = 0.12;     // 卡片与圆盘之间的间隙
  const cardW = (CW - hubDiameter - 2 * hubGap) / 2;

  const cols = (d.columns || []).slice(0, 2);

  cols.forEach((col, cIdx) => {
    const theme = THEMES[cIdx] || THEMES[0];
    const cx = cIdx === 0 ? M : (M + cardW + hubDiameter + 2 * hubGap);

    // ── 卡片底板（浅色底）──
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: bodyY, w: cardW, h: bodyH,
      rectRadius: 0.08,
      fill: { color: theme.light },
      line: { type: 'none' },
    });

    // ── 顶部小徽章（彩色底 + 白字）──
    let innerY = bodyY + 0.18;
    const badgeStr = col.badge || '';
    if (badgeStr) {
      const bw = Math.max(1.5, badgeStr.length * 0.22 + 0.5);
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.24, y: innerY, w: bw, h: 0.32,
        rectRadius: 0.16,
        fill: { color: theme.main },
        line: { type: 'none' },
      });
      t(slide, badgeStr, cx + 0.24, innerY, bw, 0.32, {
        fontSize: 10.5, color: CLR.white, bold: true,
        align: 'center', valign: 'middle',
      });
      innerY += 0.4;
    }

    // ── 卡标题（18pt，支持 <b> 高亮）──
    const cardTitle = col.title || '';
    const ctParts = String(cardTitle).split(/(<b>[^<]+<\/b>)/);
    const ctRuns = [];
    ctParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        ctRuns.push({ text: m[1], options: { fontSize: 18, color: theme.main, bold: true, fontFace: FONT_W7 } });
      } else {
        ctRuns.push({ text: p, options: { fontSize: 18, color: CLR.dark, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(ctRuns, {
      x: cx + 0.24, y: innerY, w: cardW - 0.48, h: 0.42,
      align: 'left', valign: 'middle',
    });
    innerY += 0.48;

    // ── 副简介（一句话）──
    if (col.summary) {
      t(slide, col.summary, cx + 0.24, innerY, cardW - 0.48, 0.28, {
        fontSize: 10, color: CLR.body, align: 'left', valign: 'middle',
      });
      innerY += 0.34;
    }

    // ── 子项（tag + 描述，最多 3 条）──
    const items = (col.items || []).slice(0, 3);
    const kpiH = (col.kpi || col.kpiLabel) ? 0.78 : 0;
    const itemsTotalH = bodyH - (innerY - bodyY) - kpiH - 0.32;
    const itemH = Math.max(0.4, itemsTotalH / Math.max(items.length, 1));
    items.forEach((it, i) => {
      const iy = innerY + i * itemH;
      // tag 小胶囊
      const tagStr = it.tag || '';
      const tagW = Math.max(0.9, tagStr.length * 0.22 + 0.3);
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.24, y: iy + (itemH - 0.3) / 2, w: tagW, h: 0.3,
        rectRadius: 0.05,
        fill: { color: CLR.white },
        line: { color: theme.main, width: 0.75 },
      });
      t(slide, tagStr, cx + 0.24, iy + (itemH - 0.3) / 2, tagW, 0.3, {
        fontSize: 9.5, color: theme.dark, bold: true,
        align: 'center', valign: 'middle',
      });
      // 描述
      const descX = cx + 0.24 + tagW + 0.14;
      const descW = cardW - (descX - cx) - 0.24;
      t(slide, it.desc || '', descX, iy, descW, itemH, {
        fontSize: 10, color: CLR.dark, align: 'left', valign: 'middle',
      });
    });

    // ── 底部 KPI 大字条（深色底 + 大数字 + 右侧说明）──
    if (col.kpi) {
      const kpiY = bodyY + bodyH - 0.2 - 0.6;
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.24, y: kpiY, w: cardW - 0.48, h: 0.6,
        rectRadius: 0.06,
        fill: { color: theme.dark },
        line: { type: 'none' },
      });
      // KPI 主字（左对齐大号）
      t(slide, col.kpi, cx + 0.34, kpiY, (cardW - 0.48) * 0.5, 0.6, {
        fontSize: 26, color: CLR.white, bold: true,
        align: 'left', valign: 'middle', fontFace: FONT_W7,
      });
      // 右侧说明（小字双行）
      if (col.kpiLabel) {
        t(slide, col.kpiLabel, cx + 0.34 + (cardW - 0.48) * 0.5, kpiY, (cardW - 0.48) * 0.48, 0.6, {
          fontSize: 9, color: CLR.white, align: 'right', valign: 'middle',
        });
      }
    }
  });

  // ── 4. 中央圆盘（双层阴影 + 主文 + 下方三小图标）──
  // 外层浅色大圆（阴影）
  slide.addShape(pres.shapes.OVAL, {
    x: hubX - 0.08, y: hubY - 0.08, w: hubDiameter + 0.16, h: hubDiameter + 0.16,
    fill: { color: 'DDE5F7' },
    line: { type: 'none' },
  });
  // 主圆盘（腾讯蓝实心）
  slide.addShape(pres.shapes.OVAL, {
    x: hubX, y: hubY, w: hubDiameter, h: hubDiameter,
    fill: { color: CLR.blue },
    line: { color: '0E3AA8', width: 1.5 },
  });

  // 圆盘主文：两行
  const hubTitle = d.hubTitle || '事业部数据中枢';
  const hubSub = d.hubSub || '';
  t(slide, hubTitle, hubX, hubY + hubDiameter * 0.28, hubDiameter, 0.44, {
    fontSize: 18, color: CLR.white, bold: true, fontFace: FONT_W7,
    align: 'center', valign: 'middle',
  });
  if (hubSub) {
    t(slide, hubSub, hubX, hubY + hubDiameter * 0.28 + 0.44, hubDiameter, 0.3, {
      fontSize: 10, color: 'C6D4FA', fontFace: FONT_W3,
      align: 'center', valign: 'middle',
    });
  }

  // 圆盘下方三图标行（支撑点），使用 emoji 风格 unicode 代替
  const hubIcons = d.hubIcons || [];
  if (hubIcons.length) {
    const iconN = hubIcons.length;
    const iconRowY = hubY + hubDiameter * 0.68;
    const iconCellW = hubDiameter / iconN;
    hubIcons.forEach((ic, idx) => {
      const ix = hubX + idx * iconCellW;
      // icon 大字（unicode emoji 或简短符号）
      t(slide, ic.icon || '•', ix, iconRowY, iconCellW, 0.26, {
        fontSize: 13, color: CLR.white,
        align: 'center', valign: 'middle',
      });
      // 下方小标题
      t(slide, ic.label || '', ix, iconRowY + 0.24, iconCellW, 0.22, {
        fontSize: 8, color: 'C6D4FA',
        align: 'center', valign: 'middle',
      });
    });
  }

  // ── 5. 左右双向反哺箭头（圆盘两侧各一对）──
  const arrowY = hubY + hubDiameter / 2 - 0.05;
  const arrowLen = hubGap + 0.25;
  // 左侧：圆盘 → 左卡（向左箭头）
  slide.addShape(pres.shapes.LEFT_ARROW, {
    x: hubX - arrowLen - 0.05, y: arrowY - 0.1, w: arrowLen, h: 0.22,
    fill: { color: CLR.blue },
    line: { type: 'none' },
  });
  // 左卡 → 圆盘（向右箭头）
  slide.addShape(pres.shapes.RIGHT_ARROW, {
    x: hubX - arrowLen - 0.05, y: arrowY + 0.14, w: arrowLen, h: 0.22,
    fill: { color: '6B8EE8' },
    line: { type: 'none' },
  });
  // 右侧：圆盘 → 右卡（向右箭头）
  slide.addShape(pres.shapes.RIGHT_ARROW, {
    x: hubX + hubDiameter + 0.05, y: arrowY - 0.1, w: arrowLen, h: 0.22,
    fill: { color: CLR.green },
    line: { type: 'none' },
  });
  // 右卡 → 圆盘（向左箭头）
  slide.addShape(pres.shapes.LEFT_ARROW, {
    x: hubX + hubDiameter + 0.05, y: arrowY + 0.14, w: arrowLen, h: 0.22,
    fill: { color: '73C9A2' },
    line: { type: 'none' },
  });

  // ── 6. 底部 footerBar（深蓝 + 金黄高亮）──
  if (d.footerBar) {
    const barH = 0.42;
    const barY = 5.625 - 0.38 - barH;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: barY, w: CW, h: barH,
      rectRadius: 0.05,
      fill: { color: CLR.blue },
      line: { type: 'none' },
    });
    const fbStr = d.footerBar;
    const fbParts = String(fbStr).split(/(<b>[^<]+<\/b>)/);
    const fbRuns = [];
    fbParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        fbRuns.push({ text: m[1], options: { fontSize: 13, color: 'FFE082', bold: true, fontFace: FONT_W7 } });
      } else {
        fbRuns.push({ text: p, options: { fontSize: 12.5, color: CLR.white, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(fbRuns, {
      x: M + 0.4, y: barY, w: CW - 0.8, h: barH,
      align: 'center', valign: 'middle',
    });
  }
}

// ── 9b. hero_radial — 1 大主张卡 + 2×2 能力卡 + 底部陪跑条 ─────────────────
// 适用场景：顶层服务定位 / 能力总览（"我们能做什么""腾讯提供什么"）
// 左卡传递服务方姿态 + Key Message + 金色关键词；右卡 2×2 四能力；底部金条强化交付承诺
function renderHeroRadial(slide, d) {
  // === 配色（支持覆盖） ===
  const DARK_BLUE = d.darkColor || '0E3AA8';     // 左卡深蓝底
  const GOLD      = d.accentColor || 'FFE082';   // 金色高亮

  // === 0. 顶部标题区（自渲染，徽章 + 主副标题） ===
  let cursorY = 0.28;
  const bt = d.topBadge ? String(d.topBadge) : '';
  const bw = bt ? Math.max(1.0, bt.length * 0.17 + 0.4) : 0;
  if (bt) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: cursorY + 0.05, w: bw, h: 0.32,
      rectRadius: 0.05,
      fill: { color: CLR.blue }, line: { type: 'none' },
    });
    t(slide, bt, M, cursorY + 0.05, bw, 0.32, {
      fontSize: 10, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });
  }
  const titleX = bt ? (M + bw + 0.15) : M;
  const titleW = bt ? (CW - bw - 0.15) : CW;
  t(slide, d.mainTitle || '我们能做什么', titleX, cursorY, titleW, 0.42, {
    fontSize: 20, color: CLR.dark, bold: true, align: 'left', valign: 'middle',
  });
  cursorY += 0.46;
  if (d.subTitle) {
    t(slide, d.subTitle, M, cursorY, CW, 0.26, {
      fontSize: 10.5, color: CLR.note, align: 'left', valign: 'middle',
    });
    cursorY += 0.26;
  }

  // === 布局区域 ===
  const AREA_Y = 0.98;
  const AREA_H = 4.05;   // 到 5.03
  const FB_Y   = 5.10;   // footer 条起点
  const FB_H   = 0.42;

  // === 1. 左侧主张卡（深蓝） ===
  const LX = M;
  const LY = AREA_Y;
  const LW = 2.9;
  const LH = AREA_H;

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: LX, y: LY, w: LW, h: LH,
    rectRadius: 0.08,
    fill: { color: DARK_BLUE }, line: { type: 'none' },
  });
  // 顶部亮色装饰
  slide.addShape(pres.shapes.RECTANGLE, {
    x: LX, y: LY, w: LW, h: 0.06,
    fill: { color: '4A7FFF' }, line: { type: 'none' },
  });

  // 品牌标识块
  if (d.heroBadge) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: LX + 0.25, y: LY + 0.3, w: 1.45, h: 0.3,
      rectRadius: 0.04,
      fill: { color: CLR.white, transparency: 82 }, line: { type: 'none' },
    });
    t(slide, d.heroBadge, LX + 0.25, LY + 0.3, 1.45, 0.3, {
      fontSize: 10, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });
  }

  // 主张标题（两行，第一行白 + 第二行金色，支持 heroTitleTop / heroTitleBottom）
  const tTop = d.heroTitleTop || '全链路';
  const tBottom = d.heroTitleBottom || '咨询服务方';
  t(slide, tTop, LX + 0.25, LY + 0.72, LW - 0.5, 0.5, {
    fontSize: 26, color: CLR.white, bold: true, align: 'left', valign: 'middle',
  });
  t(slide, tBottom, LX + 0.25, LY + 1.18, LW - 0.5, 0.5, {
    fontSize: 26, color: GOLD, bold: true, align: 'left', valign: 'middle',
  });

  // 金色短线
  slide.addShape(pres.shapes.LINE, {
    x: LX + 0.25, y: LY + 1.78, w: 0.5, h: 0,
    line: { color: GOLD, width: 2 },
  });

  // 核心价值说明（heroSubtitle 支持 <b></b> 标金色高亮）
  const sub = d.heroSubtitle || '';
  if (sub) {
    const parts = String(sub).split(/(<b>[^<]+<\/b>)/);
    const runs = [];
    parts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        runs.push({ text: m[1], options: { fontSize: 11.5, color: GOLD, bold: true, fontFace: FONT_W7 } });
      } else {
        runs.push({ text: p, options: { fontSize: 11.5, color: CLR.white, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(runs, {
      x: LX + 0.25, y: LY + 1.9, w: LW - 0.5, h: 0.55,
      align: 'left', valign: 'top', paraSpaceAfter: 3,
    });
  }

  // 关键词列表（最多 4 条，支持 heroKeywords: string[] 或 {text}[]）
  const keywords = (d.heroKeywords || []).slice(0, 4);
  keywords.forEach((kw, i) => {
    const text = typeof kw === 'string' ? kw : (kw.text || '');
    const ky = LY + 2.55 + i * 0.26;
    t(slide, '◆', LX + 0.25, ky, 0.22, 0.24, {
      fontSize: 10, color: GOLD, bold: true, align: 'left', valign: 'middle',
    });
    t(slide, text, LX + 0.48, ky, LW - 0.75, 0.24, {
      fontSize: 11, color: CLR.white, align: 'left', valign: 'middle',
    });
  });

  // 底部金牌（heroRibbon）
  if (d.heroRibbon) {
    const rY = LY + LH - 0.7;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: LX + 0.25, y: rY, w: LW - 0.5, h: 0.5,
      rectRadius: 0.04,
      fill: { color: GOLD }, line: { type: 'none' },
    });
    // 支持 heroRibbon 为字符串或 { prefix, main } 结构；自动把首段数字放大
    const ribbonStr = String(d.heroRibbon);
    const mNum = ribbonStr.match(/^(\d+)\s*(.+)$/);
    if (mNum) {
      slide.addText([
        { text: mNum[1], options: { fontFace: FONT_W7, fontSize: 20, color: DARK_BLUE, bold: true } },
        { text: ' ' + mNum[2], options: { fontFace: FONT_W7, fontSize: 12, color: DARK_BLUE, bold: true } },
      ], { x: LX + 0.25, y: rY, w: LW - 0.5, h: 0.5, align: 'center', valign: 'middle' });
    } else {
      t(slide, ribbonStr, LX + 0.25, rY, LW - 0.5, 0.5, {
        fontSize: 12, color: DARK_BLUE, bold: true, align: 'center', valign: 'middle',
      });
    }
  }

  // === 2. 右侧 2×2 能力卡 ===
  const RX_START = LX + LW + 0.2;     // 3.6
  const RY = AREA_Y;
  const R_TOTAL_W = (M + CW) - RX_START; // 5.9
  const GAP = 0.15;
  const CARD_W = (R_TOTAL_W - GAP) / 2;
  const CARD_H = (AREA_H - GAP) / 2;

  const cards = (d.cards || []).slice(0, 4);
  // 默认四色调色盘（蓝 / 绿 / 橙 / 紫）
  const palette = [
    { color: '1A50D6', colorLight: 'EAF1FF' },
    { color: '16A37A', colorLight: 'E8F6EF' },
    { color: 'FF7A2E', colorLight: 'FFF4ED' },
    { color: '7C5CFF', colorLight: 'F0EDFF' },
  ];

  cards.forEach((card, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const cx = RX_START + col * (CARD_W + GAP);
    const cy = RY + row * (CARD_H + GAP);
    const cc = card.color || palette[i].color;
    const cl = card.colorLight || palette[i].colorLight;

    // 卡片底
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: cy, w: CARD_W, h: CARD_H,
      rectRadius: 0.06,
      fill: { color: CLR.white },
      line: { color: CLR.border, width: 0.75 },
    });
    // 左侧色条
    slide.addShape(pres.shapes.RECTANGLE, {
      x: cx, y: cy + 0.12, w: 0.05, h: CARD_H - 0.24,
      fill: { color: cc }, line: { type: 'none' },
    });
    // 序号
    const num = card.num || String(i + 1).padStart(2, '0');
    t(slide, num, cx + 0.18, cy + 0.15, 0.55, 0.32, {
      fontSize: 18, color: cc, bold: true, align: 'left', valign: 'middle',
    });
    // 徽章
    if (card.badge) {
      const bgW = Math.max(0.85, String(card.badge).length * 0.18 + 0.3);
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.8, y: cy + 0.22, w: bgW, h: 0.22,
        rectRadius: 0.03,
        fill: { color: cl }, line: { type: 'none' },
      });
      t(slide, card.badge, cx + 0.8, cy + 0.22, bgW, 0.22, {
        fontSize: 8.5, color: cc, bold: true, align: 'center', valign: 'middle',
      });
    }
    // 标题
    t(slide, card.title || '', cx + 0.18, cy + 0.52, CARD_W - 0.3, 0.34, {
      fontSize: 12, color: CLR.dark, bold: true, align: 'left', valign: 'middle',
    });
    // 分割线
    slide.addShape(pres.shapes.LINE, {
      x: cx + 0.18, y: cy + 0.9, w: CARD_W - 0.36, h: 0,
      line: { color: CLR.border, width: 0.75 },
    });
    // Bullets（最多 3 条，支持 {k,v} 或字符串）
    const bullets = (card.bullets || []).slice(0, 3);
    bullets.forEach((bl, bi) => {
      const by = cy + 1.0 + bi * 0.28;
      // 小圆点
      slide.addShape(pres.shapes.OVAL, {
        x: cx + 0.22, y: by + 0.08, w: 0.07, h: 0.07,
        fill: { color: cc }, line: { type: 'none' },
      });
      if (typeof bl === 'string') {
        t(slide, bl, cx + 0.35, by, CARD_W - 0.5, 0.24, {
          fontSize: 9.5, color: CLR.dark, align: 'left', valign: 'middle',
        });
      } else {
        slide.addText([
          { text: (bl.k || '') + ' ', options: { fontFace: FONT_W7, fontSize: 9.5, color: cc, bold: true } },
          { text: bl.v || '', options: { fontFace: FONT_W3, fontSize: 9.5, color: CLR.dark } },
        ], {
          x: cx + 0.35, y: by, w: CARD_W - 0.5, h: 0.24,
          align: 'left', valign: 'middle',
        });
      }
    });
  });

  // === 3. 底部陪跑条 footerBar ===
  if (d.footerBar) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: FB_Y, w: CW, h: FB_H,
      rectRadius: 0.05,
      fill: { color: DARK_BLUE }, line: { type: 'none' },
    });
    // 左侧金色标签
    const fbLabel = d.footerLabel || '全程陪跑';
    const lbW = Math.max(1.0, fbLabel.length * 0.2 + 0.3);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M + 0.12, y: FB_Y + 0.08, w: lbW, h: FB_H - 0.16,
      rectRadius: 0.03,
      fill: { color: GOLD }, line: { type: 'none' },
    });
    t(slide, fbLabel, M + 0.12, FB_Y + 0.08, lbW, FB_H - 0.16, {
      fontSize: 10, color: DARK_BLUE, bold: true, align: 'center', valign: 'middle',
    });
    // 右侧交付内容（支持字符串或 runs 数组，自动用 · 连接）
    const fb = d.footerBar;
    let runs = [];
    if (typeof fb === 'string') {
      // 解析 <b></b> 为金色高亮
      const parts = fb.split(/(<b>[^<]+<\/b>)/);
      parts.forEach((p) => {
        if (!p) return;
        const m = p.match(/^<b>([^<]+)<\/b>$/);
        if (m) {
          runs.push({ text: m[1], options: { fontFace: FONT_W7, fontSize: 11, color: GOLD, bold: true } });
        } else {
          runs.push({ text: p, options: { fontFace: FONT_W7, fontSize: 11, color: CLR.white, bold: true } });
        }
      });
    } else if (Array.isArray(fb)) {
      fb.forEach((item, i) => {
        if (i > 0) {
          runs.push({ text: '  ·  ', options: { fontFace: FONT_W3, fontSize: 11, color: GOLD } });
        }
        const isHi = item.highlight;
        runs.push({
          text: typeof item === 'string' ? item : item.text,
          options: {
            fontFace: FONT_W7, fontSize: 11,
            color: isHi ? GOLD : CLR.white, bold: true,
          },
        });
      });
    }
    slide.addText(runs, {
      x: M + lbW + 0.25, y: FB_Y, w: CW - lbW - 0.4, h: FB_H,
      align: 'center', valign: 'middle',
    });
  }
}

// ── 10. formula_phases — 带公式的阶段流程 ─────────────────────────────────
function renderFormulaPhases(slide, d) {
  // 1. 渲染大公式
  const formulaY = 1.5;
  const formulas = d.formulas || [];
  if (formulas.length > 0) {
    const fw = 2.4;
    const fh = 0.5;
    const fgap = 0.6;
    const totalW = formulas.length * fw + (formulas.length - 1) * fgap;
    const startX = M + (CW - totalW) / 2;
    
    formulas.forEach((fm, i) => {
      const x = startX + i * (fw + fgap);
      // 公式卡片圆角效果（用矩形模拟，带点阴影）
      cardBox(slide, x, formulaY, fw, fh);
      s_rect(slide, x, formulaY, 0.1, fh, CLR.blue);
      t(slide, fm, x + 0.1, formulaY, fw - 0.1, fh, {
        fontSize: 13, color: CLR.dark, bold: true, align: 'center', valign: 'middle'
      });
      // 加号
      if (i < formulas.length - 1) {
        t(slide, '➕', x + fw, formulaY + 0.05, fgap, fh, {
          fontSize: 16, color: CLR.blue, bold: true, align: 'center', valign: 'middle'
        });
      }
    });
  }

  // 2. 渲染横向 4 阶段（或者动态数量阶段）
  const phases = d.phases || [];
  if (!phases.length) return;

  const bodyY = 2.3;
  const gap = 0.15;
  const colCount = phases.length;
  const colW = (CW - (colCount - 1) * gap) / colCount;
  const headerH = 0.45;
  
  // 从深到浅的渐变色系列
  const phaseColors = [CLR.blue, CLR.medBlue, CLR.ltBlue, '#A9CDE6', '#CDE0EF'];

  phases.forEach((phase, pi) => {
    const x = M + pi * (colW + gap);
    const phaseColor = phaseColors[pi % phaseColors.length];

    // 阶段标题色块
    s_rect(slide, x, bodyY, colW, headerH, phaseColor);
    t(slide, phase.name || '', x, bodyY, colW, headerH, {
      fontSize: 12, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });

    // 阶段内容卡片悬挂在下方
    const cardY = bodyY + headerH;
    const cardH = 2.2;
    cardBox(slide, x, cardY, colW, cardH);
    
    // 内容渲染
    const items = phase.items || [];
    if (items.length > 0) {
      t(slide, items.join('\n\n'), x + 0.15, cardY + 0.15, colW - 0.3, cardH - 0.3, {
        fontSize: 10.5, color: CLR.body, valign: 'top', lineSpacingMultiple: 1.2
      });
    }
  });
}

// ── 10.5 circle_loop — 环形五步闭环（左右要点） ───────────────
function renderCircleLoop(slide, d) {
  const steps = d.steps || [];
  const leftPoints = d.leftPoints || [];
  const rightPoints = d.rightPoints || [];
  const footerBar = d.footerBar;
  const coreValue = d.coreValue || {};

  const bodyY = 1.55;
  const centerX = 5.0;
  const centerY = bodyY + 1.70;
  const ringRadius = 1.38;
  const stepR = 0.42;

  // 中央虚线环
  const dashW = 2 * ringRadius;
  slide.addShape(pres.shapes.OVAL, {
    x: centerX - ringRadius, y: centerY - ringRadius, w: dashW, h: dashW,
    fill: { type: 'none' },
    line: { color: CLR.ltBlue, width: 1, dashType: 'dash' },
  });

  // 中央核心价值圆
  const innerR = 0.80;
  slide.addShape(pres.shapes.OVAL, {
    x: centerX - innerR, y: centerY - innerR, w: 2 * innerR, h: 2 * innerR,
    fill: { color: CLR.lightBlue },
    line: { color: CLR.blue, width: 1 },
  });
  t(slide, coreValue.title || '', centerX - innerR + 0.05, centerY - 0.35, 2 * innerR - 0.1, 0.6, {
    fontSize: 13, color: CLR.dark, bold: true, align: 'center', valign: 'middle',
    lineSpacingMultiple: 1.15,
  });
  t(slide, coreValue.desc || '', centerX - innerR + 0.05, centerY + 0.25, 2 * innerR - 0.1, 0.4, {
    fontSize: 8, color: CLR.body, align: 'center', valign: 'middle',
    lineSpacingMultiple: 1.2,
  });

  // 五个步骤圆（72° 分布，从正上方起顺时针）
  const angles = [-90, -18, 54, 126, 198];

  steps.slice(0, 5).forEach((step, i) => {
    const angle = angles[i] * Math.PI / 180;
    const cx = centerX + ringRadius * Math.cos(angle);
    const cy = centerY + ringRadius * Math.sin(angle);

    slide.addShape(pres.shapes.OVAL, {
      x: cx - stepR, y: cy - stepR, w: 2 * stepR, h: 2 * stepR,
      fill: { color: CLR.blue },
      line: { color: CLR.white, width: 2 },
    });

    const num = String(i + 1).padStart(2, '0');
    t(slide, num, cx - stepR, cy - stepR, 2 * stepR, 2 * stepR, {
      fontFace: 'Arial', fontSize: 22, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });

    // 圆外文字：顶部圆文字放上方，其他放下方
    const labelW = 1.7;
    let labelX = cx - labelW / 2;
    let labelY;
    if (i === 0) {
      // 正上方的圆，文字放在圆的上方
      labelY = cy - stepR - 0.5;
    } else {
      // 其余四个圆，文字放在圆的下方
      labelY = cy + stepR + 0.05;
    }

    t(slide, step.name || '', labelX, labelY, labelW, 0.3, {
      fontSize: 12, color: CLR.blue, bold: true, align: 'center', valign: 'middle',
    });

    if (step.desc) {
      t(slide, step.desc, labelX, labelY + 0.3, labelW, 0.4, {
        fontSize: 8.5, color: CLR.body, align: 'center', valign: 'top',
        lineSpacingMultiple: 1.2,
      });
    }
  });

  // 左右侧要点
  const sidePointH = 1.0;
  const sidePointGap = 0.12;
  const sidePointW = 2.4;
  const sideStartY = 1.55;

  leftPoints.slice(0, 3).forEach((pt, i) => {
    const x = M;
    const y = sideStartY + i * (sidePointH + sidePointGap);
    s_rect(slide, x, y, 0.06, sidePointH, CLR.blue);
    t(slide, pt.title || '', x + 0.18, y + 0.06, sidePointW - 0.2, 0.3, {
      fontSize: 12, color: CLR.dark, bold: true, align: 'left',
    });
    t(slide, pt.desc || '', x + 0.18, y + 0.38, sidePointW - 0.2, sidePointH - 0.42, {
      fontSize: 9, color: CLR.body, align: 'left', valign: 'top',
      lineSpacingMultiple: 1.3,
    });
  });

  rightPoints.slice(0, 3).forEach((pt, i) => {
    const x = 10 - M - sidePointW;
    const y = sideStartY + i * (sidePointH + sidePointGap);
    s_rect(slide, x, y, 0.06, sidePointH, CLR.blue);
    t(slide, pt.title || '', x + 0.18, y + 0.06, sidePointW - 0.2, 0.3, {
      fontSize: 12, color: CLR.dark, bold: true, align: 'left',
    });
    t(slide, pt.desc || '', x + 0.18, y + 0.38, sidePointW - 0.2, sidePointH - 0.42, {
      fontSize: 9, color: CLR.body, align: 'left', valign: 'top',
      lineSpacingMultiple: 1.3,
    });
  });

  if (footerBar) {
    s_rect(slide, M, 5.0, CW, 0.35, CLR.lightBlue);
    t(slide, footerBar, M, 5.0, CW, 0.35, {
      fontSize: 11, color: CLR.dark, bold: true, align: 'center', valign: 'middle',
    });
  }
}

// ── 10.6 quad_loop — 四方闭环（中央飞轮 + 四方卡片 + 循环箭头） ───
function renderQuadLoop(slide, d) {
  const cards = d.cards || [];
  const footerBar = d.footerBar;
  const centerBadge = d.centerBadge || {};

  // 顶部徽章 + 主标题同行（参考图样式）
  let titleStartX = M;
  if (d.topBadge) {
    const badgeW = 1.7;
    const badgeH = 0.36;
    const badgeY = 0.4;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: badgeY, w: badgeW, h: badgeH,
      fill: { color: CLR.blue },
      line: { type: 'none' },
      rectRadius: 0.05,
    });
    t(slide, d.topBadge, M, badgeY, badgeW, badgeH, {
      fontSize: 11, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    });
    titleStartX = M + badgeW + 0.2;
  }

  // 主标题（与徽章同行）
  t(slide, d.mainTitle || '', titleStartX, 0.35, CW - (titleStartX - M), 0.5, {
    fontSize: 22, color: CLR.dark, bold: true, valign: 'middle',
  });

  // 副标题（Action Title）
  if (d.actionTitle) {
    t(slide, d.actionTitle, M, 0.95, CW, 0.28, {
      fontSize: 11, color: CLR.body, valign: 'middle',
    });
  }

  // 区域参数（标题更紧凑 → 下方卡片区扩大）
  const bodyY = 1.35;
  const bodyH = 3.55;
  const rowGap = 0.2;
  const cardW = 3.65;
  const cardH = (bodyH - rowGap) / 2;

  const leftX = M;
  const rightX = 10 - M - cardW;
  const topY = bodyY;
  const botY = bodyY + cardH + rowGap;

  const centerX = 5.0;
  const centerY = bodyY + bodyH / 2;
  const centerR = 0.55;

  const positions = [
    { x: leftX, y: topY },
    { x: rightX, y: topY },
    { x: rightX, y: botY },
    { x: leftX, y: botY },
  ];

  cards.slice(0, 4).forEach((card, i) => {
    const pos = positions[i];
    const cx = pos.x;
    const cy = pos.y;

    // 卡片白底圆角框 + 阴影
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: cy, w: cardW, h: cardH,
      fill: { color: CLR.white },
      line: { color: CLR.border, width: 1 },
      rectRadius: 0.08,
      shadow: { type: 'outer', blur: 10, offset: 3, angle: 45, color: CLR.shadow, opacity: 0.5 },
    });

    // 头部：编号圆 + 主标题（同一行，参考图样式）
    const numText = String(i + 1).padStart(2, '0');
    const headerY = cy + 0.2;
    const numCircleR = 0.45;
    slide.addShape(pres.shapes.OVAL, {
      x: cx + 0.22, y: headerY, w: numCircleR, h: numCircleR,
      fill: { color: CLR.lightBlue },
      line: { type: 'none' },
    });
    t(slide, numText, cx + 0.22, headerY, numCircleR, numCircleR, {
      fontFace: 'Arial', fontSize: 16, color: CLR.blue, bold: true, align: 'center', valign: 'middle',
    });

    // 卡片主标题（和编号同一行，右边紧挨）
    t(slide, card.title || '', cx + 0.78, headerY - 0.02, cardW - 2.0, numCircleR + 0.04, {
      fontSize: 16, color: CLR.dark, bold: true, align: 'left', valign: 'middle',
    });

    // 标签色块（右上角，蓝底白字）
    if (card.tag) {
      const tagW = 0.85;
      const tagH = 0.28;
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + cardW - tagW - 0.18, y: headerY + 0.08, w: tagW, h: tagH,
        fill: { color: CLR.blue },
        line: { type: 'none' },
        rectRadius: 0.04,
      });
      t(slide, card.tag, cx + cardW - tagW - 0.18, headerY + 0.08, tagW, tagH, {
        fontSize: 10, color: CLR.white, bold: true, align: 'center', valign: 'middle',
      });
    }

    // 卡片描述（支持富文本：{text, highlight} 或纯字符串）
    // 把描述数组转成 pptxgenjs 富文本数组
    const descLines = Array.isArray(card.desc) ? card.desc : [card.desc || ''];
    const runs = [];
    descLines.forEach((line, li) => {
      if (li > 0) {
        runs.push({ text: '\n', options: { fontSize: 10, fontFace: FONT_W3 } });
      }
      // 识别 <b>xxx</b> 作为高亮
      const parts = String(line).split(/(<b>[^<]+<\/b>)/);
      parts.forEach((p) => {
        if (!p) return;
        const m = p.match(/^<b>([^<]+)<\/b>$/);
        if (m) {
          runs.push({
            text: m[1],
            options: { fontSize: 10, color: CLR.blue, bold: true, fontFace: FONT_W7 },
          });
        } else {
          runs.push({
            text: p,
            options: { fontSize: 10, color: CLR.body, fontFace: FONT_W3 },
          });
        }
      });
    });
    slide.addText(runs, {
      x: cx + 0.22, y: cy + 1.15, w: cardW - 0.44, h: cardH - 1.3,
      align: 'left', valign: 'top',
      lineSpacingMultiple: 1.35,
    });
  });

  // ═══ 中央飞轮 ═══
  const bigR = 0.92;
  slide.addShape(pres.shapes.OVAL, {
    x: centerX - bigR, y: centerY - bigR, w: 2 * bigR, h: 2 * bigR,
    fill: { type: 'none' },
    line: { color: CLR.ltBlue, width: 1, dashType: 'dash' },
  });

  slide.addShape(pres.shapes.OVAL, {
    x: centerX - centerR, y: centerY - centerR, w: 2 * centerR, h: 2 * centerR,
    fill: { color: CLR.blue },
    line: { type: 'none' },
  });

  // 中心主标语（纯中文）
  t(slide, centerBadge.title || '', centerX - centerR, centerY - 0.3, 2 * centerR, 0.55, {
    fontSize: 12, color: CLR.white, bold: true, align: 'center', valign: 'middle',
    lineSpacingMultiple: 1.2,
  });

  // 中心小字脚注
  if (centerBadge.desc) {
    t(slide, centerBadge.desc, centerX - centerR, centerY + 0.22, 2 * centerR, 0.25, {
      fontSize: 8, color: CLR.lightBlue, align: 'center', valign: 'middle',
    });
  }

  // ═══ 四方向循环箭头 ═══
  const arrowSize = 0.28;
  const arrowPositions = [
    { x: centerX - arrowSize / 2, y: centerY - bigR - arrowSize / 2, symbol: '▶' },
    { x: centerX + bigR - arrowSize / 2, y: centerY - arrowSize / 2, symbol: '▼' },
    { x: centerX - arrowSize / 2, y: centerY + bigR - arrowSize / 2, symbol: '◀' },
    { x: centerX - bigR - arrowSize / 2, y: centerY - arrowSize / 2, symbol: '▲' },
  ];
  arrowPositions.forEach((ap) => {
    slide.addShape(pres.shapes.OVAL, {
      x: ap.x, y: ap.y, w: arrowSize, h: arrowSize,
      fill: { color: CLR.white },
      line: { color: CLR.blue, width: 1.5 },
    });
    t(slide, ap.symbol, ap.x, ap.y, arrowSize, arrowSize, {
      fontSize: 9, color: CLR.blue, bold: true, align: 'center', valign: 'middle',
    });
  });

  // ═══ 底部 footerBar ═══
  if (footerBar) {
    const fbY = 5.02;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: fbY, w: CW, h: 0.38,
      fill: { color: CLR.blue },
      line: { type: 'none' },
      rectRadius: 0.05,
    });
    const lblW = 0.85;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M + 0.15, y: fbY + 0.07, w: lblW, h: 0.24,
      fill: { color: CLR.white },
      line: { type: 'none' },
      rectRadius: 0.03,
    });
    t(slide, '核心价值', M + 0.15, fbY + 0.07, lblW, 0.24, {
      fontSize: 9, color: CLR.blue, bold: true, align: 'center', valign: 'middle',
    });
    t(slide, footerBar, M + lblW + 0.3, fbY, CW - lblW - 0.4, 0.38, {
      fontSize: 11, color: CLR.white, bold: true, align: 'left', valign: 'middle',
    });
  }
}

// ══════════════════════════════════════════════════════════════
//  evolution_trio — 三代进化横向流程（AI 三代演进专用模板）
//  灵感来源：哈哥 2026-04-21 定稿的 slide_ai_evolution.png
//  特征：3 张独立圆角白卡 + 中间大箭头连接器 + 第三代整卡橙色高亮
//  ⚠️ 破例铁律：本布局允许使用橙色 CLR.orange = 'FF6A00'（仅限末代高亮）
//  自渲染标题（skipCommonTitle=true）
// ══════════════════════════════════════════════════════════════
function renderEvolutionTrio(slide, d) {
  // === 破例专用橙色（仅本布局允许）===
  const ORANGE      = 'FF6A00';
  const ORANGE_LT   = 'FFF0E0';  // 橙色浅底

  // === 标准三代主题（第一/二代蓝，第三代橙）===
  const THEMES = [
    { main: CLR.blue,    light: CLR.lightBlue, name: 'Generation One'   },
    { main: CLR.medBlue, light: 'E8EFFA',      name: 'Generation Two'   },
    { main: ORANGE,      light: ORANGE_LT,     name: 'Generation Three' },
  ];

  // === 1. 顶部徽章 + 主标题同行（可选，参考 hub_dual_cards 风格）===
  let cursorY = 0.32;
  const titleH = 0.5;

  const bt = d.topBadge ? String(d.topBadge) : '';
  let titleX = M;
  if (bt) {
    const bw = Math.max(1.4, bt.length * 0.2 + 0.5);
    const bh = 0.34;
    const by = cursorY + (titleH - bh) / 2;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: by, w: bw, h: bh,
      rectRadius: 0.05,
      fill: { color: CLR.blue }, line: { type: 'none' },
    });
    t(slide, bt, M, by, bw, bh, {
      fontSize: 10.5, color: CLR.white, bold: true,
      align: 'center', valign: 'middle',
    });
    titleX = M + bw + 0.2;
  }

  if (d.mainTitle) {
    const tParts = String(d.mainTitle).split(/(<b>[^<]+<\/b>)/);
    const tRuns = [];
    tParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        tRuns.push({ text: m[1], options: { fontSize: 20, color: ORANGE, bold: true, fontFace: FONT_W7 } });
      } else {
        tRuns.push({ text: p, options: { fontSize: 20, color: CLR.dark, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(tRuns, {
      x: titleX, y: cursorY, w: M + CW - titleX, h: titleH,
      align: 'left', valign: 'middle',
    });
    cursorY += titleH + 0.06;
  }

  // 副标题（可选）
  if (d.subTitle) {
    const subH = 0.32;
    const subRuns = _runsFromText(d.subTitle, 11, CLR.body, ORANGE);
    slide.addText(subRuns, {
      x: M, y: cursorY, w: CW, h: subH,
      align: 'left', valign: 'middle',
    });
    cursorY += subH + 0.08;
  }

  // === 2. 三张卡片布局计算 ===
  const phases = (d.phases || []).slice(0, 3);
  if (!phases.length) return;

  const hasFooter = !!d.footerBar;
  const footerH = hasFooter ? 0.42 : 0;
  const bottomMargin = 0.42;

  const cardY = cursorY + 0.02;
  const cardH = 5.625 - cardY - footerH - bottomMargin - (hasFooter ? 0.08 : 0);

  // 箭头区域宽度
  const arrowW = 0.32;
  const gap = 0.08; // 卡与箭头间距
  const N = phases.length;
  // 箭头数 = N-1
  const totalArrowArea = (N - 1) * (arrowW + 2 * gap);
  const cardW = (CW - totalArrowArea) / N;

  phases.forEach((phase, pi) => {
    const theme = THEMES[pi] || THEMES[0];
    const isLast = pi === N - 1;
    const cx = M + pi * (cardW + arrowW + 2 * gap);

    // 卡片底板（末代橙色底，前两代白底）
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: cx, y: cardY, w: cardW, h: cardH,
      rectRadius: 0.1,
      fill: { color: isLast ? theme.light : CLR.white },
      line: { color: isLast ? theme.main : CLR.border, width: isLast ? 1.5 : 1 },
      shadow: { type: 'outer', blur: 12, offset: 3, angle: 90, color: CLR.shadow, opacity: 0.5 },
    });

    // 左侧彩色竖条
    slide.addShape(pres.shapes.RECTANGLE, {
      x: cx, y: cardY + 0.18, w: 0.08, h: cardH - 0.36,
      fill: { color: theme.main }, line: { type: 'none' },
    });

    // —— 顶部：序号徽章圆 + Generation 英文小字 ——
    const badgeR = 0.4;
    const badgeX = cx + 0.28;
    const badgeY = cardY + 0.22;
    slide.addShape(pres.shapes.OVAL, {
      x: badgeX, y: badgeY, w: badgeR, h: badgeR,
      fill: { color: theme.main }, line: { type: 'none' },
    });
    const numStr = String(pi + 1).padStart(2, '0');
    t(slide, numStr, badgeX, badgeY, badgeR, badgeR, {
      fontFace: 'Arial', fontSize: 14, color: CLR.white, bold: true,
      align: 'center', valign: 'middle',
    });
    // Generation 英文小字
    t(slide, theme.name, badgeX + badgeR + 0.1, badgeY, cardW - badgeR - 0.55, badgeR, {
      fontSize: 9, color: theme.main, bold: true,
      align: 'left', valign: 'middle', fontFace: 'Arial',
    });

    // —— 中央大标题（代际名本身作为主视觉，根据字数自适应字号）——
    const titleBlockY = cardY + 0.72;
    const titleBlockH = 0.58;
    const titleStr = phase.title || '';
    // 字数 >9 时字号降为 14，否则 16
    const titleFS = titleStr.length > 9 ? 14 : 16;
    t(slide, titleStr, cx + 0.1, titleBlockY, cardW - 0.2, titleBlockH, {
      fontSize: titleFS, color: isLast ? theme.main : CLR.dark, bold: true,
      align: 'center', valign: 'middle',
      lineSpacingMultiple: 1.05, fontFace: FONT_W7,
    });

    // —— 代表产品标签条（可选）——
    let cursorCardY = titleBlockY + titleBlockH + 0.08;
    if (phase.products) {
      const pH = 0.3;
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.2, y: cursorCardY, w: cardW - 0.4, h: pH,
        rectRadius: 0.04,
        fill: { color: isLast ? CLR.white : theme.light },
        line: isLast ? { color: theme.main, width: 1 } : { type: 'none' },
      });
      t(slide, phase.products, cx + 0.2, cursorCardY, cardW - 0.4, pH, {
        fontSize: 9, color: theme.main, bold: true,
        align: 'center', valign: 'middle',
      });
      cursorCardY += pH + 0.1;
    }

    // —— 能力 bullets（可选，最多 3 条，严格控制高度避免撞胶囊）——
    const bullets = (phase.bullets || []).slice(0, 3);
    const bottomCapH = phase.note ? 0.5 : 0;
    const bulletsAreaY = cursorCardY;
    // 底部胶囊预留：胶囊本身 + 与卡片底的 0.08 间距 + 与 bullets 的 0.12 间距
    const reservedBottom = bottomCapH + (phase.note ? 0.2 : 0.1);
    const bulletsAreaH = (cardY + cardH) - bulletsAreaY - reservedBottom;
    if (bullets.length && bulletsAreaH > 0.3) {
      // 每条平均分配高度，上限 0.6"，下限取能放下的最小值
      const lineH = Math.min(0.6, bulletsAreaH / bullets.length);
      bullets.forEach((b, bi) => {
        const by = bulletsAreaY + bi * lineH;
        // 圆点
        slide.addShape(pres.shapes.OVAL, {
          x: cx + 0.3, y: by + 0.14, w: 0.1, h: 0.1,
          fill: { color: theme.main }, line: { type: 'none' },
        });
        // 文字（自动换行，字号 9.5 更紧凑）
        const bRuns = _runsFromText(b, 9.5, CLR.dark, theme.main);
        slide.addText(bRuns, {
          x: cx + 0.48, y: by, w: cardW - 0.68, h: lineH,
          align: 'left', valign: 'top',
          lineSpacingMultiple: 1.15, wrap: true,
        });
      });
    }

    // —— 底部胶囊条（局限/优势，带图标）——
    if (phase.note) {
      const capY = cardY + cardH - bottomCapH - 0.08;
      const capIcon = phase.noteIcon || (isLast ? '✦' : '⚠');
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + 0.2, y: capY, w: cardW - 0.4, h: bottomCapH,
        rectRadius: 0.06,
        fill: { color: theme.light }, line: { type: 'none' },
      });
      // 左侧图标
      t(slide, capIcon, cx + 0.28, capY, 0.34, bottomCapH, {
        fontSize: 14, color: theme.main, bold: true,
        align: 'center', valign: 'middle',
      });
      // 右侧说明
      t(slide, phase.note, cx + 0.62, capY, cardW - 0.82, bottomCapH, {
        fontSize: 9.5, color: isLast ? theme.main : CLR.body,
        bold: isLast, align: 'left', valign: 'middle',
      });
    }

    // —— 卡间箭头（非最后一张右侧）——
    if (pi < N - 1) {
      const ax = cx + cardW + gap;
      const ay = cardY + cardH / 2 - 0.2;
      slide.addShape(pres.shapes.RIGHT_ARROW, {
        x: ax, y: ay, w: arrowW, h: 0.4,
        fill: { color: CLR.medBlue }, line: { type: 'none' },
      });
    }
  });

  // === 3. 底部 footerBar（可选，深蓝带橙色高亮）===
  if (hasFooter) {
    const barH = 0.42;
    const barY = 5.625 - 0.38 - barH;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: M, y: barY, w: CW, h: barH,
      rectRadius: 0.05,
      fill: { color: CLR.blue }, line: { type: 'none' },
    });
    const fbStr = d.footerBar;
    const fbParts = String(fbStr).split(/(<b>[^<]+<\/b>)/);
    const fbRuns = [];
    fbParts.forEach((p) => {
      if (!p) return;
      const m = p.match(/^<b>([^<]+)<\/b>$/);
      if (m) {
        fbRuns.push({ text: m[1], options: { fontSize: 12.5, color: 'FFD580', bold: true, fontFace: FONT_W7 } });
      } else {
        fbRuns.push({ text: p, options: { fontSize: 12, color: CLR.white, bold: true, fontFace: FONT_W7 } });
      }
    });
    slide.addText(fbRuns, {
      x: M + 0.4, y: barY, w: CW - 0.8, h: barH,
      align: 'center', valign: 'middle',
    });
  }
}

// ══════════════════════════════════════════════════════════════
//  布局路由
// ══════════════════════════════════════════════════════════════

const RENDERERS = {
  cards:           renderCards,
  cards_outlined:  renderCardsOutlined,
  summary:         renderSummary,
  table:           renderTable,
  compare:         renderCompare,
  phases:          renderPhases,
  kpi:             renderKpi,
  hierarchy:       renderHierarchy,
  split_1_2:       renderSplit12,
  split_1_4:       renderSplit14,
  formula_phases:  renderFormulaPhases,
  circle_loop:     renderCircleLoop,
  quad_loop:       renderQuadLoop,
  trinity_pillars: renderTrinityPillars,
  breakthrough_trio: renderBreakthroughTrio,
  hub_dual_cards:    renderHubDualCards,
  hero_radial:       renderHeroRadial,
  evolution_trio:    renderEvolutionTrio,
};

// ── 主循环：遍历 slides 生成页面 ─────────────────────────────
data.slides.forEach((slideData, idx) => {
  const slide = pres.addSlide();

  // 自行渲染标题的布局，强制跳过公共标题，避免双标题叠字
  const selfTitleLayouts = ['quad_loop', 'trinity_pillars', 'breakthrough_trio', 'hub_dual_cards', 'hero_radial', 'evolution_trio'];
  if (selfTitleLayouts.includes(slideData.layout)) {
    slideData.skipCommonTitle = true;
  }

  // 公共元素
  renderPageCommon(slide, slideData, idx);

  // 根据 layout 字段路由到对应渲染器
  const layout = slideData.layout || 'cards';
  const renderer = RENDERERS[layout];

  if (renderer) {
    renderer(slide, slideData);
  } else {
    console.warn('Unknown layout "' + layout + '" on slide ' + (idx + 1) + ', falling back to cards');
    renderCards(slide, slideData);
  }
});

// ── 输出文件 ──────────────────────────────────────────────────
pres.writeFile({ fileName: outFile }).then(() => {
  console.log('Tenchage-ppt v2.0: PPT generated successfully at ' + outFile);
  console.log('Slides: ' + data.slides.length + ' | Layouts used: ' +
    [...new Set(data.slides.map(s => s.layout || 'cards'))].join(', '));
}).catch(err => {
  console.error('Error generating PPT:', err);
  process.exit(1);
});
