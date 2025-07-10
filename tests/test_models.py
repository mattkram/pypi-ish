from pathlib import Path

import pytest

from pypi.models import Project, Release, ReleaseFile


@pytest.fixture()
def project(app):
    project = Project(name="test-project")
    project.save()

    for version in ["1.0", "2.0"]:
        release_file = ReleaseFile(filename=f"{project.name}-{version}.whl")
        release = Release(
            project=project, version=version, release_files=[release_file]
        )
        release.save()

    return project


@pytest.fixture()
def release(project):
    return project.releases[0]


def test_project_init(project):
    assert project.name == "test-project"
    assert len(project.releases) == 2


def test_release_full_path(release):
    assert (
        release.release_files[0].full_path
        == Path("test-project") / "test-project-1.0.whl"
    )
