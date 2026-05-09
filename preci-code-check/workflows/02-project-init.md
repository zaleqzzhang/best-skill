# 项目初始化工作流

## 工作流概述

项目初始化工作流负责检测项目类型、确定扫描范围、解析配置参数等。

**⏱️ 执行时机**：环境检测完成后（步骤 [2/7]）

## 执行前置条件

- PreCI 工具已就绪（环境检测通过）
- 当前目录为 Git 仓库
- 有文件读写权限

## 执行步骤

### Step 2.1：检测项目类型

```bash
detect_project_type() {
    echo "[2/7] 项目初始化"
    echo "      [2.1] 检测项目类型..."
    
    local project_path=$1
    local project_type=""
    
    # 检测 Java 项目
    if [ -f "$project_path/pom.xml" ] || [ -f "$project_path/build.gradle" ]; then
        project_type="java"
        echo "      ✅ 检测到 Java 项目"
    # 检测 Python 项目
    elif [ -f "$project_path/setup.py" ] || [ -f "$project_path/requirements.txt" ]; then
        project_type="python"
        echo "      ✅ 检测到 Python 项目"
    # 检测 Node.js 项目
    elif [ -f "$project_path/package.json" ]; then
        project_type="node"
        echo "      ✅ 检测到 Node.js 项目"
    # 检测 Go 项目
    elif [ -f "$project_path/go.mod" ]; then
        project_type="go"
        echo "      ✅ 检测到 Go 项目"
    # 其他类型
    else
        project_type="unknown"
        echo "      ⚠️ 未识别的项目类型，将扫描所有代码文件"
    fi
    
    echo "$project_type"
}
```

### Step 2.2：解析配置参数

```bash
parse_config() {
    echo "      [2.2] 解析配置参数..."
    
    # 扫描模式（默认 combined）
    local scan_mode="${1:-combined}"
    
    # 最大重试次数（默认 3）
    local max_retry="${2:-3}"
    
    # 是否跳过 PreCI 检查（默认不跳过）
    local skip_preci="${3:-false}"
    
    echo "      📋 配置参数:"
    echo "         扫描模式: $scan_mode"
    echo "         最大重试: $max_retry 轮"
    echo "         跳过检查: $skip_preci"
}
```

### Step 2.3：确定扫描范围

```bash
determine_scan_scope() {
    echo "      [2.3] 确定扫描范围..."
    
    local scan_mode=$1
    local project_path=$2
    
    case "$scan_mode" in
        combined)
            echo "      📁 扫描范围: 未暂存 + 已暂存文件"
            ;;
        diff)
            echo "      📁 扫描范围: 未暂存文件（已修改但未 git add）"
            ;;
        pre-commit|staged)
            echo "      📁 扫描范围: 已暂存文件（已 git add）"
            ;;
        all)
            echo "      📁 扫描范围: 整个项目全部文件"
            ;;
        *)
            echo "      ⚠️ 未知扫描模式: $scan_mode，使用默认 combined"
            scan_mode="combined"
            ;;
    esac
}
```

### Step 2.4：检测并初始化项目（preci init）

检测项目是否已初始化，未初始化时自动执行规则集选择和 `preci init`。

**注意**：PreCI 将初始化状态存储在 `bbolt.db`（install dir 下的 `db/` 目录），而不是项目目录下的文件。
因此**不能**通过检查 `.preci` 目录或 `.preci.json` 文件来判断是否已初始化，必须通过执行 `preci init` 的输出来判断。

```bash
init_preci_project() {
    echo "      [2.4] 检测项目 PreCI 初始化状态..."
    
    local project_path=$1
    local project_type=$2   # 由 Step 2.1 传入
    
    # 执行 preci init，通过输出内容判断初始化结果
    # preci init 是幂等的：已初始化的项目再次执行会直接返回成功
    local init_output
    init_output=$(preci init 2>&1)
    local init_exit=$?
    
    if echo "$init_output" | grep -q "初始化成功\|SUCCESS.*初始化\|already initialized\|工具列表"; then
        echo "      ✅ 项目初始化成功（或已初始化）"
        return 0
    fi
    
    if [ $init_exit -ne 0 ]; then
        echo "      ⚠️ preci init 返回非零，但继续尝试完整初始化流程..."
    fi
    
    echo "      ⚠️ 项目需要执行完整初始化（含规则集选择）..."
    
    # Step 2.4.1：查看可用规则集
    echo "      [2.4.1] 获取可用规则集..."
    local checkerset_list
    checkerset_list=$(preci checkerset list 2>&1)
    echo "      📋 可用规则集已获取"
    
    # Step 2.4.2：根据项目语言自动选择规则集 ID
    echo "      [2.4.2] 根据项目类型自动选择规则集..."
    local checkerset_id=""
    
    case "$project_type" in
        java)
            checkerset_id="standard_java"
            echo "      ✅ 选择规则集: standard_java（腾讯代码规范 (Java) 规则集）"
            ;;
        python)
            checkerset_id="standard_python_pylint"
            echo "      ✅ 选择规则集: standard_python_pylint（腾讯代码规范 (Python) 规则集）"
            ;;
        node)
            checkerset_id="standard_javascript"
            echo "      ✅ 选择规则集: standard_javascript（腾讯代码规范 (Javascript) 规则集）"
            ;;
        go)
            checkerset_id="standard_go"
            echo "      ✅ 选择规则集: standard_go（腾讯代码规范 (Go) 规则集）"
            ;;
        kotlin)
            checkerset_id="standard_kotlin"
            echo "      ✅ 选择规则集: standard_kotlin（腾讯代码规范 (Kotlin) 规则集）"
            ;;
        cpp|c)
            checkerset_id="standard_cpp"
            echo "      ✅ 选择规则集: standard_cpp（腾讯代码规范 (C++) 规则集）"
            ;;
        csharp)
            checkerset_id="standard_csharp"
            echo "      ✅ 选择规则集: standard_csharp（Jetbrains Resharper 规则集）"
            ;;
        *)
            checkerset_id="standard_java"
            echo "      ⚠️ 未识别项目类型，默认使用规则集: standard_java"
            ;;
    esac
    
    # Step 2.4.3：指定规则集
    echo "      [2.4.3] 指定规则集: $checkerset_id"
    preci checkerset select "$checkerset_id"
    if [ $? -ne 0 ]; then
        echo "      ❌ 规则集指定失败: $checkerset_id"
        return 1
    fi
    echo "      ✅ 规则集指定成功"
    
    # Step 2.4.4：执行项目初始化
    echo "      [2.4.4] 执行 preci init..."
    preci init
    if [ $? -ne 0 ]; then
        echo "      ❌ preci init 执行失败"
        return 1
    fi
    echo "      ✅ 项目初始化成功"
    
    return 0
}
```

