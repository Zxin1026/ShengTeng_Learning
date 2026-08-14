# Day 4 Shell 基础与批量日志分析笔记

日期：2026-08-14  
学习环境：CentOS / Bash  
学习主题：Shell 变量、条件判断、循环、函数、批量日志分析

## 一、今天的目标

今天重点练习的是 Shell 脚本基础，并完成一个日志分析脚本，核心内容包括：

1. 认识 Shebang，学会给脚本添加执行权限
2. 学习普通变量、环境变量和特殊变量
3. 使用条件判断检查文件是否存在
4. 学习 `for`、`while`、`until` 循环
5. 学习函数的定义、调用和参数传递
6. 编写脚本统计日志中的 `ERROR` 数量并提取用户和 IP

## 二、整体思路

这次实验可以理解成：

```text
传入日志文件和关键字
        |
        v
检查日志文件是否存在
        |
        v
查找符合关键字的日志
        |
        v
输出数量、明细、用户和 IP
```

一句话总结：

**先接收参数并检查文件，再分析日志并输出结果。**

## 三、Shell 脚本基础

Shell 脚本一般以 `.sh` 结尾，第一行需要写 Shebang。

查看本机 Bash 路径：

```bash
which bash
```

本机输出为：

```text
/usr/bin/bash
```

因此脚本第一行可以写：

```bash
#!/usr/bin/bash
```

也可以使用更通用的写法：

```bash
#!/usr/bin/env bash
```

创建脚本后，添加执行权限：

```bash
chmod +x day4_basic.sh
```

运行脚本：

```bash
./day4_basic.sh
```

其中：

- Shebang：告诉系统使用哪个解释器运行脚本
- `chmod +x`：给脚本添加执行权限
- `./`：表示运行当前目录中的脚本

## 四、变量和特殊变量

普通变量的定义和使用：

```bash
name="zhangxin"
echo "$name"
```

变量赋值时，等号两边不能有空格：

```bash
name="zhangxin"      # 正确
name = "zhangxin"    # 错误
```

环境变量使用 `export` 定义：

```bash
export APP_ENV="test"
echo "$APP_ENV"
```

只读变量使用 `readonly` 定义，设置后不能修改：

```bash
readonly VERSION="1.0"
```

Shell 中常用的特殊变量：

| 变量 | 含义 |
|---|---|
| `$0` | 当前脚本名称 |
| `$1` | 第一个参数 |
| `$2` | 第二个参数 |
| `$#` | 参数总数 |
| `$?` | 上一条命令的执行结果，`0` 一般表示成功 |
| `$$` | 当前 Shell 的 PID |
| `$!` | 上一个后台任务的 PID |

例如执行：

```bash
./log_analyze.sh logs/app.log ERROR
```

此时：

- `$0` 是 `./log_analyze.sh`
- `$1` 是 `logs/app.log`
- `$2` 是 `ERROR`
- `$#` 是 `2`

## 五、条件、循环和函数

### 1. 条件判断

判断文件是否存在：

```bash
if [ -f "$file" ]; then
    echo "文件存在"
else
    echo "文件不存在"
fi
```

常用判断：

| 写法 | 含义 |
|---|---|
| `[ -f "$file" ]` | 判断普通文件是否存在 |
| `[ -d "$dir" ]` | 判断目录是否存在 |
| `[ -z "$name" ]` | 判断字符串是否为空 |
| `[ -n "$name" ]` | 判断字符串是否不为空 |
| `[ "$a" -eq "$b" ]` | 判断两个数字是否相等 |

### 2. 循环

`for` 循环适合批量处理文件：

```bash
for file in logs/*.log; do
    echo "$file"
done
```

`while` 循环会在条件成立时重复执行：

```bash
n=1

while [ "$n" -le 3 ]; do
    echo "$n"
    n=$((n + 1))
done
```

- `break`：立即结束整个循环
- `continue`：跳过本次，继续下一次循环
- `until`：条件不成立时重复执行

### 3. 函数

函数可以把重复使用的代码放在一起：

