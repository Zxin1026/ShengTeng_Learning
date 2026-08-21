# 昇腾学习记录

本仓库用于记录昇腾相关学习过程，采用“每日任务 + 理论笔记 + 可复现实验产物”的方式，逐步熟悉模型部署与调优工程师常用的 Linux、Shell、Python、远程任务、日志分析、图片数据准备、推理服务排障和上线前系统准备工作。

截至 2026-08-21，已完成 Day 1—Day 11，形成了 11 篇 Markdown 学习笔记、11 份每日任务文档、1 份命令速查表，以及日志解析、服务连通性、图片数据准备、JSON 推理结果报表、AI 接口批量调用和 Docker 环境准备等实验产物。

## 学习路线

当前已完成 Day 1—Day 11，学习主线如下：

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
        ↓
JSON 推理结果读取与 Markdown 报表
        ↓
requests 调用 AI 接口、异常处理与进度条
        ↓
Docker 安装、镜像管理与容器化 Python/PyTorch 环境
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
| 2026-08-19 | Python 函数、JSON 推理结果与格式化报表 | 使用 `json`、`pathlib` 和函数读取推理结果，生成 Markdown 报表，并在 CentOS 中运行脚本 | [Day 9](./Daily_Note/day09.md) |
| 2026-08-20 | requests 调用 AI 接口、异常处理与进度条 | 使用虚拟环境安装依赖，调用 OpenAI 兼容接口，处理超时/限流/服务端错误并保存 JSONL 结果 | [Day 10](./Daily_Note/day10.md) |
| 2026-08-21 | Docker 概念、安装与镜像 | 在 CentOS Stream 9 安装 Docker CE，区分软件源与镜像加速器，管理 Python/PyTorch 镜像并验证容器环境 | [Day 11](./Daily_Note/day11.md) |

## 仓库结构

```text
.
├── Daily_Note/       # 每日理论笔记、实验步骤和总结
├── Daily_Task/       # 2026-08-11 至 2026-08-21 的每日任务材料（Word 97-2003）
├── Report/           # 日志解析、端口探测、图片数据准备、JSON 报表和 AI 接口实验产物
├── SearchTable.md    # 按日期整理的 Linux、Shell、Python 与 Docker 命令速查表
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
| 2026-08-19 | [8.19.doc](./Daily_Task/8.19.doc) | [Day 9](./Daily_Note/day09.md) |
| 2026-08-20 | [8.20.doc](./Daily_Task/8.20.doc) | [Day 10](./Daily_Note/day10.md) |
| 2026-08-21 | [8.21.doc](./Daily_Task/8.21.doc) | [Day 11](./Daily_Note/day11.md) |

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
- [Day 9 Python 函数、JSON 与报表笔记](./Daily_Note/day09.md)
- [Day 9 JSON 推理示例](./Report/8.19/inference.json)
- [Day 9 报表生成脚本](./Report/8.19/report.py)
- [Day 9 一键运行脚本](./Report/8.19/run_report.sh)
- [Day 9 Markdown 报表结果](./Report/8.19/report.md)
- [Day 10 requests 调用 AI 接口笔记](./Daily_Note/day10.md)
- [Day 10 AI 批量推理脚本](./Report/8.20/ai_infer.py)
- [Day 10 示例问题列表](./Report/8.20/prompts.txt)
- [Day 10 JSONL 推理结果](./Report/8.20/results.jsonl)
- [Day 10 命令与排障速查](./SearchTable.md#2026-08-20requests-调用-ai-接口异常处理与进度条)
- [Day 11 Docker 安装、镜像与 Python 环境笔记](./Daily_Note/day11.md)
- [Day 11 Docker 命令与排障速查](./SearchTable.md#2026-08-21docker-安装镜像与-python-环境)

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

### JSON 推理结果格式化报表

`Report/8.19/report.py` 用于读取 JSON 推理结果并生成 Markdown 报表，支持从 `results`、`predictions`、`outputs`、`items` 或 `data` 字段中识别结果列表；当结果不是字典列表时，会保留为编号列表或原始 JSON，便于排查不同模型输出格式。

直接运行：

```bash
python3 Report/8.19/report.py \
  Report/8.19/inference.json \
  Report/8.19/report.md
