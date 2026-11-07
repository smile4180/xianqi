from flask import Blueprint, request

from app.commonbase.responses import success
from app.commonbase.validation import json_object
from app.services.remindercenter import service

bp = Blueprint("reminder", __name__, url_prefix="/api")


@bp.route("/reminders", methods=["GET"])
def list_reminders():
    return success(service.list_reminders(request.args.to_dict()))


@bp.route("/reminders/<int(min=1):reminder_id>/action", methods=["POST"])
def process_reminder(reminder_id):
    return success(service.process_reminder(reminder_id, json_object()))


@bp.route("/reminder/preferences", methods=["GET"])
def get_preferences():
    return success(service.get_preferences())


@bp.route("/reminder/preferences", methods=["PUT"])
def save_preferences():
    return success(service.save_preferences(json_object()))
