# Day 6 推理服务端口探测与连通性报告笔记

日期：2026-08-16  
学习环境：CentOS / Bash  
学习主题：`ss`、`curl`、Shell 探测脚本、端口监听和连通性报告

## 一、今天的目标

今天重点学习如何在 CentOS 中检查推理服务端口，并用脚本输出连通性报告，主要内容包括：

1. 使用 `ss -tlnp` 查看 TCP 端口是否监听
2. 使用 `curl` 测试 HTTP 服务
3. 编写带参数的端口探测脚本
4. 判断“拒绝连接”的具体原因
5. 处理 `8080` 和 `8000` 端口不一致问题
6. 生成 `connectivity_report_*.txt` 报告文件
7. 区分本机探测和远程服务器探测

## 二、整体思路

```text
确认服务端口 -> 启动推理服务 -> ss 查看 LISTEN -> curl 测试接口 -> 脚本生成报告
```

一句话总结：

**先确认端口有人监听，再用相同的主机、端口和 URL 测试服务。**

## 三、安装和检查工具

CentOS Stream 9 可以使用：

```bash
sudo dnf install -y iproute curl
```

CentOS 7 可以使用：

```bash
sudo yum install -y iproute curl
```

检查命令是否可用：

```bash
ss --version
curl --version
```

| 工具 | 作用 |
|---|---|
| `ss` | 查看网络连接和监听端口 |
| `curl` | 访问 HTTP/HTTPS 接口 |
| `iproute` | 提供 `ss` 等网络管理命令 |

## 四、使用 ss 检查端口监听

查看全部 TCP 监听端口：

```bash
sudo ss -tlnp
```

参数含义：

| 参数 | 含义 |
|---|---|
| `-t` | 只查看 TCP |
| `-l` | 只查看监听状态 |
| `-n` | 以数字显示地址和端口 |
| `-p` | 显示占用端口的进程 |

只检查 `8080` 端口：

```bash
sudo ss -tlnp | grep ':8080'
```

如果出现类似内容：

```text
LISTEN 0 128 127.0.0.1:8080 0.0.0.0:* users:(('python3',pid=1234,fd=3))
```

说明已经有程序监听 `8080`。如果没有任何输出，通常表示服务没有启动、端口配置错误，或者服务监听的是其他端口。

查看常见端口：

```bash
sudo ss -lntp | grep -E ':(8000|8080|7860|11434)\b'
```

## 五、使用 curl 测试 HTTP 服务

测试本机 `8080` 端口：

```bash
curl -i http://127.0.0.1:8080/
```

增加超时限制：

```bash
curl -i --connect-timeout 3 --max-time 8 \
  http://127.0.0.1:8080/
```

查看详细连接过程：

```bash
curl -v http://127.0.0.1:8080/
```

常见返回结果：

| 返回结果 | 含义 |
|---|---|
| `200 OK` | 服务可访问，请求成功 |
| `404 Not Found` | 网络已连通，但接口路径不存在 |
| `401` / `403` | 需要认证或没有访问权限 |
| `500` | 服务端内部错误 |
| `curl: (7) ... 拒绝连接` | 目标端口没有程序监听或服务尚未启动 |
| `Connection timed out` | 可能存在网络路由或防火墙问题 |

注意：`surl` 是拼写错误，正确命令是 `curl`。

## 六、用 Python 临时启动测试服务

如果暂时没有真正的推理服务，可以使用 Python 创建一个临时 HTTP 服务：

终端一执行：

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

正常情况下会显示：

```text
Serving HTTP on 127.0.0.1 port 8080
```

启动服务的终端必须保持运行。然后打开第二个终端执行：

```bash
sudo ss -lntp | grep ':8080'
curl -i http://127.0.0.1:8080/
```

Python 临时服务通常没有 `/health` 接口，因此测试时优先访问 `/`。访问 `/health` 可能返回 `404`，但这仍然说明 TCP 和 HTTP 服务已经连通。

## 七、端口参数必须保持一致

如果服务启动在 `8080`，脚本就必须检查 `8080`：

```bash
sudo ./probe_service.sh 127.0.0.1 8080 http://127.0.0.1:8080/
```

不能让服务运行在 `8080`，却让脚本检查 `8000`：

```text
服务端口：8080
脚本检查：8000
结果：拒绝连接
```

