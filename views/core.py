import logging
from typing import List
from datetime import datetime
from utils.base import Endpoints
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage_view(request: Request):
    available_endpoints = []
    base_url_str = str(request.base_url).rstrip('/')
    
    for endpoint_enum in Endpoints:
        try:
            absolute_url = request.url_for(endpoint_enum.route_name)
        except Exception as e:
            logger.warning(f"Can't find the absolute URI for the endpoint: {endpoint_enum.endpoint}. Error: {e}")
            absolute_url = f"{base_url_str}{endpoint_enum.endpoint}"
        
        available_endpoints.append({
            "absolute_url": absolute_url,
            "name": endpoint_enum.route_name,
            "api_prefix": endpoint_enum.endpoint,
            "description": endpoint_enum.description,
        })
    context = {
        "request": request,
        "available_endpoints": available_endpoints,
        
        "author_name": "@Stefan-ci",
        "current_year": datetime.now().year,
        "github_repo_url": "https://github.com/Stefan-ci/Data-Faker-API",
    }
    return templates.TemplateResponse(name="home.html", context=context)




@router.get("/all-endpoints", response_class=HTMLResponse, include_in_schema=False, name="json-list-all-endpoints")
async def all_endpoints_view(request: Request):
    available_endpoints: List[str] = []
    base_url_str = str(request.base_url).rstrip('/')
    
    for endpoint_enum in Endpoints:
        try:
            absolute_url = request.url_for(endpoint_enum.route_name)
        except Exception as e:
            logger.warning(f"Can't find the absolute URI for the endpoint: {endpoint_enum.endpoint}. Error: {e}")
            absolute_url = f"{base_url_str}{endpoint_enum.endpoint}"
        
        available_endpoints.append(str(absolute_url))
    return JSONResponse(content=available_endpoints)
