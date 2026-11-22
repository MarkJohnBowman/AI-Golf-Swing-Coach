import json

from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


def test_upload_still_works_without_the_model(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    monkeypatch.setattr(main, "MODEL_PATH", tmp_path / "missing.pt")

    response = client.post(
        "/api/videos",
        files={"file": ("swing.mp4", b"fake video data", "video/mp4")},
    )

    assert response.status_code == 200
    assert not (tmp_path / "swing.json").exists()


def test_get_club_path_returns_saved_path(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    path = [{"time": 0.0, "x": 836, "y": 1742}]
    (tmp_path / "swing.json").write_text(json.dumps(path))

    response = client.get("/api/videos/swing.mp4/path")

    assert response.status_code == 200
    assert response.json() == path


def test_get_club_path_not_ready(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)

    response = client.get("/api/videos/swing.mp4/path")

    assert response.status_code == 404