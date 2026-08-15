# 昇腾学习记录

本仓库用于记录昇腾相关学习过程，采用“每日项目案例 + 理论笔记”的方式，逐步熟悉模型部署与调优工程师常用的 Linux、Shell、远程任务和日志分析工作流。

## 学习路线

当前已完成 Day 1—Day 5，学习主线如下：

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
```

## 每日笔记

| 日期 | 学习主题 | 主要实践 | 笔记 |
|---|---|---|---|
| 2026-08-11 | Linux 文件目录与基础命令 | 创建 `~/project/{code,data,log,doc}` 工作区，练习文件创建、复制、移动和查找 | [Day 1](./Daily_Note/day01.md) |
| 2026-08-12 | Linux 环境初始化 | 创建开发用户、配置 `sudo` 权限、备份并切换 `apt` 软件源 | [Day 2](./Daily_Note/day02.md) |
| 2026-08-13 | Linux 进程与远程任务 | 配置 SSH 免密登录，使用 `ssh`、`scp` 和 `nohup` 远程提交及管理后台任务 | [Day 3](./Daily_Note/day03.md) |
| 2026-08-14 | Shell 基础与批量日志分析 | 学习变量、条件、循环、函数，编写脚本统计 `ERROR` 并提取用户和 IP | [Day 4](./Daily_Note/day04.md) |
| 2026-08-15 | 文本处理与推理日志指标 | 使用 `grep`、`sed`、`awk`、管道和重定向提取精度、耗时等指标 | [Day 5](./Daily_Note/day05.md) |

## 仓库结构

```text
.
├── Daily_Note/       # 每日理论笔记、实验步骤和总结
├── Daily_Task/       # 每日任务材料
├── fsdownload/       # 日志解析脚本及指标结果
├── SearchTable.md    # 按日期整理的 Linux / Shell 命令速查表
└── README.md         # 项目总览
```

## 快速入口

- [按日期整理的命令速查表](./SearchTable.md)
- [Day 5 日志解析脚本](./fsdownload/8.15/parse_infer_log.py)
- [Day 5 CSV 指标结果](./fsdownload/8.15/result.csv)
- [Day 5 JSON 指标结果](./fsdownload/8.15/result.json)

## 后续方向

在现有 Linux 和日志处理基础上，继续补充昇腾开发环境部署、数据处理、容器化、模型转换、推理服务交付及性能调优等内容，并保留可复现的命令、脚本和结果。
