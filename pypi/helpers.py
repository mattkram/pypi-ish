import hashlib
import re

from flask import current_app, flash
from werkzeug.datastructures import FileStorage

from pypi import ALLOWED_EXTENSIONS


def filename_is_allowed(filename: str) -> bool:
    """Return true of the filename has an allowed extension."""
    return "." in filename and any(
        filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS
    )


def normalize(name: str) -> str:
    """Normalize the package name."""
    return re.sub(r"[-_.]+", "-", name).lower()


def hash_file(filename: str) -> str:
    """Create a SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def handle_file_upload(file: FileStorage) -> None:
    """Create a new ReleaseFile instance and upload the file to disk.

    Flashes messages to browser depending on situation.

    Args:
        file: The FileStorage object passed through a POST request.

    """
    from pypi.models import ReleaseFile

    filename = file.filename
    if filename is None:
        flash("No filename provided", category="error")
        return

    if not filename_is_allowed(filename):
        flash(
            f"\u274c Invalid filename {filename}, "
            f"must have one of the following extensions: {ALLOWED_EXTENSIONS}",
            category="error",
        )
        return

    try:
        release_file = ReleaseFile.from_filename(filename)
    except ValueError:
        flash(f"Error parsing filename: {filename}", category="error")
        return
    except FileExistsError:
        flash(
            f"File {filename} already exists, skipping upload", category="warning",
        )
        return

    save_path = current_app.config["UPLOAD_FOLDER"] / release_file.full_path
    save_path.parent.mkdir(exist_ok=True, parents=True)
    file.save(str(save_path))

    release_file.save()

    flash(f"\u2714 Successfully uploaded {filename}", category="info")
