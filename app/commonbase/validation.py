"""通用字段校验；失败抛出带 field 的 ApiError，由路由外层统一转 JSON。"""
import re
from datetime import date

from flask import request

from app.commonbase.errors import ApiError


def invalid(field, message, code="VALIDATION_ERROR"):
    raise ApiError(code, message, field=field)


def json_object():
    value = request.get_json()
    if not isinstance(value, dict):
        invalid(None, "请求体必须是 JSON 对象")
    return value


def validate_required(data, fields):
    for field in fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            invalid(field, "此项为必填项")


def validate_nonneg_int(value, field, maximum=9999, minimum=0):
    if type(value) is not int or not minimum <= value <= maximum:
        invalid(field, f"请输入 {minimum}—{maximum} 之间的整数")
    return value


def validate_enum(value, choices, field):
    if value not in tuple(choices):
        invalid(field, "取值不在允许范围内")
    return value


def validate_text(value, field, minimum=0, maximum=120):
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        invalid(field, f"请输入 {minimum}—{maximum} 字的文本")
    return value.strip()


def validate_date(value, field):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        invalid(field, "日期格式必须为 YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError:
        invalid(field, "日期不存在")


def validate_date_order(start, end, start_field, end_field):
    if validate_date(start, start_field) > validate_date(end, end_field):
        invalid(end_field, "结束日期不能早于开始日期", "DATE_ORDER_ERROR")

