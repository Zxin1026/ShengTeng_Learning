# 速查表：按日期整理

## 2026-08-11｜Linux 文件目录与基础命令

### 1. 环境认知

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看系统版本 | `cat /etc/centos-release` | CentOS 常用；不存在时可用 `cat /etc/os-release` |
| 查看当前用户 | `whoami` | 显示当前登录用户 |
| 查看家目录 | `echo "$HOME"` | 当前用户的家目录 |
| 查看当前路径 | `pwd` | 确认自己在哪个目录 |

### 2. 文件目录操作

| 目的 | 命令 | 说明 |
|---|---|---|
| 创建多级目录 | `mkdir -p "$HOME/project"/{code,data,log,doc}` | 一次创建工作区结构 |
| 进入目录 | `cd "$HOME/project"` | 切换到项目目录 |
| 查看内容 | `ls` / `ls -la` | `-a` 看隐藏文件，`-l` 看详情 |
| 复制文件 | `cp code/demo.sh doc/demo_backup.sh` | 复制到指定位置 |
| 移动文件 | `mv doc/demo_backup.sh log/demo_backup.sh` | 也可用于重命名 |
| 查找目录 | `find "$HOME/project" -maxdepth 2 -type d -print` | 查看目录树 |
| 查找文件 | `find . -name "*.sh"` | 按名称匹配文件 |
| 创建空文件 | `touch code/demo.sh` | 常用于测试脚本或占位 |

### 3. 常见路径概念

| 概念 | 示例 | 说明 |
|---|---|---|
| 绝对路径 | `/home/zhangxin/project` | 从根目录开始写完整路径 |
| 相对路径 | `./code` | 依赖当前所在目录 |
| 家目录 | `~`、`$HOME` | 当前用户主目录 |

### 4. 常用命令速记

| 命令 | 作用 |
|---|---|
| `pwd` | 查看当前位置 |
| `ls -la` | 查看详细信息和隐藏文件 |
| `mkdir -p` | 创建多级目录 |
| `cp -r` | 复制目录 |
| `mv` | 移动或重命名 |
| `rm` | 删除文件 |
| `find -name` | 按名称查找 |

### 5. 易错点

- Linux 用 `$HOME`，不要写成 `%HOME%`。
- `rm -rf` 风险很高，路径一定先确认。
- `relase` 拼写错误，正确是 `release`。
- `cat` 是查看文本，不是执行命令。

## 2026-08-12｜用户、权限、sudo 与软件源

### 1. 用户和用户组

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看当前用户 | `whoami` | 显示当前登录的用户 |
| 查看用户信息 | `id 用户名` | 查看 UID、GID 和所属组 |
| 创建用户 | `useradd -m -s /bin/bash 用户名` | 同时创建家目录并指定 Shell |
| 设置用户密码 | `passwd 用户名` | 按提示输入两次密码 |
| 创建用户组 | `groupadd 组名` | 创建一个新组 |
| 把用户加入组 | `usermod -aG 组名 用户名` | `-aG` 表示追加到指定组 |
| 切换用户 | `su - 用户名` | 重新登录后权限才更完整 |

### 2. 文件权限

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看权限 | `ls -l 文件名` | 查看所有者、所属组和 rwx 权限 |
| 修改权限 | `chmod 755 文件名` | 所有者可读写执行，其他人可读和执行 |
| 修改所有者 | `chown 用户名 文件名` | 把文件所有者改成指定用户 |
| 修改所属组 | `chgrp 组名 文件名` | 把文件所属组改成指定组 |

数字权限含义：`r=4`，`w=2`，`x=1`。三位数字依次表示所有者、所属组、其他用户。

| 权限 | 含义 |
|---|---|
| `755` | 所有者可读写执行，其他人可读执行 |
| `644` | 所有者可读写，其他人只读 |
| `777` | 所有人都可读写执行，通常不建议使用 |

### 3. sudo 权限

