# Day 8 Python 基础与图片数据准备笔记

日期：2026-08-18  
学习环境：CentOS Stream 9 / Python / Bash  
学习主题：Python 基础类型、数据结构、控制流和图片数据集准备

## 一、今天的目标

今天学习 Python 基础知识，并完成一个简单的图片数据准备任务：

1. 认识 `int`、`float`、`str`、`bool` 和 `None`
2. 学习 `list`、`tuple`、`dict` 和 `set`
3. 掌握条件语句和循环语句
4. 了解 `enumerate`、`zip`、`break`、`continue` 和 `pass`
5. 了解 Python 为什么常用于人工智能
6. 在 CentOS 中批量分类、重命名图片并生成标注清单

## 二、整体思路

```text
认识数据类型 -> 学习数据结构 -> 使用条件和循环 -> 安装 Python/Pillow -> 整理图片 -> 预览 -> 正式处理 -> 查看标注清单
```

一句话总结：

**先把 Python 基础语法学会，再用脚本自动完成重复的数据准备工作。**

## 三、Python 基础类型

| 类型 | 初学者理解 | 示例 |
|---|---|---|
| `int` | 整数 | `age = 18` |
| `float` | 小数 | `score = 95.5` |
| `str` | 文字或字符串 | `name = "cat"` |
| `bool` | 真或假 | `is_ok = True` |
| `None` | 暂时没有值 | `result = None` |

查看变量类型：

```python
value = 10
print(type(value))
```

类型转换示例：

```python
number = int("10")
text = str(10)
price = float("3.5")
```

字符串和数字不能直接相加：

```python
age = 18
print("年龄：" + str(age))
```

## 四、常用数据结构

| 数据结构 | 特点 | 示例 |
|---|---|---|
| `list` | 有顺序，可以修改 | `images = ["a.jpg", "b.jpg"]` |
| `tuple` | 有顺序，通常不修改 | `size = (640, 480)` |
| `dict` | 使用键和值保存数据 | `{"label": "cat", "width": 640}` |
| `set` | 自动去重 | `set(["cat", "cat", "dog"])` |

列表切片：

```python
images = ["a.jpg", "b.jpg", "c.jpg"]
print(images[0:2])
```

列表推导式：

```python
numbers = [1, 2, 3]
double_numbers = [x * 2 for x in numbers]
```

字典推导式：

```python
names = ["cat", "dog"]
labels = {name: len(name) for name in names}
```

## 五、条件和循环

### 1. 条件判断

```python
score = 85

if score >= 60:
    print("及格")
else:
    print("需要继续练习")
```

`if`、`elif` 和 `else` 用来根据不同条件执行不同代码。条件后面要写冒号，代码块要保持缩进一致。

### 2. `for` 循环

```python
for image in ["a.jpg", "b.jpg"]:
    print(image)
```

`for` 适合依次处理列表中的每个元素，也适合遍历文件。

### 3. `while` 循环

```python
count = 1

while count <= 3:
    print(count)
    count += 1
```

`while` 会在条件为真时重复执行，必须保证条件最终会变成假，否则可能出现死循环。

### 4. 常用循环工具

| 写法 | 作用 | 示例 |
|---|---|---|
| `enumerate` | 同时得到编号和值 | `for i, item in enumerate(items)` |
| `zip` | 同时遍历多个列表 | `for name, score in zip(names, scores)` |
| `break` | 立即结束循环 | 找到目标后停止 |
| `continue` | 跳过本次循环 | 跳过不需要处理的文件 |
| `pass` | 暂时不执行任何操作 | 先占位，之后再补代码 |

## 六、Python 为什么常用于人工智能

Python 适合人工智能，主要有以下原因：

1. 语法比较简单，初学者容易学习；
2. 有很多现成的工具和库；
3. `NumPy` 可以处理数组和数学计算；
4. `Pandas` 可以处理表格数据；
5. `PyTorch` 可以进行深度学习和模型训练；
6. 社区资料多，遇到问题容易查找解决方法。

## 七、在 CentOS 中准备 Python 环境

安装 Python 和 pip：

```bash
sudo dnf install -y python3 python3-pip
```

创建项目目录并进入：

```bash
mkdir -p ~/cv_dataset
cd ~/cv_dataset
```

创建并激活虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

安装 Pillow：

```bash
python -m pip install Pillow
```

检查是否安装成功：

```bash
python -c "from PIL import Image; print(Image.__version__)"
```

