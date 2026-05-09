# 扫描执行工作流

## 工作流概述

扫描执行工作流负责根据扫描模式执行 PreCI 代码规范检查，并解析扫描结果。

**⏱️ 执行时机**：文件过滤完成后（步骤 [4/7]）

## 执行前置条件

- 文件过滤完成
- 找到至少 1 个代码文件需要扫描
- PreCI Server 运行正常

## 扫描模式

### Combined 模式（默认）

**说明**：当前 PreCI 版本不支持 `--diff` 参数，Combined 模式直接执行 `--pre-commit` 扫描，覆盖未暂存和已暂存的变更文件。

```bash
execute_combined_scan() {
    echo "[4/7] 执行扫描"
    echo "      模式: Combined（组合扫描）"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 执行 --pre-commit 扫描（覆盖所有变更文件）
    echo "      [4.1] --pre-commit 扫描..."
    local scan_output=$(preci scan --pre-commit 2>&1)
    local issue_count=$(echo "$scan_output" | grep -c 'violation' || echo 0)
    echo "      [4.1] --pre-commit 扫描: 发现 $issue_count 个问题"
    
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 输出扫描结果
    echo "$scan_output"
}
```

**关键点**：
1. ✅ **单次扫描**：`--pre-commit` 已覆盖所有变更文件，无需多次扫描合并
2. ✅ **强制输出**：必须输出执行结果和问题数量
3. ✅ **统一审查**：基于扫描结果进行统一审查

### Diff 模式

仅扫描变更文件（与 Combined 模式相同，使用 `--pre-commit`）：

```bash
execute_diff_scan() {
    echo "[4/7] 执行扫描"
    echo "      模式: Diff（变更文件）"
    
    local output=$(preci scan --pre-commit 2>&1)
    local exit_code=$?
    local issue_count=$(echo "$output" | grep -c 'violation' || echo 0)
    
    echo "      发现问题: $issue_count 个"
    echo "$output"
}
```

### Pre-commit 模式

仅扫描已暂存文件：

```bash
execute_precommit_scan() {
    echo "[4/7] 执行扫描"
    echo "      模式: Pre-commit（已暂存文件）"
    
    local output=$(preci scan --pre-commit 2>&1)
    local exit_code=$?
    local issue_count=$(echo "$output" | grep -c 'violation' || echo 0)
    
    echo "      发现问题: $issue_count 个"
    echo "$output"
}
```

### All 模式

全量扫描所有文件：

```bash
execute_all_scan() {
    echo "[4/7] 执行扫描"
    echo "      模式: All（全量扫描）"
    
    local output=$(preci scan --all 2>&1)
    local exit_code=$?
    local issue_count=$(echo "$output" | grep -c 'violation' || echo 0)
    
    echo "      发现问题: $issue_count 个"
    echo "$output"
}
```

## 扫描结果解析

### 问题分类统计

```bash
parse_scan_result() {
    local output=$1
    local -A issue_types
    
    while IFS= read -r line; do
        if [[ $line =~ \[([^\]]+)\] ]]; then
            local rule="${BASH_REMATCH[1]}"
            ((issue_types[$rule]++))
        fi
    done <<< "$output"
    
    # 输出统计
    echo "      📊 问题分类:"
    for rule in "${!issue_types[@]}"; do
        echo "         - $rule: ${issue_types[$rule]} 个"
    done
}
```

## 输出格式

### Combined 模式标准输出

```
[4/7] 执行扫描
      模式: Combined（组合扫描）
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      [4.1] --pre-commit 扫描...
      [4.1] --pre-commit 扫描: 发现 3 个问题
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      
      📊 问题分类:
         - inner_ip_leak: 1 个
         - code_style: 2 个

File: src/main/java/com/example/UserService.java
  Line 15: [code_style] 缩进不正确，应为4空格

File: src/main/java/com/example/OrderService.java
  Line 42: [inner_ip_leak] 发现内网IP地址: 10.0.0.1
  Line 56: [code_style] 缺少空格
```

### 无问题时的输出

```
[4/7] 执行扫描
      模式: Combined（组合扫描）
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      [4.1] --pre-commit 扫描...
      [4.1] --pre-commit 扫描: 发现 0 个问题
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 未发现任何代码规范问题
```

## 错误处理

### 扫描命令失败

```
[4/7] 执行扫描
      ❌ 扫描命令执行失败: preci scan --pre-commit
      错误信息: Connection refused

可能原因：
- PreCI Server 未运行或崩溃（请重新执行 preci:check，步骤 [1/7] 会重新启动 Server）
- 权限不足
- 项目配置错误

请检查 PreCI 状态并重试。
```

## 强制约束

### Combined 模式强制约束

**禁止行为**：
- ❌ 使用 `--diff` 参数（当前版本不支持）
- ❌ 扫描失败时在此步骤内重启 PreCI Server（Server 管理由步骤 [1/7] 负责）
- ❌ 不输出扫描结果就进入下一步

**必须行为**：
- ✅ 必须执行 [4.1] preci scan --pre-commit
- ✅ 输出扫描发现的问题数量
- ✅ 基于扫描结果进行统一审查

### 通用约束

**禁止行为**：
- ❌ 不输出扫描结果就进入下一步
- ❌ 不统计问题数量
- ❌ 扫描失败时静默继续

**必须行为**：
- ✅ 输出完整的扫描过程和结果
- ✅ 统计问题数量和分类
- ✅ 扫描失败时输出错误信息
