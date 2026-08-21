# Day 11 Docker 概念、安装与镜像笔记

日期：2026-08-21  
学习环境：CentOS Stream 9 / Docker / Bash  
学习主题：安装 Docker、理解镜像和容器、配置国内镜像加速器、拉取 Python/PyTorch 镜像

## 一、今天的目标

今天学习在 CentOS Stream 9 中安装和使用 Docker，并完成镜像环境准备：

1. 理解容器、镜像、仓库和 Docker C/S 架构；
2. 使用 `dnf` 安装 Docker CE；
3. 使用 `systemctl` 启动和管理 Docker 服务；
4. 区分 Docker 软件源和 Docker 镜像加速器；
5. 配置阿里云 Docker 镜像加速器；
6. 使用 `pull`、`images`、`run` 等命令管理镜像；
7. 拉取 Python/PyTorch 镜像并检查容器中的 Python 版本；
8. 排查 Docker Hub 连接失败和配置文件不存在的问题。

## 二、整体思路

```text
确认 CentOS 版本 -> 配置 Docker 软件源 -> 安装 Docker -> 启动服务 -> 配置镜像加速器 -> 拉取测试镜像 -> 拉取 Python/PyTorch 镜像 -> 运行容器验证
```

一句话总结：

**先把 Docker 服务安装并启动，再配置镜像下载地址，最后用简单容器验证环境。**

## 三、Docker 的基本概念

### 1. 容器和虚拟机

| 内容 | 初学者理解 | 作用 |
|---|---|---|
| 虚拟机 | 像一台完整的小电脑，有自己的操作系统 | 隔离性较强，但占用资源较多，启动较慢 |
| 容器 | 在宿主机中隔离出来的运行环境 | 启动快、占用资源少，适合部署程序 |
| 容器和宿主机 | 容器不是完全独立的电脑，会共享部分系统资源 | 可以快速运行相同的开发和推理环境 |

容器适合运行 Python、PyTorch 和推理服务，可以减少不同项目之间的环境冲突。

### 2. 镜像、容器和仓库

| 概念 | 初学者理解 | 示例 |
|---|---|---|
| 镜像（Image） | 可以运行程序的环境模板 | `python:3.9-slim-bookworm` |
| 容器（Container） | 镜像启动后真正运行的实例 | `docker run` 创建的运行环境 |
| 仓库（Registry） | 保存和下载镜像的地方 | Docker Hub、阿里云镜像仓库 |
| Docker 客户端 | 接收用户输入的命令 | `docker pull`、`docker run` |
| Docker 服务端（daemon） | 真正创建和管理容器的后台服务 | `dockerd` |

## 四、在 CentOS Stream 9 中安装 Docker

### 1. 检查系统版本

```bash
cat /etc/centos-release
uname -m
```

我的系统是 CentOS Stream 9，架构为 `x86_64`。

### 2. 安装基础工具

```bash
sudo dnf install -y dnf-plugins-core ca-certificates curl
```

这些工具用于添加软件源、访问 HTTPS 地址和下载软件包。

### 3. 配置 Docker 软件源

最开始访问 Docker 官方源时出现了 SSL 连接错误：

```text
Curl error (35): SSL connect error
```

因此改用阿里云 Docker 软件源：

```bash
sudo dnf config-manager --add-repo \
https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

清理并重新生成缓存：

```bash
sudo dnf clean all
sudo dnf makecache --refresh
```

### 4. 安装 Docker 软件包

```bash
sudo dnf install -y \
docker-ce \
docker-ce-cli \
containerd.io \
docker-buildx-plugin \
docker-compose-plugin
```

### 5. 启动 Docker 服务

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager
```

看到下面的内容，说明 Docker 服务已经启动：

```text
Active: active (running)
```

## 五、Docker 软件源和镜像加速器的区别

这两个配置解决的是不同问题：

| 配置 | 解决的问题 | 常见位置 |
|---|---|---|
| Docker 软件源 | 安装或更新 Docker 软件包 | `/etc/yum.repos.d/docker-ce.repo` |
| Docker 镜像加速器 | 加快 `docker pull` 下载镜像 | `/etc/docker/daemon.json` |

这次把 Docker 软件源换成阿里云，只能帮助安装 Docker，不能保证拉取 `hello-world` 时不访问 Docker Hub。

