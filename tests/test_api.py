import json
import re
from pathlib import Path

import pytest

from app.commonbase.db import TABLES, get_db

CONTRACTS = json.loads((Path(__file__).resolve().parents[1] / "docs/api-routes.json").read_text(encoding="utf-8"))


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json["data"]
    assert data["calculation_date"] == "2026-11-04"
    assert data["business_modules_implemented"] is False
    assert data["schema_version"] == 1


@pytest.mark.parametrize("contract", CONTRACTS, ids=lambda c: f'{c["method"]} {c["path"]}')
def test_all_business_routes_fail_explicitly_without_writes(app, client, contract):
    path = re.sub(r"\{\w+\}", "1", contract["path"])
    response = client.open(path, method=contract["method"], json={})
    assert response.status_code == 501
    assert response.json["ok"] is False
    assert response.json["error"]["error_code"] == "NOT_IMPLEMENTED"
    with app.app_context():
        for table in TABLES:
            assert get_db().execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0


@pytest.mark.parametrize("body", [[], None, "text", 3])
def test_write_body_must_be_object(client, body):
    response = client.post("/api/food/items", data=json.dumps(body), content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"]["error_code"] == "VALIDATION_ERROR"


def test_protocol_errors_keep_json_envelope_and_allow_header(client):
    assert client.get("/api/missing").json["error"]["error_code"] == "NOT_FOUND"
    response = client.delete("/api/food/items")
    assert response.status_code == 405
    assert "GET" in response.headers["Allow"]
    assert response.json["ok"] is False
    assert client.post("/api/food/items", data="{").status_code == 415
    malformed = client.post("/api/food/items", data="{", content_type="application/json")
    assert malformed.status_code == 400 and malformed.is_json


def test_unexpected_errors_do_not_expose_details(app):
    @app.get("/test-error")
    def error():
        raise RuntimeError("private database details")
    response = app.test_client().get("/test-error")
    assert response.status_code == 500
    assert response.json["error"]["error_code"] == "SERVER_ERROR"
    assert "private" not in response.text

