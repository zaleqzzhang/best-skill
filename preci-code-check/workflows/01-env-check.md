# 环境检测工作流

## 工作流概述

环境检测是 PreCI 代码规范检查的**第一步**，负责检测 PreCI 工具是否已安装、路径配置是否正确、服务是否运行等。

**⏱️ 执行时机**：每次 PreCI 检查的第一步（步骤 [1/7]）

## 执行前置条件

- 当前目录为 Git 仓库
- 有网络连接（如需安装 PreCI）
- 具有文件读写权限

## 执行步骤

### Step 1.1：检测 PreCI 命令路径

**🔴 强制约束**：必须按以下顺序执行所有检测步骤，每步都必须输出检测结果。

```bash
# Step 1.1【必须】：检测默认路径
echo "[1/7] 环境检测"
echo "      [1.1] 检测 PreCI 命令路径..."

if [ -x "$HOME/PreCI/preci" ]; then
    PRECI_CMD="$HOME/PreCI/preci"
    echo "      ✅ 在默认路径找到 PreCI: $PRECI_CMD"
    PRECI_FOUND=true
else
    echo "      ⚠️ 默认路径未找到 PreCI: $HOME/PreCI/preci"
    PRECI_FOUND=false
fi

# Step 1.2【必须】：若 Step 1.1 未找到，检测系统 PATH
if [ "$PRECI_FOUND" = false ]; then
    if command -v preci &>/dev/null; then
        PRECI_CMD="preci"
        echo "      ✅ 在系统 PATH 找到 PreCI: $(which preci)"
        PRECI_FOUND=true
    else
        echo "      ⚠️ 系统 PATH 未找到 PreCI"
    fi
fi

# Step 1.3【必须】：输出最终检测结果
if [ "$PRECI_FOUND" = true ]; then
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      ✅ PreCI 检测成功"
    echo "         命令路径: $PRECI_CMD"
    echo "         版本信息: $($PRECI_CMD version 2>/dev/null || echo '无法获取')"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      ❌ PreCI 检测失败（两个路径均未找到）"
    echo "         已检测: $HOME/PreCI/preci, 系统 PATH"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    # 进入安装流程
fi
```

**关键点**：
1. ✅ **步骤编号**：`[1.1]`、`[1.2]` 明确执行进度
2. ✅ **强制输出**：每步都必须输出检测结果（成功或失败）
3. ✅ **状态变量**：`PRECI_FOUND` 确保逻辑连贯
4. ✅ **最终汇总**：输出完整检测报告

### Step 1.2：自动安装 PreCI（如需要）

若未找到 PreCI，执行自动安装流程。

**核心策略**：`install.sh` 包含多处交互式 `read` 提示（root 身份确认、目录覆盖确认等），在非交互式 AI 执行环境中会直接失败。
因此**绕过 `install.sh`，直接将 `scripts/PreCI/` 目录中的二进制文件和配置拷贝到目标目录**。

