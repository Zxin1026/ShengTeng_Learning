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

## 2026-08-16｜推理服务端口探测与连通性报告

### 1. 任务目标

使用 `ss -tlnp` 查看服务端口是否监听，再使用 `curl` 测试 HTTP 接口，最后由 Shell 脚本生成连通性报告。

### 2. 检查工具

| 目的 | 命令 | 说明 |
|---|---|---|
| 安装网络工具 | `sudo dnf install -y iproute curl` | CentOS Stream 9 常用；CentOS 7 可用 `sudo yum install -y iproute curl` |
| 检查 `ss` | `ss --version` | `ss` 通常由 `iproute` 提供 |
| 检查 `curl` | `curl --version` | 用于访问 HTTP/HTTPS 服务 |
| 查看当前路径 | `pwd` | 报告文件默认保存在当前目录 |

### 3. 查看端口监听

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看全部 TCP 监听端口 | `sudo ss -tlnp` | `-t` TCP，`-l` 监听，`-n` 数字显示，`-p` 显示进程 |
| 查看指定端口 | `sudo ss -tlnp \| grep ':8080'` | 检查 8080 是否有程序监听 |
| 查看常见推理端口 | `sudo ss -lntp \| grep -E ':(8000\|8080\|7860\|11434)\b'` | 排查端口配置不一致 |
| 没有匹配时给出提示 | `sudo ss -lntp \| grep ':8000' \|\| echo '8000 没有服务监听'` | `\|\|` 表示前一条命令失败时执行后一条 |

如果没有看到 `LISTEN` 行，表示该端口没有程序监听，不能直接用 `curl` 访问。

### 4. 使用 curl 测试服务

| 目的 | 命令 | 说明 |
|---|---|---|
| 测试本机接口 | `curl -i http://127.0.0.1:8080/` | `127.0.0.1` 表示当前虚拟机 |
| 设置连接超时 | `curl -i --connect-timeout 3 --max-time 8 URL` | 避免服务异常时一直等待 |
| 查看详细过程 | `curl -v http://127.0.0.1:8080/` | 显示 DNS、TCP 和 HTTP 过程 |
| 测试健康接口 | `curl -i http://127.0.0.1:8000/health` | 前提是服务确实提供 `/health` |

常见结果：

| 结果 | 含义 |
|---|---|
| `200 OK` | 服务可访问且请求成功 |
| `404 Not Found` | 网络已连通，但接口路径不存在 |
| `401` / `403` | 需要认证或没有权限 |
| `500` | 服务端内部错误 |
| `curl: (7) ... 拒绝连接` | 目标端口没有服务监听，或服务尚未启动 |
| `Connection timed out` | 可能是网络路由或防火墙问题 |

### 5. 端口参数必须保持一致

如果 Python 服务启动在 `8080`：

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

就应在另一个终端检查 `8080`：

```bash
sudo ss -lntp | grep ':8080'
sudo ./probe_service.sh 127.0.0.1 8080 http://127.0.0.1:8080/
```

不能让服务运行在 `8080`，却让脚本默认检查 `8000`。脚本中常见的默认参数写法如下：

```bash
HOST="${1:-127.0.0.1}"
PORT="${2:-8080}"
URL="${3:-http://${HOST}:${PORT}/}"
```

也可以不修改脚本，每次直接传入主机、端口和 URL。

### 6. 连通性探测脚本

`probe_service.sh` 示例：

