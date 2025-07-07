from utils.base import Endpoints
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage_view(request: Request):
    available_endpoints = []
    for endpoint in Endpoints:
        available_endpoints.append({
            "endpoint": endpoint.endpoint,
            "description": endpoint.description,
        })
    context = {
        "request": request,
        "available_endpoints": available_endpoints,
    }
    return templates.TemplateResponse(name="home.html", context=context)