| 目的 | 命令 | 说明 |
|---|---|---|
| 安装 sudo | `dnf install -y sudo` | CentOS Stream 9 使用 `dnf` |
| 编辑 sudo 配置 | `visudo` | 不要直接改 `/etc/sudoers` |
| 检查配置语法 | `visudo -c` | 显示 `parsed OK` 表示正确 |
| 测试 sudo | `sudo whoami` | 成功时输出 `root` |

`/etc/sudoers` 中常见配置：

```sudoers
%wheel ALL=(ALL) ALL
```

`%wheel` 表示 wheel 组，`ALL=(ALL) ALL` 表示可使用 sudo 执行所有命令。

### 4. 软件包与国内源

| 目的 | 命令 |
|---|---|
| 安装软件 | `dnf install -y 软件名` |
| 更新软件 | `dnf update` |
| 删除软件 | `dnf remove 软件名` |
| 查看仓库 | `dnf repolist` |
| 清理缓存 | `dnf clean all` |
| 重新生成缓存 | `dnf makecache` |

常见仓库配置文件：

```text
/etc/yum.repos.d/centos-stream-local.repo
```

切换为阿里云源时常用步骤：

```bash
cp -a /etc/yum.repos.d/centos-stream-local.repo \
/etc/yum.repos.d/centos-stream-local.repo.tuna.bak

sed -i 's|mirrors.tuna.tsinghua.edu.cn|mirrors.aliyun.com|g' \
/etc/yum.repos.d/centos-stream-local.repo

dnf clean all
dnf makecache
dnf repolist
```

CentOS Stream 9 主要仓库：

```text
BaseOS
AppStream
CRB
```

如果 `extras-common` 出现 404，可在仓库文件中改成：

```ini
enabled=0
```

### 5. 今日流程速记

**建用户 -> 配 sudo -> 换软件源 -> 再装工具。**

## 2026-08-13｜Linux 进程、SSH 与远程任务

### 1. 两台虚拟机角色

| 目的 | 命令 / 配置 | 说明 |
|---|---|---|
| 确定 client | CentOS 7 | 作为提交端，负责发起 SSH、上传脚本、提交任务 |
| 确定 server | CentOS 9 | 作为训练端，负责接收任务、运行训练脚本 |
| 查看 IP | `ip addr` | 在两台机器都执行，记录 server 的 IP |
| 测试网络 | `ping server的IP` | 在 client 上执行，能 ping 通说明网络连通 |

### 2. 新建用户

| 目的 | 命令 | 说明 |
|---|---|---|
| 新建用户 | `sudo useradd trainer` | 在 server 上创建训练用户 |
| 设置密码 | `sudo passwd trainer` | 按提示输入两次密码 |
| 查看用户信息 | `id trainer` | 查看 UID、GID 和所属组 |
| 切换用户 | `su - trainer` | 切换到 trainer 用户环境 |
| 加入 sudo 组 | `sudo usermod -aG wheel trainer` | 可选；让 trainer 具备 sudo 权限 |

### 3. SSH 服务与免密登录

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看 SSH 服务 | `sudo systemctl status sshd` | 在 server 上确认 SSH 是否运行 |
| 启动 SSH | `sudo systemctl start sshd` | 如果没有启动，就手动启动 |
| 开机自启 SSH | `sudo systemctl enable sshd` | 防止重启后 SSH 不能用 |
| 开放 SSH 防火墙 | `sudo firewall-cmd --permanent --add-service=ssh` | CentOS 9 上常用 |
| 重新加载防火墙 | `sudo firewall-cmd --reload` | 让防火墙配置生效 |
| 密码登录测试 | `ssh trainer@server的IP` | 在 client 上执行，先确认能用密码登录 |
| 生成密钥 | `ssh-keygen -t rsa -b 4096` | 在 client 上执行，一路回车即可 |
| 复制公钥 | `ssh-copy-id trainer@server的IP` | 把 client 公钥放到 server |
| 测试免密 | `ssh trainer@server的IP` | 如果不用输密码，说明免密成功 |

