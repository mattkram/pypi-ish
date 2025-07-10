import os
from pathlib import Path

import pytest

import pypi
from pypi.models import db


@pytest.fixture(scope="session")
def app(tmpdir_factory):
    """Return an app with context, with an initialized database."""
    temp_dir = tmpdir_factory.mktemp("temp")
    app = pypi.create_app(instance_path=Path(temp_dir))
    os.environ["FLASK_APP_SETTINGS"] = "pypi.config.TestingConfig"

    with app.app_context():
        db.create_all()
        yield app


# @pytest.fixture(scope="session")
# def app_with_loaded_db(app):
#     load_data_from_dir(dwsc_site.DATA_DIR)
#     assert len(Facility.query.all()) > 0
#     yield app
#


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