```bash
#!/usr/bin/env bash

set -u

HOST="${1:-127.0.0.1}"
PORT="${2:-8080}"
URL="${3:-http://${HOST}:${PORT}/}"
REPORT="connectivity_report_$(date +%Y%m%d_%H%M%S).txt"
BODY_FILE="$(mktemp)"
ERR_FILE="$(mktemp)"

trap 'rm -f "$BODY_FILE" "$ERR_FILE"' EXIT

{
    echo "========== 推理服务连通性报告 =========="
    echo "时间: $(date '+%F %T')"
    echo "目标主机: $HOST"
    echo "目标端口: $PORT"
    echo "探测 URL: $URL"
    echo

    echo "[1] ss 端口监听检查"
    ALL_LISTEN="$(ss -tlnp 2>/dev/null || true)"
    LISTEN_INFO="$(printf '%s\n' "$ALL_LISTEN" | awk -v pattern=":${PORT}$" 'NR > 1 && $4 ~ pattern')"

    if [[ -n "$LISTEN_INFO" ]]; then
        echo "结果: 端口正在监听"
        echo "$LISTEN_INFO"
    else
        echo "结果: 未发现端口监听"
    fi

    echo
    echo "[2] curl HTTP 连通性检查"
    HTTP_CODE="$(curl -sS -o "$BODY_FILE" -w '%{http_code}' \
        --connect-timeout 3 --max-time 8 "$URL" 2>"$ERR_FILE")"
    CURL_RC=$?
    [[ -n "$HTTP_CODE" ]] || HTTP_CODE="000"

    echo "curl 返回码: $CURL_RC"
    echo "HTTP 状态码: $HTTP_CODE"

    if (( CURL_RC == 0 )); then
        case "$HTTP_CODE" in
            2*) echo "结果: HTTP 服务正常" ;;
            3*) echo "结果: 服务可访问，但发生重定向" ;;
            4*) echo "结果: 网络可达，但请求或接口可能有问题" ;;
            5*) echo "结果: 服务端内部错误" ;;
            *)  echo "结果: 已连接，但 HTTP 状态异常" ;;
        esac
    else
        echo "结果: HTTP 连接失败"
        sed 's/^/  /' "$ERR_FILE"
    fi

    echo
    echo "========== 报告结束 =========="
} | tee "$REPORT"

echo "报告已保存到: $REPORT"
```

赋予执行权限并运行：

```bash
chmod +x probe_service.sh
sudo ./probe_service.sh 127.0.0.1 8080 http://127.0.0.1:8080/
```

### 7. 报告文件

| 文件 | 说明 |
|---|---|
| `connectivity_report_20260816_073746.txt` | 按日期和时间命名的连通性报告示例 |
| `connectivity_report_*.txt` | 查看当前目录下所有报告 |
| `cat connectivity_report_*.txt` | 查看报告内容 |
| `pwd` | 确认报告所在目录 |

脚本中的 `mktemp` 只创建临时文件，脚本退出时会由 `trap` 删除，不会留下额外的 `.txt` 文件。

### 8. 是否需要两台虚拟机

| 场景 | 是否需要两台虚拟机 | 说明 |
|---|---|---|
| 本机启动服务并本机探测 | 不需要 | 在同一台 CentOS 虚拟机开两个终端即可 |
| 探测另一台服务器 | 需要另一台可访问的主机 | `ss` 在服务端执行，`curl` 可从客户端执行 |
| 模拟 client/server 网络 | 可选 | 为练习远程访问时使用两台虚拟机 |

### 9. 易错点

- `surl` 是拼写错误，正确命令是 `curl`。
- 服务监听在 `8080` 时，脚本不能默认检查 `8000`；主机、端口和 URL 必须一致。
- `curl` 报“拒绝连接”通常表示端口没有监听，不是 `/health` 路径本身的问题。
- Python `http.server` 默认没有 `/health` 接口，测试时优先使用 `/`。
- 启动 Python 服务的终端必须保持运行；如果立刻回到命令提示符，应先检查启动报错。
- `127.0.0.1` 只表示当前机器，不能用它探测另一台虚拟机。
- 远程探测时，服务端要确认 `sshd`、服务监听地址和防火墙配置。
- 报告文件生成在执行脚本时的当前目录，不一定在脚本文件所在目录。

### 10. 今日流程速记

**确认实际端口 -> 启动服务 -> `ss` 查看 LISTEN -> 用相同端口执行 `curl` -> 脚本生成连通性报告 -> 根据返回码定位问题。**

## 2026-08-17｜CentOS 镜像源、防火墙与服务端口

### 1. 任务目标

配置国内软件镜像源，开放业务端口，并确认服务可以访问，模拟上线前准备。

### 2. CentOS 命令对应关系

| 文档中的工具 | CentOS 中的工具 | 说明 |
|---|---|---|
| `apt` | `dnf` / `yum` | CentOS 使用它们安装和更新软件 |
| `ufw` | `firewalld` | CentOS 默认使用的防火墙 |
| `pip` | `pip` | Python 软件包工具，仍然可以使用 |

图片中的内容是命令执行结果，不是新的操作指令。

### 3. 配置 pip 国内镜像

