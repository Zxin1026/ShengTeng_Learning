# Day 12 Docker 生命周期、exec 与 CPU 推理容器笔记

日期：2026-08-22  
学习环境：CentOS Stream 9 / Docker 29.7.2 / Docker Compose 5.5.0 / Bash  
学习主题：Docker 生命周期、`docker exec`、运行参数、目录挂载和 CPU 推理容器

## 一、今天的目标

今天在已经安装 Docker 的 CentOS Stream 9 环境中，完成一个简单的容器内推理案例：

1. 检查 Docker 服务、镜像和容器状态；
2. 理解 `run`、`start`、`stop`、`restart`、`rm` 和 `ps` 的作用；
3. 理解 `-d`、`--name`、`-v` 和 `-it` 等常用参数；
4. 创建一个简单的 Python 推理脚本；
5. 启动一个 CPU 模式的 Python 容器；
6. 使用 `docker exec` 进入运行中的容器；
7. 在容器内执行 Python 推理脚本并查看 JSON 输出；
8. 理解容器与宿主机在文件、网络和进程方面的边界。

本次不使用 GPU，也不使用 `--gpus all`，只验证 Docker 和 Python 容器的基本流程。

## 二、整体思路

```text
确认 Docker 环境 -> 查看已有镜像 -> 编写 Python 脚本 -> 启动 CPU 容器 -> 查看容器状态 -> exec 进入容器 -> 执行推理脚本 -> 查看输出
```

一句话总结：

**先用镜像启动一个保持运行的容器，再用 `docker exec` 进入容器执行 Python 推理。**

## 三、Docker 环境检查

### 1. 查看系统和 Docker 版本

```bash
cat /etc/centos-release
uname -m
command -v docker
docker --version
docker compose version
```

本次检查结果：

| 检查项目 | 结果 | 我的理解 |
|---|---|---|
| 系统 | CentOS Stream 9 | 符合本次实验环境 |
| 架构 | `x86_64` | 常见的 64 位服务器架构 |
| Docker 路径 | `/usr/bin/docker` | Docker 命令已经安装 |
| Docker 版本 | `29.7.2` | Docker 客户端可以使用 |
| Compose 版本 | `v5.5.0` | Compose 插件已经安装 |

### 2. 查看 Docker 服务

```bash
systemctl is-enabled docker
systemctl is-active docker
```

输出：

```text
enabled
active
```

`enabled` 表示 Docker 开机自动启动，`active` 表示当前服务正在运行。

### 3. 查看 Docker 信息

```bash
docker info
```

本次环境的重要信息：

| 项目 | 结果 |
|---|---|
| Server Version | `29.7.2` |
| Operating System | `CentOS Stream 9` |
| Architecture | `x86_64` |
| CPU | 2 个 |
| 内存 | 约 3.5 GiB |
| Images | 6 个 |
| Containers | 0 个 |
| Default Runtime | `runc` |

虽然 `docker info` 中可以看到 `nvidia` runtime，但本次不使用 GPU。默认运行时是 `runc`，后面的命令也不添加 `--gpus all`。

### 4. 查看本地镜像

```bash
docker image ls
```

本次已经存在的镜像包括：

```text
hello-world:latest
python:3.12-slim-bookworm
python:3.9-slim-bookworm
my-pytorch:2.4.1
pytorch/pytorch:2.4.1-cuda12.1-cudnn9-runtime
nvidia/cuda:12.4.1-base-ubuntu22.04
```

查看容器：

```bash
docker ps
docker ps -a
```

开始操作前没有正在运行或已经停止的容器，因此新建 `python-infer-cpu` 容器进行练习。

## 四、Docker 生命周期命令

| 命令 | 初学者理解 | 使用场景 |
|---|---|---|
| `docker run` | 根据镜像创建并启动新容器 | 第一次运行应用 |
| `docker start` | 启动已经停止的容器 | 重复使用旧容器 |
| `docker stop` | 停止正在运行的容器 | 暂停服务 |
| `docker restart` | 停止后重新启动容器 | 服务异常或配置改变后 |
| `docker rm` | 删除容器 | 清理不用的容器 |
| `docker ps` | 查看运行中的容器 | 确认容器是否为 `Up` |
| `docker ps -a` | 查看所有容器 | 查找已经退出的容器 |
| `docker logs` | 查看容器输出 | 排查程序启动失败 |
| `docker exec` | 在运行中的容器内执行命令 | 进入容器或运行脚本 |

常用示例：

```bash
docker ps
docker ps -a
docker stop python-infer-cpu
docker start python-infer-cpu
docker restart python-infer-cpu
docker logs python-infer-cpu
docker rm python-infer-cpu
```

易错点：

- `docker ps` 默认只显示运行中的容器；
- `docker exec` 只能操作运行中的容器；
- 容器停止后可以用 `docker start` 再次启动；
- 运行中的容器不能直接删除，通常先停止，或者使用 `docker rm -f`；
- 删除容器不等于删除镜像。

## 五、`docker run` 常用参数