**规则集 ID 对照表**：

| 项目类型 | 规则集 ID | 规则集名称 |
|---------|-----------|-----------|
| Java | `standard_java` | 腾讯代码规范 (Java) 规则集 |
| Python | `standard_python_pylint` | 腾讯代码规范 (Python) 规则集 |
| Node.js / JavaScript | `standard_javascript` | 腾讯代码规范 (Javascript) 规则集 |
| Go | `standard_go` | 腾讯代码规范 (Go) 规则集 |
| Kotlin | `standard_kotlin` | 腾讯代码规范 (Kotlin) 规则集 |
| C / C++ | `standard_cpp` | 腾讯代码规范 (C++) 规则集 |
| C# | `standard_csharp` | Jetbrains Resharper 规则集 |
| 未识别 | `standard_java`（默认） | - |

### Step 2.5：初始化工作目录

```bash
init_working_directory() {
    echo "      [2.5] 初始化工作目录..."
    
    local project_path=$1
    
    # 切换到项目根目录
    cd "$project_path" || {
        echo "      ❌ 无法进入项目目录: $project_path"
        return 1
    }
    
    echo "      ✅ 工作目录: $project_path"
    
    # 检查 Git 状态
    if ! git rev-parse --git-dir &>/dev/null; then
        echo "      ❌ 当前目录不是 Git 仓库"
        return 1
    fi
    
    echo "      ✅ Git 仓库检测通过"
    
    return 0
}
```

## 输出格式

### 标准输出

```
[2/7] 项目初始化
      [2.1] 检测项目类型...
      ✅ 检测到 Java 项目
      [2.2] 解析配置参数...
      📋 配置参数:
         扫描模式: combined
         最大重试: 3 轮
         跳过检查: false
      [2.3] 确定扫描范围...
      📁 扫描范围: 未暂存 + 已暂存文件
      [2.4] 检测项目 PreCI 初始化状态...
      ⚠️ 项目尚未初始化，开始自动初始化...
      [2.4.1] 获取可用规则集...
      📋 可用规则集已获取
      [2.4.2] 根据项目类型自动选择规则集...
      ✅ 选择规则集: standard_java（腾讯代码规范 (Java) 规则集）
      [2.4.3] 指定规则集: standard_java
      ✅ 规则集指定成功
      [2.4.4] 执行 preci init...
      ✅ 项目初始化成功
      [2.5] 初始化工作目录...
      ✅ 工作目录: /path/to/project
      ✅ Git 仓库检测通过
```

## 错误处理

### 非 Git 仓库

```
[2/7] 项目初始化
      [2.5] 初始化工作目录...
      ❌ 当前目录不是 Git 仓库

❌ PreCI 检查需要在 Git 仓库中执行。
请在 Git 仓库中重新执行，或先运行 git init 初始化仓库。
```

### 无效配置

```
[2/7] 项目初始化
      [2.2] 解析配置参数...
      ⚠️ 无效的扫描模式: invalid_mode，使用默认 combined
      ⚠️ 无效的重试次数: -1，使用默认 3
      📋 配置参数:
         扫描模式: combined
         最大重试: 3 轮
         跳过检查: false
```

## 强制约束

### 禁止行为

- ❌ 跳过项目类型检测
- ❌ 不校验配置参数有效性
- ❌ 未确认 Git 仓库就继续
- ❌ 不输出配置参数
- ❌ 已初始化的项目重复执行 `preci init`

### 必须行为

- ✅ 检测并输出项目类型
- ✅ 校验并输出所有配置参数
- ✅ 未初始化时根据项目语言自动选择规则集并执行 `preci init`
- ✅ 确认当前目录为 Git 仓库
- ✅ 输出完整的初始化报告
