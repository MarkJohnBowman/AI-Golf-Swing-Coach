from fastapi import FastAPI

app = FastAPI(title="AI Golf Swing Coach")

# When a GET request is sent to /api/health, run the function below
@app.get("/api/health") 
def health() -> dict[str, str]:
    """Check that the backend is running."""
    return {"status": "ok"}