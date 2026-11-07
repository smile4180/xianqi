from flask import jsonify
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    def __init__(self, error_code, message, status=400, field=None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status = status
        self.field = field


class FeatureNotImplemented(ApiError):
    def __init__(self, feature):
        super().__init__("NOT_IMPLEMENTED", f"{feature}尚未实现", 501)


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def api_error(error):
        return jsonify(ok=False, error={
            "error_code": error.error_code,
            "message": error.message,
            "field": error.field,
        }), error.status

    @app.errorhandler(HTTPException)
    def http_error(error):
        messages = {
            400: ("VALIDATION_ERROR", "请求格式不正确"),
            404: ("NOT_FOUND", "接口或对象不存在"),
            405: ("METHOD_NOT_ALLOWED", "请求方法不支持"),
            413: ("PAYLOAD_TOO_LARGE", "请求内容过大"),
            415: ("UNSUPPORTED_MEDIA_TYPE", "请使用 application/json"),
        }
        code, message = messages.get(error.code, ("HTTP_ERROR", "请求无法处理"))
        # 保留 Allow 等 HTTP 协议头，替换默认 HTML 错误正文。
        response = error.get_response()
        response.set_data(app.json.dumps({"ok": False, "error": {
            "error_code": code, "message": message, "field": None,
        }}))
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def unexpected(error):
        app.logger.exception("Unhandled server error")
        return api_error(ApiError("SERVER_ERROR", "服务暂时不可用，请重新加载", 500))