### 4. ~/.ssh 目录与 authorized_keys

| 文件 / 目录 | 作用 | 常用权限 |
|---|---|---|
| `~/.ssh/` | 保存 SSH 密钥和配置 | `chmod 700 ~/.ssh` |
| `~/.ssh/id_rsa` | client 的私钥，不能给别人 | `chmod 600 ~/.ssh/id_rsa` |
| `~/.ssh/id_rsa.pub` | client 的公钥，可以放到 server | 一般不用手动改 |
| `~/.ssh/authorized_keys` | server 上保存允许登录的公钥 | `chmod 600 ~/.ssh/authorized_keys` |

### 5. 创建远程训练任务

| 目的 | 命令 | 说明 |
|---|---|---|
| 创建训练目录 | `mkdir -p ~/train_demo/logs` | 在 server 上创建脚本和日志目录 |
| 进入训练目录 | `cd ~/train_demo` | 切换到训练目录 |
| 创建训练脚本 | `vim train.py` | 写模拟训练代码 |
| 创建启动脚本 | `vim run_train.sh` | 写 nohup 后台运行命令 |
| 加执行权限 | `chmod +x run_train.sh` | 让脚本可以直接执行 |

`train.py` 示例：

```python
import time

for epoch in range(1, 101):
    print('epoch {}: training...'.format(epoch), flush=True)
    time.sleep(2)

print('training finished', flush=True)
```

`run_train.sh` 示例：

```bash
#!/bin/bash

cd ~/train_demo || exit 1

mkdir -p logs

nohup python3 train.py > logs/train.log 2>&1 &

echo $! > logs/train.pid
echo "Training started"
echo "PID: $(cat logs/train.pid)"
echo "Log: ~/train_demo/logs/train.log"
```

### 6. 进程与后台运行

| 目的 | 命令 | 说明 |
|---|---|---|
| 后台运行 | `nohup python3 train.py > logs/train.log 2>&1 &` | 关闭终端后任务也能继续运行 |
| 保存 PID | `echo $! > logs/train.pid` | `$!` 表示上一个后台任务的 PID |
| 查看进程 | `ps -ef \| grep train.py` | 判断训练程序是否还在运行 |
| 查看当前终端后台任务 | `jobs` | 只看当前 shell 里启动的后台任务 |
| 停止任务 | `kill $(cat logs/train.pid)` | 根据保存的 PID 停止训练 |
| 实时看日志 | `tail -f logs/train.log` | 持续查看训练输出 |

### 7. 从 client 远程提交和查看

| 目的 | 命令 | 说明 |
|---|---|---|
| 远程创建目录 | `ssh trainer@server的IP "mkdir -p ~/train_demo/logs"` | client 直接让 server 执行命令 |
| 上传文件 | `scp train.py run_train.sh trainer@server的IP:~/train_demo/` | 把本地脚本传到 server |
| 提交任务 | `ssh trainer@server的IP "cd ~/train_demo && ./run_train.sh"` | 在 server 后台启动训练 |
| 查看日志 | `ssh trainer@server的IP "tail -f ~/train_demo/logs/train.log"` | client 远程查看 server 日志 |
| 查看进程 | `ssh trainer@server的IP "ps -ef \| grep train.py"` | 确认训练是否在跑 |
| 停止任务 | `ssh trainer@server的IP "kill \$(cat ~/train_demo/logs/train.pid)"` | 远程停止训练 |

### 8. 系统资源查看

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看系统内核 | `uname -a` | 看系统和内核信息 |
| 查看磁盘空间 | `df -h` | 看每个磁盘分区剩余空间 |
| 查看目录大小 | `du -sh 目录名` | 看某个目录占多大 |
| 查看内存 | `free -h` | 看内存和 swap 使用情况 |
| 查看 GPU | `nvidia-smi` | 有 NVIDIA 显卡时查看显存、温度、进程 |

### 9. 易错点

