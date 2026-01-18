from .main import router as main_router
from .search import router as search_router
from .analytics import router as analytics_router
from .static import router as static_router

__all__ = ["main_router", "search_router", "analytics_router", "static_router"]
