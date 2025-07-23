from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .forecast import forecast_demand

app = FastAPI()

# This must match: your CWD/templates must exist!
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    result = forecast_demand()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "forecast": result
    })

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})