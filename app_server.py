"""本地演示服务入口。终端 Ctrl+C 停止；不启用调试器或自动重载。"""
import logging
import sqlite3

from app import create_app
from app.commonbase.db import verify_database


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    app = create_app()
    try:
        with app.app_context():
            verify_database()
    except (sqlite3.Error, RuntimeError):
        app.logger.exception("数据库无法打开。首次运行请执行 python -m flask --app app init-db；已有数据库请检查路径与备份。")
        raise SystemExit(1)
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=False, use_reloader=False)


if __name__ == "__main__":
    main()

