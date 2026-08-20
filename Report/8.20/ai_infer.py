#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import requests
from tqdm import tqdm


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def extract_text(data):
    """
    解析 OpenAI 兼容接口返回结果。
    可根据实际接口格式进行修改。
    """

    # OpenAI Chat Completions 格式
    try:
        content = data["choices"][0]["message"]["content"]

        if isinstance(content, str):
            return content

        # 部分模型返回内容块列表
        if isinstance(content, list):
            result = []
            for item in content:
                if isinstance(item, dict):
                    result.append(item.get("text", ""))
                else:
                    result.append(str(item))
            return "".join(result)

    except (KeyError, IndexError, TypeError):
        pass

    # 某些接口直接返回 output_text
    if isinstance(data, dict) and "output_text" in data:
        return str(data["output_text"])

    # 无法识别时，保留完整 JSON
    return json.dumps(data, ensure_ascii=False)


def call_api(
    session,
    api_url,
    api_key,
    model,
    prompt,
    max_retries=3
):
    """
    调用 AI 接口，并处理超时、网络异常、限流和服务端异常。
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # OpenAI 兼容格式
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
    }

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = session.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=(10, 120)
            )

            status_code = response.status_code

            # 限流或服务端临时错误，允许重试
            if status_code == 429 or 500 <= status_code <= 599:
                if attempt == max_retries:
                    response.raise_for_status()

                retry_after = response.headers.get("Retry-After")

                try:
                    wait_seconds = int(float(retry_after))
                except (TypeError, ValueError):
                    wait_seconds = 2 ** (attempt - 1)

                wait_seconds = min(max(wait_seconds, 1), 60)

                logging.warning(
                    "接口返回 %s，第 %s/%s 次重试，等待 %s 秒",
                    status_code,
                    attempt,
                    max_retries,
                    wait_seconds
                )

                time.sleep(wait_seconds)
                continue

            # 其他 4xx 错误通常属于参数、权限或地址错误，不重复请求
            response.raise_for_status()

            try:
                result = response.json()
            except ValueError as exc:
                raise RuntimeError(
                    f"接口返回内容不是合法 JSON：{response.text[:500]}"
                ) from exc

            return extract_text(result), result

        except requests.exceptions.Timeout as exc:
            last_error = exc

            if attempt == max_retries:
                break

            wait_seconds = 2 ** (attempt - 1)

            logging.warning(
                "请求超时，第 %s/%s 次重试，等待 %s 秒",
                attempt,
                max_retries,
                wait_seconds
            )

            time.sleep(wait_seconds)

        except requests.exceptions.ConnectionError as exc:
            last_error = exc

            if attempt == max_retries:
                break

            wait_seconds = 2 ** (attempt - 1)

            logging.warning(
                "网络连接失败，第 %s/%s 次重试，等待 %s 秒",
                attempt,
                max_retries,
                wait_seconds
            )

            time.sleep(wait_seconds)

        except requests.exceptions.HTTPError as exc:
            response_text = ""

            if exc.response is not None:
                response_text = exc.response.text[:500]

            raise RuntimeError(
                f"HTTP 请求失败：{exc}，响应内容：{response_text}"
            ) from exc

        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"请求异常：{exc}") from exc

    raise RuntimeError(
        f"请求失败，已重试 {max_retries} 次：{last_error}"
    )


def load_prompts(input_file):
    """
    读取文本文件，每行一个问题。
    忽略空行。
    """

    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(f"输入文件不存在：{input_file}")

    prompts = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            prompt = line.strip()

            if prompt:
                prompts.append(prompt)

    if not prompts:
        raise ValueError("输入文件中没有有效问题")

    return prompts


def main():
    parser = argparse.ArgumentParser(
        description="使用 requests 调用 AI 推理接口"
    )

    parser.add_argument(
        "--input",
        default="prompts.txt",
        help="输入文件，每行一个问题"
    )

    parser.add_argument(
        "--output",
        default="results.jsonl",
        help="输出文件，默认 results.jsonl"
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="单个请求最大重试次数"
    )

    args = parser.parse_args()

    api_url = os.getenv("AI_API_URL")
    api_key = os.getenv("AI_API_KEY")
    model = os.getenv("AI_MODEL", "default-model")

    if not api_url:
        logging.error("没有设置 AI_API_URL")
        sys.exit(1)

    if not api_key:
        logging.error("没有设置 AI_API_KEY")
        sys.exit(1)

    prompts = load_prompts(args.input)

    session = requests.Session()

    output_path = Path(args.output)

    success_count = 0
    failed_count = 0

    with output_path.open("w", encoding="utf-8") as output_file:
        progress = tqdm(
            prompts,
            total=len(prompts),
            desc="AI 推理进度",
            unit="条"
        )

        for index, prompt in enumerate(progress, start=1):
            record = {
                "index": index,
                "prompt": prompt,
            }

            try:
                answer, raw_response = call_api(
                    session=session,
                    api_url=api_url,
                    api_key=api_key,
                    model=model,
                    prompt=prompt,
                    max_retries=args.max_retries
                )

                record["success"] = True
                record["answer"] = answer
                record["response"] = raw_response

                success_count += 1

            except Exception as exc:
                logging.error(
                    "第 %s 条推理失败：%s",
                    index,
                    exc
                )

                # 单条失败不影响后续任务
                record["success"] = False
                record["error"] = str(exc)

                failed_count += 1

            output_file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            # 每完成一条立即保存，程序中断时不会丢失全部结果
            output_file.flush()

            progress.set_postfix(
                success=success_count,
                failed=failed_count
            )

    logging.info(
        "任务完成：成功 %s 条，失败 %s 条，结果文件：%s",
        success_count,
        failed_count,
        output_path
    )


if __name__ == "__main__":
    main()
