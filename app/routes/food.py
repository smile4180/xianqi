from flask import Blueprint, request

from app.commonbase.responses import success
from app.commonbase.validation import json_object
from app.services.foodstock import service

bp = Blueprint("food", __name__, url_prefix="/api")


@bp.route("/food/items", methods=["GET"])
def list_items():
    return success(service.list_items(request.args.to_dict()))


@bp.route("/food/items", methods=["POST"])
def create_item():
    return success(service.create_item(json_object()), status=201)


@bp.route("/food/items/<int(min=1):item_id>", methods=["GET"])
def get_item(item_id):
    return success(service.get_item(item_id))


@bp.route("/food/items/<int(min=1):item_id>", methods=["PUT"])
def update_item(item_id):
    return success(service.update_item(item_id, json_object()))


@bp.route("/food/items/<int(min=1):item_id>/open", methods=["POST"])
def open_item(item_id):
    return success(service.open_item(item_id, json_object()))


@bp.route("/food/items/<int(min=1):item_id>/process", methods=["POST"])
def process_item(item_id):
    return success(service.process_item(item_id, json_object()))
