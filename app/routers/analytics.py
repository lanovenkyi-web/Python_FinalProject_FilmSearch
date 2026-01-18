from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from databases.db_mongo import get_popular_queries, get_recent_queries
from app.utils.helpers import get_common_data
from app.core.logging import get_logger
from app.core.exceptions import handle_route_error

logger = get_logger(__name__)
router = APIRouter()


@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    """Страница аналитики - история поиска и популярные запросы"""
    try:
        common_data = get_common_data()
        from app.core.templates import templates
        return templates.TemplateResponse("analytics.html", {
            "request": request,
            "popular": get_popular_queries(5),
            "recent": get_recent_queries(5),
            **common_data
        })
    except Exception as e:
        return handle_route_error(request, e, "analytics_page")


@router.get("/analytics/data")
def analytics_data(limit: int = 5):
    """API endpoint для получения данных аналитики в JSON формате"""
    try:
        limit = min(max(1, int(limit)), 100) if isinstance(limit, int) else 5
        trends = get_popular_queries(limit)
        recent = get_recent_queries(5)
        
        return JSONResponse({
            "trends": trends,
            "recent": recent
        })
    except Exception as e:
        logger.error(f"Error in analytics_data: {e}")
        return JSONResponse({"error": "Internal Server Error", "trends": [], "recent": []}, status_code=500)