| 目的 | 命令 | 说明 |
|---|---|---|
| 安装 pip | `sudo dnf install -y python3-pip` | CentOS 7 可使用 `yum` |
| 配置清华源 | `python3 -m pip config set --user global.index-url https://pypi.tuna.tsinghua.edu.cn/simple` | 以后安装 Python 包更快 |
| 查看配置 | `python3 -m pip config list` | 确认镜像地址是否生效 |
| 临时使用镜像 | `python3 -m pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple` | 只对本次安装生效 |

### 4. 配置 dnf/yum 国内镜像

| 目的 | 命令 | 说明 |
|---|---|---|
| 备份仓库配置 | `sudo cp -a /etc/yum.repos.d /etc/yum.repos.d.backup` | 修改前先留一份备份 |
| 清理缓存 | `sudo dnf clean all` | 删除旧的缓存信息 |
| 重新生成缓存 | `sudo dnf makecache` | 检查镜像是否能访问 |
| 查看仓库 | `dnf repolist` | 确认软件源已启用 |

CentOS 7/8 已停止维护，不能随意使用其他版本的仓库文件。应下载与系统版本匹配的国内镜像配置。

### 5. 开放 8080 端口

| 目的 | 命令 | 说明 |
|---|---|---|
| 启动防火墙 | `sudo systemctl enable --now firewalld` | 启动并设置开机自启 |
| 开放端口 | `sudo firewall-cmd --permanent --add-port=8080/tcp` | `--` 是两个短横线 |
| 重新加载规则 | `sudo firewall-cmd --reload` | 让新规则生效 |
| 查看已开放端口 | `sudo firewall-cmd --list-ports` | 应看到 `8080/tcp` |

防火墙开放端口，只表示允许访问；它不会自动启动业务程序。

### 6. 查看端口和服务

| 目的 | 命令 | 说明 |
|---|---|---|
| 查看全部监听端口 | `sudo ss -lntp` | 查看 TCP 监听端口和对应进程 |
| 检查 8080 | `sudo ss -lntp \| grep 8080` | 没有输出表示没有服务监听 |
| 测试本机服务 | `curl http://127.0.0.1:8080` | 测试 HTTP 服务是否能访问 |

本次检查结果中：

- `0.0.0.0:22` 和 `[::]:22` 是 SSH，表示 SSH 正在监听。
- `127.0.0.1:631` 和 `[::1]:631` 是 CUPS，只允许本机访问。
- `8080` 没有 `LISTEN`，所以 `curl` 会提示“拒绝连接”。

### 7. 启动测试服务

如果只是练习端口，可以运行：

```bash
mkdir -p ~/test-web
echo "CentOS service is running" > ~/test-web/index.html
cd ~/test-web
python3 -m http.server 8080 --bind 0.0.0.0
```

另开一个终端检查：

```bash
sudo ss -lntp | grep 8080
curl http://127.0.0.1:8080
```

### 8. 易错点

- 正确写法是 `--add-port=8080/tcp`，少一个短横线会报参数错误。
- 防火墙显示 `8080/tcp`，不代表 8080 已经有程序运行。
- `curl` 拒绝连接，先用 `ss` 检查端口是否有 `LISTEN`。
- 远程访问时，程序应监听 `0.0.0.0:8080`，不能只监听 `127.0.0.1:8080`。
- 远程修改防火墙前，先确保 SSH 的 `22` 端口可以使用。
- CentOS 使用 `dnf/yum + firewalld`，不是 Ubuntu 常用的 `apt + ufw`。

### 9. 今日流程速记

**配置 pip/dnf 镜像 -> 启动 firewalld -> 开放 8080 -> 用 `ss` 检查监听 -> 启动服务 -> 用 `curl` 测试。**

## 2026-08-18｜Python 基础与图片数据准备

### 1. 基础类型和类型转换

| 类型 / 写法 | 初学者理解 | 示例 |
|---|---|---|
| `int` | 整数 | `age = 18` |
| `float` | 小数 | `score = 95.5` |
| `str` | 文字 | `name = "cat"` |
| `bool` | 真或假 | `is_ok = True` |
| `None` | 暂时没有值 | `result = None` |
| 类型转换 | 把数据转换成另一种类型 | `int("10")`、`str(10)` |

### 2. 常用数据结构