## 六、配置 Docker 镜像加速器

### 1. 创建配置目录和文件

如果执行下面命令提示文件不存在，这是正常的，说明配置文件还没有创建：

```text
/etc/docker/daemon.json: 没有那个文件或目录
```

创建目录：

```bash
sudo mkdir -p /etc/docker
```

创建配置文件：

```bash
sudo vi /etc/docker/daemon.json
```

写入阿里云控制台提供的专属镜像加速地址：

```json
{
  "registry-mirrors": [
    "https://你的专属地址.mirror.aliyuncs.com"
  ]
}
```

这里的地址需要替换成自己在阿里云容器镜像服务中获取的地址。

### 2. 检查配置并重启 Docker

```bash
sudo dockerd --validate --config-file=/etc/docker/daemon.json
sudo systemctl daemon-reload
sudo systemctl restart docker
```

查看加速器是否生效：

```bash
sudo docker info | sed -n '/Registry Mirrors:/,/Live Restore Enabled/p'
```

如果能看到 `Registry Mirrors` 和阿里云地址，说明配置已经被 Docker 读取。

## 七、验证 Docker 是否正常

### 1. 查看 Docker 版本

```bash
sudo docker version
```

### 2. 运行测试容器

```bash
sudo docker run --rm hello-world
```

第一次运行时，如果本地没有 `hello-world` 镜像，Docker 会先尝试下载：

```text
Unable to find image 'hello-world:latest' locally
```

这句话本身不是错误，只是说明本地没有这个镜像。

### 3. 本次遇到的网络错误

实际拉取时出现：

```text
failed to resolve reference "docker.io/library/hello-world:latest"
connect: connection refused
```

这说明 Docker 访问 `registry-1.docker.io` 失败。需要检查：

```bash
sudo cat /etc/docker/daemon.json
sudo docker info
sudo systemctl status docker --no-pager
sudo docker pull hello-world
```

如果 `docker info` 中没有 `Registry Mirrors`，说明镜像加速器还没有生效。

## 八、Docker 常用镜像操作

| 命令 | 初学者理解 | 作用 |
|---|---|---|
| `sudo docker pull 镜像名` | 下载镜像 | 把镜像保存到本地 |
| `sudo docker images` | 查看镜像 | 查看名称、标签、大小 |
| `sudo docker run 镜像名` | 运行容器 | 根据镜像创建并启动容器 |
| `sudo docker ps` | 查看运行中的容器 | 只显示正在运行的容器 |
| `sudo docker ps -a` | 查看所有容器 | 包括已经停止的容器 |
| `sudo docker tag 旧镜像 新镜像` | 给镜像增加一个名字 | 方便管理和使用 |
| `sudo docker rmi 镜像名` | 删除镜像 | 删除前确认没有容器正在使用 |

查看镜像：

```bash
sudo docker images
```

## 九、配置普通用户使用 Docker

默认情况下，普通用户可能没有访问 Docker 守护进程的权限：

```bash
sudo usermod -aG docker "$USER"
newgrp docker
```

然后测试：

```bash
docker ps
```

如果仍然提示权限不足，可以退出终端后重新登录，或者暂时在命令前使用 `sudo`。

## 十、宿主机 Python 和容器 Python

宿主机执行：

```bash
python --version
```

得到：

```text
Python 3.9.25
```

这只表示 CentOS 宿主机的 Python 版本。Docker 容器中的 Python 与宿主机相互独立。

### 1. 使用 Python 3.9 镜像

如果项目需要 Python 3.9，可以拉取：

```bash
sudo docker pull python:3.9-slim-bookworm
```

检查容器中的版本：

```bash
sudo docker run --rm \
python:3.9-slim-bookworm \
python --version
```

进入容器：

```bash
sudo docker run --rm -it \
python:3.9-slim-bookworm \
bash
```

### 2. 是否需要 Python 3.12

不需要因为宿主机是 Python 3.9.25，就一定拉取 Python 3.12 镜像。

| 情况 | 建议 |
|---|---|
| 项目要求 Python 3.9 | 使用 `python:3.9-slim-bookworm` |
| 项目没有固定版本 | 可以使用 Python 3.11 或 3.12 |
| 只是在宿主机使用 Python | 不需要拉取 Python 镜像 |

