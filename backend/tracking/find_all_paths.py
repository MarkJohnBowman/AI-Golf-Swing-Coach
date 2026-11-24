from app.main import ALLOWED_EXTENSIONS, UPLOAD_DIR, save_club_path

for video in UPLOAD_DIR.iterdir():
    # Only videos that don't have a club path yet
    if video.suffix.lower() in ALLOWED_EXTENSIONS and not video.with_suffix(".json").exists():
        print("Finding club path for", video.name)
        save_club_path(video)

print("Done")