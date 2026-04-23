#!/usr/bin/env node

/**
 * wechat-publisher: 发布文章到微信公众号草稿箱
 *
 * 支持 HTML 输入（Markdown 请由 AI 预排版为 HTML），自动处理：
 *   - 封面图上传 → thumb_media_id
 *   - 正文内本地图片上传 → URL 回填替换
 *   - 无封面时自动生成默认封面
 *
 * 用法:
 *   node publish.js <article.html>
 *
 * 文件格式要求 (frontmatter):
 *   ---
 *   title: 文章标题 (必填)
 *   cover: /path/to/cover.jpg (可选)
 *   author: 作者名 (可选)
 *   ---
 */

const fs = require("fs");
const path = require("path");
const os = require("os");
const WechatApi = require("./wechat-api");

// ─── 配置 ──────────────────────────────────────────────────────

const supportsColor = process.stdout.isTTY;
const color = {
  red: function (s) {
    return supportsColor ? "\x1b[31m" + s + "\x1b[0m" : s;
  },
  green: function (s) {
    return supportsColor ? "\x1b[32m" + s + "\x1b[0m" : s;
  },
  yellow: function (s) {
    return supportsColor ? "\x1b[33m" + s + "\x1b[0m" : s;
  },
};

// ════════════════════════════════════════════════════════════════
// 图片处理（扫描 HTML 中本地图片，逐个上传并替换 URL）
// ════════════════════════════════════════════════════════════════

/**
 * 扫描 HTML 中所有本地图片路径，逐个上传并替换 URL
 * 匹配 <img src="..."> 和 background-image:url(...)
 * 返回 { html, uploadedCount }
 */
async function processInlineImages(api, htmlContent, basePath) {
  // 收集所有本地路径（去重）
  var localPaths = {};
  var imgRegex =
    /<img[^>]+src=["']([^"'\s]+\.(?:jpg|jpeg|png|gif|bmp|webp))["'][^>]*>/gi;
  var bgRegex = /url\(["']?([^"'\s)]+\.(?:jpg|jpeg|png|gif|bmp|webp))["']?\)/gi;

  var match;
  while ((match = imgRegex.exec(htmlContent)) !== null) {
    localPaths[match[1]] = true;
  }
  imgRegex.lastIndex = 0;
  while ((match = bgRegex.exec(htmlContent)) !== null) {
    localPaths[match[1]] = true;
  }

  var paths = Object.keys(localPaths);
  if (paths.length === 0) return { html: htmlContent, uploadedCount: 0 };

  console.log(
    color.yellow("📤 检测到 " + paths.length + " 张本地图片，正在上传...")
  );

  var replacements = [];

  for (var i = 0; i < paths.length; i++) {
    var src = paths[i];
    var absPath;

    if (path.isAbsolute(src)) {
      absPath = src;
    } else if (basePath) {
      absPath = path.resolve(path.dirname(basePath), src);
    } else {
      absPath = path.resolve(src);
    }

    console.log(
      "   [" + (i + 1) + "/" + paths.length + "] " + path.basename(src)
    );
    try {
      var result = await api.uploadImage(absPath);
      replacements.push({ local: src, url: result.url });
      console.log(
        color.green("      ✅ " + result.media_id.substring(0, 12) + "...")
      );
    } catch (e) {
      console.log(color.yellow("      ⚠️ " + e.message));
    }
  }

  // 替换 HTML 中的路径
  var newHtml = htmlContent;
  for (var j = 0; j < replacements.length; j++) {
    var rep = replacements[j];
    newHtml = newHtml.split(rep.local).join(rep.url);
  }

  return { html: newHtml, uploadedCount: replacements.length };
}

// ════════════════════════════════════════════════════════════════
// 默认封面生成
// ════════════════════════════════════════════════════════════════

function generateDefaultCover(outputPath) {
  var pyPaths = ["/tmp/pyenv/bin/python3", "/tmp/pyenv/bin/python"];
  for (var i = 0; i < pyPaths.length; i++) {
    try {
      var execSync = require("child_process").execSync;
      execSync(
        pyPaths[i] +
          " -c \"from PIL import Image;img=Image.new('RGB',(900,500),(74,144,217));img.save('" +
          outputPath +
          "','JPEG',quality=85)\"",
        { stdio: "pipe" }
      );
      if (fs.existsSync(outputPath) && fs.statSync(outputPath).size > 1000)
        return true;
    } catch (e) {}
  }
  return false;
}

// ════════════════════════════════════════════════════════════════
// Frontmatter 解析
// ════════════════════════════════════════════════════════════════

/**
 * 解析 frontmatter，若缺失则自动生成
 * 标题提取优先级：
 *   frontmatter.title > HTML <title> > MD 第一个 # 标题 > 文件名（去掉扩展名）
 */
