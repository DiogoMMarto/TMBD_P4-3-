from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Load API URL from environment variable
api_url = os.getenv("API_URL", "http://localhost:8000")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "api_url": api_url})