- Linux 路径区分大小写，`/home` 和 `/HOME` 不是一个目录。
- `cd /HOME` 表示进入根目录下的 `HOME`，如果目录不存在就会报错。
- `cd HOME` 表示进入当前目录下的 `HOME`，`cd ~/HOME` 表示进入家目录下的 `HOME`。
- `nohup` 后面通常要加 `&`，否则命令还会占着终端。
- `kill` 后面跟的是 PID，不是脚本文件名。
- `ssh-copy-id` 是在 client 上执行，把公钥复制到 server。
- 私钥 `id_rsa` 不能泄露，公钥 `id_rsa.pub` 可以放到 server。
- `tail -f` 只是查看日志，按 `Ctrl + C` 只会停止看日志，不会停止训练任务。
- Python 报错时先用 `cat -n train.py` 查看行号，重点检查冒号、缩进和括号。
- `scp` 远程路径中间有冒号，例如 `trainer@192.168.119.128:~/train_demo/`。

### 10. 今日流程速记

**确认 IP -> server 开 SSH -> server 建 trainer -> client 生成密钥 -> 复制公钥 -> 免密登录 -> 写 train.py -> 写 run_train.sh -> nohup 后台运行 -> tail -f 查看日志。**

## 2026-08-14｜Shell 基础与批量日志分析

### 1. 创建和运行 Shell 脚本

| 目的 | 命令 / 写法 | 说明 |
|---|---|---|
| 指定 Bash | `#!/usr/bin/env bash` | 写在脚本第一行，告诉系统使用 Bash 执行 |
| 查看 Bash 路径 | `which bash` | 本机结果为 `/usr/bin/bash` 时，也可以写 `#!/usr/bin/bash` |
| 添加执行权限 | `chmod +x 脚本名.sh` | 让脚本可以直接运行 |
| 直接运行脚本 | `./脚本名.sh` | 需要脚本具有执行权限 |
| 使用 Bash 运行 | `bash 脚本名.sh` | 没有执行权限时也可以使用 |
| 检查语法 | `bash -n 脚本名.sh` | 没有输出一般表示语法正确 |
| 调试脚本 | `bash -x 脚本名.sh 参数` | 显示每一步执行过程，方便找错 |

### 2. 变量与环境变量

| 类型 | 示例 | 说明 |
|---|---|---|
| 普通变量 | `name="zhangxin"` | 保存脚本中要使用的数据 |
| 使用变量 | `echo "$name"` | 使用变量时最好加双引号 |
| 环境变量 | `export APP_ENV="test"` | 当前 Shell 启动的子进程也能使用 |
| 只读变量 | `readonly VERSION="1.0"` | 设置后不能再次修改 |
| 删除变量 | `unset name` | 删除普通变量；不能删除只读变量 |
| 命令结果赋值 | `now=$(date)` | 把命令输出保存到变量中 |

变量赋值时，等号两边不能有空格：

```bash
name="zhangxin"      # 正确
name = "zhangxin"    # 错误
```

### 3. Shell 特殊变量

| 变量 | 含义 | 示例 |
|---|---|---|
| `$0` | 当前脚本名称 | `echo "$0"` |
| `$1`、`$2` | 第一个、第二个参数 | `./log_analyze.sh logs/app.log ERROR` |
| `$#` | 参数个数 | 判断用户是否传入文件名 |
| `$?` | 上一条命令的退出状态 | `0` 通常表示成功，非 `0` 表示失败 |
| `$$` | 当前 Shell 的 PID | 可用于区分不同脚本进程 |
| `$!` | 上一个后台任务的 PID | 常用于保存后台任务 PID |

参数示例：

```bash
./log_analyze.sh logs/app.log ERROR
```

此时 `$0` 是 `./log_analyze.sh`，`$1` 是 `logs/app.log`，`$2` 是 `ERROR`，`$#` 是 `2`。

### 4. 条件判断

