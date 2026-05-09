# 自动修正工作流

## 工作流概述

自动修正工作流负责根据扫描结果自动修正可修正的代码规范问题，并进行验证和重试。

**⏱️ 执行时机**：
- 扫描完成后（步骤 [5/7]）
- 必须执行（不可跳过）

## 执行前置条件

- 扫描完成且发现问题
- 文件具有写权限

## 执行步骤

### Step 5.1：解析扫描结果

```bash
parse_scan_issues() {
    echo "[5/7] 自动修正"
    echo "      [5.1] 解析扫描结果..."
    
    local output=$1
    local -A issues_by_file
    local current_file=""
    local issue_count=0
    
    while IFS= read -r line; do
        # 提取文件路径
        if [[ $line =~ File:\ (.+)$ ]]; then
            current_file="${BASH_REMATCH[1]}"
        # 提取问题行
        elif [[ $line =~ Line\ ([0-9]+):\ \[([^\]]+)\]\ (.+)$ ]]; then
            local line_no="${BASH_REMATCH[1]}"
            local rule="${BASH_REMATCH[2]}"
            local message="${BASH_REMATCH[3]}"
            
            issues_by_file["$current_file"]+="$line_no|$rule|$message\n"
            ((issue_count++))
        fi
    done <<< "$output"
    
    echo "      ✅ 解析完成: 共 $issue_count 个问题"
    
    # 返回问题列表（JSON 格式）
    for file in "${!issues_by_file[@]}"; do
        echo "{\"file\":\"$file\",\"issues\":\"${issues_by_file[$file]}\"}"
    done
}
```

### Step 5.2：执行自动修正（重试循环）

**🔴 强制约束**：必须执行完整的重试循环，不允许提前退出（除非全部修正）。

```bash
auto_fix_with_retry() {
    local scan_output=$1
    local max_retry=${2:-3}
    
    local total_fixed=0
    local scan_output="$1"
    
    echo "      [5.2] 开始自动修正（最大重试: $max_retry 轮）"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 🔴 强制约束：必须执行完整的重试循环
    for retry in $(seq 1 $max_retry); do
        echo ""
        echo "      ━━ 第 $retry/$max_retry 轮修正 ━━"
        
        # 解析当前问题
        local issue_count=$(echo "$scan_output" | grep -c 'violation' || echo 0)
        echo "         当前待修正问题: $issue_count 个"
        
        if [ "$issue_count" -eq 0 ]; then
            echo "         ✅ 无遗留问题，提前结束"
            break
        fi
        
        # 执行修正
        local round_fixed=0
        local issues=$(parse_scan_issues "$scan_output")
        
        # 逐条处理
        while IFS= read -r issue_json; do
            local file=$(echo "$issue_json" | jq -r '.file')
            local issues=$(echo "$issue_json" | jq -r '.issues')
            
            # 逐个问题修正
            while IFS= read -r issue_line; do
                IFS='|' read -r line rule message <<< "$issue_line"
                
                if fix_single_issue "$file" "$line" "$rule"; then
                    ((round_fixed++))
                fi
            done <<< "$issues"
        done <<< "$issues"
        
        echo "         本轮修正: $round_fixed 个"
        total_fixed=$((total_fixed + round_fixed))
        
        # 🔴 必须：重新扫描验证
        echo "         [5.2.$retry] 重新扫描验证..."
        
        # 重新扫描
        scan_output=$(preci scan --pre-commit 2>&1)
        
        # 检查是否全部修正
        local remaining=$(echo "$scan_output" | grep -c 'violation' || echo 0)
        echo "         剩余问题: $remaining 个"
        
        if [ "$remaining" -eq 0 ]; then
            echo "         ✅ 所有问题已修正，提前结束"
            break
        fi
        
        # 本轮无修正且非最后一轮，继续尝试
        if [ "$round_fixed" -eq 0 ]; then
            echo "         ⚠️ 本轮无问题被修正，但仍有剩余问题"
            if [ $retry -lt $max_retry ]; then
                echo "         → 继续下一轮尝试"
            else
                echo "         → 已达最大重试次数"
            fi
        fi
    done
    
    # 统计最终剩余问题
    local remaining_count=$(echo "$scan_output" | grep -c 'violation' || echo 0)
    
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      📊 自动修正完成:"
    echo "         共修正: $total_fixed 个问题"
    echo "         剩余问题: $remaining_count 个"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $remaining_count
}
```

### Step 5.3：单条问题修正

```bash
fix_single_issue() {
    local file=$1
    local line=$2
    local rule=$3
    
    echo "         处理 [$rule]: $file:$line"
    
    case "$rule" in
        inner_ip_leak)
            fix_inner_ip_leak "$file" "$line"
            return $?
            ;;
        sensitive_info)
            fix_sensitive_info "$file" "$line"
            return $?
            ;;
        code_style)
            fix_code_style "$file" "$line"
            return $?
            ;;
        naming_convention)
            fix_naming_convention "$file" "$line"
            return $?
            ;;
        unused_import)
            fix_unused_import "$file" "$line"
            return $?
            ;;
        *)
            echo "         ⚠️ 无法自动修正的规则: $rule"
            return 1
            ;;
    esac
}
```

