# Day 9 Python 函数、JSON 推理结果与格式化报表笔记

日期：2026-08-19  
学习环境：CentOS Stream 9 / Python / Bash  
学习主题：Python 函数、模块、文件操作、JSON 处理和推理结果报表

## 一、今天的目标

今天继续学习 Python，并完成“读取 JSON 推理输出，生成格式化报表”的任务：

1. 了解函数、参数、返回值和作用域；
2. 学习模块、包和常用标准库；
3. 掌握文件读取和写入方法；
4. 使用 Python 读取 JSON 推理结果；
5. 把模型输出整理成 Markdown 报表；
6. 在 CentOS 中运行脚本并检查结果。

## 二、整体思路

```text
模型推理输出 -> inference.json -> Python 读取 -> 整理字段 -> report.md
```

一句话总结：

**先读取 JSON，再提取需要的内容，最后生成容易查看的报表。**

## 三、Python 函数

函数就是把一段代码打包起来，需要时可以重复使用。

### 1. 基本函数

```python
def add(a, b):
    return a + b


result = add(2, 3)
print(result)
```

这里的 `a` 和 `b` 是参数，`return` 返回计算结果。

### 2. 常见参数写法

| 写法 | 初学者理解 | 示例 |
|---|---|---|
| 普通参数 | 函数需要的输入 | `def add(a, b):` |
| 默认参数 | 没有传值时使用默认内容 | `def greet(name="user"):` |
| `*args` | 接收多个普通参数 | `def total(*args):` |
| `**kwargs` | 接收多个键值参数 | `def show(**kwargs):` |
| `return` | 把结果交给调用者 | `return result` |
| `lambda` | 简单的一行匿名函数 | `square = lambda x: x * x` |

### 3. 作用域 LEGB

Python 查找变量时，通常按照下面的顺序进行：

```text
L：Local，局部作用域
E：Enclosing，外层函数作用域
G：Global，全局作用域
B：Built-in，内置作用域
```

初学时最容易遇到的问题是：函数内部的局部变量，不能直接当成全局变量使用。

## 四、模块、包和标准库

### 1. 模块和包

| 内容 | 初学者理解 | 作用 |
|---|---|---|
| 模块 | 一个 `.py` 文件 | 保存一组相关代码 |
| 包 | 一组模块组成的目录 | 方便管理较大的项目 |
| `import` | 导入整个模块 | `import json` |
| `from ... import` | 导入模块中的指定内容 | `from pathlib import Path` |
| `__init__.py` | 包目录中的初始化文件 | 帮助 Python 识别和管理包 |
| `__name__` | 当前文件的特殊名称 | 判断文件是被导入还是直接运行 |

常见写法：

```python
def main():
    print("程序开始运行")


if __name__ == "__main__":
    main()
```

### 2. 常用标准库

| 模块 | 主要用途 | 本次任务中的用法 |
|---|---|---|
| `os` | 操作系统功能 | 获取环境变量、检查文件 |
| `sys` | Python 运行参数 | 获取命令行参数 |
| `json` | 处理 JSON 数据 | 读取推理结果 |
| `pathlib` | 处理文件路径 | 拼接输入和输出路径 |
| `subprocess` | 执行系统命令 | 必要时调用 CentOS 命令 |

## 五、文件操作

### 1. 读取和写入文件

```python
with open("inference.json", "r", encoding="utf-8") as file:
    data = file.read()

with open("report.md", "w", encoding="utf-8") as file:
    file.write("# 推理结果报表\n")
```

`r` 表示读取，`w` 表示覆盖写入，`a` 表示追加写入。使用 `with` 后，文件会自动关闭。

### 2. 使用 `pathlib`

```python
from pathlib import Path

input_file = Path("inference.json")

if not input_file.exists():
    print("文件不存在")
```

相比手动拼接字符串，`pathlib` 处理路径更清楚，也更不容易写错。

## 六、读取 JSON 推理结果

### 1. 示例 JSON

创建 `inference.json`：

```json
{
  "model": "resnet50",
  "task": "image_classification",
  "timestamp": "2026-08-19 10:30:00",
  "status": "success",
  "results": [
    {
      "label": "cat",
      "score": 0.9821
    },
    {
      "label": "dog",
      "score": 0.0132
    }
  ],
  "summary": "预测结果为 cat"
}
```

### 2. 使用 `json` 模块读取

```python
import json

with open("inference.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data["model"])
print(data["results"])
```

