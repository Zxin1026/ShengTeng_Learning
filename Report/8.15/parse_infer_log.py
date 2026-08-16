#!/usr/bin/env python3

import argparse
import csv
import json
import re
import statistics
from pathlib import Path


ACC_RE = re.compile(
    r"(?i)(?:top[-_ ]?1[-_ ]?)?"
    r"(?:accuracy|acc|精度)\s*[:=]\s*"
    r"([0-9]+(?:\.[0-9]+)?)\s*(%)?"
)

TIME_RE = re.compile(
    r"(?i)(?P<key>inference[_ -]?time|latency|"
    r"elapsed(?:[_ -]?time)?|耗时|推理时间)"
    r"(?:[_ -]?(?P<keyunit>ms|s))?\s*[:=]\s*"
    r"(?P<value>[0-9]+(?:\.[0-9]+)?)\s*"
    r"(?P<unit>ms|milliseconds|s|sec|seconds|秒)?"
)


def parse_file(path):
    accuracies = []
    latencies = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for match in ACC_RE.finditer(line):
                value = float(match.group(1))

                # 0.923 自动转换成 92.3%
                if not match.group(2) and value <= 1:
                    value *= 100

                accuracies.append(value)

            for match in TIME_RE.finditer(line):
                value = float(match.group("value"))
                unit = match.group("unit") or match.group("keyunit") or "ms"
                unit = unit.lower()

                if unit in ("s", "sec", "seconds", "秒"):
                    value *= 1000

                latencies.append(value)

    accuracy = round(statistics.mean(accuracies), 4) if accuracies else None
    latency = round(statistics.mean(latencies), 4) if latencies else None

    return accuracy, latency, len(accuracies), len(latencies)


def diagnose(accuracy, latency, acc_threshold, latency_threshold):
    problems = []

    if accuracy is None and latency is None:
        return "未匹配到精度和耗时，检查日志格式或正则表达式"

    if accuracy is None:
        problems.append("未发现精度指标")

    elif accuracy < acc_threshold:
        problems.append(
            "精度偏低：检查模型版本、权重、数据集、预处理和量化配置"
        )

    if latency is None:
        problems.append("未发现耗时指标")

    elif latency > latency_threshold:
        problems.append(
            "耗时偏高：检查Batch Size、数据搬运、线程数和设备利用率"
        )

    return "；".join(problems) if problems else "正常/待人工确认"


def collect_files(input_path):
    path = Path(input_path)

    if path.is_file():
        return [path]

    return sorted(
        p for p in path.rglob("*")
        if p.is_file() and p.suffix.lower() in (".log", ".txt")
    )


def main():
    parser = argparse.ArgumentParser(
        description="解析模型推理日志，提取精度和耗时"
    )
    parser.add_argument("--input", required=True, help="日志文件或日志目录")
    parser.add_argument("--csv", default="result.csv", help="CSV 输出文件")
    parser.add_argument("--json", default="result.json", help="JSON 输出文件")
    parser.add_argument("--acc-threshold", type=float, default=90.0)
    parser.add_argument("--latency-threshold", type=float, default=200.0)

    args = parser.parse_args()

    records = []

    for path in collect_files(args.input):
        accuracy, latency, acc_count, latency_count = parse_file(path)

        record = {
            "file": str(path),
            "accuracy_pct": accuracy,
            "latency_ms": latency,
            "accuracy_count": acc_count,
            "latency_count": latency_count,
            "diagnosis": diagnose(
                accuracy,
                latency,
                args.acc_threshold,
                args.latency_threshold,
            ),
        }

        records.append(record)

    with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys() if records else [
            "file",
            "accuracy_pct",
            "latency_ms",
            "accuracy_count",
            "latency_count",
            "diagnosis",
        ])
        writer.writeheader()
        writer.writerows(records)

    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"共处理 {len(records)} 个日志文件")
    print(f"CSV结果：{args.csv}")
    print(f"JSON结果：{args.json}")

    for record in records:
        print(
            f"\n文件：{record['file']}\n"
            f"精度：{record['accuracy_pct']}%\n"
            f"耗时：{record['latency_ms']} ms\n"
            f"结论：{record['diagnosis']}"
        )


if __name__ == "__main__":
    main()
