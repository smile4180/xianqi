"""Flask 应用工厂；导入不创建数据库、不启动服务器。"""
from flask import Flask

from app.commonbase import db
from app.commonbase.errors import register_error_handlers
from app.routes import register_routes
from config import load_config


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(load_config())
    if test_config:
        app.config.update(test_config)
    app.json.ensure_ascii = False
    db.init_app(app)
    register_error_handlers(app)
    register_routes(app)
    return app