function parseFrontmatter(content, filePath) {
  var match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);

  var meta = {};
  var body;

  if (match) {
    // 有 frontmatter，解析已知字段
    var lines = match[1].split("\n");
    for (var i = 0; i < lines.length; i++) {
      var m = lines[i].match(/^(\w[\w-]*)\s*:\s*(.+)$/);
      if (m) meta[m[1].trim()] = m[2].trim();
    }
    body = match[2];
  } else {
    // 无 frontmatter，全文作为 body
    body = content;
  }

  // 缺失标题时自动提取
  if (!meta.title) {
    if (!match || !meta.title) {
      // HTML：从 <title> 提取
      var titleMatch = content.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
      if (titleMatch) {
        meta.title = titleMatch[1].trim();
      } else {
        // Markdown：从第一个 # 标题提取
        var h1Match = content.match(/^#\s+(.+)$/m);
        if (h1Match) {
          meta.title = h1Match[1].trim();
        } else {
          // 兜底：使用文件名
          meta.title = path.basename(filePath).replace(/\.[^.]+$/, "");
        }
      }
    }
    console.log(color.yellow("📌 自动提取标题: " + meta.title));
  }

  return { meta: meta, body: body };
}

// ════════════════════════════════════════════════════════════════
// 凭证检查（委托给 WechatApi）
// ════════════════════════════════════════════════════════════════

function checkEnv() {
  return WechatApi.checkEnv();
}

// ════════════════════════════════════════════════════════════════
// 核心发布流程
// ════════════════════════════════════════════════════════════════

async function publish(file, appId, secret) {
  var api = new WechatApi(appId, secret);
  var ext = path.extname(file).toLowerCase();
  if (ext !== ".html") {
    console.error(color.red("❌ 仅支持 .html 文件！"));
    console.log("");
    console.log(color.yellow("请先由 AI 将 Markdown 智能排版为 HTML，再传入本脚本："));
    console.log("  1. 阅读 SKILL.md 中「AI 智能排版」指引");
    console.log("  2. 排版完成后: node publish.js article.html");
    process.exit(1);
  }

  console.log(color.green("📝 准备发布文章..."));
  console.log("  文件: " + file);
  console.log("");

  // ── Step 0: 读取 & 解析文件 ──────────────────────────────
  var absFile = path.resolve(file);
  var rawContent = fs.readFileSync(absFile, "utf-8");
  var parsed = parseFrontmatter(rawContent, absFile);

  if (!parsed || !parsed.meta.title) {
    console.error(color.red("❌ 无法确定文章标题！"));
    console.log(
      color.yellow(
        "请在文件中添加 frontmatter（title 字段），或提供 HTML <title> / Markdown # 标题。"
      )
    );
    process.exit(1);
  }

  var meta = parsed.meta;
  var body = parsed.body;

  console.log("  标题: " + meta.title);

  // ── Step 1: 获取 Token ────────────────────────────────────
  console.log(color.yellow("\n🔑 获取 Access Token..."));
  try {
    await api.getToken();
  } catch (e) {
    console.error(color.red("❌ " + e.message));
    process.exit(1);
  }
  console.log(color.green("✅ Token OK"));

  // ── Step 2: 正文内容（已由 AI 智能排版为 HTML）──────────
  var htmlContent = body;
  console.log(color.yellow("\n📄 HTML 正文（" + body.length + " chars）"));

  // ── Step 3: 处理正文中的本地图片 ─────────────────────────
  var imageResult = await processInlineImages(api, htmlContent, absFile);
  htmlContent = imageResult.html;

  if (imageResult.uploadedCount > 0) {
    console.log(
      color.green("✅ " + imageResult.uploadedCount + " 张图片已上传并替换 URL")
    );
  }

  // ── Step 4: 封面图 ────────────────────────────────────────
  var thumbMediaId = "";
  var coverPath = meta.cover ? meta.cover : null;

  if (coverPath) {
    coverPath = path.isAbsolute(coverPath)
      ? coverPath
      : path.resolve(path.dirname(absFile), coverPath);

    if (fs.existsSync(coverPath)) {
      console.log(color.yellow("\n📤 上传封面图: " + path.basename(coverPath)));
      try {
        var coverResult = await api.uploadImage(coverPath);
        thumbMediaId = coverResult.media_id;
        console.log(
          color.green(
            "✅ 封面 OK, media_id=" + thumbMediaId.substring(0, 16) + "..."
          )
        );
      } catch (e) {
        console.log(
          color.yellow("⚠️ 封面上传失败: " + e.message + ", 使用默认封面")
        );
      }
    } else {
      console.log(
        color.yellow("⚠️ 封面图不存在: " + coverPath + ", 使用默认封面")
      );
    }
  }

  // 无有效封面 → 自动生成
  if (!thumbMediaId) {
    console.log(color.yellow("\n📤 生成默认封面..."));
    var tmpCover = path.join(os.tmpdir(), "wc_cover_" + Date.now() + ".jpg");
    var ok = generateDefaultCover(tmpCover);
    if (ok) {
      try {
        var defResult = await api.uploadImage(tmpCover);
        thumbMediaId = defResult.media_id;
        console.log(
          color.green(
            "✅ 默认封面 OK, media_id=" + thumbMediaId.substring(0, 16) + "..."
          )
        );
      } catch (e) {
        console.log(color.yellow("⚠️ 默认封面上传失败: " + e.message));
      }
    } else {
      console.log(color.yellow("⚠️ 无法生成默认封面（需安装 Pillow）"));
    }
    try {
      fs.unlinkSync(tmpCover);
    } catch (_) {}
  }

  if (!thumbMediaId) {
    console.error(
      color.red("\n❌ 无可用封面图，发布可能失败！建议提供 --cover 参数")
    );
  }

  // ── Step 5: 摘要（必须从 frontmatter digest 读取）────
  var digest = meta.digest || "";
  if (!digest) {
    console.error(
      color.red("❌ 缺少摘要（digest）！")
    );
    console.log("");
    console.log(
      color.yellow("请在文件 frontmatter 中添加 digest 字段：")
    );
    console.log("  ---");
    console.log("  digest: 文章摘要内容");
    console.log("  ---");
    process.exit(1);
  }

  // ── Step 6: 发布草稿 ──────────────────────────────────────
  console.log(color.yellow("\n🚀 发布到公众号草稿箱..."));

  var articleData = {
    articles: [
      {
        title: meta.title,
        content: htmlContent,
        digest: digest || undefined,
        content_source_url: "",
        thumb_media_id: thumbMediaId,
        author: meta.author || "",
        need_open_comment: 0,
        only_fans_can_comment: 0,
      },
    ],
  };

  try {
    var result = await api.publishDraft(articleData);

    if (result.media_id) {
      console.log("");
      console.log(color.green("╔══════════════════════════════════╗"));
      console.log(color.green("║       🎉 发布成功！              ║"));
      console.log(color.green("╠══════════════════════════════════╣"));
      console.log("  标题:     " + meta.title);
      console.log("  格式:     HTML");
      console.log("  图片:     " + imageResult.uploadedCount + " 张");
      console.log("  media_id: " + result.media_id);
      console.log("");
      console.log(color.yellow("  👉 前往查看: https://mp.weixin.qq.com/"));
      console.log(color.green("╚══════════════════════════════════╝"));
    } else {
      console.log("");
      console.error(
        color.red("❌ 发布失败: " + (result.errmsg || JSON.stringify(result)))
      );

      var tips = {
        41001: "Access Token 无效或过期",
        40007: "封面图 media_id 无效",
        45009: "发布频率超限",
        48006: "正文内容违规",
        48004: "标题违规",
      };
      if (tips[result.errcode]) {
        console.log(color.yellow("💡 提示: " + tips[result.errcode]));
      }
    }
  } catch (e) {
    console.error(color.red("❌ 请求异常: " + e.message));
    process.exit(1);
  }
}