```bash
check_file() {
    local file="$1"

    if [ -f "$file" ]; then
        echo "文件存在: $file"
        return 0
    fi

    echo "文件不存在: $file"
    return 1
}

check_file "logs/app.log"
```

其中：

- `local`：定义只在函数内部使用的变量
- `$1`：函数接收的第一个参数
- `return`：返回状态码
- `echo`：输出文字或数据

## 六、批量日志分析脚本

先创建日志目录和测试日志：

```bash
mkdir -p logs
vim logs/app.log
```

测试日志中一共有 6 条记录，其中有 3 条 `ERROR`。

创建 `log_analyze.sh`：

```bash
#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo "用法: $0 日志文件 [关键字]"
    exit 1
fi

log_file="$1"
keyword="${2:-ERROR}"

if [ ! -f "$log_file" ]; then
    echo "错误: 日志文件不存在: $log_file"
    exit 2
fi

echo "===== 日志分析开始 ====="
echo "日志文件: $log_file"
echo "关键字: $keyword"
echo

echo "1. $keyword 日志总数:"
grep -c -- "$keyword" "$log_file"
echo

echo "2. $keyword 日志明细:"
grep -- "$keyword" "$log_file"
echo

echo "3. 涉及用户统计:"
grep -- "$keyword" "$log_file" | awk '{
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^user=/) print $i
    }
}' | sort | uniq -c

echo
echo "4. 涉及 IP 统计:"
grep -- "$keyword" "$log_file" | awk '{
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^ip=/) print $i
    }
}' | sort | uniq -c

echo
echo "===== 日志分析结束 ====="
```

添加执行权限：

```bash
chmod +x log_analyze.sh
```

运行脚本：

```bash
./log_analyze.sh logs/app.log ERROR
```

运行后，`ERROR` 日志总数应该输出：

```text
3
```

如果不写第二个参数，脚本会默认查找 `ERROR`：

```bash
./log_analyze.sh logs/app.log
```

## 七、今天学到的命令

| 命令 | 用途 |
|---|---|
| `which bash` | 查看 Bash 的路径 |
| `chmod +x` | 给脚本添加执行权限 |
| `./脚本名.sh` | 运行当前目录中的脚本 |
| `bash -n 脚本名.sh` | 检查脚本语法 |
| `bash -x 脚本名.sh` | 显示脚本执行过程，帮助排错 |
| `test`、`[ ]` | 进行条件判断 |
| `grep` | 查找包含指定关键字的日志 |
| `grep -c` | 统计匹配的日志条数 |
| `awk` | 提取日志中的字段 |
| `sort` | 对内容进行排序 |
| `uniq -c` | 去重并统计出现次数 |

## 八、易错点

1. Shebang 必须写在脚本第一行，并且 Bash 路径要正确。
2. 变量赋值时等号两边不能有空格，正确写法是 `log_file="$1"`。
3. 使用变量时最好加双引号，例如 `"$log_file"`。
4. `[ ]` 中的条件与方括号之间必须留空格。
5. 日志文件的正确路径是 `logs/app.log`，不是 `logs/app/log`。
6. 关键字是 `ERROR`，不能误写成 `ERRPR`。
7. 如果错误提示中的文件名为空，要检查 `log_file="$1"` 是否写对。
8. 可以使用 `bash -x ./log_analyze.sh logs/app.log ERROR` 查看参数有没有正确传入。
9. Windows 换行符可能造成脚本报错，可以执行 `sed -i 's/\r$//' log_analyze.sh`。
10. Vim 中一行太长时可能自动换行显示，但文件中不一定真的多了一行。

## 九、今日总结

今天的重点是理解 Shell 脚本处理任务的基本流程：

**接收参数 -> 检查文件 -> 判断条件 -> 分析日志 -> 输出统计结果。**

通过这次练习，我学会了使用 `$1` 和 `$2` 接收参数，也知道了遇到脚本错误时，可以先用 `bash -n` 检查语法，再用 `bash -x` 查看执行过程。以后处理服务器日志、批量检查文件和编写自动化脚本时都会用到这些知识。
