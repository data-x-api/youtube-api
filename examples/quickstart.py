#!/usr/bin/env python3
"""YouTube 视频搜索：取几页结果，存成 CSV（每条一行，嵌套的字段展开成 author.name 这样的列）。

    python3 quickstart.py 'meteor shower' --pages 2          # 只报价，不调用
    python3 quickstart.py 'meteor shower' --pages 2 --yes    # 真跑

接口 youtube.videos.search，$0.002 一次，出错不收费。只用 Python 标准库，3.9 以上。
"""

from __future__ import annotations

import argparse
import csv
import sys
from decimal import Decimal
from pathlib import Path

from dataxapi import Api, ApiError, need_key

SOURCE = "gh-youtube-api"
SIGN_UP = f"https://dataxapi.com/zh/signin/?button={SOURCE}"
ENDPOINT = "youtube.videos.search"
PARAM = "query"
PRICE = Decimal("0.002")  # 现价见 https://dataxapi.com/zh/apis/youtube/videos/search/?ref=gh-youtube-api


def flatten(item: dict, prefix: str = "") -> dict:
    row = {}
    for key, value in item.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict) and not prefix:
            row.update(flatten(value, name + "."))
        elif isinstance(value, list):
            row[name] = "、".join(str(v) for v in value if not isinstance(v, (dict, list)))
        elif not isinstance(value, dict):
            row[name] = value
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description="YouTube 视频搜索")
    parser.add_argument(PARAM, help="搜索词")
    parser.add_argument("--pages", type=int, default=1, help="取几页，每页一次调用")
    parser.add_argument("--out", default="youtube.csv")
    parser.add_argument("--yes", action="store_true", help="确认调用（不加只报价）")
    args = parser.parse_args()

    print(f"{args.pages} 页：最多调用 {args.pages} 次、${PRICE * args.pages}，出错不收费。")
    if not args.yes:
        print("加 --yes 真跑。")
        return
    need_key(SIGN_UP)

    api, rows, cursor = Api(SOURCE), [], None
    for page in range(args.pages):
        try:
            answer = api.call(ENDPOINT, **{PARAM: getattr(args, PARAM)}, cursor=cursor)
        except ApiError as error:
            print(f"第 {page + 1} 页没取到：{error}（出错不扣费，已取到的照常保存）", file=sys.stderr)
            break
        data = answer.get("data") or {}
        rows += [flatten(item) for item in data.get("items") or ([data["item"]] if data.get("item") else [])]
        cursor = (answer.get("page") or {}).get("next_cursor")
        if not cursor:
            break

    columns = list(dict.fromkeys(key for row in rows for key in row))
    with Path(args.out).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    print(f"写好 {args.out}：{len(rows)} 条，调用 {api.calls} 次，实际花费 ${api.charged}。")


if __name__ == "__main__":
    main()
