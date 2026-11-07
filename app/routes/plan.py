from flask import Blueprint, request

from app.commonbase.responses import success
from app.commonbase.validation import json_object
from app.services.planstats import service

bp = Blueprint("plan", __name__, url_prefix="/api")


@bp.route("/plans/generate", methods=["POST"])
def generate_plan():
    return success(service.generate_plan(json_object()), status=201)


@bp.route("/plans/current", methods=["GET"])
def get_current_plan():
    return success(service.get_current_plan())


@bp.route("/plans/<int(min=1):plan_id>/entries", methods=["GET"])
def list_entries(plan_id):
    return success(service.list_entries(plan_id))


@bp.route("/plans/entries/<int(min=1):entry_id>/action", methods=["POST"])
def process_entry(entry_id):
    return success(service.process_entry(entry_id, json_object()))


@bp.route("/plans/<int(min=1):plan_id>/reschedule", methods=["POST"])
def reschedule_plan(plan_id):
    return success(service.reschedule_plan(plan_id))


@bp.route("/summary", methods=["GET"])
def get_summary():
    return success(service.get_summary())


@bp.route("/stats", methods=["GET"])
def get_stats():
    return success(service.get_stats(request.args.to_dict()))
