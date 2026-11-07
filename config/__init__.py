"""默认配置 < 本机 TOML < 环境变量。"""
import os
import re
import tomllib
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
KEYS = {"database", "host", "port", "timezone", "demo_date"}


def load_config():
    values = {}
    for name in ("default.toml", "local.toml"):
        path = ROOT / "config" / name
        if path.exists():
            with path.open("rb") as file:
                content = tomllib.load(file)
            unknown = content.keys() - KEYS
            if unknown:
                raise ValueError(f"未知配置项: {sorted(unknown)}")
            values.update(content)
    for key in KEYS:
        env = f"XQQJ_{key.upper()}"
        if env in os.environ:
            values[key] = os.environ[env]
    port = int(values["port"])
    if not 1 <= port <= 65535:
        raise ValueError("port 必须在 1—65535 之间")
    demo = values["demo_date"]
    if demo:
        if not isinstance(demo, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", demo):
            raise ValueError("demo_date 必须为 YYYY-MM-DD")
        date.fromisoformat(demo)
    ZoneInfo(values["timezone"])
    if not values["database"] or not values["host"]:
        raise ValueError("database 和 host 不能为空")
    database = Path(values["database"])
    if not database.is_absolute():
        database = ROOT / database
    return {
        "DATABASE": str(database.resolve()),
        "HOST": values["host"],
        "PORT": port,
        "TIMEZONE": values["timezone"],
        "DEMO_DATE": demo or None,
        "MAX_CONTENT_LENGTH": 1024 * 1024,
    }

