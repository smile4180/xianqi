"""请求级 SQLite 连接；事务由最外层调用方持有，内部调用共享连接。"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import click
from flask import current_app, g

SCHEMA_VERSION = 1
TABLES = frozenset({
    "item_batch", "category_rule", "inventory_event", "risk_snapshot", "risk_config",
    "reminder", "reminder_preference", "daily_plan", "plan_entry",
})


def connect(path, *, create=False):
    mode = "rwc" if create else "rw"
    connection = sqlite3.connect(f"{Path(path).resolve().as_uri()}?mode={mode}", uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_db():
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE"])
    return g.db


def close_db(error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def query(sql, params=(), *, connection=None):
    return (connection if connection is not None else get_db()).execute(sql, params).fetchall()


def execute(sql, params=(), *, connection=None):
    db = connection if connection is not None else get_db()
    if not db.in_transaction:
        raise RuntimeError("写入必须在 transaction() 中执行")
    return db.execute(sql, params)


@contextmanager
def transaction(connection=None):
    db = connection if connection is not None else get_db()
    if db.in_transaction:
        raise RuntimeError("事务已开启；内部函数应复用连接，不另开事务或自行提交")
    db.execute("BEGIN IMMEDIATE")
    try:
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise


def verify_database(connection=None):
    db = connection if connection is not None else get_db()
    version = db.execute("PRAGMA user_version").fetchone()[0]
    tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if version != SCHEMA_VERSION or not TABLES <= tables:
        raise RuntimeError("数据库未初始化或结构版本不兼容；请先执行 init-db，已有数据不得直接重建")


def initialize_database():
    path = Path(current_app.config["DATABASE"])
    path.parent.mkdir(parents=True, exist_ok=True)
    db = connect(path, create=True)
    try:
        tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if tables or db.execute("PRAGMA user_version").fetchone()[0]:
            verify_database(db)
            return False
        schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
        db.executescript(f"BEGIN IMMEDIATE;\n{schema}\nPRAGMA user_version = {SCHEMA_VERSION};\nCOMMIT;")
        verify_database(db)
        return True
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        """首次创建九张空表；再次运行只检查版本，不删除任何数据。"""
        created = initialize_database()
        click.echo("Database initialized (schema v1)." if created else "Database already initialized; unchanged.")

