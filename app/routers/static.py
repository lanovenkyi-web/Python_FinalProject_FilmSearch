import os
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/static/images/posters/{filename}")
async def get_poster(request: Request, filename: str):
    """Возвращает постер фильма или заглушку если файл не найден"""
    poster_path = f"app/static/images/posters/{filename}"
    if os.path.exists(poster_path):
        return FileResponse(poster_path)
    else:
        return FileResponse("app/static/images/posters/placeholder.svg")
