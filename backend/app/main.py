import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI(title="AI Golf Swing Coach")

UPLOAD_DIR = Path("uploads")

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