| 结构 | 初学者理解 | 常用写法 |
|---|---|---|
| `list` | 有顺序、可以修改的一组数据 | `images = ["a.jpg", "b.jpg"]` |
| `tuple` | 有顺序、通常不修改的数据 | `size = (640, 480)` |
| `dict` | 用“键:值”保存数据 | `{"label": "cat", "width": 640}` |
| `set` | 自动去重的数据集合 | `set(["cat", "cat", "dog"])` |
| 切片 | 取出一部分数据 | `images[0:2]` |
| 列表推导式 | 用一行代码生成列表 | `[x * 2 for x in numbers]` |

### 3. 控制流

| 语法 | 作用 | 注意事项 |
|---|---|---|
| `if / elif / else` | 根据条件选择执行内容 | 条件后面要写冒号，注意缩进 |
| `for` | 依次处理一组数据 | 适合遍历列表和文件 |
| `while` | 条件满足时重复执行 | 要注意不要造成死循环 |
| `enumerate` | 遍历时同时得到编号 | `for i, item in enumerate(items)` |
| `zip` | 同时遍历多个列表 | 两个列表长度不同时要小心 |
| `break` | 立即结束循环 | 只结束当前循环 |
| `continue` | 跳过本次循环 | 继续执行下一次循环 |
| `pass` | 暂时不执行任何操作 | 常用于先占一个位置 |

### 4. Python 为什么常用于 AI

- 语法比较简单，初学者容易上手。
- 有大量现成的库，例如 `NumPy`、`Pandas`、`PyTorch`。
- 可以快速完成数据处理、模型训练和结果分析。
- 社区资料多，遇到问题比较容易找到答案。

### 5. 图片数据准备流程

任务目标：批量分类图片、重新命名，并生成标注清单。

| 步骤 | 命令 / 做法 | 说明 |
|---|---|---|
| 创建虚拟环境 | `python3 -m venv .venv` | 为项目单独准备 Python 环境 |
| 激活环境 | `source .venv/bin/activate` | 后续命令使用这个环境 |
| 安装 Pillow | `python -m pip install Pillow` | 读取图片尺寸和检查图片 |
| 准备原图 | `raw/cat/a.jpg` | 第一级目录名作为分类标签 |
| 先预览 | `python3 prepare_dataset.py --input ./raw --output ./dataset --mode copy --dry-run` | 只查看结果，不修改文件 |
| 正式处理 | `python3 prepare_dataset.py --input ./raw --output ./dataset --mode copy` | 复制图片并重新命名 |

输出内容：

```text
dataset/images/cat/cat_000001.jpg
dataset/annotations.csv
dataset/annotations.json
```

标注清单可以记录文件名、分类、宽度、高度、文件大小和 SHA-256 值。

### 6. 易错点

- 字符串和数字不能直接相加，需要先进行类型转换。
- Python 使用缩进表示代码层级，缩进不一致会报错。
- 列表下标从 `0` 开始，切片结束位置通常不包含在结果中。
- `while` 循环必须保证条件最终会变成假。
- 运行脚本时要确认使用的是同一个 Python 环境。
- Pillow 没有安装时，图片状态可能显示为 `[not_checked]`。
- `--dry-run` 只预览，不会真正复制或移动图片。
- 默认使用 `copy` 比 `move` 更安全，可以保留原始图片。

### 7. 今日流程速记

**认识数据类型 -> 学习数据结构 -> 使用条件和循环 -> 安装 Python/Pillow -> 预览图片处理结果 -> 批量分类重命名 -> 生成 CSV/JSON 标注清单。**

## 2026-08-19｜Python 基础、JSON 推理结果与格式化报表

### 1. 函数和作用域

| 理论要点 | 我的理解 | 为什么重要 / 用在哪 | 易错点 |
|---|---|---|---|
| 参数和返回值 | 参数是输入，`return` 是输出。 | 把重复代码写成函数，方便反复使用。 | 忘记写 `return`，函数就不会返回想要的结果。 |
| `*args` 和 `**kwargs` | `*args` 接收多个普通参数，`**kwargs` 接收多个键值参数。 | 参数数量不固定时使用。 | `args` 和 `kwargs` 的顺序不能写错。 |
| `lambda` | 一种很短的匿名函数。 | 适合写简单的一行计算。 | 逻辑复杂时不要强行使用。 |
| LEGB 作用域 | Python 查找变量的顺序是：局部、外层、全局、内置。 | 帮助判断变量到底来自哪里。 | 函数里的局部变量不能直接代替外部变量。 |

