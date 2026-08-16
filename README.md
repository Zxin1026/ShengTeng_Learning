# 昇腾学习记录

本仓库用于记录昇腾相关学习过程，采用“每日任务 + 理论笔记 + 可复现实验产物”的方式，逐步熟悉模型部署与调优工程师常用的 Linux、Shell、远程任务、日志分析和推理服务排障工作流。

## 学习路线

当前已完成 Day 1—Day 6，学习主线如下：

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

## 仓库结构

```text
.
├── Daily_Note/       # 每日理论笔记、实验步骤和总结
├── Daily_Task/       # 每日任务材料
├── Report/           # 日志解析结果、端口探测脚本及实验报告
├── SearchTable.md    # 按日期整理的 Linux / Shell 命令速查表
└── README.md         # 项目总览
```

## 快速入口

- [按日期整理的命令速查表](./SearchTable.md)
- [Day 5 日志解析脚本](./Report/8.15/parse_infer_log.py)
- [Day 5 CSV 指标结果](./Report/8.15/result.csv)
- [Day 5 JSON 指标结果](./Report/8.15/result.json)
- [Day 6 端口探测脚本](./Report/8.16/probe_service.sh)
- [Day 6 拒绝连接报告（8000）](./Report/8.16/connectivity_report_20260816_073746.txt)
- [Day 6 连通成功报告（8080）](./Report/8.16/connectivity_report_20260816_074055.txt)

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

## 后续方向

在现有 Linux、日志处理和服务连通性排障基础上，继续补充昇腾开发环境部署、数据处理、容器化、模型转换、推理服务交付及性能调优等内容，并持续保留可复现的命令、脚本和结果。
