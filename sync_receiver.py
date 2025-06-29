import os
import shutil

from fastapi import FastAPI, UploadFile

app = FastAPI()
STORAGE = os.path.expanduser("~/piwardrive-sync")
os.makedirs(STORAGE, exist_ok=True)


@app.post("/")
async def receive(file: UploadFile):
    dest = os.path.join(STORAGE, file.filename)
    with open(dest, "wb") as fh:
        shutil.copyfileobj(file.file, fh)
    return {"saved": dest}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
