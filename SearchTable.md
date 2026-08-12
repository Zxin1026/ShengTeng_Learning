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