| 参数 | 初学者理解 | 示例 |
|---|---|---|
| `-d` | 让容器在后台运行 | `docker run -d ...` |
| `--name` | 给容器设置容易记的名字 | `--name python-infer-cpu` |
| `-p` | 映射端口，格式为“主机端口:容器端口” | `-p 8080:8080` |
| `-v` | 挂载目录，格式为“主机目录:容器目录” | `-v "$HOME/docker-infer-cpu:/app:Z"` |
| `-it` | 分配终端并允许交互操作 | `docker exec -it 容器名 sh` |
| `--rm` | 运行结束后自动删除容器 | `docker run --rm hello-world` |
| `--restart unless-stopped` | Docker 重启后自动恢复容器 | 后台服务常用 |

参数之间的区别：

- `-d` 主要用于后台运行；
- `-it` 主要用于进入交互式终端；
- `-p` 只在容器提供网络服务时使用；
- `-v` 用于共享代码、模型或数据；
- `--name` 让后续的 `ps`、`exec`、`logs` 命令更容易书写。

## 六、创建 Python 推理脚本

### 1. 创建目录

```bash
mkdir -p "$HOME/docker-infer-cpu"
cd "$HOME/docker-infer-cpu"
```

### 2. 编写 `infer.py`

```bash
vi infer.py
```

写入以下内容：

```python
import argparse
import json


def predict(text):
    text_lower = text.lower()

    if any(word in text_lower for word in ["good", "great", "excellent", "好", "优秀"]):
        label = "positive"
    else:
        label = "neutral"

    return {
        "input": text,
        "label": label,
        "device": "cpu"
    }


parser = argparse.ArgumentParser()
parser.add_argument("--text", required=True)
args = parser.parse_args()

print(json.dumps(predict(args.text), ensure_ascii=False))
```

这个脚本不依赖 PyTorch，只用于验证容器、Python 和 `exec` 流程。它接收 `--text` 参数，根据文字返回一个简单的分类结果，并明确标记使用 `cpu`。

## 七、启动 CPU 推理容器

```bash
docker run -d \
  --name python-infer-cpu \
  --restart unless-stopped \
  -v "$HOME/docker-infer-cpu:/app:Z" \
  python:3.12-slim-bookworm \
  python -c 'import time; time.sleep(10**9)'
```

命令说明：

| 内容 | 作用 |
|---|---|
| `-d` | 后台启动容器 |
| `--name python-infer-cpu` | 设置容器名称 |
| `--restart unless-stopped` | Docker 重启后自动启动 |
| `-v "$HOME/docker-infer-cpu:/app:Z"` | 把宿主机脚本目录挂载到容器的 `/app` |
| `python:3.12-slim-bookworm` | 使用已有的 Python 3.12 镜像 |
| `python -c 'import time; ...'` | 让容器主进程保持运行，方便后续 `exec` |

本次没有使用：

```bash
--gpus all
```

因此容器按 CPU 模式运行。

## 八、查看容器运行状态

```bash
docker ps --filter name=python-infer-cpu
```

预期看到类似结果：

```text
CONTAINER ID   IMAGE                        COMMAND                  STATUS       NAMES
xxxxxxxxxxxx   python:3.12-slim-bookworm   "python -c import..."   Up ...       python-infer-cpu
```

这张终端截图可以作为“容器正在运行”的实验结果。

也可以查看更详细的状态：

```bash
docker inspect python-infer-cpu \
  --format 'Status={{.State.Status}} Image={{.Config.Image}}'
```

如果输出：

```text
Status=running Image=python:3.12-slim-bookworm
```

说明容器正在运行。

## 九、使用 `docker exec` 进入容器

### 1. 进入交互式 shell

```bash
docker exec -it python-infer-cpu sh
```

进入容器后可以执行：

```bash
python --version
ls -l /app
```

预期可以看到 Python 版本和挂载进来的 `infer.py` 文件。

### 2. 在容器内执行推理

```bash
/usr/local/bin/python /app/infer.py \
  --text "CPU Docker inference test"
```

预期输出：

```json
{"input": "CPU Docker inference test", "label": "neutral", "device": "cpu"}
```

如果输入带有 `good`、`great` 或“好”等词，结果会变成 `positive`：

```bash
/usr/local/bin/python /app/infer.py \
  --text "This is a great test"
```

退出容器：

```bash
exit
```

### 3. 不进入 shell，直接执行命令

```bash
docker exec python-infer-cpu \
  /usr/local/bin/python /app/infer.py \
  --text "CPU Docker inference test"
```

`-it` 适合进入交互式终端；直接执行一次性命令时可以不加 `-it`。

## 十、这次遇到的参数错误

执行命令时出现过：

```text
infer.py: error: unrecognized arguments: /app/infer.py
```

这表示脚本收到了重复的 `/app/infer.py` 参数，常见原因是 `python` 命令被设置成别名，或者命令被重复粘贴。

检查命令来源：

```bash
type python
command -v python
```

可以使用 Python 的绝对路径绕过别名：

```bash
/usr/local/bin/python /app/infer.py \
  --text "CPU Docker inference test"
```

还要注意，终端中的 `#` 是 shell 提示符，不要把它作为命令的一部分输入。

