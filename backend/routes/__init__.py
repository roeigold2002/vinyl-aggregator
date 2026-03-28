"""Package init for routes"""
from .search import router as search_router
from .records import router as records_router
from .stores import router as stores_router

__all__ = [
    "search_router",
    "records_router",
    "stores_router",
]
