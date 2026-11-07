from datetime import datetime

import pytest

from app.commonbase.clock import now, today
from app.commonbase.errors import ApiError
from app.commonbase.constants import ItemType
from app.commonbase.validation import validate_date, validate_date_order, validate_enum, validate_nonneg_int, validate_required
from config import load_config


def test_clock_freezes_once_per_request_but_real_time_is_separate(app):
    with app.test_request_context():
        assert today() == "2026-11-04"
        app.config["DEMO_DATE"] = "2000-01-01"
        assert today() == "2026-11-04"
        assert datetime.strptime(now(), "%Y-%m-%d %H:%M:%S").year > 2000
    with app.test_request_context():
        assert today() == "2000-01-01"


@pytest.mark.parametrize("value", [True, False, 1.5, "1", -1, 10000, None])
def test_integer_validation_rejects_non_integer_and_out_of_range(value):
    with pytest.raises(ApiError) as error:
        validate_nonneg_int(value, "quantity")
    assert error.value.field == "quantity"


def test_required_allows_zero_and_false():
    validate_required({"quantity": 0, "enabled": False}, ["quantity", "enabled"])
    with pytest.raises(ApiError):
        validate_required({"name": "   "}, ["name"])


def test_enum_accepts_raw_json_string_and_rejects_unknown_value():
    assert validate_enum("FOOD", ItemType, "item_type") == "FOOD"
    with pytest.raises(ApiError):
        validate_enum({}, ItemType, "item_type")


@pytest.mark.parametrize("value", ["2026-02-29", "20261104", "2026-1-01", "2026-11-04T00:00:00", None])
def test_invalid_dates(value):
    with pytest.raises(ApiError):
        validate_date(value, "date")


def test_date_order_allows_same_day_and_leap_day():
    validate_date("2024-02-29", "date")
    validate_date_order("2026-11-04", "2026-11-04", "start", "end")
    with pytest.raises(ApiError) as error:
        validate_date_order("2026-11-05", "2026-11-04", "start", "end")
    assert error.value.error_code == "DATE_ORDER_ERROR"


def test_environment_overrides_config(monkeypatch):
    monkeypatch.setenv("XQQJ_PORT", "5001")
    monkeypatch.setenv("XQQJ_DEMO_DATE", "2026-11-05")
    values = load_config()
    assert values["PORT"] == 5001 and values["DEMO_DATE"] == "2026-11-05"
    monkeypatch.setenv("XQQJ_DEMO_DATE", "2026-02-29")
    with pytest.raises(ValueError):
        load_config()

