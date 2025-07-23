# main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from vip_logic import compute_vip_score

app = FastAPI(title="VIP Customer Detector")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def detect_vip(
    request: Request,
    customer_id1: str = Form(None),
    customer_id2: str = Form(None),
    customer_id3: str = Form(None)
):
    results = []
    for cid in [customer_id1, customer_id2, customer_id3]:
        if cid:
            results.append(compute_vip_score(cid))
    return templates.TemplateResponse("index.html", {"request": request, "results": results})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
