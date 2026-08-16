# Day 7 CentOS 镜像源、防火墙与服务端口准备笔记

日期：2026-08-17  
学习环境：CentOS / Bash  
学习主题：`pip` 国内镜像、`dnf/yum` 软件源、`firewalld`、`ss` 和 `curl`

## 一、今天的目标

今天学习如何在 CentOS 中完成上线前的基础准备：

1. 配置 Python 国内镜像源
2. 认识 CentOS 中 `apt` 和 `ufw` 的替代工具
3. 使用 `firewalld` 开放业务端口
4. 用 `ss` 判断端口是否真的有服务监听
5. 用 `curl` 测试服务是否可以访问
6. 理解“防火墙已开放，但连接仍被拒绝”的原因

## 二、整体思路

```text
确认系统 -> 配置镜像源 -> 开放防火墙端口 -> 启动业务服务 -> ss 检查监听 -> curl 测试
```

一句话总结：

**防火墙负责放行，业务程序负责监听；两者都正常，服务才能访问。**

## 三、CentOS 中的工具对应关系

| 其他系统常用工具 | CentOS 中的工具 | 作用 |
|---|---|---|
| `apt` | `dnf` / `yum` | 安装、更新和删除软件 |
| `ufw` | `firewalld` | 管理防火墙和开放端口 |
| `pip` | `pip` | 安装 Python 软件包 |

图片或文档中的内容是学习目标或命令执行结果，不是必须原样执行的命令。使用 CentOS 时，应使用 CentOS 对应的工具。

## 四、配置 pip 国内镜像源

先安装 pip：

```bash
sudo dnf install -y python3-pip
```

CentOS 7 可以使用：

```bash
sudo yum install -y python3-pip
```

配置清华源：

```bash
python3 -m pip config set --user \
  global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

查看配置：

```bash
python3 -m pip config list
```

测试安装：

```bash
python3 -m pip install requests
```

如果只想临时使用镜像，可以写成：

```bash
python3 -m pip install flask \
  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 五、配置 dnf/yum 软件源

修改软件源前先备份：

```bash
sudo cp -a /etc/yum.repos.d \
  /etc/yum.repos.d.backup
```

刷新软件源缓存：

```bash
sudo dnf clean all
sudo dnf makecache
```

查看可用仓库：

```bash
dnf repolist
```

CentOS 7、CentOS 8 和 CentOS Stream 9 的仓库地址不同，不能混用仓库文件。CentOS 7/8 已停止维护，生产环境应使用仍受支持的系统和匹配版本的软件源。

## 六、使用 firewalld 开放端口

启动防火墙并设置开机自启：

```bash
sudo systemctl enable --now firewalld
```

开放 `8080` 端口：

```bash
sudo firewall-cmd --permanent --add-port=8080/tcp
```

重新加载规则：

```bash
sudo firewall-cmd --reload
```

查看已经开放的端口：

```bash
sudo firewall-cmd --list-ports
```

如果看到下面内容，说明防火墙已经允许访问：

```text
8080/tcp
```

注意：防火墙开放端口，不等于端口上已经有程序运行。

## 七、使用 ss 查看端口监听

查看全部监听端口：

```bash
sudo ss -lntp
```

参数含义：

| 参数 | 含义 |
|---|---|
| `-l` | 只显示监听状态 |
| `-n` | 用数字显示地址和端口 |
| `-t` | 只查看 TCP |
| `-p` | 显示对应进程 |

只检查 `8080`：

```bash
sudo ss -lntp | grep 8080
```

本次检查结果中：

| 监听地址 | 服务 | 含义 |
|---|---|---|
| `0.0.0.0:22`、`[::]:22` | `sshd` | SSH 正在监听所有网卡 |
| `127.0.0.1:631`、`[::1]:631` | `cupsd` | CUPS 只允许本机访问 |
| 没有 `8080` | 无 | 8080 没有程序监听 |

如果 `grep 8080` 没有输出，说明服务还没有启动，或者实际使用的是其他端口。