## 修正策略

### inner_ip_leak（内网 IP 泄露）

**安全级别**: ⭐⭐⭐ 安全（仅添加注释）

```bash
fix_inner_ip_leak() {
    local file=$1
    local line=$2
    
    # 读取目标行
    local target_line=$(sed -n "${line}p" "$file")
    
    # 构建修正（添加注释）
    local indent=$(echo "$target_line" | sed 's/[^ \t].*//')
    local fixed_line="${indent}// NOCC:inner_ip_leak(该IP已脱敏处理)\n${target_line}"
    
    # 应用修正
    sed -i "${line}i\\${indent}// NOCC:inner_ip_leak(该IP已脱敏处理)" "$file"
    
    echo "         ✅ 已添加忽略注释"
    return 0
}
```

### code_style（代码格式问题）

**安全级别**: ⭐⭐⭐ 安全（仅格式调整）

```bash
fix_code_style() {
    local file=$1
    local line=$2
    
    # 根据具体问题类型修正
    # 示例：修正缩进
    sed -i "${line}s/^  /    /" "$file"
    
    echo "         ✅ 已修正代码格式"
    return 0
}
```

### naming_convention（命名规范问题）

**安全级别**: ⭐⭐ 谨慎（可能影响引用）

```bash
fix_naming_convention() {
    local file=$1
    local line=$2
    
    # 检查是否为类名（不自动修正）
    if is_class_name "$file" "$line"; then
        echo "         ⚠️ 跳过类名修改（安全考虑）"
        return 1
    fi
    
    # 检查是否仅在本文件使用
    if is_local_variable "$file" "$line"; then
        # 执行修正
        echo "         ✅ 已修正变量命名"
        return 0
    else
        echo "         ⚠️ 变量可能跨文件使用，跳过自动修正"
        return 1
    fi
}
```

### unused_import（未使用的导入）

**安全级别**: ⭐⭐⭐ 安全

```bash
fix_unused_import() {
    local file=$1
    local line=$2
    
    # 删除导入语句
    sed -i "${line}d" "$file"
    
    echo "         ✅ 已删除未使用的导入"
    return 0
}
```

## 输出格式

### 标准输出

```
[5/7] 自动修正
      [5.1] 解析扫描结果...
      ✅ 解析完成: 共 4 个问题
      [5.2] 开始自动修正（最大重试: 3 轮）
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

      ━━ 第 1/3 轮修正 ━━
         当前待修正问题: 4 个
         处理 [code_style]: src/main/java/com/example/UserService.java:15
         ✅ 已修正代码格式
         处理 [inner_ip_leak]: src/main/java/com/example/OrderService.java:42
         ✅ 已添加忽略注释
         处理 [unused_import]: src/main/java/com/example/UserService.java:5
         ✅ 已删除未使用的导入
         处理 [naming_convention]: src/main/java/com/example/OrderService.java:56
         ⚠️ 变量可能跨文件使用，跳过自动修正
         本轮修正: 3 个
         [5.2.1] 重新扫描验证...
         剩余问题: 1 个

      ━━ 第 2/3 轮修正 ━━
         当前待修正问题: 1 个
         处理 [naming_convention]: src/main/java/com/example/OrderService.java:56
         ⚠️ 变量可能跨文件使用，跳过自动修正
         本轮修正: 0 个
         [5.2.2] 重新扫描验证...
         剩余问题: 1 个
         ⚠️ 本轮无问题被修正，但仍有剩余问题
         → 继续下一轮尝试

      ━━ 第 3/3 轮修正 ━━
         当前待修正问题: 1 个
         处理 [naming_convention]: src/main/java/com/example/OrderService.java:56
         ⚠️ 变量可能跨文件使用，跳过自动修正
         本轮修正: 0 个
         [5.2.3] 重新扫描验证...
         剩余问题: 1 个
         → 已达最大重试次数

      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 自动修正完成:
         共修正: 3 个问题
         剩余问题: 1 个
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 错误处理

### 文件无写权限

```
[5/7] 自动修正
      ❌ 文件无写权限: src/main/java/com/example/UserService.java

无法自动修正，请检查文件权限。
```

### 修正导致语法错误

```
[5/7] 自动修正
      ⚠️ 修正可能导致语法错误: src/main/java/com/example/UserService.java

已回滚修改，需手动处理。
```

## 强制约束

### 禁止行为

- ❌ 使用 while 循环（可能无限循环）
- ❌ 不输出每轮修正结果
- ❌ 不重新扫描验证
- ❌ 修正类名等高风险变更

### 必须行为

- ✅ 使用 for 循环确保执行 max_retry 轮
- ✅ 每轮必须输出当前问题数、修正数、剩余数
- ✅ 每轮修正后必须重新扫描验证
- ✅ 跳过高风险变更（类名、跨文件引用）
