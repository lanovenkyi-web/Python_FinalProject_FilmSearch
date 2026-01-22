"""
 модуль приложения Film Search API.

Создаем и настраиваем FastAPI приложение для поиска фильмов,
включая middleware, rout и обработку исключений.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app.routers import home, search, analytics, static
from app.exceptions.handlers import validation_exception_handler

# Логирование ошибок
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI(title="Film Search API", version="2.0")

# Настройка CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# Обработка валидации и исключения запросов
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Подключение статических файлов  app/static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Роуты
app.include_router(home.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(static.router)

if __name__ == "__main__":
    """
    Точка входа для запуска приложения 
    """
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
