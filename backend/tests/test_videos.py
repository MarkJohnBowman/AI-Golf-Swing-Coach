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

    

def test_list_videos_returns_uploaded_files(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    (tmp_path / "swing.mp4").write_bytes(b"video")
    (tmp_path / "notes.txt").write_bytes(b"not a video")

    response = client.get("/api/videos")

    assert response.status_code == 200
    assert response.json() == ["swing.mp4"]


def test_list_videos_when_no_uploads_yet(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path / "missing")

    response = client.get("/api/videos")

    assert response.status_code == 200
    assert response.json() == []


def test_get_video_returns_file(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    (tmp_path / "swing.mp4").write_bytes(b"video data")

    response = client.get("/api/videos/swing.mp4")

    assert response.status_code == 200
    assert response.content == b"video data"


def test_get_video_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)

    response = client.get("/api/videos/missing.mp4")

    assert response.status_code == 404


def test_videos_page_shows_list():
    response = client.get("/")

    assert response.status_code == 200
    assert "Swing Videos" in response.text