from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.core.logging import get_logger
from app.core.exceptions import render_error_page

logger = get_logger(__name__)


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации запросов"""
    logger.warning(f"Validation error: {exc}")
    return render_error_page(
        request, 
        "Ошибка валидации: проверьте поле 'title'", 
        422
    )
