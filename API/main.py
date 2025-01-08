from fastapi import FastAPI, File, UploadFile

from lib import process_image

app = FastAPI(prefix="/api")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def process(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "class" : process_image(file.file)
        }