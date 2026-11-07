from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


def test_upload_page_shows_form():
    response = client.get("/upload")

    assert response.status_code == 200
    assert "Upload Swing Video" in response.text


def test_upload_video_saves_file(tmp_path, monkeypatch):
    # Save uploads to a temporary folder instead of the real uploads folder
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)

    response = client.post(
        "/api/videos",
        files={"file": ("swing.mp4", b"fake video data", "video/mp4")},
    )

    assert response.status_code == 200
    assert response.json() == {"filename": "swing.mp4", "status": "uploaded"}
    assert (tmp_path / "swing.mp4").read_bytes() == b"fake video data"


def test_upload_rejects_other_file_types(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)

    response = client.post(
        "/api/videos",
        files={"file": ("notes.txt", b"not a video", "text/plain")},
    )

    assert response.status_code == 400
    assert not (tmp_path / "notes.txt").exists()