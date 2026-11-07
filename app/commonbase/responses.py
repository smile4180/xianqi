from flask import jsonify


def success(data=None, status=200):
    return jsonify(ok=True, data=data), status

