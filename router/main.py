from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def open_env() -> list[str]:
    ret: list[str] = []
    if IP_API := os.getenv("IP_API","localhost:8000"):
        ret.append(IP_API)
    i = 1
    while True:
        IP = os.getenv(f"IP_REPLICA{i}",None)
        print(i,IP)
        if IP:
            ret.append(IP)
            i = i + 1
            continue
        break
    return ret

servers = open_env()
index = 0
print("[30]",servers)

async def req_res(request: Request,url) -> Response:
    async with httpx.AsyncClient(follow_redirects=True,timeout=20.0) as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            data=await request.body()
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
        
# reroute traffic from /api to a server in round robin mode
@app.middleware("http")
async def reroute_traffic(request: Request, call_next):
    global index
    global servers
    if len(servers) == 0:
        print("[ERROR] No servers")
        return await call_next(request)
    for _ in range(len(servers)):
        target_server = servers[index]
        index = (index + 1) % len(servers)
        url_ = str(request.url).split("/api")
        url = f"http://{target_server}/api{url_[1] if len(url_) > 1 else ''}"
        print("[REDIRECTING]",url)
        try:
            req = await req_res(request,url)
            if req.status_code == 200:
                return req
        except httpx.ReadTimeout:
            return JSONResponse({"error": "Request timed out, please try again later."}, status_code=408)
        
    return JSONResponse({"error": "No server could resolve request."}, status_code=409)

@app.get("/api")
async def root():
    return {"message": "Traffic Sign Classification API"}