### 2. 模块、包和标准库

| 理论要点 | 我的理解 | 为什么重要 / 用在哪 | 易错点 |
|---|---|---|---|
| `import` / `from ... import` | 用来使用其他 Python 文件或库。 | 可以直接使用已经写好的功能。 | 模块名写错，或当前目录不正确。 |
| `__name__ == "__main__"` | 只有直接运行这个文件时，里面的代码才执行。 | 让文件既能被导入，也能单独运行。 | 字符串必须写成 `"__main__"`。 |
| `__init__.py` | 表示一个目录可以作为 Python 包使用。 | 方便组织多个模块。 | 导入路径和目录层级要对应。 |
| `os`、`sys`、`json`、`pathlib`、`subprocess` | 分别用于系统操作、程序参数、JSON、路径和执行命令。 | CentOS 上做文件处理和运行命令时很常用。 | 路径写错，或命令失败后没有检查返回结果。 |

### 3. 读取 JSON 并生成报表

目标流程：

```text
模型推理输出 -> inference.json -> Python 读取 -> 整理字段 -> report.md
```

| 操作 | 示例 | 说明 |
|---|---|---|
| 安装 Python | `sudo dnf install -y python3` | CentOS 7 可使用 `yum`。 |
| 查看 JSON | `jq . inference.json` | 检查 JSON 是否写对。 |
| 检查 JSON | `jq empty inference.json` | 没有输出通常表示格式正确。 |
| 运行整理脚本 | `python3 report.py inference.json report.md` | 把推理结果整理成 Markdown 报表。 |
| 查看报表 | `cat report.md` | 在终端查看生成内容。 |

常见 JSON 字段：

```json
{
  "model": "resnet50",
  "status": "success",
  "results": [
    {"label": "cat", "score": 0.9821}
  ]
}
```

### 4. 文件操作

| 理论要点 | 我的理解 | 为什么重要 / 用在哪 | 易错点 |
|---|---|---|---|
| `open()` | 用来打开文件。 | 读取 JSON 或写入报表。 | 文件路径不对会报错。 |
| `r` / `w` / `a` | `r` 读取，`w` 覆盖写入，`a` 追加写入。 | 控制文件打开方式。 | `w` 会覆盖原来的内容。 |
| `with open(...)` | 使用完文件后自动关闭。 | 更安全，推荐使用。 | 编码建议写成 `encoding="utf-8"`。 |
| JSON/YAML | JSON 适合程序交换数据，YAML 更适合人阅读配置。 | 保存模型输出、配置和报表数据。 | JSON 的双引号、逗号和括号必须正确。 |

### 5. 易错点和排查方法

- 先用 `pwd` 确认当前目录，再检查输入文件是否存在。
- JSON 报错时，先执行 `jq empty 文件名.json`。
- `report.py` 找不到文件时，检查输入路径和文件名拼写。
- CentOS 8/9 通常使用 `dnf`，CentOS 7 通常使用 `yum`。
- 报表脚本只负责读取和整理，不会自动产生模型推理结果。
- 需要定时生成报表时，可以使用 `crontab` 定期运行脚本。

### 6. 今日流程速记

**学习函数和模块 -> 使用标准库 -> 读取 JSON -> 整理推理结果 -> 生成 Markdown 报表 -> 检查文件和 JSON 格式。**

## 2026-08-20｜requests 调用 AI 接口、异常处理与进度条

### 1. Python 虚拟环境和依赖

| 理论要点 | 我的理解（概念） | 为什么需要 / 用在哪里 | 易错点 / 我踩过的坑 |
|---|---|---|---|
| `venv` 虚拟环境 | 给当前项目单独准备一个 Python 环境。 | 不同项目使用不同版本的库，避免互相影响。 | 使用前要先执行 `source .venv/bin/activate`，否则可能找不到已安装的库。 |
| `pip` 安装依赖 | 用 `pip` 安装 Python 第三方库。 | 安装 `requests`、`tqdm` 等工具。 | 要确认包装在当前虚拟环境中，可以用 `python -m pip` 安装。 |
| `requests` 和 `tqdm` | `requests` 用来调用 HTTP 接口，`tqdm` 用来显示进度。 | 批量调用 AI 推理服务时，可以看到处理到第几条。 | `requests` 和 `tqdm` 没安装时，运行程序会报 `ModuleNotFoundError`。 |