`json.load()` 用来从文件读取 JSON，`json.loads()` 用来从字符串读取 JSON。

## 七、生成 Markdown 报表

创建 `report.py`：

```python
import json
import sys
from datetime import datetime


def escape_md(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_report(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    lines = [
        "# 推理结果报表",
        "",
        f"- 报表生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]

    for key in ["model", "task", "timestamp", "status", "summary"]:
        if key in data:
            lines.append(f"- {key}：{escape_md(data[key])}")

    rows = data.get("results", [])
    if rows:
        lines.extend(["", "## 推理结果", ""])
        columns = list(rows[0].keys())
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

        for row in rows:
            values = [escape_md(row.get(column, "")) for column in columns]
            lines.append("| " + " | ".join(values) + " |")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"报表已生成：{output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python3 report.py 输入JSON 输出报表")
        sys.exit(1)

    format_report(sys.argv[1], sys.argv[2])
```

脚本做了三件事：读取 JSON、提取字段、写入 Markdown 表格。

## 八、在 CentOS 中运行

### 1. 安装工具

CentOS Stream 8/9：

```bash
sudo dnf install -y python3 python3-pip jq
```

CentOS 7 通常使用：

```bash
sudo yum install -y python3 python3-pip jq
```

### 2. 创建工作目录

```bash
mkdir -p ~/json-report
cd ~/json-report
```

把 `inference.json` 和 `report.py` 放到这个目录中。

### 3. 检查 JSON

```bash
jq . inference.json
jq empty inference.json
```

如果第二条命令没有输出，通常说明 JSON 格式正确。

### 4. 生成报表

```bash
python3 report.py inference.json report.md
cat report.md
```

生成结果：

```text
inference.json -> report.md
```

## 九、报表示例

生成的 `report.md` 大致如下：

```markdown
# 推理结果报表

- model：resnet50
- task：image_classification
- status：success
- summary：预测结果为 cat

## 推理结果

| label | score |
| --- | --- |
| cat | 0.9821 |
| dog | 0.0132 |
```

这样可以把原本不容易阅读的 JSON，整理成比较清楚的报表。

## 十、常见问题排查

| 现象 | 可能原因 | 处理方法 |
|---|---|---|
| `No such file` | 输入文件路径错误 | 使用 `pwd` 和 `ls -l` 检查路径 |
| JSON 解析失败 | JSON 的引号、逗号或括号错误 | 执行 `jq empty inference.json` |
| `KeyError` | 代码读取了不存在的字段 | 先用 `print(data.keys())` 查看字段 |
| 报表为空 | JSON 中没有 `results` | 检查模型输出字段名称 |
| `python3: command not found` | Python 没有安装 | 使用 `dnf` 或 `yum` 安装 Python |
| 中文显示异常 | 文件编码不正确 | 读写文件时使用 `encoding="utf-8"` |
| `w` 模式导致内容消失 | `w` 会覆盖文件 | 追加内容时使用 `a`，重要文件先备份 |

## 十一、今天学到的命令和写法

| 命令 / 写法 | 用途 |
|---|---|
| `def function():` | 定义函数 |
| `return value` | 返回函数结果 |
| `import json` | 导入 JSON 模块 |
| `with open(...)` | 安全地读写文件 |
| `json.load(file)` | 从文件读取 JSON |
| `json.dump(data, file)` | 把数据写入 JSON 文件 |
| `jq . file.json` | 格式化查看 JSON |
| `jq empty file.json` | 检查 JSON 格式 |
| `python3 report.py input output` | 执行报表脚本 |
| `cat report.md` | 查看报表 |

## 十二、易错点

1. 函数忘记写 `return` 时，调用结果可能是 `None`。
2. `*args` 和 `**kwargs` 的含义不同，不能混用。
3. `__name__ == "__main__"` 中的下划线和大小写不能写错。
4. `w` 模式会覆盖原文件，操作前要确认文件名。
5. JSON 使用双引号，不能随意改成单引号。
6. `results` 字段名称必须和实际模型输出保持一致。
7. CentOS 8/9 通常使用 `dnf`，CentOS 7 通常使用 `yum`。
8. 报表脚本只负责整理已有 JSON，不会自动完成模型推理。

## 十三、今日总结

今天学习了函数、模块、标准库和文件操作，并完成了一个简单的 JSON 报表整理流程。

**Python 读取 JSON，提取模型推理结果，再生成 Markdown 报表；CentOS 负责提供运行脚本的环境。**
