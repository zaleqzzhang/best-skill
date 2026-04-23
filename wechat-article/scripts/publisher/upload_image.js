#!/usr/bin/env node

/**
 * upload_image: 上传图片到微信公众号永久素材库
 *
 * 用法:
 *   node upload_image.js <image-file> [image-file2 ...]
 *
 * 返回每张图片的 media_id 和 url
 * 支持: jpg / jpeg / png / gif / bmp / webp
 */

const path = require("path");
const WechatApi = require("./wechat-api");

// ─── 终端颜色 ────────────────────────────────────────────────
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

// ─── 帮助 ─────────────────────────────────────────────────────
function showHelp() {
  console.log(
    [
      "Usage: node upload_image.js <image-file> [image-file2 ...]",
      "",
      "Examples:",
      "  node upload_image.js cover.jpg",
      "  node upload_image.js img1.png img2.jpg img3.png",
      "",
      "Supported formats: jpg, jpeg, png, gif, bmp, webp",
      "",
      'Output: JSON array with { file, media_id, url } for each image',
    ].join("\n")
  );
}

// ─── 主函数 ──────────────────────────────────────────────────
async function main() {
  var args = process.argv.slice(2);

  if (args.length === 0 || args[0] === "-h" || args[0] === "--help") {
    showHelp();
    process.exit(0);
  }

  var creds = WechatApi.checkEnv();

  var api = new WechatApi(creds.appId, creds.secret);

  console.log(color.yellow("🔑 获取 Access Token..."));
  try {
    await api.getToken();
  } catch (e) {
    console.error(color.red("❌ " + e.message));
    process.exit(1);
  }
  console.log(color.green("✅ Token OK"));

  var results = [];
  for (var i = 0; i < args.length; i++) {
    var file = args[i];
    var absPath = path.resolve(file);
    console.log(color.yellow("📤 上传: " + path.basename(absPath)));
    try {
      var result = await api.uploadImage(absPath);
      result.file = absPath;
      console.log(
        color.green("✅ 成功: media_id=" + result.media_id)
      );
      console.log("   url: " + result.url);
      results.push(result);
    } catch (e) {
      console.error(
        color.red("❌ 失败 (" + path.basename(absPath) + "): " + e.message)
      );
      results.push({ file: absPath, error: e.message });
    }
  }

  console.log("");
  console.log("📋 结果汇总:");
  console.log(JSON.stringify(results, null, 2));
}

main();