// ════════════════════════════════════════════════════════════════
// 帮助 & 主入口
// ════════════════════════════════════════════════════════════════

function showHelp() {
  console.log(
    [
      "",
      "  wechat-publisher — 微信公众号草稿发布工具",
      "",
      "  Usage:",
      "    node publish.js <article.html>",
      "",
      "  说明: 仅接受 .html 文件。Markdown 需先由 AI 智能排版为 HTML。",
      "",
      "  Frontmatter (可选):",
      "    ---",
      "    title: 文章标题          (可选，缺失则自动从 HTML <title> 提取)",
      "    cover: /abs/path/to/cover.jpg   (可选，缺失则自动生成)",
      "    author: 作者名                   (可选)",
      "    ---",
      "",
      "  支持特性:",
      "    • 本地图片自动上传至微信素材库并回填 URL",
      "    • 无封面时自动生成蓝色默认封面",
      "    • 不依赖 wenyan-cli，直接调用微信 API",
      "",
    ].join("\n")
  );
}

async function main() {
  var args = process.argv.slice(2);

  if (args.length === 0 || args[0] === "-h" || args[0] === "--help") {
    showHelp();
    process.exit(0);
  }

  var file = args[0];

  if (!fs.existsSync(file)) {
    console.error(color.red("❌ 文件不存在: " + file));
    process.exit(1);
  }

  var creds = checkEnv();

  try {
    await publish(file, creds.appId, creds.secret);
  } catch (e) {
    console.error(color.red("\n❌ 未预期的错误: " + e.message));
    process.exit(1);
  }
}

main();
