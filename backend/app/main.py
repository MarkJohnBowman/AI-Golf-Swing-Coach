import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(title="AI Golf Swing Coach")

# Folder where swing videos are saved no matter where the server is started from
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"

ALLOWED_EXTENSIONS = {".mp4", ".mov"}


# When a GET request is sent to /api/health, run the function below
@app.get("/api/health")
def health() -> dict[str, str]:
    """Check that the backend is running."""
    return {"status": "ok"}


@app.get("/upload", response_class=HTMLResponse)
def upload_page() -> str:
    """Simple page the phone opens in its browser to upload a video."""
    return """
    <!doctype html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Upload Swing</title>
      </head>
      <body>
        <h1>Upload Swing Video</h1>
        <form action="/api/videos" method="post" enctype="multipart/form-data">
          <input type="file" name="file" accept="video/*">
          <button type="submit">Upload</button>
        </form>
      </body>
    </html>
    """


@app.post("/api/videos")
def upload_video(file: UploadFile) -> dict[str, str]:
    """Save an uploaded swing video to the uploads folder."""
    # Only keep the file name, so a name like "../../file" can't save outside the folder
    filename = Path(file.filename or "").name
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .mp4 and .mov videos can be uploaded")

    UPLOAD_DIR.mkdir(exist_ok=True)
    save_path = UPLOAD_DIR / filename
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": filename, "status": "uploaded"}


@app.get("/api/videos")
def list_videos() -> list[str]:
    """List the uploaded videos, newest first."""
    if not UPLOAD_DIR.exists():
        return []
    videos = [path for path in UPLOAD_DIR.iterdir() if path.suffix.lower() in ALLOWED_EXTENSIONS]
    videos.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return [path.name for path in videos]


@app.get("/api/videos/{filename}")
def get_video(filename: str) -> FileResponse:
    """Send one uploaded video so the browser can play it."""
    path = UPLOAD_DIR / Path(filename).name
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(path)


@app.get("/", response_class=HTMLResponse)
def videos_page() -> str:
    """Laptop page showing the swing list and the face-on and down-the-line panels."""
    return """
    <!doctype html>
    <html>
      <head>
        <title>Swing Videos</title>
        <style>
          body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0e1411;
            color: #e8eee9;
          }
          header{
            padding: 20px 32px;
            border-bottom: 1px solid #243029;
          }
          h1{
            margin: 0;
            font-size: 26px;
          }
          .subtitle{
            margin-top: 4px;
            color: #a3b0a7;
          }
          main{
            display: flex;
            gap: 24px;
            padding: 24px 32px;
          }
          .sidebar {
            width: 260px;
          }
          .sidebar h2 {
            margin: 0 0 12px;
            font-size: 14px;
            color: #a3b0a7;
            text-transform: uppercase;
          }
          .swing-list {
            list-style: none;
            margin: 0;
            padding: 0;
          }
          .swing-list li {
            padding: 12px 14px;
            margin-bottom: 8px;
            background: #18221c;
            border: 1px solid #243029;
            border-radius: 8px;
            cursor: pointer;
          }
          .swing-list li:hover {
            border-color: #c4f25a;
          }
          .swing-list li.selected {
            background: #1e2b17;
            border-color: #c4f25a;
            color: #c4f25a;
          }
          .panels {
            flex: 1;
            display: flex;
            gap: 20px;
          }
          .panel {
            flex: 1;
            background: #121a15;
            border: 1px solid #243029;
            border-radius: 12px;
            padding: 16px;
          }
          .panel h2 {
            margin: 0 0 12px;
            font-size: 14px;
            color: #a3b0a7;
            text-transform: uppercase;
          }
          .panel-body {
            height: 60vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #000;
            border-radius: 8px;
          }
          video {
            width: 100%;
            height: 100%;
            border-radius: 8px;
          }
          .placeholder {
            color: #a3b0a7;
            text-align: center;
            padding: 0 20px;
          }
        </style>
      </head>
      <body>
        <header>
          <h1>AI Golf Swing Coach</h1>
          <div class="subtitle">Swing Videos</div>
        </header>
        <main>
          <section class="sidebar">
            <h2>Swings</h2>
            <ul id="swing-list" class="swing-list"></ul>
          </section>

          <section class="panels">
            <div class="panel">
              <h2>Face-on - Kinect skeleton</h2>
              <div class="panel-body">
                <p class="placeholder">The Kinect skeleton will appear here once the Kinect is connected.</p>
              </div>
            </div>
            <div class="panel">
              <h2>Down-the-line - Phone video</h2>
              <div class="panel-body">
                <video id="player" controls></video>
              </div>
            </div>
          </section>
        </main>

        <script>
          async function loadSwings() {
            const response = await fetch("/api/videos");
            const videos = await response.json();
            const list = document.getElementById("swing-list");

             if (videos.length === 0) {
              list.innerHTML = "<li>No swings uploaded yet</li>";
              return;
            }

            videos.forEach((name, index) => {
              const item = document.createElement("li");
              item.textContent = "Swing " + (videos.length - index) + " - " + name;
              item.onclick = () => {
                document.querySelectorAll(".swing-list li").forEach((li) => {
                  li.classList.remove("selected");
                });
                item.classList.add("selected");
                document.getElementById("player").src = "/api/videos/" + name;
              };
              list.appendChild(item);
            });
          }

          loadSwings();
        </script>
      </body>
    </html>
    """
