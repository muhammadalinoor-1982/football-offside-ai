# add for deployment
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# add for deployment

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from video_processor import process_video

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# add for deployment
""" app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
) """

# bug fixing code
app.mount(
    "/assets",
    StaticFiles(directory="static/assets"),
    name="assets"
)
# bug fixing code

# add for deployment

app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)

# add for deployment
@app.get("/")
async def root():
    return FileResponse("static/index.html")
# add for deployment

@app.post("/process")
async def upload_video(video: UploadFile):

    input_path = f"uploads/{video.filename}"

    with open(input_path, "wb") as f:
        f.write(await video.read())

    verdict, output_file = process_video(input_path)

    return {
        "verdict": verdict,
        "video_url": f"http://localhost:8000/outputs/{output_file}"
    }


