# Day 10 requests 调用 AI 接口、异常处理与进度条笔记

日期：2026-08-20  
学习环境：CentOS Stream 9 / Python / Bash  
学习主题：使用 requests 调用 AI 推理接口、处理异常、使用 tqdm 显示进度和排查 HTTP 404

## 一、今天的目标

今天学习使用 Python 调用 AI 推理接口，并完成批量处理任务：

1. 创建 Python 虚拟环境并安装依赖；
2. 使用 `requests` 发送 HTTP 请求；
3. 使用环境变量保存接口地址、模型名和 API Key；
4. 使用 `try / except` 处理请求异常；
5. 对超时、限流和服务端错误进行重试；
6. 使用 `tqdm` 显示批量推理进度；
7. 使用 `curl` 测试接口并排查 `404` 错误。

## 二、整体思路

```text
创建虚拟环境 -> 安装 requests/tqdm -> 配置接口信息 -> curl 测试 -> Python 调用接口 -> 处理异常和重试 -> 保存结果
```

一句话总结：

**先确认接口地址可以访问，再用 Python 批量调用，并把成功和失败结果都保存下来。**

## 三、创建虚拟环境和安装依赖

### 1. 创建并激活虚拟环境

```bash
mkdir -p ~/ai_requests_demo
cd ~/ai_requests_demo

python3 -m venv .venv
source .venv/bin/activate
```

命令行前出现 `(.venv)`，说明虚拟环境已经激活。

### 2. 安装 Python 库

```bash
python -m pip install --upgrade pip
python -m pip install requests tqdm
```

检查是否安装成功：

```bash
python -c "import requests, tqdm; print('依赖安装成功')"
```

### 3. 常见概念

| 内容 | 初学者理解 | 作用 |
|---|---|---|
| 虚拟环境 | 给一个项目单独准备的 Python 环境 | 防止不同项目的依赖互相影响 |
| `pip` | Python 的软件包安装工具 | 安装 `requests`、`tqdm` 等库 |
| `requests` | 发送 HTTP 请求的库 | 调用 AI 接口 |
| `tqdm` | 显示循环进度的库 | 查看批量任务完成情况 |

## 四、配置 AI 接口信息

不建议把 API Key 直接写在 Python 文件中，可以使用环境变量：

```bash
export AI_API_URL="https://api.example.com/v1/chat/completions"
export AI_API_KEY="你的_API_KEY"
export AI_MODEL="你的模型名称"
```

查看变量：

```bash
echo "$AI_API_URL"
echo "$AI_MODEL"
```

Python 中读取环境变量：

```python
import os

api_url = os.getenv("AI_API_URL")
api_key = os.getenv("AI_API_KEY")
model = os.getenv("AI_MODEL", "default-model")
```

如果变量没有设置，程序应当先提示错误，而不是继续发送空请求。

## 五、使用 requests 调用接口

### 1. 基本请求示例

OpenAI 兼容接口通常可以这样调用：

```python
import requests

url = "https://api.example.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
}
payload = {
    "model": "your-model",
    "messages": [
        {"role": "user", "content": "你好，请介绍一下自己。"}
    ],
    "temperature": 0.2,
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=(10, 120),
)
response.raise_for_status()
data = response.json()
print(data)
```

### 2. 请求中的主要内容

| 内容 | 初学者理解 | 作用 |
|---|---|---|
| URL | 接口地址 | 告诉程序请求哪个服务 |
| `headers` | 请求说明和身份信息 | 设置 JSON 格式和 API Key |
| `payload` | 要提交的数据 | 保存模型名称、问题和参数 |
| `timeout` | 最长等待时间 | 防止程序一直卡住 |
| `response.json()` | 读取 JSON 返回值 | 获取模型回答 |
| `raise_for_status()` | 检查 HTTP 状态码 | 发现 `401`、`404`、`500` 等错误 |

## 六、异常处理和重试

### 1. 常见异常

