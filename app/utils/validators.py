def validate_year(year):
    """Валидируем и возвращаем год в диапазоне 1900-2100 или None"""
    if not year or not str(year).strip() or str(year) == "None":
        return None
    try:
        year = int(year)
        return year if 1900 <= year <= 2100 else None
    except (ValueError, TypeError):
        return None


def validate_page_param(page):
    """Валидация параметра страницы"""
    try:
        page = int(page) if page else 1
        return max(1, page)
    except (ValueError, TypeError):
        return 1


def validate_search_query(query: str) -> str:
    """Валидация поискового запроса"""
    if not query or not query.strip():
        return ""

    query = query.strip()
    if len(query) > 100:
        query = query[:100]
    return query


def validate_genre_name(genre: str | None) -> str | None:
    """Валидация названия жанра"""
    if genre and not genre.strip():
        return ""
    return genre.strip() if genre else None


def validate_year_range(year_from: int = None, year_to: int = None) -> tuple:
    """Валидация диапазона лет"""
    year_from = validate_year(year_from)
    year_to = validate_year(year_to)
    if year_from and year_to and year_from > year_to:
        year_from, year_to = year_to, year_from
    return year_from, year_to