```bash
install_preci() {
    echo "      [1.2] 开始安装 PreCI（非交互式直接拷贝模式）..."

    # ── Step A：定位 SKILL_BASE ──────────────────────────────────────
    local SKILL_BASE=""

    # 1. 项目目录下的 skill 路径（最优先）
    local project_skill_path
    project_skill_path=$(find /data/workspace -maxdepth 5 \
        -path "*/preci-code-check/SKILL.md" -type f 2>/dev/null \
        | head -1 | xargs -r dirname 2>/dev/null)
    [ -d "$project_skill_path" ] && SKILL_BASE="$project_skill_path"

    # 2. root/.codebuddy 路径
    [ ! -d "$SKILL_BASE" ] && SKILL_BASE="/root/.codebuddy/skills/preci-code-check"

    # 3. HOME/.codebuddy 备选路径
    [ ! -d "$SKILL_BASE" ] && SKILL_BASE="$HOME/.codebuddy/skills/preci-code-check"

    # 4. 兜底搜索
    if [ ! -d "$SKILL_BASE" ]; then
        SKILL_BASE=$(find ~ -path "*/preci-code-check/SKILL.md" -type f 2>/dev/null \
            | head -1 | xargs -r dirname)
    fi

    local src_dir="${SKILL_BASE}/scripts/PreCI"

    if [ ! -d "$src_dir" ]; then
        echo "      ❌ 未找到 PreCI 源文件目录: $src_dir"
        return 1
    fi
    echo "         源文件目录: $src_dir"

    # ── Step B：准备目标目录 ─────────────────────────────────────────
    local target_dir="$HOME/PreCI"
    echo "         安装目录  : $target_dir"

    # 若目标目录已存在且有 preci 进程，先停止
    if [ -d "$target_dir" ]; then
        local preci_pids
        preci_pids=$(pgrep -f "preci-server" 2>/dev/null || true)
        if [ -n "$preci_pids" ]; then
            echo "         停止已有 PreCI 进程..."
            echo "$preci_pids" | xargs kill -15 2>/dev/null || true
            sleep 1
        fi
    fi
    mkdir -p "$target_dir"

    # ── Step C：直接拷贝文件（跳过 install.sh 的交互流程）──────────────
    local files_to_copy=(
        "preci" "preci-server" "preci-mcp"
        "config" "checkerset"
        "install.sh" "uninstall.sh" "uninstall_old_preci.sh"
    )
    local dirs_to_create=("db" "log" "tool")

    echo "         拷贝文件..."
    for item in "${files_to_copy[@]}"; do
        local src="${src_dir}/${item}"
        local dst="${target_dir}/${item}"
        if [ -e "$src" ]; then
            cp -r "$src" "$dst"
            # 为可执行文件授权
            case "$item" in preci|preci-server|preci-mcp) chmod +x "$dst" ;; esac
        fi
    done

    echo "         创建辅助目录..."
    for d in "${dirs_to_create[@]}"; do
        mkdir -p "${target_dir}/${d}"
    done

    echo "         ✅ 文件拷贝完成"
    return 0
}
```

**安装说明**：
- 直接从技能内置的 `scripts/PreCI/` 目录拷贝二进制文件，**完全绕过交互式 `install.sh`**
- 安装完成后如需将 `~/PreCI` 加入 PATH，可手动执行 `source ~/.bashrc`
- 安装后 PreCI Server 从 `~/PreCI/preci` 启动，install dir 自动指向正确路径

### Step 1.3：安装后验证

```bash
verify_installation() {
    echo "      [1.3] 验证安装结果..."
    
    # 重新检测 PreCI 路径
    if [ -x "$HOME/PreCI/preci" ]; then
        PRECI_CMD="$HOME/PreCI/preci"
        echo "      ✅ PreCI 安装成功: $PRECI_CMD"
        return 0
    elif command -v preci &>/dev/null; then
        PRECI_CMD="preci"
        echo "      ✅ PreCI 安装成功: $(which preci)"
        return 0
    else
        echo "      ❌ PreCI 安装验证失败"
        return 1
    fi
}
```

### Step 1.4：检测登录状态

**🔴 强制约束**：
- 登录状态检测**必须在 Server 启动后执行**
- 检测到未登录或 token 无效时，**立即硬停止全部后续步骤**，输出登录命令，等待用户在终端完成登录并告知 AI 后，方可继续
- **登录操作本身只能由用户在终端手工执行，AI 禁止代劳**

