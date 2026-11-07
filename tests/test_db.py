import sqlite3

import pytest

from app import create_app
from app.commonbase.db import connect, execute, get_db, initialize_database, query, transaction, verify_database


def add_category(db, name="测试类别"):
    return execute("INSERT INTO category_rule(category_name,item_type) VALUES (?,?)", (name, "FOOD"), connection=db).lastrowid


def test_transaction_commits_and_initialization_preserves_data(app):
    with app.app_context():
        with transaction() as db:
            add_category(db)
        assert initialize_database() is False
        assert len(query("SELECT * FROM category_rule")) == 1
        assert get_db().execute("PRAGMA foreign_keys").fetchone()[0] == 1


def test_transaction_rolls_back_all_writes_and_releases_connection(app):
    with app.app_context():
        with pytest.raises(sqlite3.IntegrityError):
            with transaction() as db:
                add_category(db)
                add_category(db)
        assert query("SELECT * FROM category_rule") == []
        with transaction() as db:
            add_category(db, "下一次写入")
        assert len(query("SELECT * FROM category_rule")) == 1


def test_writes_require_explicit_transaction_and_nested_transaction_rolls_back(app):
    with app.app_context():
        with pytest.raises(RuntimeError):
            add_category(get_db())
        with pytest.raises(RuntimeError):
            with transaction() as db:
                add_category(db)
                with transaction(db):
                    pass
        assert query("SELECT * FROM category_rule") == []


def test_parameterized_values_are_not_executable_sql(app):
    name = "'); DROP TABLE category_rule; --"
    with app.app_context():
        with transaction() as db:
            add_category(db, name)
        assert query("SELECT category_name FROM category_rule")[0][0] == name


def test_missing_database_is_not_created_on_normal_connect(tmp_path):
    path = tmp_path / "missing.db"
    with pytest.raises(sqlite3.OperationalError):
        connect(path)
    assert not path.exists()


def test_unknown_existing_database_is_never_rebuilt(tmp_path):
    path = tmp_path / "other.db"
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE existing_data (name TEXT)")
    app = create_app({"DATABASE": str(path)})
    with app.app_context(), pytest.raises(RuntimeError):
        initialize_database()
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() == [("existing_data",)]


def test_nullable_fields_and_foreign_keys(app):
    with app.app_context():
        with transaction() as db:
            category = add_category(db)
            item = execute("""INSERT INTO item_batch
                (item_type,name,category_id,quantity,display_unit,date_kind,production_or_purchase_date,package_expiry)
                VALUES (?,?,?,?,?,?,?,?)""", ("FOOD", "测试", category, 1, "份", "PURCHASE", "2026-11-04", "2026-11-05"), connection=db).lastrowid
            assert query("SELECT opened_days FROM item_batch WHERE item_id=?", (item,), connection=db)[0][0] is None
        with pytest.raises(sqlite3.IntegrityError):
            with transaction() as db:
                execute("DELETE FROM category_rule WHERE category_id=?", (category,), connection=db)
        verify_database()


def test_only_one_current_config_per_type_with_history(app):
    sql = """INSERT INTO risk_config
        (item_type,risk_weights,time_window,model_version,is_current,level_thresholds)
        VALUES ('MEDICINE','[55,10,15,15,5]',30,?,?,'[25,50,75]')"""
    with app.app_context():
        with transaction() as db:
            execute(sql, ("v1", 1), connection=db)
        with pytest.raises(sqlite3.IntegrityError):
            with transaction() as db:
                execute(sql, ("v2", 1), connection=db)
        with transaction() as db:
            execute("UPDATE risk_config SET is_current=0", connection=db)
            execute(sql, ("v2", 1), connection=db)
        assert len(query("SELECT * FROM risk_config")) == 2

