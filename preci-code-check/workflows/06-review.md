# 结果审查工作流

## 工作流概述

结果审查工作流负责分析扫描结果，进行问题分类统计，评估代码质量，并生成结构化报告。

**⏱️ 执行时机**：
- 自动修正完成后（步骤 [6/7]）
- 必须执行（不可跳过）

## 执行前置条件

- 扫描已完成
- 自动修正已执行（即使修正数为 0）
- 已获取最终扫描结果

## 执行步骤

### Step 6.1：解析扫描结果

```bash
parse_final_scan_result() {
    echo "[5/7] 结果分析"
    echo "      [5.1] 解析扫描结果..."
    
    local scan_output=$1
    local issue_count=0
    local -A issues_by_type
    local -A issues_by_severity
    local -A issues_by_file
    
    # 解析问题（按类型、严重性、文件分组）
    while IFS= read -r line; do
        if [[ $line =~ \[([^\]]+)\]\ Line\ ([0-9]+):\ (.+)$ ]]; then
            local rule="${BASH_REMATCH[1]}"
            local line_no="${BASH_REMATCH[2]}"
            local message="${BASH_REMATCH[3]}"
            
            ((issue_count++))
            ((issues_by_type[$rule]++))
            
            # 判断严重性
            if [[ $rule =~ (security|inner_ip_leak|sensitive_info) ]]; then
                ((issues_by_severity["error"]++))
            elif [[ $rule =~ (code_style|naming_convention) ]]; then
                ((issues_by_severity["warning"]++))
            else
                ((issues_by_severity["info"]++))
            fi
        fi
    done <<< "$scan_output"
    
    echo "      ✅ 解析完成: 共 $issue_count 个问题"
    
    # 输出分类统计
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      📊 按类型分类:"
    for type in "${!issues_by_type[@]}"; do
        echo "         ├─ $type: ${issues_by_type[$type]} 个"
    done
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      📊 按严重性分类:"
    for severity in "${!issues_by_severity[@]}"; do
        echo "         ├─ $severity: ${issues_by_severity[$severity]} 个"
    done
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $issue_count
}
```

### Step 6.2：评估代码质量

```bash
evaluate_code_quality() {
    local total_issues=$1
    local fixed_issues=$2
    local remaining_issues=$3
    
    echo "      [5.2] 评估代码质量..."
    
    # 计算修正率
    local fix_rate=0
    if [ "$total_issues" -gt 0 ]; then
        fix_rate=$((fixed_issues * 100 / total_issues))
    fi
    
    # 评估质量等级
    local quality_level=""
    if [ "$remaining_issues" -eq 0 ]; then
        quality_level="优秀 ⭐⭐⭐⭐⭐"
    elif [ "$remaining_issues" -le 2 ]; then
        quality_level="良好 ⭐⭐⭐⭐"
    elif [ "$remaining_issues" -le 5 ]; then
        quality_level="中等 ⭐⭐⭐"
    elif [ "$remaining_issues" -le 10 ]; then
        quality_level="待改进 ⭐⭐"
    else
        quality_level="需重构 ⭐"
    fi
    
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      📊 质量评估:"
    echo "         修正率: $fix_rate%"
    echo "         质量等级: $quality_level"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━"
}
```

### Step 6.3：生成结构化报告

```bash
generate_structured_report() {
    local total_issues=$1
    local fixed_issues=$2
    local remaining_issues=$3
    local -n issues_by_type=$4
    
    echo "      [5.3] 生成结构化报告..."
    
    # 生成 JSON 格式报告
    cat > /tmp/preci_report.json <<EOF
{
  "success": $([ "$remaining_issues" -eq 0 ] && echo "true" || echo "false"),
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "projectPath": "$(pwd)",
  "scanMode": "$SCAN_MODE",
  "summary": {
    "totalIssues": $total_issues,
    "fixedIssues": $fixed_issues,
    "remainingIssues": $remaining_issues
  },
  "issuesByType": {
$(for type in "${!issues_by_type[@]}"; do
    echo "    \"$type\": ${issues_by_type[$type]},"
done | sed '$ s/,$//')
  }
}
EOF
    
    echo "      ✅ 报告已生成: /tmp/preci_report.json"
}
```

## 输出格式

### 标准输出

```
[5/7] 结果分析
      [5.1] 解析扫描结果...
      ✅ 解析完成: 共 4 个问题
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 按类型分类:
         ├─ code_style: 2 个
         ├─ naming_convention: 1 个
         └─ unused_import: 1 个
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 按严重性分类:
         ├─ warning: 3 个
         └─ info: 1 个
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      [5.2] 评估代码质量...
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 质量评估:
         修正率: 100%
         质量等级: 优秀 ⭐⭐⭐⭐⭐
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      [5.3] 生成结构化报告...
      ✅ 报告已生成: /tmp/preci_report.json
```

### 无问题时的输出

```
[5/7] 结果分析
      [5.1] 解析扫描结果...
      ✅ 未发现任何问题
      [5.2] 评估代码质量...
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 质量评估:
         修正率: N/A
         质量等级: 优秀 ⭐⭐⭐⭐⭐
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      [5.3] 生成结构化报告...
      ✅ 报告已生成: /tmp/preci_report.json
```

## 质量等级标准

| 剩余问题数 | 质量等级 | 建议 |
|-----------|---------|------|
| 0 | 优秀 ⭐⭐⭐⭐⭐ | 可直接提交 |
| 1-2 | 良好 ⭐⭐⭐⭐ | 建议修复后提交 |
| 3-5 | 中等 ⭐⭐⭐ | 必须修复后提交 |
| 6-10 | 待改进 ⭐⭐ | 需要重构 |
| >10 | 需重构 ⭐ | 建议全面重构 |

## 结构化报告格式

```json
{
  "success": true,
  "timestamp": "2026-03-16T10:30:00Z",
  "projectPath": "/path/to/project",
  "scanMode": "combined",
  "summary": {
    "totalIssues": 4,
    "fixedIssues": 4,
    "remainingIssues": 0
  },
  "issuesByType": {
    "code_style": 2,
    "naming_convention": 1,
    "unused_import": 1
  },
  "issuesBySeverity": {
    "error": 0,
    "warning": 3,
    "info": 1
  },
  "qualityLevel": "优秀",
  "fixRate": 100
}
```

## 错误处理

### 解析失败

```
[5/7] 结果分析
      ❌ 解析扫描结果失败

无法解析扫描输出，请检查扫描是否正常执行。
```

### 生成报告失败

```
[5/7] 结果分析
      ⚠️ 生成结构化报告失败: /tmp/preci_report.json

已完成问题统计，但报告文件生成失败。
```

## 强制约束

### 禁止行为

- ❌ 跳过问题分类统计
- ❌ 不输出质量评估
- ❌ 不生成结构化报告

### 必须行为

- ✅ 必须按类型和严重性分类统计
- ✅ 必须评估代码质量并输出等级
- ✅ 必须生成 JSON 格式报告
- ✅ 所有统计数据必须准确
