#!/usr/bin/env python3

import json
import sys
from datetime import datetime


def escape_md(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_report(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = [
        "# 推理结果报表",
        "",
        f"- 报表生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]

    if isinstance(data, dict):
        for key in ["model", "task", "timestamp", "status", "summary"]:
            if key in data:
                lines.append(f"- {key}：{escape_md(data[key])}")

        lines.append("")

        rows = None
        row_name = None

        for key in ["results", "predictions", "outputs", "items", "data"]:
            if isinstance(data.get(key), list):
                rows = data[key]
                row_name = key
                break

        if rows is not None and rows:
            lines.append(f"## {row_name}")
            lines.append("")

            if all(isinstance(row, dict) for row in rows):
                columns = []
                for row in rows:
                    for key in row.keys():
                        if key not in columns:
                            columns.append(key)

                lines.append("| " + " | ".join(columns) + " |")
                lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

                for row in rows:
                    values = [
                        escape_md(row.get(column, ""))
                        for column in columns
                    ]
                    lines.append("| " + " | ".join(values) + " |")
            else:
                for index, row in enumerate(rows, 1):
                    lines.append(f"{index}. {escape_md(row)}")
        else:
            lines.extend([
                "## 原始 JSON",
                "",
                "```json",
                json.dumps(data, ensure_ascii=False, indent=2),
                "```"
            ])

    elif isinstance(data, list):
        lines.append("## 推理结果")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(data, ensure_ascii=False, indent=2))
        lines.append("```")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"报表已生成：{output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python3 report.py 输入JSON 输出报表")
        sys.exit(1)

    format_report(sys.argv[1], sys.argv[2])
