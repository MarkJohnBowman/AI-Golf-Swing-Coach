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

def test_over_the_top_endpoint(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "UPLOAD_DIR", tmp_path)
    path = [
        {"time": 0.0, "x": 100, "y": 100},
        {"time": 0.1, "x": 50, "y": 50},
        {"time": 0.2, "x": 0, "y": 0},
        {"time": 0.3, "x": 80, "y": 50},
        {"time": 0.4, "x": 100, "y": 100},
    ]
    (tmp_path / "swing.json").write_text(json.dumps(path))

    response = client.get("/api/videos/swing.mp4/over-the-top")

    assert response.status_code == 200
    assert response.json()["result"] == "Over the top"