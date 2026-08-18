# 昇腾学习记录

本仓库用于记录昇腾相关学习过程，采用“每日任务 + 理论笔记 + 可复现实验产物”的方式，逐步熟悉模型部署与调优工程师常用的 Linux、Shell、Python、远程任务、日志分析、图片数据准备、推理服务排障和上线前系统准备工作。

截至 2026-08-18，已完成 Day 1—Day 8，形成了 8 篇 Markdown 学习笔记、8 份每日任务文档、1 份命令速查表，以及日志解析、服务连通性和图片数据准备实验产物。

## 学习路线

当前已完成 Day 1—Day 8，学习主线如下：

```text
Linux 文件与目录
        ↓
Linux 环境初始化
        ↓
SSH 远程登录与后台任务
        ↓
Shell 脚本与批量日志分析
        ↓
模型推理日志指标提取
        ↓
推理服务端口探测与连通性报告
        ↓
CentOS 镜像源、防火墙与服务端口准备
        ↓
Python 基础与图片数据集准备
```

## 每日笔记

| 日期 | 学习主题 | 主要实践 | 笔记 |
|---|---|---|---|
| 2026-08-11 | Linux 文件目录与基础命令 | 创建 `~/project/{code,data,log,doc}` 工作区，练习文件创建、复制、移动和查找 | [Day 1](./Daily_Note/day01.md) |
| 2026-08-12 | Linux 环境初始化 | 创建开发用户、配置 `sudo` 权限、备份并切换 `apt` 软件源 | [Day 2](./Daily_Note/day02.md) |
| 2026-08-13 | Linux 进程与远程任务 | 配置 SSH 免密登录，使用 `ssh`、`scp` 和 `nohup` 远程提交及管理后台任务 | [Day 3](./Daily_Note/day03.md) |
| 2026-08-14 | Shell 基础与批量日志分析 | 学习变量、条件、循环、函数，编写脚本统计 `ERROR` 并提取用户和 IP | [Day 4](./Daily_Note/day04.md) |
| 2026-08-15 | 文本处理与推理日志指标 | 使用 `grep`、`sed`、`awk`、管道和重定向提取精度、耗时等指标 | [Day 5](./Daily_Note/day05.md) |
| 2026-08-16 | 推理服务端口探测与连通性 | 使用 `ss` 检查监听端口，使用 `curl` 验证 HTTP 服务，并编写脚本生成连通性报告 | [Day 6](./Daily_Note/day06.md) |
| 2026-08-17 | CentOS 上线前基础准备 | 配置 `pip`/`dnf` 镜像源，使用 `firewalld` 开放 8080 端口，并用 `ss`、`curl` 验证服务 | [Day 7](./Daily_Note/day07.md) |
| 2026-08-18 | Python 基础与图片数据准备 | 学习 Python 类型、数据结构和控制流，使用 Pillow 批量分类、重命名图片并生成 CSV/JSON 标注 | [Day 8](./Daily_Note/day08.md) |

## 仓库结构

```text
.
├── Daily_Note/       # 每日理论笔记、实验步骤和总结
├── Daily_Task/       # 2026-08-11 至 2026-08-18 的每日任务材料（Word 97-2003）
├── Report/           # 日志解析、端口探测和图片数据准备实验产物
├── SearchTable.md    # 按日期整理的 Linux / Shell 命令速查表
└── README.md         # 项目总览
```

## 每日任务材料

任务文档按日期保存在 `Daily_Task/` 目录中，与每日笔记一一对应：

| 日期 | 任务文档 | 对应笔记 |
|---|---|---|
| 2026-08-11 | [8.11.doc](./Daily_Task/8.11.doc) | [Day 1](./Daily_Note/day01.md) |
| 2026-08-12 | [8.12.doc](./Daily_Task/8.12.doc) | [Day 2](./Daily_Note/day02.md) |
| 2026-08-13 | [8.13.doc](./Daily_Task/8.13.doc) | [Day 3](./Daily_Note/day03.md) |
| 2026-08-14 | [8.14.doc](./Daily_Task/8.14.doc) | [Day 4](./Daily_Note/day04.md) |
| 2026-08-15 | [8.15.doc](./Daily_Task/8.15.doc) | [Day 5](./Daily_Note/day05.md) |
| 2026-08-16 | [8.16.doc](./Daily_Task/8.16.doc) | [Day 6](./Daily_Note/day06.md) |
| 2026-08-17 | [8.17.doc](./Daily_Task/8.17.doc) | [Day 7](./Daily_Note/day07.md) |
| 2026-08-18 | [8.18.doc](./Daily_Task/8.18.doc) | [Day 8](./Daily_Note/day08.md) |

## 快速入口

