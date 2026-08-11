# Day 1 Linux 文件目录学习笔记

日期：2026-08-11  
学习环境：CentOS Linux  
学习模块：Linux 系统认知 / 文件目录

## 一、今日项目案例

### 案例标题

案例 1：搭建 Linux 学习工作区

### 任务目标

在当前用户的家目录下创建 `~/project`，并按用途划分为代码、数据、日志和文档目录：

```text
~/project/
├── code/
├── data/
├── log/
└── doc/
```

### 二、我的实现步骤

#### 1. 查看 CentOS 系统版本

```bash
cat /etc/centos-release
```

如果该文件不存在，可以使用：

```bash
cat /etc/os-release
```

#### 2. 查看当前用户和家目录

```bash
whoami
echo "$HOME"
pwd
```

Linux 中使用 `$HOME` 或 `~` 表示当前用户的家目录，不使用 Windows 风格的 `%HOME%`。

#### 3. 创建项目目录

```bash
mkdir -p "$HOME/project"/{code,data,log,doc}
```

#### 4. 进入项目目录并确认位置

```bash
cd "$HOME/project"
pwd
```

#### 5. 查看目录内容

```bash
ls
ls -la
```

#### 6. 使用 `find` 查看目录结构

```bash
find "$HOME/project" -maxdepth 2 -type d -print
```

#### 7. 验证文件操作命令

```bash
touch code/demo.sh
cp code/demo.sh doc/demo_backup.sh
mv doc/demo_backup.sh log/demo_backup.sh
find "$HOME/project" -name "*.sh" -print
```

#### 8. 查看最终目录树

如果已安装 `tree`，执行：

```bash
tree "$HOME/project" | tee day01_directory_tree.txt
```

CentOS 7 安装命令：

```bash
sudo yum install -y tree
```

CentOS Stream 8/9 安装命令：

```bash
sudo dnf install -y tree
```

### 三、运行结果

`day1_setup.sh` 已成功运行，工作区创建在：

```text
/home/zhangxin/project
```

目录结构包含：

```text
project/
├── code/
│   └── demo.sh
├── data/
├── doc/
└── log/
    └── demo_backup.sh
```

### 四、产出物

- 目录树记录：[day01_directory_tree.txt](./day01_directory_tree.txt)
- 目录树截图：`day01_directory_tree.png`
- Linux 命令速查表：[day01_command_cheatsheet.md](./day01_command_cheatsheet.md)

## 五、今日理论笔记

| 理论要点 | 我的理解 | 为什么重要 | 易错点 |
|---|---|---|---|
| Ubuntu、CentOS、Debian 和用户空间 | Ubuntu、CentOS、Debian 都是 Linux 系统。用户空间就是我们平时运行命令和程序的地方。 | 了解系统类型后，才能选择合适的安装命令和软件。 | 不同系统的安装命令可能不同，CentOS 常用 `yum` 或 `dnf`。 |
| Linux 常见目录 | `/home` 放普通用户文件，`/root` 放 root 用户文件，`/tmp` 放临时文件，`/var` 放日志，`/etc` 放配置文件，`/usr` 放系统程序。 | 知道文件应该放在哪里，查找配置和日志时会更方便。 | `/root` 是 root 用户的家目录，不是整个 Linux 系统；不要随便删除 `/etc` 和 `/var` 中的内容。 |
| 常用命令 | `pwd` 查看当前位置，`ls` 查看文件，`cd` 切换目录，`mkdir` 创建目录，`cp` 复制，`mv` 移动，`find` 查找文件。 | 这些命令是 Linux 日常操作的基础，搭建项目和查看文件都会用到。 | `ls -a` 才能看到隐藏文件；使用 `rm -rf` 前一定要确认路径。 |
| 绝对路径、相对路径和 `~` | `/home/zhangxin/project` 是绝对路径；`./code` 是相对路径；`~` 和 `$HOME` 表示当前用户的家目录。 | 路径写对了，命令才能找到正确的文件和目录。 | Linux 使用 `$HOME`，不能写成 `%HOME%`；相对路径会受到当前目录影响。 |

## 六、Linux 常用命令速查

| 命令 | 作用 | 示例 |
|---|---|---|
| `pwd` | 查看当前路径 | `pwd` |
| `ls` | 查看目录内容 | `ls` |
| `ls -la` | 查看详细信息和隐藏文件 | `ls -la` |
| `cd` | 切换目录 | `cd ~/project` |
| `mkdir -p` | 创建多级目录 | `mkdir -p data/raw` |
| `touch` | 创建空文件 | `touch code/demo.sh` |
| `cp` | 复制文件 | `cp code/demo.sh doc/` |
| `cp -r` | 复制目录 | `cp -r data data_backup` |
| `mv` | 移动或重命名 | `mv old.txt new.txt` |
| `find -name` | 按名称查找文件 | `find . -name "*.sh"` |
| `rm` | 删除文件 | `rm test.txt` |

## 七、易错记录

1. `relase` 拼写错误，正确文件名是 `centos-release`。
2. Linux 使用 `$HOME`，不能写成 `%HOME/project`。
3. `./day01_command_cheatsheet.md` 是 Markdown 文件路径，不是可以直接执行的命令。
4. 查看 Markdown 文件应使用：

```bash
cat ./day01_command_cheatsheet.md
```

5. 执行 Shell 脚本应使用：

```bash
bash ./day1_setup.sh
```

## 八、今日自检

- [x] 已确认 CentOS 系统信息
- [x] 已创建 `~/project/{code,data,log,doc}`
- [x] 已完成目录切换和查看
- [x] 已验证文件创建、复制、移动和查找
- [x] 已完成理论笔记
- [ ] 已保存目录树截图
- [ ] 已补充独立的命令速查表文件

### 今日总结

今天我学会了 Linux 的基本目录结构和常用命令，并成功创建了项目工作区。以后写代码、保存数据、查看日志和整理文档时，可以分别放到不同目录中，项目会更加清晰。