脚本的参数含义如下：

| 参数 | 示例 | 含义 |
|---|---|---|
| `$1` | `127.0.0.1` | 目标主机 |
| `$2` | `8080` | 目标端口 |
| `$3` | `http://127.0.0.1:8080/` | HTTP 探测 URL |

## 八、连通性探测脚本

创建脚本：

```bash
vim probe_service.sh
```

脚本内容：

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

保存后赋予执行权限：

```bash
chmod +x probe_service.sh
```

指定 `8080` 端口运行：

```bash
sudo ./probe_service.sh \
  127.0.0.1 \
  8080 \
  http://127.0.0.1:8080/
```

## 九、连通性报告文件

脚本会生成类似文件：

```text
connectivity_report_20260816_073746.txt
```

查看报告：

```bash
ls -l connectivity_report_*.txt
cat connectivity_report_*.txt
```

报告保存在执行脚本时的当前目录，可以使用下面的命令确认位置：

```bash
pwd
```

脚本中的 `mktemp` 只创建临时文件，脚本退出时会自动删除，不会留下额外的 `.txt` 文件。

## 十、拒绝连接问题排查

| 现象 | 检查命令 | 处理方式 |
|---|---|---|
| 8080 没有监听 | `sudo ss -lntp \| grep ':8080'` | 启动服务或确认实际端口 |
| 脚本检查错端口 | 查看脚本输出的“目标端口” | 传入正确的 `$2` 参数 |
| Python 服务已退出 | 查看启动终端报错 | 修正命令并保持服务运行 |
| `/health` 返回 404 | `curl -i URL` | 改用实际存在的健康检查接口 |
| 远程访问超时 | `ping IP`、检查防火墙 | 确认路由、监听地址和防火墙 |

排查顺序：

```text
先看 ss 是否有 LISTEN -> 再看端口是否正确 -> 再用 curl 测试 -> 最后检查接口路径和防火墙
```

## 十一、是否需要两台虚拟机

| 场景 | 是否需要两台虚拟机 | 说明 |
|---|---|---|
| 同一台 CentOS 启动并探测服务 | 不需要 | 开两个终端即可 |
| 探测另一台服务器 | 需要另一台可访问的主机 | 服务端运行 `ss`，客户端运行 `curl` |
| 模拟 client/server 网络 | 可选 | 适合练习远程访问和防火墙 |

`127.0.0.1` 只表示当前机器。如果推理服务运行在另一台虚拟机，应使用那台机器的实际 IP 地址。

## 十二、今天学到的命令

| 命令 | 用途 |
|---|---|
| `ss -tlnp` | 查看 TCP 监听端口和进程 |
| `curl -i` | 查看 HTTP 响应头和状态 |
| `curl -v` | 查看详细连接过程 |
| `grep` | 过滤指定端口或关键字 |
| `awk` | 从 `ss` 输出中提取字段 |
| `mktemp` | 创建临时文件 |
| `tee` | 同时显示并保存报告 |
| `trap` | 在脚本结束时执行清理操作 |

## 十三、易错点

1. `surl` 是拼写错误，正确命令是 `curl`。
2. 服务启动在 `8080` 时，脚本不能默认检查 `8000`。
3. `curl` 报“拒绝连接”通常说明目标端口没有监听。
4. Python `http.server` 默认没有 `/health` 接口，测试时应先访问 `/`。
5. 启动 Python 服务的终端必须保持运行。
6. `127.0.0.1` 只能表示本机，不能代替另一台虚拟机的 IP。
7. `curl` 返回 `404` 不等于网络不通，可能只是接口路径不存在。
8. 报告文件生成在执行脚本时的当前目录，而不是一定生成在脚本所在目录。
9. 修改脚本默认端口后，仍应使用 `ss` 确认实际监听端口。

## 十四、今日总结

**`ss` 负责确认端口是否监听，`curl` 负责确认 HTTP 服务是否可访问，Shell 脚本负责把检查结果整理成报告。**

今天还理解了“拒绝连接”的基本原因：服务未启动、端口写错、服务监听地址不正确，或者客户端和服务端并不是同一台机器。实际排查时，应先确认 `LISTEN`，再确认端口和 URL，最后检查接口路径、防火墙和远程网络。

