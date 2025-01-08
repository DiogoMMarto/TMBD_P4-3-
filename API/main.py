from fastapi import FastAPI, File, UploadFile

from lib import process_image

app = FastAPI()

@app.get("/api")
async def root():
    return {"message": "Hello World"}

@app.post("/api")
async def process(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "class" : process_image(file.file)
        }