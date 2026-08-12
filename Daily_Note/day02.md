# Day 2 Linux 环境初始化笔记

日期：2026-08-12  
学习环境：Linux / Ubuntu / Debian 系  
学习主题：`init_env.sh` 环境初始化脚本

## 一、今天的目标

今天重点练习的是一键初始化 Linux 开发环境，核心内容包括：

1. 创建专用用户
2. 配置 `sudo` 权限
3. 将 `apt` 软件源切换为国内镜像
4. 让后续安装软件更稳定、更快

## 二、`init_env.sh` 的作用

`init_env.sh` 的目标不是做复杂业务，而是先把机器整理成一个适合学习和开发的状态。  
典型流程是：

```bash
useradd
passwd
usermod
visudo
sed
apt update
```

它的思路可以概括为一句话：

**先建好一个普通开发用户，再给它必要的管理员能力，最后把系统软件源调顺。**

## 三、脚本重点

### 1. 创建专用用户

专用用户的意义是把日常开发和系统管理分开，避免一直用 `root`。

常见命令：

```bash
sudo useradd -m -s /bin/bash zhangxin
sudo passwd zhangxin
```

参数说明：

- `-m`：自动创建家目录
- `-s /bin/bash`：指定登录 Shell

### 2. 配置 sudo

如果希望这个用户可以临时执行管理员命令，需要把它加入 `sudo` 组。

```bash
sudo usermod -aG sudo zhangxin
```

验证方式：

```bash
su - zhangxin
sudo whoami
```

如果输出是 `root`，说明 sudo 权限可用。

### 3. apt 换国内源

国内环境下，`apt` 默认源有时比较慢，所以常见做法是改成镜像站。

常见流程：

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo sed -i 's|http://archive.ubuntu.com/ubuntu/|https://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list
sudo apt update
```

如果是 Debian 或其他版本，源地址可能不同，需要按系统版本调整。

## 四、脚本结构理解

一个比较清晰的 `init_env.sh` 通常会分成三段：

```bash
#!/usr/bin/env bash
set -e

echo "create user"
# useradd / passwd

echo "configure sudo"
# usermod

echo "switch apt mirror"
# backup sources.list and replace mirror
```

这样的写法有两个好处：

- 出错时更容易定位
- 后面想扩展安装常用工具也方便

## 五、今天学到的命令

| 命令 | 用途 |
|---|---|
| `useradd` | 创建用户 |
| `passwd` | 设置密码 |
| `usermod -aG` | 加入用户组 |
| `visudo` | 安全编辑 sudo 配置 |
| `cp` | 备份配置文件 |
| `sed -i` | 批量替换文本 |
| `apt update` | 更新软件包索引 |
| `apt install` | 安装软件 |

## 六、易错点

1. 不要直接长期使用 `root` 登录。
2. 修改 `sources.list` 前先备份。
3. `sed` 替换时要确认系统版本和镜像地址是否匹配。
4. 加完 `sudo` 组后，通常需要重新登录用户才会生效。

## 七、今日总结

今天的重点不是记住某一条命令，而是理解 Linux 环境初始化的顺序：

**建用户 -> 给权限 -> 调软件源 -> 再开始装工具和做开发。**

这套流程以后在虚拟机、云服务器和新机器上都很常用。

