from app.databases.db_mysql import (
    get_categories_with_stats,
    get_year_range
)
from app.databases.db_mongo import (
    get_popular_queries,
    get_recent_queries
)


def get_common_data():
    """Получаем общие данные для всех шаблонов:
    категории, популярные запросы, годы"""
    min_year, max_year = get_year_range()
    return {
        "return_categories": get_categories_with_stats(),
        "popular": get_popular_queries(5),
        "recent": get_recent_queries(5),
        "min_year": min_year,
        "max_year": max_year
    }
