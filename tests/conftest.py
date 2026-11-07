import pytest

from app import create_app
from app.commonbase.db import initialize_database


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db"), "DEMO_DATE": "2026-11-04"})
    with app.app_context():
        initialize_database()
    return app


@pytest.fixture
def client(app):
    return app.test_client()

