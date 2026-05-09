# 输出报告工作流

## 工作流概述

输出报告工作流负责汇总所有检查结果，生成最终报告，并输出给用户。

**⏱️ 执行时机**：
- 结果审查完成后（步骤 [6/7]）
- 必须执行（不可跳过）
- 作为最后一个步骤输出

## 执行前置条件

- 所有检查步骤已完成
- 结果审查已完成
- 已生成结构化报告

## 执行步骤

### Step 7.1：汇总统计

```bash
summarize_results() {
    echo "[7/7] 输出报告"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local success=$1
    local total_issues=$2
    local fixed_issues=$3
    local remaining_issues=$4
    
    # 确定检查状态
    if [ "$success" = true ]; then
        echo "      ✅ 检查通过"
    else
        echo "      ❌ 检查未通过"
    fi
    
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      📊 问题统计:"
    echo "         - 发现问题: $total_issues 个"
    echo "         - 已修正: $fixed_issues 个"
    echo "         - 剩余问题: $remaining_issues 个"
    
    # 输出详细分类（如果有问题）
    if [ "$remaining_issues" -gt 0 ]; then
        echo ""
        echo "      📋 剩余问题详情:"
        # 读取并输出剩余问题
        cat /tmp/preci_remaining_issues.txt 2>/dev/null || echo "         （无详情）"
    fi
}
```

### Step 7.2：输出建议

```bash
output_suggestions() {
    local remaining_issues=$1
    
    if [ "$remaining_issues" -gt 0 ]; then
        echo ""
        echo "      💡 建议:"
        
        if [ "$remaining_issues" -le 2 ]; then
            echo "         - 建议修复剩余问题后再提交"
            echo "         - 可手动修复或重新运行自动修正"
        elif [ "$remaining_issues" -le 5 ]; then
            echo "         - 必须修复所有问题后再提交"
            echo "         - 建议手动修复无法自动修正的问题"
        else
            echo "         - 问题较多，建议全面重构"
            echo "         - 可分批修复，逐步提交"
        fi
    else
        echo ""
        echo "      💡 建议:"
        echo "         - 代码质量优秀，可以提交"
        echo "         - 继续保持良好的编码规范"
    fi
}
```

### Step 7.3：输出成功/失败标识

```bash
output_final_status() {
    local success=$1
    
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ "$success" = true ]; then
        echo "✅ PreCI 代码检查完成"
    else
        echo "❌ PreCI 代码检查完成（存在未修复问题）"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}
```

## 输出格式

### 检查通过（无剩余问题）

```
[7/7] 输出报告
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ✅ 检查通过
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 问题统计:
         - 发现问题: 4 个
         - 已修正: 4 个
         - 剩余问题: 0 个

      💡 建议:
         - 代码质量优秀，可以提交
         - 继续保持良好的编码规范
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PreCI 代码检查完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 检查未通过（存在剩余问题）

```
[7/7] 输出报告
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ❌ 检查未通过
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 问题统计:
         - 发现问题: 5 个
         - 已修正: 3 个
         - 剩余问题: 2 个

      📋 剩余问题详情:
         1. src/main/java/com/example/UserService.java:42
            [naming_convention] 变量名不符合规范: userName 应为 user_name

         2. src/main/java/com/example/OrderService.java:56
            [code_complexity] 方法复杂度过高（15），建议重构

      💡 建议:
         - 建议修复剩余问题后再提交
         - 可手动修复或重新运行自动修正
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ PreCI 代码检查完成（存在未修复问题）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 跳过检查（无代码文件）

```
[7/7] 输出报告
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ⏭️ 跳过 PreCI 检查
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

原因:
  - 没有暂存或未暂存的代码文件

提示:
  - 如需检查全部代码，请使用: preci:check -a

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏭️ PreCI 代码检查已跳过
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 返回结果结构

```typescript
interface PreciCheckResult {
  // 基础信息【必须】
  success: boolean;                 // 检查是否通过
  projectPath: string;              // 项目路径
  scanMode: 'combined' | 'diff' | 'pre-commit' | 'all';
  skipped: boolean;                 // 是否跳过检查
  skipReason?: string;              // 跳过原因
  
  // 文件统计【必须】
  filesChanged: number;             // 变更文件总数
  filesCode: number;                // 代码文件数
  filesNonCode: number;             // 非代码文件数
  filesScanned: number;             // 实际扫描文件数
  
  // Combined 模式详情【combined 模式必须】
  combinedDetails?: {
    diffIssues: number;             // --diff 发现的问题数
    stagedIssues: number;           // --pre-commit 发现的问题数
    mergedIssues: number;           // 去重后的总问题数
  };
  
  // 问题统计【必须】
  issuesFound: number;
  issuesFixed: number;
  issuesRemaining: number;
  issuesByType: Record<string, number>;  // 按类型分组
  
  // 详细信息【必须】
  details: IssueDetail[];
  
  // 自动修正信息【必须】
  retryCount: number;
  fixRounds: FixRound[];
}

interface IssueDetail {
  file: string;
  line: number;
  column?: number;
  rule: string;
  severity: 'error' | 'warning' | 'info';
  message: string;
  autoFixed: boolean;
  fixMethod?: string;
}

interface FixRound {
  round: number;
  fixed: number;
  remaining: number;
}
```

## 字段说明表

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `success` | boolean | ✅ | 检查是否通过（剩余问题=0） |
| `projectPath` | string | ✅ | 项目绝对路径 |
| `scanMode` | string | ✅ | 扫描模式 |
| `skipped` | boolean | ✅ | 是否跳过检查 |
| `skipReason` | string | 跳过时必须 | 跳过原因 |
| `filesChanged` | number | ✅ | 变更文件总数 |
| `filesCode` | number | ✅ | 代码文件数 |
| `filesNonCode` | number | ✅ | 非代码文件数 |
| `filesScanned` | number | ✅ | 实际扫描文件数 |
| `combinedDetails` | object | Combined 模式必须 | Combined 扫描详情 |
| `issuesFound` | number | ✅ | 发现的问题总数 |
| `issuesFixed` | number | ✅ | 已修正问题数 |
| `issuesRemaining` | number | ✅ | 剩余问题数 |
| `issuesByType` | object | ✅ | 按类型分类统计 |
| `details` | array | ✅ | 问题详情列表 |
| `retryCount` | number | ✅ | 实际重试轮数 |
| `fixRounds` | array | ✅ | 每轮修正详情 |

## 强制约束

### 禁止行为

- ❌ 跳过最终汇总
- ❌ 不输出检查状态（成功/失败）
- ❌ 返回结构不完整
- ❌ 字段缺失或类型错误

### 必须行为

- ✅ 必须输出最终汇总报告
- ✅ 必须明确标识检查状态（✅/❌/⏭️）
- ✅ 必须返回完整的结果结构
- ✅ 所有必须字段都存在且类型正确
- ✅ Combined 模式必须包含 combinedDetails
