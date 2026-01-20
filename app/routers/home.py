from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.databases.db_mysql import new_films
from app.utils.helpers import get_common_data
from app.core.logging import get_logger
from app.core.exceptions import handle_route_error
from app.utils.validators import validate_page_param

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, page: int = 1):
    """Главная страница отображает самые новые фильмы"""
    try:
        page = validate_page_param(page)
        offset = (page - 1) * 10
        common_data = get_common_data()
        
        from app.core.templates import templates
        return templates.TemplateResponse("index.html", {
            "return_films": new_films(offset),
            "request": request,
            "page": page,
            **common_data
        })
    except Exception as e:
        return handle_route_error(request, e, "home")
