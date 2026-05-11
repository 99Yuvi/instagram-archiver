import os
import uuid
import glob
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp

app = FastAPI(title="Instagram Archiver")

DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


class DownloadRequest(BaseModel):
    url: str
    use_cookies: bool = False


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/download")
def download_video(req: DownloadRequest):
    job_id = str(uuid.uuid4())
    output_template = str(DOWNLOADS_DIR / f"{job_id}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_template,
        "format": "best",
        "quiet": True,
        "no_warnings": True,
    }

    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req.url, download=True)
            title = info.get("title", "instagram_video")
            ext = info.get("ext", "mp4")
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

    # Find the downloaded file
    matches = glob.glob(str(DOWNLOADS_DIR / f"{job_id}.*"))
    if not matches:
        raise HTTPException(status_code=500, detail="Downloaded file not found")

    file_path = matches[0]
    ext = Path(file_path).suffix.lstrip(".")
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-")[:60]
    filename = f"{safe_title}.{ext}" if safe_title else f"instagram_video.{ext}"

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=filename,
        background=None,
    )


@app.on_event("startup")
def cleanup_old_downloads():
    """Remove any leftover files from previous runs."""
    for f in DOWNLOADS_DIR.glob("*"):
        try:
            f.unlink()
        except Exception:
            pass
