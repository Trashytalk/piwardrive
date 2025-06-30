import os
import shutil

from fastapi import FastAPI, UploadFile

app = FastAPI()
STORAGE = os.path.expanduser("~/piwardrive-sync")
os.makedirs(STORAGE, exist_ok=True)


@app.post("/")
async def receive(file: UploadFile):
    dest = os.path.join(STORAGE, file.filename)
    try:
        with open(dest, "wb") as fh:
            shutil.copyfileobj(file.file, fh)
    except OSError as exc:  # pragma: no cover - I/O failure
        return {"error": str(exc)}
    return {"saved": dest}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9000)
