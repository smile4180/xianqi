from flask import Blueprint, current_app

from app.commonbase.clock import now, today
from app.commonbase.db import verify_database
from app.commonbase.responses import success

bp = Blueprint("system", __name__, url_prefix="/api")


@bp.get("/health")
def health():
    verify_database()
    return success({
        "service": "xqqj", "status": "ok", "stage": "scaffold",
        "schema_version": 1, "calculation_date": today(), "server_time": now(),
        "timezone": current_app.config["TIMEZONE"],
        "business_modules_implemented": False,
    })

