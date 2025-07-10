import re
from pathlib import Path
from typing import Any, List

import click
from flask import Flask, current_app
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename

from pypi.helpers import normalize

PACKAGE_NAME_PATTERN = re.compile(r"([\w\-.]+)-(\d[\d.]+\d)")


class ModelBase(Model):
    id = Column(Integer, primary_key=True)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()


db: Any = SQLAlchemy(model_class=ModelBase)
migrate: Any = Migrate(db=db)


class Project(db.Model):
    name = Column(String(100))
    releases = relationship("Release", backref="project", lazy=True)

    def __repr__(self) -> str:
        return f"Project(name={self.name})"


class Release(db.Model):
    version = Column(String(10))
    project_id = Column(Integer, ForeignKey("project.id"))
    release_files = relationship("ReleaseFile", backref="release", lazy=True)

    def __repr__(self) -> str:
        return f"Release(project={self.project}, version={self.version})"

    @property
    def filenames(self) -> List[str]:
        return [f.filename for f in self.release_files]


class ReleaseFile(db.Model):
    filename = Column(String(100))
    release_id = Column(Integer, ForeignKey("release.id"))

    @classmethod
    def from_filename(cls, filename: str) -> "ReleaseFile":
        """Alternative constructor to create a ReleaseFile directly from a filename."""
        m = PACKAGE_NAME_PATTERN.match(filename)
        if not m:
            raise ValueError

        project_name = normalize(m.group(1))
        version = m.group(2)

        project = Project.query.filter_by(name=project_name).one_or_none()
        if not project:
            project = Project(name=project_name)
            project.save()

        release = Release.query.filter_by(
            project=project, version=version
        ).one_or_none()
        if not release:
            release = Release(project=project, version=version)

        secured_filename = secure_filename(filename)

        if secured_filename in release.filenames:
            raise FileExistsError

        release_file = cls(release=release, filename=secured_filename)
        return release_file

    def __repr__(self) -> str:
        return f"ReleaseFile(filename={self.filename})"

    @property
    def full_path(self) -> Path:
        return Path(self.release.project.name) / self.filename


@click.command("add-existing-releases")
@with_appcontext
def add_existing_releases() -> None:
    click.echo("Adding existing releases from UPLOAD_FOLDER")
    for file_path in Path(current_app.config["UPLOAD_FOLDER"]).glob("*/*"):
        try:
            release_file = ReleaseFile.from_filename(file_path.name)
        except FileExistsError:
            pass
        else:
            release_file.save()


def init_app(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app)

    app.cli.add_command(add_existing_releases)
