"""业务日期可固定，实际提交时间始终取真实时钟。"""
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import current_app, g, has_request_context


def now():
    return datetime.now(ZoneInfo(current_app.config["TIMEZONE"])).strftime("%Y-%m-%d %H:%M:%S")


def today():
    if has_request_context() and "calculation_date" in g:
        return g.calculation_date
    value = current_app.config.get("DEMO_DATE") or now()[:10]
    if has_request_context():
        g.calculation_date = value
    return value

