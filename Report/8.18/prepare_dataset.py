#!/usr/bin/env python3

from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import shutil
import sys

try:
    from PIL import Image
except ImportError:
    Image = None


IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp",
    ".gif", ".webp", ".tif", ".tiff"
}


def safe_label(name):
    """
    清理分类名称，避免目录名包含特殊字符。
    """
    name = re.sub(r"[^\w.-]+", "_", name, flags=re.UNICODE)
    name = name.strip("._")
    return name or "uncategorized"


def calculate_sha256(path):
    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def inspect_image(path):
    """
    返回图片宽度、高度和状态。
    """
    if Image is None:
        return None, None, "not_checked"

    try:
        with Image.open(path) as image:
            image.verify()

        with Image.open(path) as image:
            width, height = image.size

        return width, height, "ok"

    except Exception as error:
        return None, None, f"unreadable:{type(error).__name__}"


def main():
    parser = argparse.ArgumentParser(
        description="批量分类、重命名图片并生成标注清单"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="原始图片目录"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="输出数据集目录"
    )

    parser.add_argument(
        "--mode",
        choices=["copy", "move"],
        default="copy",
        help="copy 保留原图，move 移动原图，默认 copy"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览操作，不复制或移动文件"
    )

    args = parser.parse_args()

    input_dir = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"输入目录不存在：{input_dir}", file=sys.stderr)
        sys.exit(1)

    # 防止输出目录位于输入目录中，导致重复扫描
    try:
        output_dir.relative_to(input_dir)
        print("错误：输出目录不能位于输入目录内部。", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        pass

    files = sorted(
        path for path in input_dir.rglob("*")
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not files:
        print("没有找到支持的图片文件。")
        sys.exit(0)

    counters = {}
    records = []

    for source in files:
        relative_path = source.relative_to(input_dir)

        # 使用原始图片的第一级父目录作为分类名称
        if len(relative_path.parts) >= 2:
            label = safe_label(relative_path.parts[0])
        else:
            label = "uncategorized"

        counters.setdefault(label, 0)
        counters[label] += 1

        extension = source.suffix.lower()
        number = counters[label]

        destination_dir = output_dir / "images" / label

        # 避免覆盖已经存在的文件
        while True:
            filename = f"{label}_{number:06d}{extension}"
            destination = destination_dir / filename

            if not destination.exists():
                break

            number += 1
            counters[label] = number

        width, height, status = inspect_image(source)
        file_size = source.stat().st_size
        sha256 = calculate_sha256(source)

        record = {
            "id": len(records) + 1,
            "source_file": str(source),
            "relative_source": relative_path.as_posix(),
            "output_file": destination.relative_to(output_dir).as_posix(),
            "label": label,
            "width": width,
            "height": height,
            "bytes": file_size,
            "sha256": sha256,
            "status": status
        }

        records.append(record)

        print(
            f"[{record['id']:06d}] "
            f"{relative_path} -> {record['output_file']} "
            f"[{status}]"
        )

        if not args.dry_run:
            destination_dir.mkdir(parents=True, exist_ok=True)

            if args.mode == "copy":
                shutil.copy2(source, destination)
            else:
                shutil.move(str(source), str(destination))

    if args.dry_run:
        print("\n预览完成，没有修改任何文件。")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "annotations.csv"
    json_path = output_dir / "annotations.json"

    csv_fields = [
        "id",
        "source_file",
        "relative_source",
        "output_file",
        "label",
        "width",
        "height",
        "bytes",
        "sha256",
        "status"
    ]

    # utf-8-sig 方便使用 Excel 打开中文
    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(records)

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)

    print("\n处理完成。")
    print(f"图片目录：{output_dir / 'images'}")
    print(f"CSV 标注：{csv_path}")
    print(f"JSON 标注：{json_path}")
    print(f"图片数量：{len(records)}")


if __name__ == "__main__":
    main()
