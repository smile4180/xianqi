from flask import Blueprint, request

from app.commonbase.responses import success
from app.services.foodstock import service

bp = Blueprint("shared_inventory", __name__, url_prefix="/api")


@bp.get("/categories")
def categories():
    return success(service.list_categories(request.args.to_dict()))


@bp.get("/items/<int(min=1):item_id>/events")
def events(item_id):
    return success(service.list_events(item_id))
