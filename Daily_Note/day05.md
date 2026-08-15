# Day 5 grep、sed、awk 与日志指标提取笔记

日期：2026-08-15  
学习环境：CentOS / Bash  
学习主题：grep、sed、awk、管道、重定向和模型推理日志分析

## 一、今天的目标

今天重点学习 Linux 中常用的文本处理命令，并尝试分析模型推理日志，主要内容包括：

1. 认识 `grep`、`sed`、`awk` 的作用
2. 使用 `grep` 查找日志内容
3. 使用 `sed` 替换和删除文本
4. 使用 `awk` 提取字段和统计数据
5. 理解管道和重定向
6. 提取模型日志中的精度和耗时
7. 生成简单的指标报表

## 二、整体思路

```text
读取日志 -> grep 查找 -> sed 修改 -> awk 提取和统计 -> 输出指标报表
```

一句话总结：

**先找到日志，再提取指标，最后整理成报表。**

## 三、grep：查找和过滤内容

`grep` 主要用于查找包含指定内容的行。

```bash
grep "ERROR" logs/infer.log
grep -n "ERROR" logs/infer.log
grep -i "error" logs/infer.log
grep -r "accuracy" logs/
grep -E "ERROR|WARN" logs/infer.log
```

| 参数 | 作用 |
|---|---|
| `-r` | 递归查找目录中的文件 |
| `-n` | 显示匹配行的行号 |
| `-i` | 忽略大小写 |
| `-c` | 统计匹配行数 |
| `-E` | 使用扩展正则表达式 |

统计错误数量：

```bash
grep -c "ERROR" logs/infer.log
```

## 四、sed：替换和删除文本

`sed` 主要用于修改文本内容。

```bash
sed 's/old/new/g' file.txt
sed -i 's/old/new/g' file.txt
sed '2d' file.txt
sed '/DEBUG/d' logs/infer.log
```

- `s` 表示替换
- `d` 表示删除
- `g` 表示一行中全部替换
- `-i` 表示直接修改原文件

## 五、awk：提取字段和统计数据

`awk` 适合处理按空格或其他分隔符分开的文本。

```bash
awk '{print $1}' logs/infer.log
awk '{print $NF}' logs/infer.log
awk '{print NR, $0}' logs/infer.log
```

| 写法 | 含义 |
|---|---|
| `$1` | 第一列 |
| `$NF` | 最后一列 |
| `$0` | 当前整行 |
| `NR` | 当前行号 |
| `NF` | 当前行的列数 |
| `BEGIN` | 开始处理前执行 |
| `END` | 处理结束后执行 |

## 六、管道和重定向

管道可以把前一个命令的输出交给后一个命令：

```bash
grep "ERROR" logs/infer.log | wc -l
```

| 符号 | 作用 | 示例 |
|---|---|---|
| `|` | 连接两个命令 | `grep "ERROR" app.log \| wc -l` |
| `>` | 覆盖写入文件 | `echo "test" > result.txt` |
| `>>` | 追加写入文件 | `echo "test" >> result.txt` |
| `2>` | 保存错误信息 | `command 2> error.log` |

注意：`>` 会覆盖原有内容，`>>` 才是追加内容。

## 七、模型推理日志指标提取

模型推理日志中常见的指标有：

```text
accuracy=0.9234
latency=185 ms
```

查找精度和耗时：

```bash
grep -Ei "accuracy|latency|elapsed|耗时" logs/infer.log
```

可以编写 Python 解析脚本，提取精度、平均耗时和错误信息，并生成 `result.csv` 或 `result.json`。这两个文件就是指标报表。

## 八、模拟问题排查

| 现象 | 可能原因 |
|---|---|
| 精度偏低 | 模型权重、预处理、标签顺序或量化配置有问题 |
| 耗时偏高 | Batch Size、数据搬运、预热或设备利用率有问题 |
| 没有提取到指标 | 日志格式和脚本中的匹配规则不一致 |

查看错误和耗时：

```bash
grep -nEi "ERROR|FAIL|latency|耗时" logs/infer.log
```

## 九、今天学到的命令

| 命令 | 用途 |
|---|---|
| `grep` | 查找和过滤文本 |
| `sed` | 替换或删除文本 |
| `awk` | 提取字段和统计数据 |
| `wc -l` | 统计行数 |
| `sort` | 排序 |
| `uniq -c` | 去重并统计 |

## 十、易错点

1. `grep` 主要负责查找，`sed` 主要负责修改，`awk` 主要负责字段处理。
2. `sed 's/old/new/g'` 中的 `g` 表示全部替换。
3. `>` 会覆盖文件，`>>` 才是追加内容。
4. `awk` 的 `$1` 是第一列，`$NF` 是最后一列。
5. 使用 `sed -i` 前最好先备份原文件。
6. `accuracy=0.9234` 可能需要转换成 `92.34%`。
7. 不同模型的日志格式可能不同，解析规则需要调整。

## 十一、今日总结

**grep 负责查找，sed 负责修改，awk 负责提取和统计。**

通过管道可以组合多个命令处理日志。结合 Python 脚本后，可以提取模型推理日志中的精度和耗时，并生成指标报表，用来辅助排查问题。
