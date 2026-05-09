# 文件过滤工作流

## 工作流概述

文件过滤工作流负责根据扫描模式获取变更文件列表，并过滤出代码文件。

**⏱️ 执行时机**：项目初始化完成后（步骤 [3/7]）

## 执行前置条件

- 项目初始化完成
- 已确定扫描模式
- 当前目录为 Git 仓库

## 执行步骤

### Step 3.1：获取变更文件列表

```bash
get_changed_files() {
    echo "[3/7] 文件过滤"
    echo "      [3.1] 获取变更文件列表..."
    
    local scan_mode=$1
    local all_files=()
    
    case "$scan_mode" in
        combined)
            # Combined 模式：获取未暂存 + 已暂存文件
            local diff_files=$(git diff --name-only)
            local staged_files=$(git diff --cached --name-only)
            all_files=($(echo -e "$diff_files\n$staged_files" | sort -u))
            echo "      📁 未暂存文件: $(echo "$diff_files" | wc -l) 个"
            echo "      📁 已暂存文件: $(echo "$staged_files" | wc -l) 个"
            ;;
        diff)
            # Diff 模式：仅获取未暂存文件
            all_files=($(git diff --name-only))
            echo "      📁 未暂存文件: ${#all_files[@]} 个"
            ;;
        pre-commit|staged)
            # Pre-commit 模式：仅获取已暂存文件
            all_files=($(git diff --cached --name-only))
            echo "      📁 已暂存文件: ${#all_files[@]} 个"
            ;;
        all)
            # All 模式：获取所有文件
            all_files=($(git ls-files))
            echo "      📁 全部文件: ${#all_files[@]} 个"
            ;;
        *)
            echo "      ❌ 未知扫描模式: $scan_mode"
            return 1
            ;;
    esac
    
    # 输出文件列表
    printf '%s\n' "${all_files[@]}"
}
```

### Step 3.2：过滤代码文件

```bash
# 代码文件扩展名白名单
CODE_FILE_EXTENSIONS='\.(java|kt|scala|groovy|py|js|ts|jsx|tsx|go|c|cpp|cc|cxx|h|hpp|rs|rb|php|cs|swift|m|mm)$'

is_code_file() {
    local file=$1
    
    # 检查扩展名是否在白名单中
    if echo "$file" | grep -qiE "$CODE_FILE_EXTENSIONS"; then
        return 0  # 是代码文件
    fi
    
    return 1  # 非代码文件
}

filter_code_files() {
    echo "      [3.2] 过滤代码文件..."
    
    local all_files=("$@")
    local code_files=()
    local non_code_count=0
    
    for file in "${all_files[@]}"; do
        if is_code_file "$file"; then
            code_files+=("$file")
            echo "         ✅ $file"
        else
            ((non_code_count++))
            echo "         ⏭️ 跳过非代码文件: $file"
        fi
    done
    
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "      📊 文件统计:"
    echo "         总文件数: ${#all_files[@]}"
    echo "         代码文件: ${#code_files[@]}"
    echo "         非代码文件: $non_code_count"
    echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 输出代码文件列表
    printf '%s\n' "${code_files[@]}"
}
```

### Step 3.3：检查是否有代码文件需要扫描

**🔴 强制约束**：当没有代码文件时，**禁止**自动降级为全量扫描，必须直接跳过检查。

```bash
check_code_files_exist() {
    echo "      [3.3] 检查是否有代码文件需要扫描..."
    
    local code_files=("$@")
    
    if [ ${#code_files[@]} -eq 0 ]; then
        echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "      ⏭️ 无代码文件需要扫描，跳过 PreCI 检查"
        echo "         原因: 没有暂存或未暂存的代码文件"
        echo "         提示: 如需全量扫描，请显式使用 --all 模式"
        echo "      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return 1  # 无代码文件，跳过检查
    fi
    
    echo "      ✅ 找到 ${#code_files[@]} 个代码文件需要扫描"
    return 0
}
```

## 代码文件白名单

### 支持的文件类型

| 语言 | 文件扩展名 |
|------|-----------|
| Java | `.java`, `.kt`, `.scala`, `.groovy` |
| Python | `.py` |
| JavaScript/TypeScript | `.js`, `.ts`, `.jsx`, `.tsx` |
| Go | `.go` |
| C/C++ | `.c`, `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp` |
| Rust | `.rs` |
| Ruby | `.rb` |
| PHP | `.php` |
| C# | `.cs` |
| Objective-C | `.m`, `.mm` |
| Swift | `.swift` |

### 自动跳过的文件类型

以下文件类型会被自动跳过：

| 类别 | 文件类型 |
|------|---------|
| 文档 | `.md`, `.txt`, `.pdf`, `.doc`, `.docx` |
| 配置 | `.xml`, `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.properties` |
| 构建 | `Makefile`, `CMakeLists.txt`, `.gradle` |
| 图片 | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico` |
| 其他 | `.gitignore`, `.gitattributes`, `LICENSE`, `README` |

## 输出格式

### 标准输出

```
[3/7] 文件过滤
      [3.1] 获取变更文件列表...
      📁 未暂存文件: 5 个
      📁 已暂存文件: 3 个
      [3.2] 过滤代码文件...
         ✅ src/main/java/com/example/UserService.java
         ✅ src/main/java/com/example/OrderService.java
         ⏭️ 跳过非代码文件: README.md
         ⏭️ 跳过非代码文件: pom.xml
         ✅ src/test/java/com/example/UserServiceTest.java
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 文件统计:
         总文件数: 5
         代码文件: 3
         非代码文件: 2
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      [3.3] 检查是否有代码文件需要扫描...
      ✅ 找到 3 个代码文件需要扫描
```

### 无代码文件时的输出

```
[3/7] 文件过滤
      [3.1] 获取变更文件列表...
      📁 未暂存文件: 2 个
      📁 已暂存文件: 1 个
      [3.2] 过滤代码文件...
         ⏭️ 跳过非代码文件: README.md
         ⏭️ 跳过非代码文件: pom.xml
         ⏭️ 跳过非代码文件: docs/design.md
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      📊 文件统计:
         总文件数: 3
         代码文件: 0
         非代码文件: 3
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      [3.3] 检查是否有代码文件需要扫描...
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ⏭️ 无代码文件需要扫描，跳过 PreCI 检查
         原因: 没有暂存或未暂存的代码文件
         提示: 如需全量扫描，请显式使用 --all 模式
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 错误处理

### Git 命令失败

```
[3/7] 文件过滤
      [3.1] 获取变更文件列表...
      ❌ Git 命令执行失败: git diff --name-only

可能原因：
- 不在 Git 仓库中
- Git 仓库损坏
- 权限不足

请检查 Git 状态并重试。
```

## 强制约束

### 禁止行为（无代码文件时）

- ❌ 自动降级为全量扫描（`--all` 模式）
- ❌ 强制执行扫描
- ❌ 不输出跳过原因就继续
- ❌ 返回错误状态码

### 必须行为

- ✅ 输出所有文件的过滤结果
- ✅ 统计代码文件和非代码文件数量
- ✅ 无代码文件时输出友好提示
- ✅ 无代码文件时返回成功状态码（0）