| 异常或状态 | 初学者理解 | 处理方式 |
|---|---|---|
| `Timeout` | 等待服务器太久 | 等待后重试，设置最大重试次数 |
| `ConnectionError` | 无法连接服务器 | 检查网络、地址和端口后重试 |
| `401` | API Key 错误或缺失 | 检查环境变量和鉴权信息 |
| `404` | 请求路径不存在 | 检查完整 URL 和接口版本 |
| `429` | 请求太频繁 | 根据 `Retry-After` 等待后重试 |
| `5xx` | 服务端临时错误 | 等待后重试，并记录错误 |
| JSON 解析错误 | 返回内容不是合法 JSON | 保存响应内容，检查接口格式 |

### 2. 基本异常处理写法

```python
import requests

try:
    response = requests.post(url, headers=headers, json=payload, timeout=(10, 120))
    response.raise_for_status()
    result = response.json()
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.ConnectionError:
    print("网络连接失败")
except requests.exceptions.HTTPError as exc:
    print(f"HTTP 请求失败：{exc}")
except ValueError:
    print("接口返回的内容不是合法 JSON")
except requests.exceptions.RequestException as exc:
    print(f"请求出现其他异常：{exc}")
```

### 3. 为什么要重试

网络偶尔会断开，服务端也可能暂时繁忙。对 `429` 和 `5xx` 进行有限次数重试，可以提高批量任务的成功率。

简单的等待方式：

```python
import time

for attempt in range(1, 4):
    try:
        # 发送请求
        break
    except requests.exceptions.RequestException:
        if attempt == 3:
            raise
        time.sleep(2 ** (attempt - 1))
```

这里的等待时间会逐渐增加，叫作指数退避。

## 七、使用 tqdm 显示批量进度

准备 `prompts.txt`，每行写一个问题：

```text
请介绍一下昇腾 AI 处理器。
什么是深度学习？
请解释 Transformer 的基本原理。
```

基本写法：

```python
from tqdm import tqdm

prompts = ["问题一", "问题二", "问题三"]

for prompt in tqdm(prompts, desc="AI 推理进度", unit="条"):
    print(prompt)
```

运行时可能看到：

```text
AI 推理进度: 100%|██████████| 3/3 [00:08<00:00, 2.65s/条]
```

如果还想显示成功和失败数量，可以使用：

```python
progress.set_postfix(success=success_count, failed=failed_count)
```

## 八、批量推理结果保存

建议使用 JSON Lines 格式，每完成一条就写入一行：

```python
import json

record = {
    "index": 1,
    "prompt": "你好",
    "success": True,
    "answer": "你好，我是一个 AI 助手。",
}

with open("results.jsonl", "a", encoding="utf-8") as file:
    file.write(json.dumps(record, ensure_ascii=False) + "\n")
```

这种方式的好处是：即使程序中途停止，已经完成的结果也不会全部丢失。

失败结果也应该保存：

```json
{"index": 2, "prompt": "问题二", "success": false, "error": "请求超时"}
```

## 九、使用 curl 先测试接口

运行 Python 程序前，先用 `curl` 测试接口，可以快速判断地址、网络和 API Key 是否正确：

```bash
curl -i -sS "$AI_API_URL" \
  -H "Authorization: Bearer $AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"$AI_MODEL"'",
    "messages": [
      {"role": "user", "content": "你好，请简单介绍一下自己。"}
    ],
    "temperature": 0.2
  }'
```

常见状态码：

| 状态码 | 含义 | 常见原因 |
|---|---|---|
| `200` | 请求成功 | 地址、参数和 Key 基本正确 |
| `401` | 没有通过认证 | API Key 错误或没有发送 |
| `403` | 没有权限 | 账号或接口权限不足 |
| `404` | 找不到请求路径 | URL 写错或接口路径不对 |
| `429` | 请求过于频繁 | 超过服务商的访问限制 |
| `500` | 服务端内部错误 | 服务暂时异常 |

## 十、HTTP 404 错误排查

如果返回：

```text
HTTP/2 404
```

通常说明：服务器已经连接成功，但请求路径不存在。这一般不是网络不通，而是 URL 写错。

### 1. 检查当前接口地址

```bash
echo "$AI_API_URL"
python -c "import os; print(repr(os.getenv('AI_API_URL')))"
```

### 2. 检查完整路径

例如某些 OpenAI 兼容服务使用：

```text
https://api.example.com/v1/chat/completions
```

