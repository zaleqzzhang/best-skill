#!/usr/bin/env node

/**
 * WechatApi: 微信公众号 API 统一封装
 *
 * 职责：
 *   - 凭证管理（appId/secret → access_token）
 *   - 图片上传（永久素材库）
 *   - 草稿发布
 *
 * 用法:
 *   var api = new WechatApi(appId, secret);
 *   var token = await api.getToken();
 *   var result = await api.uploadImage(filePath);
 *   var draft = await api.publishDraft(articleData);
 */

const https = require("https");
const fs = require("fs");
const path = require("path");
const os = require("os");

// ─── 配置 ──────────────────────────────────────────────────────
var TOOLS_MD_PATHS = [
  path.join(__dirname, "..", "..", "TOOLS.md"),
  path.join(os.homedir(), ".openclaw", "workspace", "TOOLS.md"),
];

// ════════════════════════════════════════════════════════════════
// WechatApi 类
// ════════════════════════════════════════════════════════════════

function WechatApi(appId, secret) {
  this.appId = appId;
  this.secret = secret;
  this._token = null;
}

// ─── 静态方法：凭证读取 ─────────────────────────────────────

WechatApi.loadCredentials = function () {
  var appId = process.env.WECHAT_APP_ID || "";
  var secret = process.env.WECHAT_APP_SECRET || "";
  var author = process.env.WECHAT_AUTHOR || "";
  if (appId && secret) return { appId: appId, secret: secret, author: author };

  for (var idx = 0; idx < TOOLS_MD_PATHS.length; idx++) {
    var toolsPath = TOOLS_MD_PATHS[idx];
    if (!fs.existsSync(toolsPath)) continue;
    var content = fs.readFileSync(toolsPath, "utf-8");
    var lines = content.split("\n");
    for (var i = 0; i < lines.length; i++) {
      var idMatch = lines[i].match(/export\s+WECHAT_APP_ID=(\S+)/);
      if (idMatch) appId = idMatch[1];
      var secretMatch = lines[i].match(/export\s+WECHAT_APP_SECRET=(\S+)/);
      if (secretMatch) secret = secretMatch[1];
      var authorMatch = lines[i].match(/export\s+WECHAT_AUTHOR=(\S+)/);
      if (authorMatch) author = authorMatch[1];
    }
    if (appId && secret) {
      return { appId: appId, secret: secret, author: author };
    }
  }
  return { appId: appId, secret: secret, author: author };
};

WechatApi.checkEnv = function () {
  var creds = WechatApi.loadCredentials();
  if (!creds.appId || !creds.secret) {
    console.error("❌ 环境变量未设置！");
    console.log("");
    console.log("请设置微信公众号 API 凭证：");
    console.log("  export WECHAT_APP_ID=your_app_id");
    console.log("  export WECHAT_APP_SECRET=your_app_secret");
    console.log("  或在 TOOLS.md 中添加上述两行");
    process.exit(1);
  }
  return creds;
};

// ─── 实例方法 ─────────────────────────────────────────────────

/**
 * HTTP 请求封装（支持 GET 字符串和 POST 对象/Bufer）
 */
WechatApi.prototype.httpRequest = function (opts, postData) {
  return new Promise(function (resolve, reject) {
    var req = https.request(opts, function (res) {
      var chunks = [];
      res.on("data", function (c) { chunks.push(c); });
      res.on("end", function () {
        var raw = Buffer.concat(chunks).toString("utf-8");
        try {
          resolve(JSON.parse(raw));
        } catch (e) {
          reject(new Error("JSON parse error: " + raw.substring(0, 300)));
        }
      });
    });
    req.on("error", reject);
    req.setTimeout(30000, function () {
      req.destroy();
      reject(new Error("request timeout"));
    });
    if (postData != null) {
      var payload;
      if (Buffer.isBuffer(postData)) payload = postData;
      else if (typeof postData === "string") payload = postData;
      else payload = JSON.stringify(postData);
      req.setHeader("Content-Length", Buffer.byteLength(payload));
      req.write(payload);
    }
    req.end();
  });
};

/**
 * 获取 access_token（带缓存，避免重复请求）
 */
WechatApi.prototype.getToken = async function () {
  if (this._token) return this._token;

  var url =
    "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" +
    this.appId +
    "&secret=" +
    this.secret;
  var r = await this.httpRequest(url);
  if (r.errcode)
    throw new Error("Token 获取失败: " + r.errmsg + " (" + r.errcode + ")");

  this._token = r.access_token;
  return this._token;
};

/**
 * 上传图片到永久素材库
 * 返回 { media_id, url }
 */
WechatApi.prototype.uploadImage = async function (filePath) {
  if (!fs.existsSync(filePath))
    throw new Error("图片不存在: " + filePath);

  var ext = path.extname(filePath).toLowerCase().replace(".", "");
  var mimeTypes = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
    bmp: "image/bmp",
    webp: "image/webp",
  };
  var mime = mimeTypes[ext] || "image/jpeg";

  var fileData = fs.readFileSync(filePath);
  var filename = path.basename(filePath);
  var boundary = "----WeChatBoundary" + Date.now();

  var header = Buffer.from(
    "--" +
      boundary +
      "\r\n" +
      'Content-Disposition: form-data; name="media"; filename="' +
      filename +
      '"\r\n' +
      "Content-Type: " +
      mime +
      "\r\n\r\n"
  );
  var footer = Buffer.from("\r\n--" + boundary + "--\r\n");
  var body = Buffer.concat([header, fileData, footer]);

  var token = await this.getToken();
  var r = await this.httpRequest(
    {
      hostname: "api.weixin.qq.com",
      path:
        "/cgi-bin/material/add_material?access_token=" + token + "&type=image",
      method: "POST",
      headers: { "Content-Type": "multipart/form-data; boundary=" + boundary },
    },
    body
  );

  if (r.errcode)
    throw new Error("上传失败: " + r.errmsg + " (" + r.errcode + ")");
  return { media_id: r.media_id, url: r.url };
};

/**
 * 发布文章到草稿箱
 * articleData: { articles: [{ title, content, digest, thumb_media_id, author }] }
 * 返回 { media_id }
 */
WechatApi.prototype.publishDraft = async function (articleData) {
  var token = await this.getToken();

  var result = await this.httpRequest(
    {
      hostname: "api.weixin.qq.com",
      path: "/cgi-bin/draft/add?access_token=" + token,
      method: "POST",
      headers: { "Content-Type": "application/json" },
    },
    articleData
  );

  if (result.errcode)
    throw new Error("发布失败: " + result.errmsg + " (" + result.errcode + ")");
  return result;
};

module.exports = WechatApi;
