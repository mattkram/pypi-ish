from flask import url_for


def test_missing_project_404(client):
    response = client.get("/simple/some-project/")
    assert response.status_code == 404


def test_construct_url_with_hash(app):
    """Ensure there is no slash placed between the filename and the hash."""
    project_name = "project_name"
    filename = "filename"
    my_hash = "sha256=my_hash"
    with app.test_request_context():
        url = (
            url_for(
                "simple.download_release",
                project_name=project_name,
                filename=filename,
                _anchor=my_hash,
            )
            .replace("%3D", "=")
            .replace("/#", "#")
        )
        assert url == f"/simple/{project_name}/{filename}#{my_hash}"