不能只写：

```text
https://api.example.com
```

也要注意不要重复拼接 `/v1`：

```text
错误：.../v1/v1/chat/completions
```

如果使用 DeepSeek 官方接口，常见地址是：

```bash
export AI_API_URL="https://api.deepseek.com/chat/completions"
export AI_MODEL="deepseek-chat"
```

实际地址仍然要以所使用服务的官方文档为准。

## 十一、文件名和运行命令排错

今天还遇到了一个文件名错误：

```bash
vi ai_infer,py
chmod +x ai_infer.py
```

这里把英文句点 `.` 写成了逗号 `,`，所以系统找不到 `ai_infer.py`。

检查并修复：

```bash
ls -l ai_infer*
mv -i ai_infer,py ai_infer.py
chmod +x ai_infer.py
```

也可以直接使用 Python 运行，不一定需要执行权限：

```bash
python ai_infer.py --input prompts.txt --output results.jsonl
```

## 十二、常见问题排查

| 现象 | 可能原因 | 处理方法 |
|---|---|---|
| `ModuleNotFoundError` | 依赖没有安装，或没有激活虚拟环境 | `source .venv/bin/activate` 后重新安装 |
| `No such file or directory` | 文件名或路径写错 | 使用 `pwd`、`ls -l` 检查 |
| `401` | API Key 不正确 | 检查 `AI_API_KEY` 环境变量 |
| `404` | 接口 URL 路径错误 | 检查完整 URL，避免重复 `/v1` |
| `Connection refused` | 目标端口没有服务监听 | 使用 `ss -lntp` 检查服务端口 |
| 请求一直等待 | 没有设置超时 | 在 `requests.post()` 中设置 `timeout` |
| 进度条不显示 | 没有把循环对象传给 `tqdm` | 使用 `for item in tqdm(items):` |
| 任务中途停止后结果全丢 | 最后才统一写文件 | 每完成一条就写入并 `flush()` |

## 十三、今天学到的命令和写法

| 命令 / 写法 | 用途 |
|---|---|
| `python3 -m venv .venv` | 创建虚拟环境 |
| `source .venv/bin/activate` | 激活虚拟环境 |
| `python -m pip install requests tqdm` | 安装依赖 |
| `os.getenv("AI_API_URL")` | 读取环境变量 |
| `requests.post(...)` | 发送 POST 请求 |
| `timeout=(10, 120)` | 设置连接和读取超时 |
| `response.raise_for_status()` | 检查 HTTP 错误 |
| `response.json()` | 读取 JSON 响应 |
| `tqdm(items)` | 显示循环进度 |
| `curl -i -sS URL` | 测试 HTTP 接口 |
| `echo "$AI_API_URL"` | 查看接口地址 |
| `ls -l ai_infer*` | 检查脚本文件名 |

## 十四、易错点

1. 使用 Python 前要先激活正确的虚拟环境。
2. `requests` 请求要设置超时，不能让程序无限等待。
3. API Key 建议放到环境变量中，不要直接写入代码或提交到仓库。
4. `404` 说明路径不存在，重点检查完整 URL，而不是只检查网络。
5. `429`、`500`、`502`、`503`、`504` 可以有限重试，但不能无限重试。
6. 文件名中的句点是 `.`，`ai_infer.py` 不能写成 `ai_infer,py`。
7. `chmod +x` 只负责增加执行权限，使用 `python ai_infer.py` 时可以不执行它。
8. 批量任务要保存成功和失败结果，不能因为一条失败就停止全部任务。
9. `tqdm` 只负责显示进度，不负责自动处理请求错误。
10. 使用 `curl` 测试成功后，再运行 Python 程序，更容易定位问题。

## 十五、今日总结

今天学习了如何在 CentOS 中使用虚拟环境安装 `requests` 和 `tqdm`，并用 Python 调用 AI 推理接口。通过 `try / except`、超时设置和有限重试，可以让批量请求更加稳定；通过 `tqdm` 可以直观看到任务进度；通过 `curl` 和 HTTP 状态码可以快速排查接口问题。

**先检查环境和接口地址，再发送请求；请求失败要记录和重试，批量结果要及时保存。**
