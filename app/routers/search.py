from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.databases.db_mysql import (
    search_by_title, search_genre_year, new_films,
    count_films_by_title, count_films_by_genre_year
)
from app.databases.db_mongo import save_search_query
from app.utils.helpers import get_common_data
from app.utils.validators import (
    validate_year, validate_page_param,
    validate_search_query, validate_genre_name
)
from app.core.logging import get_logger
from app.core.exceptions import handle_route_error

logger = get_logger(__name__)
router = APIRouter()


@router.get("/search_title", response_class=HTMLResponse)
@router.post("/search_title", response_class=HTMLResponse)
async def search_title(request: Request, title: str = None, page: int = 1):
    """Поиск фильмов по названию"""
    try:
        if request.method == "POST":
            form = await request.form()
            title = form.get("title")

        if not title or not title.strip():
            from app.core.templates import templates
            common_data = get_common_data()
            return templates.TemplateResponse("index.html", {
                "request": request, "return_films": new_films(0),
                "page": 1, "error": "Поле 'title' обязательно",
                **common_data
            }, status_code=422)

        title = validate_search_query(title)
        page = validate_page_param(page)
        offset = (page - 1) * 10
        if page == 1:
            save_search_query(title)
        results = search_by_title(title, offset)
        total_count = count_films_by_title(title)
        common_data = get_common_data()
        from app.core.templates import templates
        return templates.TemplateResponse(
            "results.html", {
                "request": request,
                "results": results,
                "search_term": title,
                "page": page,
                "total_count": total_count,
                **common_data
            }
        )
    except Exception as e:
        return handle_route_error(request, e, "search_title")


@router.post("/search_filter", response_class=HTMLResponse)
@router.get("/search_filter", response_class=HTMLResponse)
async def search_filter_route(
    request: Request,
    category: str = None,
    year_from: int = None,
    year_to: int = None,
    page: int = 1
):
    """Обрабатывает фильтрацию фильмов по жанру и году"""
    try:
        if request.method == "POST":
            form = await request.form()
            category = form.get("category", "").strip() or None
            year_from = form.get("year_from", "").strip() or None
            year_to = form.get("year_to", "").strip() or None
            page = form.get("page", "1")
        else:
            # Для GET-запросов используем параметры из URL
            category = (
                category.strip() if category and category.strip() else None
            )
        page = validate_page_param(page)
        year_from, year_to = validate_year(year_from), validate_year(year_to)
        genre = validate_genre_name(category)
        search_label = (
            f"Фильтр: {genre or 'Все'} ({year_from or ''}-{year_to or ''})"
        )
        if search_label and search_label.strip() and page == 1:
            save_search_query(search_label)

        offset = (page - 1) * 10
        results = search_genre_year(genre, year_from, year_to, offset)
        total_count = count_films_by_genre_year(genre, year_from, year_to)
        common_data = get_common_data()
        from app.core.templates import templates
        return templates.TemplateResponse(
            "results.html", {
                "request": request,
                "results": results,
                "search_term": search_label,
                "page": page,
                "total_count": total_count,
                "category": genre,
                "year_from": year_from,
                "year_to": year_to,
                **common_data
            }
        )
    except Exception as e:
        return handle_route_error(request, e, "search_filter")


@router.get("/genre/{genre_name}", response_class=HTMLResponse)
async def genre_page(
    request: Request,
    genre_name: str,
    page: int = 1,
    year_from: int = None,
    year_to: int = None
):
    """Страница жанра - отображает фильмы по конкретному жанру"""
    try:
        page = validate_page_param(page)
        year_from, year_to = validate_year(year_from), validate_year(year_to)
        offset = (page - 1) * 10
        results = search_genre_year(genre_name, year_from, year_to, offset)
        total_count = count_films_by_genre_year(genre_name, year_from, year_to)
        common_data = get_common_data()
        search_label = (
            f"Жанр: {genre_name} ({year_from or ''}-{year_to or ''})"
        )

        if page == 1:
            save_search_query(search_label)
        from app.core.templates import templates
        return templates.TemplateResponse(
            "results.html", {
                "request": request,
                "results": results,
                "search_term": search_label,
                "page": page,
                "total_count": total_count,
                "category": genre_name,
                "year_from": year_from,
                "year_to": year_to,
                **common_data
            }
        )
    except Exception as e:
        return handle_route_error(request, e, "genre_page")
