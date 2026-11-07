from flask import Blueprint, request

from app.commonbase.responses import success
from app.commonbase.validation import json_object
from app.services.riskeval import service

bp = Blueprint("risk", __name__, url_prefix="/api")


@bp.route("/risk/refresh", methods=["POST"])
def refresh_all():
    return success(service.refresh_all())


@bp.route("/risk/refresh/<int(min=1):item_id>", methods=["POST"])
def refresh_item(item_id):
    return success(service.refresh_item(item_id))


@bp.route("/risk/snapshots", methods=["GET"])
def list_snapshots():
    return success(service.list_snapshots(request.args.to_dict()))


@bp.route("/risk/snapshots/<int(min=1):item_id>", methods=["GET"])
def get_snapshot(item_id):
    return success(service.get_snapshot(item_id))


@bp.route("/risk/config", methods=["GET"])
def get_config():
    return success(service.get_config(request.args.to_dict()))


@bp.route("/risk/config", methods=["POST"])
def save_config():
    return success(service.save_config(json_object()))


@bp.route("/risk/config/preview", methods=["POST"])
def preview_config():
    return success(service.preview_config(json_object()))