### 2. 使用 requests 调用 AI 接口

| 理论要点 | 我的理解（概念） | 为什么需要 / 用在哪里 | 易错点 / 我踩过的坑 |
|---|---|---|---|
| 请求地址和请求体 | 请求地址告诉程序调用哪个接口，请求体保存模型和问题。 | 调用 AI 推理接口并提交文本。 | 地址必须写完整，模型名称和字段名要符合接口要求。 |
| 请求头和 API Key | 请求头说明数据格式，API Key 用来验证身份。 | 访问需要鉴权的 AI 服务。 | API Key 不要直接写进代码，建议使用环境变量。 |
| `response.json()` | 把接口返回的 JSON 文字转换成 Python 数据。 | 读取模型回答和状态信息。 | 返回内容不是合法 JSON 时会解析失败，要做好异常处理。 |
| `response.raise_for_status()` | HTTP 状态码出错时主动抛出异常。 | 及时发现 `401`、`404`、`500` 等问题。 | 只打印响应而不检查状态码，容易忽略接口调用失败。 |

### 3. 异常处理和重试

| 理论要点 | 我的理解（概念） | 为什么需要 / 用在哪里 | 易错点 / 我踩过的坑 |
|---|---|---|---|
| `try / except` | 把可能出错的代码放进 `try`，在 `except` 中处理错误。 | 网络请求失败时，避免整个批量任务直接停止。 | 不要只写空的 `except:`，否则看不到真正的错误原因。 |
| 超时和连接异常 | 请求太久没有返回，或无法连接服务器。 | 防止程序一直卡住，网络断开时可以重试。 | `timeout` 不能省略，连接超时和读取超时都要考虑。 |
| `429` 和 `5xx` 重试 | `429` 表示请求太频繁，`5xx` 通常是服务端临时错误。 | 等待一段时间后再次请求，提高任务成功率。 | 重试次数不能无限增加，等待时间也要设置上限。 |
| 单条失败继续执行 | 某一条失败时记录错误，然后处理下一条。 | 批量推理时尽量保留成功结果。 | 失败记录中要保存问题编号和错误信息，方便之后重新处理。 |

### 4. curl 测试和 HTTP 状态码

| 理论要点 | 我的理解（概念） | 为什么需要 / 用在哪里 | 易错点 / 我踩过的坑 |
|---|---|---|---|
| 先用 `curl` 测试 | 在运行 Python 前，先用命令行确认接口能不能访问。 | 区分是网络问题、地址问题，还是 Python 代码问题。 | `curl` 命令中的 URL、请求头和 JSON 内容都要写正确。 |
| `404 Not Found` | 服务器能连接上，但请求路径不存在。 | 排查接口地址是否写错。 | 不能只看服务器能访问；要检查完整路径，例如 `/chat/completions`，还要防止重复写 `/v1`。 |
| 常见状态码 | `200` 成功，`401` Key 错误，`403` 无权限，`429` 频率过高，`5xx` 服务端错误。 | 根据状态码快速判断问题位置。 | `404` 通常不是网络不通，而是 URL 路径错误。 |

### 5. 文件名和运行命令

| 理论要点 | 我的理解（概念） | 为什么需要 / 用在哪里 | 易错点 / 我踩过的坑 |
|---|---|---|---|
| Python 文件名 | 文件名中的句点要写成 `.`，例如 `ai_infer.py`。 | 运行和管理 Python 脚本。 | 把 `ai_infer.py` 误写成 `ai_infer,py` 会导致 `chmod` 找不到文件。 |
| `chmod +x` 和运行脚本 | `chmod +x` 是增加执行权限；也可以直接用 `python ai_infer.py`。 | 让脚本可以用 `./ai_infer.py` 直接运行。 | 执行前先用 `ls -l ai_infer*` 检查文件名是否正确。 |

### 6. 今日流程速记

**创建并激活虚拟环境 -> 安装 `requests` 和 `tqdm` -> 设置 API 地址和 Key -> 先用 `curl` 测试 -> Python 调接口 -> 处理异常并重试 -> 用 `tqdm` 显示进度 -> 保存成功和失败结果。**
