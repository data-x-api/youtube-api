"""DataXAPI 的最小客户端：只用标准库，Python 3.9 以上。

Key 放在环境变量 DATAXAPI_API_KEY。出错不扣费；遇到限流或服务端错误自动重试一次。
每次调用实际扣了多少，累计在 Api.charged（美元）。
"""

from __future__ import annotations

import json
import os
import sys
import time
import uuid
from decimal import Decimal
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = os.environ.get("DATAXAPI_API_BASE", "https://api.dataxapi.com").rstrip("/") + "/v1/"
LIST_PARAMS = {"ids", "keywords"}  # 带这两个参数时用 POST 和 JSON 请求体


class ApiError(Exception):
    pass


class Api:
    def __init__(self, source: str, key: str | None = None):
        self.key = key if key is not None else os.environ.get("DATAXAPI_API_KEY", "")
        self.source = source
        self.calls, self.charged = 0, Decimal(0)

    def call(self, endpoint: str, **params) -> dict:
        params = {k: v for k, v in params.items() if v not in (None, "", [])}
        url = BASE + endpoint.replace(".", "/")
        headers = {
            "Authorization": f"Bearer {self.key}",
            "X-Source": self.source,
            "User-Agent": self.source,
            "Idempotency-Key": str(uuid.uuid4()),  # 重试时用同一个，保证最多扣一次
        }
        if LIST_PARAMS & params.keys():
            request = Request(url, data=json.dumps(params).encode(), headers={**headers, "Content-Type": "application/json"}, method="POST")
        else:
            request = Request(url + ("?" + urlencode(params) if params else ""), headers=headers)
        for last in (False, True):
            self.calls += 1
            try:
                with urlopen(request, timeout=120) as response:
                    body = json.load(response)
                self.charged += Decimal(str((body.get("meta") or {}).get("billing", {}).get("amount") or 0))
                return body
            except HTTPError as error:
                if not last and error.code in (429, 500, 502, 503, 504):
                    time.sleep(3)
                    continue
                try:
                    answer = json.load(error)
                    message = answer.get("message_zh") or answer.get("message")
                except ValueError:
                    message = None
                raise ApiError(message or f"HTTP {error.code}") from error
            except OSError as error:
                raise ApiError(f"连不上接口：{error}") from error
        raise AssertionError


def need_key(sign_up: str) -> None:
    if not os.environ.get("DATAXAPI_API_KEY"):
        sys.exit(f"先设置 DATAXAPI_API_KEY。还没有 Key：{sign_up}（免费试用最多 333 次，不用绑卡）")