## 八、使用 curl 测试服务

测试本机的 `8080` 服务：

```bash
curl http://127.0.0.1:8080
```

如果出现：

```text
Failed to connect to 127.0.0.1 port 8080: 拒绝连接
```

通常表示 `8080` 没有程序监听。此时先执行：

```bash
sudo ss -lntp | grep 8080
```

不要只重复修改防火墙规则，因为问题可能是业务程序没有启动。

## 九、启动一个临时测试服务

如果暂时没有真正的业务服务，可以用 Python 做测试：

```bash
mkdir -p ~/test-web
echo "CentOS service is running" > ~/test-web/index.html
cd ~/test-web
python3 -m http.server 8080 --bind 0.0.0.0
```

然后打开另一个终端检查：

```bash
sudo ss -lntp | grep 8080
curl http://127.0.0.1:8080
```

如果能看到 `CentOS service is running`，说明端口监听和 HTTP 访问都正常。

这个 Python 服务只适合练习，不适合直接作为生产服务。测试结束后，可以在运行服务的终端按 `Ctrl+C` 停止它。

## 十、问题排查顺序

| 现象 | 先检查什么 | 可能原因 |
|---|---|---|
| `firewall-cmd` 参数错误 | 检查命令中的短横线 | `--add-port` 少写了一个 `-` |
| 防火墙显示 `8080/tcp` | 执行 `ss -lntp` | 只说明防火墙放行，不说明服务已启动 |
| `ss` 没有 8080 | 检查应用启动状态和配置 | 服务没启动或端口写错 |
| `curl` 拒绝连接 | 先检查 `ss` | 目标端口没有监听 |
| 本机可以访问，远程不行 | 检查监听地址和云安全组 | 只监听了 `127.0.0.1`，或外部防火墙未放行 |

排查流程：

```text
先看 ss 是否有 LISTEN -> 再看端口是否正确 -> 再用 curl 测试 -> 最后检查防火墙和远程网络
```

## 十一、远程访问时的注意事项

远程修改防火墙前，先确认 SSH 端口仍然开放：

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

如果业务服务要被其他机器访问，程序应监听：

```text
0.0.0.0:8080
```

而不是只监听：

```text
127.0.0.1:8080
```

云服务器还需要在安全组中开放相同端口。CUPS 的 `631` 端口一般不建议直接暴露到公网。

## 十二、今天学到的命令

| 命令 | 用途 |
|---|---|
| `python3 -m pip config set` | 配置 pip 镜像源 |
| `dnf clean all` | 清理软件源缓存 |
| `dnf makecache` | 重新生成软件源缓存 |
| `firewall-cmd --add-port` | 开放防火墙端口 |
| `firewall-cmd --reload` | 重新加载防火墙规则 |
| `ss -lntp` | 查看监听端口和进程 |
| `curl` | 测试 HTTP 服务 |
| `python3 -m http.server` | 启动临时 HTTP 测试服务 |

## 十三、易错点

1. 正确写法是 `--add-port=8080/tcp`，少一个短横线会报参数错误。
2. 防火墙开放 `8080`，不代表 8080 已经有服务运行。
3. `ss` 没有显示 `LISTEN` 时，`curl` 通常会提示“拒绝连接”。
4. 远程访问时，服务不能只监听 `127.0.0.1`。
5. CentOS 使用 `dnf/yum + firewalld`，不是 Ubuntu 常用的 `apt + ufw`。
6. 修改远程服务器防火墙前，要先确认 SSH 的 `22` 端口可以使用。
7. 软件源配置必须和 CentOS 版本匹配，不能直接混用不同版本的仓库文件。

## 十四、今日总结

今天明白了上线前准备的三个关键点：

1. 镜像源解决软件下载速度问题；
2. 防火墙决定端口是否允许访问；
3. 业务程序决定端口上是否真的有服务。

**判断服务是否正常，不能只看防火墙规则，还要用 `ss` 确认端口监听，再用 `curl` 验证实际访问。**