```bash
check_login_status() {
    echo "      [1.4] 检测 PreCI 登录状态..."

    # 使用 preci init 做实际鉴权探测：
    # - checkerset list 读取本地缓存，无需联网，即使 token 过期也返回成功，无法判断登录态
    # - preci init 会向服务端发起鉴权请求，token 无效时返回 100005 错误，能准确反映登录状态
    local login_check
    login_check=$($PRECI_CMD init 2>&1)

    # 匹配所有未登录 / token 失效的特征字符串（含 init 和 server start 返回的错误码）
    if echo "$login_check" | grep -qiE \
        "未登录|not logged|login required|unauthorized|access token|token.*无效|100005|100004|自动登录失败"; then

        echo "      ⚠️ PreCI 登录状态无效（未登录或 token 已过期）"
        echo ""
        echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "      🔐 需要登录 PreCI，请在终端执行以下命令："
        echo ""
        echo "      ~/PreCI/preci login -u <企微英文名> -p <蓝盾项目id> --pin <pin码> -t <ioa token>"
        echo ""
        echo "      参数说明："
        echo "        -u      企微英文名（如：zhangsan）"
        echo "        -p      蓝盾项目 ID"
        echo "        --pin   PIN 码"
        echo "        -t      IOA Token（从 https://ioa.tencent.com 获取）"
        echo ""
        echo "      ⏸️  登录完成后，请告知 AI「已完成登录，继续执行」"
        echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        # 硬停止：返回特殊退出码，调用方必须终止后续所有步骤
        return 2
    fi

    echo "      ✅ PreCI 登录状态正常"
    return 0
}
```

**调用方处理规则（必须遵守）**：

```bash
check_login_status
login_exit=$?

if [ $login_exit -eq 2 ]; then
    # 硬停止：不执行 1.5、1.6 及后续任何步骤
    # 等待用户在对话中回复「已完成登录，继续执行」后，从头重新执行步骤 [1/7]
    exit 0
fi
```

**处理规则**：
- 返回 `2`（未登录）→ **立即终止**，输出登录命令，**停止执行 1.5/1.6 及所有后续步骤**，等待用户登录并确认
- 返回 `0`（已登录）→ 继续执行 1.5 检测 Server 状态

### Step 1.5：检测 PreCI Server 状态

```bash
check_server_status() {
    echo "      [1.5] 检测 PreCI Server 状态..."

    local status_output
    status_output=$($PRECI_CMD server status 2>&1)

    if echo "$status_output" | grep -q "preci server is running"; then
        echo "      ✅ PreCI Server 运行正常"
        return 0
    else
        echo "      ⚠️ PreCI Server 未运行"
        return 1
    fi
}
```

### Step 1.6：启动 PreCI Server（如需要）

```bash
start_server() {
    echo "      [1.6] 启动 PreCI Server..."
    $PRECI_CMD server start 2>&1

    # 等待服务启动（最多 10 秒）
    local max_wait=10
    local waited=0

    while [ $waited -lt $max_wait ]; do
        sleep 1
        if $PRECI_CMD server status 2>&1 | grep -q "preci server is running"; then
            echo "      ✅ PreCI Server 启动成功"
            return 0
        fi
        waited=$((waited + 1))
        echo "         等待中... ($waited/$max_wait)"
    done

    echo "      ⚠️ PreCI Server 启动超时，继续执行后续步骤..."
    return 1
}
```

**执行顺序说明**：Server 启动完成后，**必须执行 Step 1.7 登录状态校验**。
Server 启动过程中若出现 `自动登录失败` 等字样，不视为登录成功，仍需执行 Step 1.7。

### Step 1.7：校验登录状态（Server 启动后必须执行）

> 此步骤是对 Step 1.4 `check_login_status()` 的实际调用入口，
> 放在 Server 启动后执行，确保 Server 已就绪再发起认证检测。

```bash
echo "      [1.7] 校验 PreCI 登录状态（Server 启动后）..."

check_login_status   # 定义见 Step 1.4
login_exit=$?

if [ $login_exit -eq 2 ]; then
    # ⛔ 硬停止：不执行任何后续步骤（步骤 [2/7] ~ [7/7] 全部跳过）
    # 等待用户在对话中回复「已完成登录，继续执行」
    exit 0
fi

echo "      ✅ 环境检测完成，进入项目初始化"
```

## 执行顺序总览

