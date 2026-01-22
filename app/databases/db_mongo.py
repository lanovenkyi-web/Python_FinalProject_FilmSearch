from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

from app.core.logging import get_logger

logger = get_logger(__name__)

load_dotenv()
MONGODB_URL_EDIT = os.getenv("MONGODB_URL_EDIT")
db_edit = MongoClient(MONGODB_URL_EDIT)
COLLECTION_NAME = "final_project_010825-ptm_Serhii_Lanovenkyi"
db_edit = db_edit["ich_edit"]


def save_search_query(query: str):
    """Сохраняем поисковый запрос в MongoDB с подсчетом количества использований."""
    if not query or not query.strip():
        return
    clean_query = query.strip().lower()
    try:
        db_edit[COLLECTION_NAME].update_one(
            {"query": clean_query},
            {
                "$set": {"last_searched": datetime.now()},
                "$inc": {"count": 1}
            },
            upsert=True
        )
    except Exception as e:
        logger.error(f"Ошибка записи в MongoDB: {e}")


def get_popular_queries(
        limit: int = 5
):
    """Возвращаем самые популярные поисковые запросы, отсортированные по количеству использований."""
    try:
        cursor = (
            db_edit[COLLECTION_NAME].find()
            .sort("count", -1)
            .limit(limit)
        )
        results = []
        for doc in cursor:
            if doc and "query" in doc:
                results.append({
                    "query": doc["query"],
                    "count": doc.get("count", 0)
                })
        return results
    except Exception as error:
        logger.error(f"Ошибка чтения популярных: {error}")
        return []


def get_recent_queries(
        limit: int = 5
):
    """Возвращаем последние поисковые запросы, отсортированные по времени использования."""
    try:
        cursor = (
            db_edit[COLLECTION_NAME].find()
            .sort("last_searched", -1)
            .limit(limit)
        )
        results = []
        for doc in cursor:
            if doc and "query" in doc:
                results.append(doc["query"])
        return results
    except Exception as e:
        logger.error(f"Ошибка чтения последних: {e}")
        return []
