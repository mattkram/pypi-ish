import logging
import os
import sys
from pathlib import Path
from typing import Union

from flask import Flask

PROJECT_ROOT = Path(__file__).parents[1].absolute()
DEFAULT_INSTANCE_PATH = PROJECT_ROOT / "instance"
TEMPLATE_DIR = PROJECT_ROOT / "templates"
RELATIVE_PACKAGE_DIR = "projects"
ALLOWED_EXTENSIONS = {"tar.gz", "tar.bz2", "zip", "whl"}

if sys.argv[-1] == "--debug":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def create_app(instance_path: Union[Path, str] = None) -> Flask:
    instance_path = Path(instance_path) if instance_path else DEFAULT_INSTANCE_PATH

    app = Flask(
        __name__, template_folder=str(TEMPLATE_DIR), instance_path=str(instance_path)
    )

    # Ensure the instance folder exists
    instance_path.mkdir(exist_ok=True)

    app.config.from_object(
        os.environ.get("FLASK_APP_SETTINGS", "pypi.config.DefaultConfig")
    )

    # Set Database URI here to have app context
    app.config.from_mapping(
        UPLOAD_FOLDER=instance_path / RELATIVE_PACKAGE_DIR,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{instance_path / app.config['DB_NAME']}",
    )

    from pypi import routes

    routes.init_app(app)

    from pypi import models

    models.init_app(app)

    return app