| 判断目的 | 写法 | 说明 |
|---|---|---|
| 判断文件存在 | `[ -f "$file" ]` | 普通文件存在时条件成立 |
| 判断目录存在 | `[ -d "$dir" ]` | 目录存在时条件成立 |
| 判断字符串为空 | `[ -z "$name" ]` | 变量没有内容时条件成立 |
| 判断字符串非空 | `[ -n "$name" ]` | 变量有内容时条件成立 |
| 判断数字相等 | `[ "$a" -eq "$b" ]` | 数字比较使用 `-eq` |
| 判断字符串相等 | `[ "$a" = "$b" ]` | 字符串比较使用 `=` |

基本结构：

```bash
if [ 条件 ]; then
    要执行的命令
elif [ 其他条件 ]; then
    要执行的命令
else
    要执行的命令
fi
```

### 5. 循环

| 类型 | 示例 | 适用场景 |
|---|---|---|
| `for` | `for file in logs/*.log; do echo "$file"; done` | 批量处理一组文件 |
| `while` | `while [ "$n" -le 5 ]; do echo "$n"; n=$((n+1)); done` | 条件成立时持续执行 |
| `until` | `until [ -f result.txt ]; do sleep 1; done` | 条件不成立时持续执行 |
| `break` | `break` | 立即结束整个循环 |
| `continue` | `continue` | 跳过本次，进入下一次循环 |

### 6. 函数

| 目的 | 写法 | 说明 |
|---|---|---|
| 定义函数 | `say_hello() { echo "hello"; }` | 把重复操作放在一起 |
| 调用函数 | `say_hello` | 直接写函数名即可调用 |
| 传入参数 | `say_hello "zhangxin"` | 函数内部用 `$1` 接收 |
| 局部变量 | `local name="$1"` | 只在当前函数中使用 |
| 返回状态 | `return 0` | `0` 表示成功，非 `0` 表示失败 |
| 返回文字 | `echo "$result"` | 文字或数据通常用 `echo` 输出 |