```

也可以使用 `Report/8.19/run_report.sh` 在 CentOS 的固定工作目录 `/opt/json-report` 中执行：

```bash
sudo mkdir -p /opt/json-report
sudo cp Report/8.19/report.py Report/8.19/inference.json Report/8.19/run_report.sh /opt/json-report/
sudo chmod +x /opt/json-report/run_report.sh
/opt/json-report/run_report.sh
```

该脚本默认从 `/opt/json-report/inference.json` 读取，并将结果写入 `/opt/json-report/report.md`；如果改用其他目录，需要同步调整脚本中的 `BASE_DIR`。

示例输入包含 `model`、`task`、`timestamp`、`status`、`summary` 和 `results` 字段，生成结果见 [report.md](./Report/8.19/report.md)。脚本只负责读取和整理已有 JSON，不负责执行模型推理；运行前应先用 `jq empty <file>.json` 检查 JSON 格式。

### AI 接口批量调用与结果保存

`Report/8.20/ai_infer.py` 是一个使用 `requests` 调用 OpenAI 兼容聊天接口的批处理示例。脚本从文本文件逐行读取问题，使用 `tqdm` 显示进度，并将每条请求的成功结果或错误信息立即写入 JSONL 文件，便于任务中断后保留已完成记录。

运行前先创建并激活虚拟环境，安装依赖，并通过环境变量提供接口地址、API Key 和模型名：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests tqdm

export AI_API_URL="https://api.example.com/v1/chat/completions"
export AI_API_KEY="你的_API_KEY"
export AI_MODEL="你的模型名称"
```

建议先用 `curl` 验证 URL、鉴权和请求路径，再执行批量脚本：

```bash
curl -i -sS "$AI_API_URL" \
  -H "Authorization: Bearer $AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"'"$AI_MODEL"'","messages":[{"role":"user","content":"你好"}]}'

python Report/8.20/ai_infer.py \
  --input Report/8.20/prompts.txt \
  --output Report/8.20/results.jsonl
```

脚本对超时、连接异常、`429` 和 `5xx` 错误进行有限重试，对其他 `4xx` 错误直接报告；每完成一条请求都会 `flush()` 输出文件。仓库中的 `prompts.txt` 是示例问题列表，当前 `results.jsonl` 保存了 2 条成功调用记录，包含请求索引、问题、回答和原始响应 JSON。不要把真实 API Key 写入脚本或提交到仓库。

### Docker 容器环境准备

Day 11 记录了在 CentOS Stream 9 中安装和验证 Docker 的完整流程，重点包括 Docker CE 软件源、`systemctl` 服务管理、普通用户权限、`/etc/docker/daemon.json` 镜像加速器配置，以及 Docker Hub 连接失败时的排障方法。Docker 软件源只负责安装 Docker 软件包，镜像加速器则影响 `docker pull` 的下载路径，两者需要分别配置。

常用验证命令如下：

```bash
sudo systemctl enable --now docker
sudo docker version
sudo docker run --rm hello-world
sudo docker run --rm python:3.9-slim-bookworm python --version
sudo docker run --rm \
  pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime \
  python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

`python --version` 只检查宿主机 Python；容器内版本必须通过 `docker run` 单独确认。`torch.cuda.is_available()` 返回 `False` 时，还需结合宿主机驱动、NVIDIA Container Toolkit 和 GPU 运行参数继续判断，不能直接认定 PyTorch 安装失败。

## 当前实验产物

| 日期 | 产物 | 用途 |
|---|---|---|
| 2026-08-15 | `Report/8.15/parse_infer_log.py`、`result.csv`、`result.json` | 批量提取推理日志中的精度、耗时等指标 |
| 2026-08-16 | `Report/8.16/probe_service.sh` | 使用 `ss` 和 `curl` 探测端口及 HTTP 服务 |
| 2026-08-16 | 两份 `connectivity_report_*.txt` | 保存 8000 拒绝连接和 8080 连通成功的对照结果 |
| 2026-08-17 | `SearchTable.md` 新增 CentOS 章节 | 汇总镜像源、防火墙、端口监听和服务验证命令 |
| 2026-08-18 | `Report/8.18/prepare_dataset.py`、`annotations.csv`、`annotations.json` | 批量分类、重命名图片，并生成包含尺寸、哈希和状态的标注清单 |
| 2026-08-19 | `Report/8.19/report.py`、`run_report.sh`、`inference.json`、`report.md` | 读取 JSON 推理输出，生成可读的 Markdown 结果报表 |
| 2026-08-20 | `Report/8.20/ai_infer.py`、`prompts.txt`、`results.jsonl` | 调用 AI 接口，显示批量进度，有限重试并逐条保存成功/失败结果 |
| 2026-08-21 | `Daily_Note/day11.md`、`Daily_Task/8.21.doc`、`SearchTable.md` Docker 章节 | 记录 Docker 安装、镜像加速器、容器权限、Python/PyTorch 镜像验证和常见网络排障 |

## 后续方向

在现有 Linux、Python、日志处理、图片数据准备、服务连通性排障、AI 接口调用和 Docker 容器环境基础上，继续补充昇腾开发环境部署、模型转换、推理服务交付及性能调优等内容，并持续保留可复现的命令、脚本和结果。