- [按日期整理的命令速查表](./SearchTable.md)
- [Day 5 日志解析脚本](./Report/8.15/parse_infer_log.py)
- [Day 5 CSV 指标结果](./Report/8.15/result.csv)
- [Day 5 JSON 指标结果](./Report/8.15/result.json)
- [Day 6 端口探测脚本](./Report/8.16/probe_service.sh)
- [Day 6 拒绝连接报告（8000）](./Report/8.16/connectivity_report_20260816_073746.txt)
- [Day 6 连通成功报告（8080）](./Report/8.16/connectivity_report_20260816_074055.txt)
- [Day 7 CentOS 镜像源、防火墙与服务端口笔记](./Daily_Note/day07.md)
- [Day 7 命令与排障速查](./SearchTable.md#2026-08-17centos-镜像源防火墙与服务端口)
- [Day 8 Python 基础与图片数据准备笔记](./Daily_Note/day08.md)
- [Day 8 图片数据集准备脚本](./Report/8.18/prepare_dataset.py)
- [Day 8 CSV 标注结果](./Report/8.18/annotations.csv)
- [Day 8 JSON 标注结果](./Report/8.18/annotations.json)

## 实验脚本

### 推理日志指标提取

`Report/8.15/parse_infer_log.py` 支持从单个日志文件或目录中提取精度、耗时等指标，并输出 CSV 和 JSON 结果，适合用于批量检查推理日志。

### 推理服务连通性探测

`Report/8.16/probe_service.sh` 结合 `ss` 和 `curl` 检查目标端口是否监听、HTTP 接口是否可访问，并将结果保存为带时间戳的 `connectivity_report_*.txt` 文件。

```bash
chmod +x Report/8.16/probe_service.sh
./Report/8.16/probe_service.sh \
  127.0.0.1 8080 http://127.0.0.1:8080/
```

脚本参数依次为目标主机、目标端口和探测 URL；三者应与实际推理服务配置保持一致。报告中的 `8000` 拒绝连接案例和 `8080` 成功案例，可对照学习端口不一致、服务未启动及接口路径错误等问题的排查方法。

### CentOS 服务上线前检查

Day 7 目前以笔记和命令速查为主，重点记录以下流程：

```text
配置 pip/dnf 镜像 -> 启动 firewalld -> 开放 8080
-> 用 ss 确认 LISTEN -> 启动业务服务 -> 用 curl 验证访问
```

需要注意：防火墙放行只代表允许连接，不能证明业务程序已经启动；远程访问还需确认程序监听 `0.0.0.0:8080`，并检查云安全组等外部网络策略。

### 图片数据集准备

`Report/8.18/prepare_dataset.py` 会递归扫描输入目录中的常见图片格式，以原始图片的第一级目录作为分类标签，按 `label_000001.jpg` 的格式复制或移动图片，并生成包含尺寸、文件大小、SHA-256 和读取状态的 CSV/JSON 标注清单。

建议先使用 `--dry-run` 预览，确认分类和目标路径后再正式执行：

```bash
python3 Report/8.18/prepare_dataset.py \
  --input ./raw \
  --output ./dataset \
  --mode copy \
  --dry-run

python3 Report/8.18/prepare_dataset.py \
  --input ./raw \
  --output ./dataset \
  --mode copy
```

脚本默认使用 `copy` 保留原图，也支持 `--mode move`；需要安装 Pillow 才能检查图片尺寸和完整性。输出目录包含 `images/<label>/`、`annotations.csv` 和 `annotations.json`。本次示例共处理 4 张图片，分类为 `car`、`cat` 和 `dog`，图片检查状态均为 `ok`。

## 当前实验产物

| 日期 | 产物 | 用途 |
|---|---|---|
| 2026-08-15 | `Report/8.15/parse_infer_log.py`、`result.csv`、`result.json` | 批量提取推理日志中的精度、耗时等指标 |
| 2026-08-16 | `Report/8.16/probe_service.sh` | 使用 `ss` 和 `curl` 探测端口及 HTTP 服务 |
| 2026-08-16 | 两份 `connectivity_report_*.txt` | 保存 8000 拒绝连接和 8080 连通成功的对照结果 |
| 2026-08-17 | `SearchTable.md` 新增 CentOS 章节 | 汇总镜像源、防火墙、端口监听和服务验证命令 |
| 2026-08-18 | `Report/8.18/prepare_dataset.py`、`annotations.csv`、`annotations.json` | 批量分类、重命名图片，并生成包含尺寸、哈希和状态的标注清单 |

## 后续方向

在现有 Linux、Python、日志处理、图片数据准备和服务连通性排障基础上，继续补充昇腾开发环境部署、容器化、模型转换、推理服务交付及性能调优等内容，并持续保留可复现的命令、脚本和结果。
