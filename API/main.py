from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from lib import process_image

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model("model.h5")

app.mount("/api/static", StaticFiles(directory="static"), name="static")

@app.get("/api")
async def root():
    return {"message": "Traffic Sign Classification API"}

@app.post("/api")
async def process(file: UploadFile):
    content = await file.read()
    pred = process_image(content, model)

    return {
        "filename": file.filename,
        "class": pred,
        "traffic_sign": f"/static/traffic_signs/{pred}.png",
    }
