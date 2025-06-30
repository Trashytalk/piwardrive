import os
import shutil

from fastapi import FastAPI, UploadFile, HTTPException

from piwardrive.security import sanitize_filename

app = FastAPI()
STORAGE = os.path.expanduser("~/piwardrive-sync")
os.makedirs(STORAGE, exist_ok=True)


@app.post("/")
async def receive(file: UploadFile):
    try:
        name = sanitize_filename(file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    dest = os.path.join(STORAGE, name)
    try:
        with open(dest, "wb") as fh:
            shutil.copyfileobj(file.file, fh)
    except OSError as exc:  # pragma: no cover - I/O failure
        return {"error": str(exc)}
    return {"saved": dest}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9000)