```
[1/7] 环境检测
  1.1  检测 PreCI 命令路径
  1.2  若未找到：自动安装（非交互式拷贝）
  1.3  安装后验证
  1.5  检测 Server 状态
  1.6  若未运行：启动 Server
  1.7  校验登录状态  ← Server 启动后执行，未登录则硬停止
```

> **注意**：Step 1.4 `check_login_status()` 是函数定义，实际调用入口是 Step 1.7。

## 输出格式

### 成功输出

```
[1/7] 环境检测
      [1.1] 检测 PreCI 命令路径...
      ✅ 在默认路径找到 PreCI: /root/PreCI/preci
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ✅ PreCI 检测成功
         命令路径: /root/PreCI/preci
         版本信息: v0.8.18
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      [1.5] 检测 PreCI Server 状态...
      ✅ PreCI Server 运行正常
      [1.7] 校验 PreCI 登录状态（Server 启动后）...
      ✅ PreCI 登录状态正常
      ✅ 环境检测完成，进入项目初始化
```

### 需要安装 + 需要登录的输出

```
[1/7] 环境检测
      [1.1] 检测 PreCI 命令路径...
      ⚠️ 默认路径未找到 PreCI: /root/PreCI/preci
      ⚠️ 系统 PATH 未找到 PreCI
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ❌ PreCI 检测失败（两个路径均未找到）
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      [1.2] 开始安装 PreCI（非交互式直接拷贝模式）...
         源文件目录: .../scripts/PreCI
         安装目录  : /root/PreCI
         拷贝文件... 创建辅助目录...
         ✅ 文件拷贝完成
      [1.3] 验证安装结果...
      ✅ PreCI 安装成功: /root/PreCI/preci
      [1.5] 检测 PreCI Server 状态...
      ⚠️ PreCI Server 未运行
      [1.6] 启动 PreCI Server...
      ✅ PreCI Server 启动成功
      [1.7] 校验 PreCI 登录状态（Server 启动后）...
      ⚠️ PreCI 登录状态无效（未登录或 token 已过期）

      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      🔐 需要登录 PreCI，请在终端执行以下命令：

      ~/PreCI/preci login -u <企微英文名> -p <蓝盾项目id> --pin <pin码> -t <ioa token>

      参数说明：
        -u      企微英文名（如：zhangsan）
        -p      蓝盾项目 ID
        --pin   PIN 码
        -t      IOA Token（从 https://ioa.tencent.com 获取）

      ⏸️  登录完成后，请告知 AI「已完成登录，继续执行」
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 错误处理

### 安装失败处理

```
❌ PreCI 安装失败（可能原因：源文件目录不存在或权限不足）。

请选择操作：
a. 重试安装 — 尝试重新安装 PreCI
b. 手动安装 — 手动安装后输入「已完成，继续」
c. 中止 — 停止当前任务执行
```

### 服务启动失败

服务启动超时**不阻塞流程**，输出警告后继续执行 Step 1.7：

```
⚠️ PreCI Server 启动超时，继续执行后续步骤...
（若扫描失败，请手动执行 ~/PreCI/preci server start 后重试）
```

## 强制约束

### 禁止行为

- ❌ 跳过任何检测步骤
- ❌ 不输出检测结果就进入下一步
- ❌ 未验证安装成功就继续
- ❌ Step 1.7 检测到未登录后继续执行后续步骤（[2/7] ~ [7/7]）
- ❌ 代替用户执行 `preci login` 命令（登录只能由用户在终端手工执行）
- ❌ Server 启动过程中出现"自动登录失败"就跳过 Step 1.7

### 必须行为

- ✅ 按 1.1 → 1.2/1.3（需要时）→ 1.5 → 1.6（需要时）→ 1.7 顺序执行
- ✅ 每步都必须输出执行状态
- ✅ Step 1.7 检测到未登录时：输出登录命令 → **硬停止** → 等待用户确认
- ✅ 用户告知「已完成登录，继续执行」后：**从步骤 [1/7] 重新开始**（重新执行完整环境检测）