如果能够显示版本号，说明 Pillow 可以正常使用。

## 八、准备图片目录

建议按照分类建立目录：

```text
cv_dataset/
├── raw/
│   ├── cat/
│   │   ├── cat.jpg
│   │   └── cat2.jpg
│   ├── dog/
│   │   └── dog.jpg
│   └── car/
│       └── car.jpg
└── prepare_dataset.py
```

创建目录：

```bash
mkdir -p raw/cat raw/dog raw/car
```

脚本会把 `raw` 下的第一级目录名作为图片标签，例如 `cat`、`dog` 和 `car`。

## 九、批量分类和重命名图片

使用已经准备好的 `prepare_dataset.py` 脚本。

先预览，不修改文件：

```bash
python3 prepare_dataset.py \
  --input ./raw \
  --output ./dataset \
  --mode copy \
  --dry-run
```

预览结果示例：

```text
[000001] cat/cat.jpg -> images/cat/cat_000001.jpg [ok]
[000002] dog/dog.jpg -> images/dog/dog_000001.jpg [ok]
```

确认结果正确后正式执行：

```bash
python3 prepare_dataset.py \
  --input ./raw \
  --output ./dataset \
  --mode copy
```

`copy` 模式会保留原始图片。如果使用 `move`，原图片会被移动，初学时建议优先使用 `copy`。

## 十、生成的文件

处理完成后，目录大致如下：

```text
dataset/
├── images/
│   ├── cat/cat_000001.jpg
│   ├── dog/dog_000001.jpg
│   └── car/car_000001.jpg
├── annotations.csv
└── annotations.json
```

标注清单可以记录以下内容：

| 字段 | 含义 |
|---|---|
| `id` | 图片编号 |
| `output_file` | 重命名后的图片路径 |
| `label` | 图片分类 |
| `width`、`height` | 图片宽度和高度 |
| `bytes` | 文件大小 |
| `sha256` | 文件哈希值，可辅助查重 |
| `status` | 图片是否可以正常读取 |

查看 CSV：

```bash
column -s, -t < dataset/annotations.csv | less -S
```

## 十一、问题排查

| 现象 | 可能原因 | 处理方法 |
|---|---|---|
| 找不到图片 | `raw` 路径写错或目录为空 | 使用 `find raw -type f` 检查 |
| 显示 `[not_checked]` | 当前 Python 没有加载 Pillow | 使用同一个 Python 环境安装 Pillow |
| 显示 `unreadable` | 图片损坏或扩展名不正确 | 更换或检查图片文件 |
| 只预览没有输出文件 | 使用了 `--dry-run` | 去掉 `--dry-run` 后重新执行 |
| 图片分类不正确 | 原图父目录名称不正确 | 检查 `raw` 下的分类目录 |

验证当前 Python 和 pip 是否对应：

```bash
which python3
python3 -m pip --version
```

## 十二、今天学到的命令和写法

| 命令 / 写法 | 用途 |
|---|---|
| `python3 -m venv .venv` | 创建 Python 虚拟环境 |
| `source .venv/bin/activate` | 激活虚拟环境 |
| `python -m pip install Pillow` | 安装 Pillow |
| `type(value)` | 查看变量类型 |
| `enumerate(items)` | 遍历时获取编号 |
| `zip(list1, list2)` | 同时遍历多个列表 |
| `Path.rglob()` | 递归查找文件 |
| `--dry-run` | 只预览，不真正修改文件 |

## 十三、易错点

1. Python 字符串和数字不能直接相加，需要先转换类型。
2. Python 对缩进敏感，代码块的缩进必须保持一致。
3. 列表下标从 `0` 开始，切片结束位置通常不包含在结果中。
4. `while` 循环要注意避免死循环。
5. 安装 Pillow 后，要确认运行脚本时使用的是同一个 Python 环境。
6. `[not_checked]` 表示没有检查图片，不一定表示图片损坏。
7. `--dry-run` 只用于预览，不会复制或移动文件。
8. 处理原始数据时，优先使用 `copy`，避免误删原图。

## 十四、今日总结

今天学习了 Python 的基本数据类型、常用数据结构和控制流。通过图片数据准备练习，了解了如何把 Python 基础语法用于实际任务。

**Python 负责处理逻辑，Pillow 负责读取图片，CSV/JSON 负责保存数据标注；三者结合可以完成简单的数据集准备工作。**