## 十一、PyTorch 镜像示例

可以根据项目需要拉取 PyTorch 镜像：

```bash
sudo docker pull pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime
```

检查 PyTorch 和 CUDA 是否可用：

```bash
sudo docker run --rm \
  pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime \
  python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

如果输出 `False`，不一定代表 PyTorch 安装失败，也可能是宿主机没有 NVIDIA 驱动，或者运行容器时没有配置 GPU。

## 十二、常见问题排查

| 现象 | 可能原因 | 处理方法 |
|---|---|---|
| 安装 Docker 时 SSL 连接失败 | Docker 官方源当前无法访问 | 换用阿里云 Docker 软件源后执行 `dnf clean all` 和 `dnf makecache --refresh` |
| `daemon.json` 不存在 | Docker 配置文件还没有创建 | `sudo mkdir -p /etc/docker` 后手动创建 |
| `docker pull` 仍访问 Docker Hub | 镜像加速器未配置或未生效 | 检查 `daemon.json`、重启 Docker、查看 `docker info` |
| `connect: connection refused` | 网络无法连接镜像仓库 | 检查网络、代理、加速器和 Docker 日志 |
| `Cannot connect to the Docker daemon` | Docker 服务没有启动 | `sudo systemctl enable --now docker` |
| `permission denied` | 当前用户没有 Docker 权限 | 加入 `docker` 组或暂时使用 `sudo` |
| `torch.cuda.is_available()` 为 `False` | 没有 GPU 或 GPU 运行时未配置 | 检查 `nvidia-smi`、NVIDIA Container Toolkit 和 `--gpus all` |

查看 Docker 日志：

```bash
sudo journalctl -u docker -n 50 --no-pager
```

## 十三、今天学到的命令和写法

| 命令 / 写法 | 用途 |
|---|---|
| `dnf install -y` | 安装 CentOS 软件包 |
| `dnf config-manager --add-repo` | 添加软件仓库 |
| `systemctl enable --now docker` | 启动 Docker 并设置开机启动 |
| `docker version` | 查看 Docker 版本 |
| `docker pull` | 下载镜像 |
| `docker images` | 查看本地镜像 |
| `docker run --rm` | 运行并自动清理容器 |
| `docker ps -a` | 查看所有容器 |
| `docker info` | 查看 Docker 服务和镜像加速器信息 |
| `dockerd --validate` | 检查 Docker 配置文件格式 |
| `journalctl -u docker` | 查看 Docker 服务日志 |

## 十四、易错点

1. Docker 软件源和 Docker 镜像加速器不是同一个配置。
2. 阿里云软件源可以帮助安装 Docker，但不一定自动解决 Docker Hub 镜像下载问题。
3. `/etc/docker/daemon.json` 不存在时，需要先创建目录和文件。
4. 修改 `daemon.json` 后必须重启 Docker 服务。
5. `Unable to find image locally` 只是说明本地没有镜像，不一定是报错。
6. `docker run` 会自动拉取本地不存在的镜像，所以网络不通时会失败。
7. `python --version` 查看的是宿主机 Python，容器里的版本要单独检查。
8. `docker rmi` 删除的是镜像，不是容器；正在使用的镜像不能直接删除。
9. `torch.cuda.is_available()` 为 `False` 可能是 GPU 配置问题，不一定是 PyTorch 安装失败。
10. 镜像加速器地址应使用阿里云控制台提供的专属地址，不要把示例地址直接当成自己的地址。

## 十五、今天的总结

今天学习了 Docker 的基本概念，并在 CentOS Stream 9 中安装了 Docker CE。安装过程中遇到 Docker 官方软件源 SSL 连接失败，因此切换到阿里云软件源。拉取 `hello-world` 时又发现，安装软件使用的源和拉取镜像使用的加速器是两回事；如果没有创建 `/etc/docker/daemon.json`，Docker 仍可能直接访问 Docker Hub。

还了解到宿主机的 Python 3.9.25 与 Docker 容器中的 Python 相互独立。项目需要哪个版本，就选择对应的 Python 镜像，不必因为宿主机是 3.9 就一定使用 3.12。

**先安装并启动 Docker，再单独配置镜像加速器，最后用 `hello-world` 和 Python/PyTorch 镜像验证容器环境。**
