# app/__init__.py
from .main import app, ApiError  # экспортируем для тестов

__all__ = ["app", "ApiError"]