函数示例：

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
```

### 7. 批量日志分析脚本

创建目录和日志文件：

```bash
mkdir -p logs
vim logs/app.log
```

`log_analyze.sh` 示例：

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

运行脚本：

```bash
chmod +x log_analyze.sh
./log_analyze.sh logs/app.log ERROR
```

第二个参数不写时，脚本会默认统计 `ERROR`：

```bash
./log_analyze.sh logs/app.log
```

### 8. 日志分析常用命令

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看日志 | `cat logs/app.log` | 一次显示全部内容 |
| 查看错误行 | `grep "ERROR" logs/app.log` | 找出包含 `ERROR` 的行 |
| 统计错误数 | `grep -c "ERROR" logs/app.log` | 输出匹配行数 |
| 统计用户 | `grep "ERROR" logs/app.log \| awk ...` | 提取 `user=` 字段后统计 |
| 查看文件是否存在 | `ls -l logs/app.log` | 同时检查路径和文件名 |

### 9. 脚本排错

| 现象 | 检查方法 | 常见原因 |
|---|---|---|
| 提示文件不存在，文件名为空 | `bash -x ./log_analyze.sh logs/app.log ERROR` | `log_file="$1"` 写错或漏写 `$1` |
| 提示文件不存在，但文件就在 `logs` 中 | `ls -l logs` | 路径写成了 `logs/app/log`，正确是 `logs/app.log` |
| 统计结果为 0 | `grep "ERROR" logs/app.log` | 把 `ERROR` 拼成了 `ERRPR`，或大小写不一致 |
| 提示权限不足 | `chmod +x log_analyze.sh` | 脚本没有执行权限 |
| 出现 `^M` 或奇怪报错 | `sed -i 's/\r$//' log_analyze.sh` | 文件使用了 Windows 换行符 |
| 不知道哪一行出错 | `bash -n log_analyze.sh` | 先检查 Shell 语法 |

### 10. 易错点

- Shebang 必须放在脚本第一行，路径也要正确。
- 变量赋值的等号两边不能有空格，例如 `log_file="$1"`。
- 使用变量时最好加双引号，例如 `"$log_file"`，避免路径中有空格时出错。
- `[ ]` 内部的条件和方括号之间必须留空格。
- 文件路径要写准确：本次文件是 `logs/app.log`，不是 `logs/app/log`。
- 关键字要拼写准确：正确是 `ERROR`，不是 `ERRPR`。
- `return` 主要返回状态码；需要输出文字时使用 `echo`。
- Vim 中一行太长时可能自动换行显示，但不一定真的多出了一行。

### 11. 今日流程速记

**创建日志 -> 编写 Shell 脚本 -> 用 `$1` 接收文件路径 -> 判断文件是否存在 -> 用 `$2` 接收关键字 -> 统计并显示结果 -> `bash -n` 检查语法 -> `bash -x` 调试错误。**

## 2026-08-15｜grep、sed、awk 与日志指标提取

### 1. 三个命令的作用

| 命令 | 作用 | 简单理解 |
|---|---|---|
| `grep` | 查找内容 | 过滤出需要的行 |
| `sed` | 修改文本 | 替换或删除内容 |
| `awk` | 处理字段 | 提取和统计列数据 |

### 2. 常用写法

| 目的 | 命令 | 说明 |
|---|---|---|
| 递归查找 | `grep -r "ERROR" logs/` | 查找目录下所有文件 |
| 显示行号 | `grep -n "ERROR" app.log` | 显示匹配内容所在行 |
| 忽略大小写 | `grep -i "error" app.log` | `error` 和 `ERROR` 都能找到 |
| 使用扩展正则 | `grep -E "ERROR|WARN" app.log` | 查找多个关键词 |
| 替换内容 | `sed 's/old/new/g' file.txt` | 把旧内容替换成新内容 |
| 删除指定行 | `sed '2d' file.txt` | 删除第 2 行 |
| 提取第一列 | `awk '{print $1}' file.txt` | 输出每行第一列 |
| 提取最后一列 | `awk '{print $NF}' file.txt` | 输出每行最后一列 |

### 3. awk 常用概念

| 概念 | 含义 |
|---|---|
| `$1` | 第一列 |
| `$NF` | 最后一列 |
| `NR` | 当前处理的行号 |
| `BEGIN` | 正式处理前执行 |
| `END` | 全部处理完成后执行 |

示例：

```bash
awk 'BEGIN {print "开始"} {print NR, $1} END {print "结束"}' app.log
```

### 4. 管道和重定向

| 符号 | 作用 | 示例 |
|---|---|---|
| `|` | 把前一个命令的结果交给下一个命令 | `grep "ERROR" app.log \| wc -l` |
| `>` | 覆盖写入文件 | `echo "test" > result.txt` |
| `>>` | 追加写入文件 | `echo "test" >> result.txt` |
| `2>` | 保存错误信息 | `command 2> error.log` |

### 5. 日志指标提取

模型推理日志可以通过脚本提取：

- 精度，例如 `accuracy=0.9234`；
- 耗时，例如 `latency: 185 ms`；
- 错误信息，例如 `ERROR` 或 `FAIL`。

脚本运行后可以生成 `result.csv` 或 `result.json`，这就是指标报表。

### 6. 易错点

- `grep` 主要负责查找，`sed` 主要负责修改，`awk` 主要负责处理字段。
- `sed 's/old/new/g'` 中的 `g` 表示一行中全部替换。
- `>` 会覆盖原文件，`>>` 才是追加内容。
- 使用管道时，前一个命令的输出会成为后一个命令的输入。
- `awk` 的 `$1` 是第一列，`$NF` 是最后一列，不要混淆。
- 修改文件前最好先备份，避免 `sed -i` 改错内容。

### 7. 今日流程速记

**grep 查找 -> sed 修改 -> awk 提取和统计 -> 管道组合命令 -> 脚本解析日志 -> 生成指标报表。**
