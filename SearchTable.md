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
