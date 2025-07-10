from typing import Any

from flask import (
    Blueprint,
    Flask,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from sqlalchemy.orm.exc import NoResultFound

from pypi.helpers import handle_file_upload, hash_file
from pypi.models import Project, ReleaseFile

bp = Blueprint("simple", __name__)

RouteResponse = Any


@bp.route("/", methods=("GET", "POST"))
def index() -> RouteResponse:
    if request.method == "POST":
        files = request.files.getlist("files") + request.files.getlist("content")
        if not files:
            flash("No files selected", category="error")
        else:
            for file in files:
                handle_file_upload(file)
        return redirect(request.url)
    return redirect(url_for("simple.main_index"))


@bp.route("/simple/")
def main_index() -> RouteResponse:
    projects = Project.query.order_by(Project.name)
    return render_template("index.html", projects=projects)


@bp.route("/simple/<project_name>/")
def project_index(project_name: str) -> RouteResponse:
    try:
        project = Project.query.filter_by(name=project_name).one()
    except NoResultFound:
        return abort(404)

    def create_hash(release_file: ReleaseFile) -> str:
        release_path = current_app.config["UPLOAD_FOLDER"] / release_file.full_path
        hashed_file = hash_file(release_path)
        return f"sha256={hashed_file}"

    return render_template("project.html", project=project, create_hash=create_hash)


@bp.route("/upload/", methods=["GET", "POST"])
def upload_file() -> RouteResponse:
    if request.method == "POST":
        return redirect(url_for("index"), code=307)
    return render_template("upload_file.html")


@bp.route("/simple/<project_name>/<filename>/")
def download_release(project_name: str, filename: str) -> RouteResponse:
    release_file = ReleaseFile.query.filter_by(filename=filename).one()
    file_path = current_app.config["UPLOAD_FOLDER"] / release_file.full_path
    return send_file(
        str(file_path), mimetype="application/octet-stream", as_attachment=True
    )


def init_app(app: Flask) -> None:
    app.register_blueprint(bp)
    app.add_url_rule("/", endpoint="index")