## 十一、容器与宿主机的边界

| 内容 | 初学者理解 | 易错点 |
|---|---|---|
| 文件系统 | 容器有自己的文件系统，只有挂载目录才能和主机共享 | 容器删除后，未挂载的数据可能丢失 |
| 目录挂载 | `-v 主机目录:容器目录` 可以共享代码和数据 | 主机路径和容器路径容易写反 |
| 网络 | 容器有自己的网络，使用 `-p` 才能把服务端口暴露给主机 | 容器里的 `localhost` 指的是容器自己 |
| 进程 | 容器中的进程和宿主机进程相互隔离 | `docker exec` 执行的是容器内命令 |
| 权限 | 容器内外用户和文件权限可能不同 | CentOS 使用 SELinux 时目录挂载通常加 `:Z` |

本次通过：

```bash
-v "$HOME/docker-infer-cpu:/app:Z"
```

让宿主机的 `infer.py` 出现在容器的 `/app/infer.py` 中。修改宿主机文件后，容器内可以直接看到修改结果。

## 十二、生成实验结果

### 1. 查看容器运行截图

```bash
docker ps --filter name=python-infer-cpu
```

截图中应包含容器名称 `python-infer-cpu` 和 `Up` 状态。

### 2. 查看推理输出截图

```bash
docker exec python-infer-cpu \
  /usr/local/bin/python /app/infer.py \
  --text "CPU Docker inference test"
```

截图中应包含 JSON 推理结果和 `"device": "cpu"`。

### 3. 一次性保存结果

```bash
{
  echo "===== Container Status ====="
  docker ps --filter name=python-infer-cpu
  echo "===== Inference Output ====="
  docker exec python-infer-cpu \
    /usr/local/bin/python /app/infer.py \
    --text "CPU Docker inference test"
} | tee docker-infer-result.txt
```

## 十三、常见问题排查

| 现象 | 可能原因 | 处理方法 |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker 服务没有启动 | `sudo systemctl enable --now docker` |
| 普通用户 `permission denied` | 没有加入 `docker` 组 | `sudo usermod -aG docker "$USER"` 后重新登录 |
| `docker exec` 提示容器未运行 | 容器状态是 `Exited` | `docker ps -a`、`docker logs python-infer-cpu`、`docker start python-infer-cpu` |
| 找不到 `/app/infer.py` | 挂载路径写错或文件不在主机目录 | 检查 `pwd`、`ls -l "$HOME/docker-infer-cpu"` 和 `ls -l /app` |
| `unrecognized arguments: /app/infer.py` | `python` 命令被重复传参或设置了别名 | 使用 `/usr/local/bin/python /app/infer.py ...` |
| 挂载目录权限错误 | SELinux 标签或权限问题 | CentOS 挂载时添加 `:Z`，并检查目录权限 |
| 容器一启动就退出 | 主进程结束 | 查看 `docker logs`，让主进程保持运行 |
| 推理没有输出 | 脚本没有执行到 `print`，或命令没有真正回车 | 用 `sed -n '1,120p' /app/infer.py` 检查脚本 |

## 十四、清理容器

停止容器：

```bash
docker stop python-infer-cpu
```

删除容器：

```bash
docker rm python-infer-cpu
```

宿主机的脚本仍保存在：

```text
$HOME/docker-infer-cpu/infer.py
```

这是因为脚本目录使用了 `-v` 挂载，容器删除不会删除宿主机上的脚本。

## 十五、易错点

1. `docker ps` 默认只显示运行中的容器，查看停止容器要使用 `docker ps -a`。
2. `docker exec` 只能进入运行中的容器。
3. `docker run` 是创建并启动新容器，`docker start` 只启动已有容器。
4. `-p` 是端口映射，`-v` 是目录挂载，两者作用不同。
5. `-v` 的路径格式是“主机目录:容器目录”，不要写反。
6. CentOS 开启 SELinux 时，目录挂载通常需要添加 `:Z`。
7. 容器里的 `localhost` 指向容器本身，不一定是宿主机。
8. 本次只使用 CPU，不要添加 `--gpus all`，也不需要执行 `nvidia-smi`。
9. `python --version` 在宿主机和容器内可能不同，要分别检查。
10. `#` 是终端提示符，不要把它和命令一起复制执行。

## 十六、今天的总结

今天学习了 Docker 容器的基本生命周期，知道了镜像、容器和正在运行的进程之间的关系。通过 `docker run -d` 启动了一个后台运行的 Python 容器，再使用 `docker ps` 查看容器状态，并用 `docker exec -it` 进入容器执行 Python 脚本。

通过 `-v` 挂载目录后，宿主机中的 `infer.py` 可以在容器的 `/app` 目录中使用。推理脚本返回了 JSON 格式的结果，并明确显示使用的是 CPU。本次没有使用 GPU，也没有添加 `--gpus all`。

**先确认 Docker 环境 -> 启动 CPU 容器 -> 查看 `Up` 状态 -> 用 `exec` 进入容器 -> 执行 Python 推理 -> 查看 JSON 输出。**
