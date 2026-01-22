from fastapi import Request
from typing import Any

from app.core.templates import templates
from app.utils.helpers import get_common_data
from app.databases.db_mysql import new_films


def render_error_page(
    request: Request,
    error_message: str,
    status_code: int = 500,
    template_name: str = "index.html"
):
    """Централизованная обработка ошибок и рендеринг страниц с ошибками"""
    try:
        common_data = get_common_data()
        return templates.TemplateResponse(template_name, {
            "request": request,
            "return_films": new_films(0),
            "page": 1,
            "error": error_message,
            **common_data
        }, status_code=status_code)
    except Exception:
        # Fallback если даже базовые данные недоступны
        return templates.TemplateResponse(template_name, {
            "request": request,
            "return_films": [],
            "page": 1,
            "error": error_message
        }, status_code=status_code)


def handle_route_error(
    request: Request,
    e: Exception,
    context: str = ""
) -> Any:
    """Универсальная обработка ошибок в rout"""
    from app.core.logging import get_logger
    logger = get_logger(__name__)
    logger.error(f"Error in {context}: {e}")
    return render_error_page(request, "Ошибка сервера", 500)
