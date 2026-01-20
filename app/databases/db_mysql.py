from dotenv import load_dotenv
import os
import pymysql
from contextlib import contextmanager

from app.core.logging import get_logger

logger = get_logger(__name__)

load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
dbconfig_write = {"host": MYSQL_HOST, "user": MYSQL_USER, "password": MYSQL_PASSWORD, "database": MYSQL_DB, "charset": "utf8mb4"}

@contextmanager
def get_db_connection():
    """Устанавливаем подключение к MySQL базе данных с автоматическим закрытием"""
    connection = None
    try:
        connection = pymysql.connect(**dbconfig_write)
        yield connection
    except pymysql.Error as e:
        logger.error(f"Ошибка подключения к БД: {e}")
        raise
    finally:
        if connection:
            connection.close()
def select_query(connection, query, params=None):
    """Выполняет SQL-запрос и возвращает результат"""
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result
    except pymysql.Error as e:
        logger.error(f"Ошибка выполнения запроса: {e}")
        return []
def _get_films_base_query(where_clause="", offset=0, limit=10):
    """Базовый SQL запрос для получения фильмов с общей структурой"""
    base = """SELECT f.title, f.release_year, f.rating, f.length, f.description, c.name
              FROM film f
              JOIN film_category f_c ON f.film_id = f_c.film_id
              JOIN category c ON f_c.category_id = c.category_id"""
    
    if where_clause:
        query = f"{base} WHERE {where_clause} ORDER BY f.release_year DESC LIMIT {limit} OFFSET {offset}"
    else:
        query = f"{base} ORDER BY f.release_year DESC LIMIT {limit} OFFSET {offset}"
    
    return query
def get_categories_with_stats():
    """Возвращает категории со статистикой (название, количество, min/max годы)"""
    query = """SELECT c.name, COUNT(*) as cnt, MIN(f.release_year) as min_year, MAX(f.release_year) as max_year 
              FROM film f 
              JOIN film_category f_c ON f.film_id = f_c.film_id 
              JOIN category c ON f_c.category_id = c.category_id 
              GROUP BY c.name 
              ORDER BY cnt DESC"""
    try:
        with get_db_connection() as conn:
            return select_query(conn, query)
    except Exception as e:
        logger.error(f"Ошибка при получении статистики категорий: {e}")
        return []


def get_year_range():
    """Возвращает минимальный и максимальный год выпуска фильмов в БД"""
    query = "SELECT MIN(release_year), MAX(release_year) FROM film"
    try:
        with get_db_connection() as conn:
            result = select_query(conn, query)
            if result and result[0]:
                min_year = result[0][0] if result[0][0] else 1900
                max_year = result[0][1] if result[0][1] else 2100
                return min_year, max_year
            return 1900, 2100
    except Exception as e:
        logger.error(f"Ошибка при получении диапазона лет: {e}")
        return 1900, 2100


def count_films_by_genre_year(genre_name, year_from=None, year_to=None):
    """Подсчитываем количество найденых фильмов по жанру и диапазону лет"""
    where_parts = []
    params = []
    
    if genre_name and genre_name.strip():
        where_parts.append("c.name = %s")
        params.append(genre_name.strip())
    
    if year_from and year_to:
        where_parts.append("f.release_year BETWEEN %s AND %s")
        params.extend([int(year_from), int(year_to)])
    elif year_from:
        where_parts.append("f.release_year >= %s")
        params.append(int(year_from))
    elif year_to:
        where_parts.append("f.release_year <= %s")
        params.append(int(year_to))
    
    where_clause = " AND ".join(where_parts) if where_parts else "1=1"
    
    query = f"""SELECT COUNT(*) FROM film f 
               JOIN film_category f_c ON f.film_id = f_c.film_id 
               JOIN category c ON f_c.category_id = c.category_id 
               WHERE {where_clause}"""
    
    try:
        with get_db_connection() as conn:
            result = select_query(conn, query, params)
            return result[0][0] if result and result[0] else 0
    except Exception as e:
        logger.error(f"Ошибка при подсчете фильмов: {e}")
        return 0


def new_films(offset=0):
    """Возвращает список новых фильмов в порядке убывания года выпуска"""
    query = _get_films_base_query(where_clause="", offset=offset)
    try:
        with get_db_connection() as conn:
            return select_query(conn, query)
    except Exception as e:
        logger.error(f"Ошибка при получении новых фильмов: {e}")
        return []


def search_genre_year(name_category, year_from=None, year_to=None, offset=0):
    """Ищем фильмы по жанру и/или диапазону лет"""
    where_clauses = []
    params = []
    
    if name_category and name_category.strip():
        where_clauses.append("c.name = %s")
        params.append(name_category.strip())
    
    if year_from and year_to:
        where_clauses.append("f.release_year BETWEEN %s AND %s")
        params.extend([int(year_from), int(year_to)])
    elif year_from:
        where_clauses.append("f.release_year >= %s")
        params.append(int(year_from))
    elif year_to:
        where_clauses.append("f.release_year <= %s")
        params.append(int(year_to))

    where_sql = " AND ".join(where_clauses) if where_clauses else ""
    query = _get_films_base_query(where_clause=where_sql, offset=offset)
    
    try:
        with get_db_connection() as conn:
            return select_query(conn, query, params)
    except Exception as e:
        logger.error(f"Ошибка при поиске по жанру/году: {e}")
        return []


def count_films_by_title(title):
    """Считаем количество найденых фильмов по названию (частичное совпадение)"""
    if not title or not title.strip():
        return 0
    
    query = (f"SELECT COUNT(*) "
             f"FROM film f "
             f"JOIN film_category f_c ON f.film_id = f_c.film_id "
             f"JOIN category c ON f_c.category_id = c.category_id "
             f"WHERE LOWER(f.title) LIKE LOWER(%s)")
    
    try:
        with get_db_connection() as conn:
            result = select_query(conn, query, (f"%{title.strip()}%",))
            return result[0][0] if result and result[0] else 0
    except Exception as e:
        logger.error(f"Ошибка при подсчете фильмов по названию: {e}")
        return 0


def search_by_title(title, offset=0, limit=10):
    """Ищем фильмы по названию (с частичным совпадением)"""
    if not title or not title.strip():
        return []
    
    query = (f"SELECT f.title, f.release_year, f.rating, f.length, f.description, c.name "
             f"FROM film f "
             f"JOIN film_category f_c ON f.film_id = f_c.film_id "
             f"JOIN category c ON f_c.category_id = c.category_id "
             f"WHERE LOWER(f.title) LIKE LOWER(%s) "
             f"ORDER BY f.title LIMIT {limit} OFFSET {offset}")
    
    try:
        with get_db_connection() as conn:
            return select_query(conn, query, (f"%{title.strip()}%",))
    except Exception as e:
        logger.error(f"Ошибка при поиске по названию: {e}")
        return []







