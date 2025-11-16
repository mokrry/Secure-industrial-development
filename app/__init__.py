# app/__init__.py
from .main import ApiError, app  # экспортируем для тестов

__all__ = ["app", "ApiError"]
