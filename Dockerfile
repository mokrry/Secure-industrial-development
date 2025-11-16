# ===== 1. Stage: builder (для зависимостей / тестов, если нужно) =====
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Ставим прод + dev зависимости (если будут тесты и т.п.)
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Кладём весь код (если захочешь гонять pytest в контейнере)
COPY . .

# Опционально — можно раскомментировать, если тесты зелёные
# RUN pytest -q


# ===== 2. Stage: runtime (лёгкий образ для запуска сервиса) =====
FROM python:3.11-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Ставим ТОЛЬКО продакшн-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

# Создаём отдельного пользователя и отдаём ему каталог /app
RUN useradd -m appuser && chown -R appuser:appuser /app

# Переходим под non-root пользователя
USER appuser

# Кладём только код приложения (без тестов, скриптов и т.п., если они не нужны)
COPY app ./app

# Порт приложения внутри контейнера
EXPOSE 8000

# HEALTHCHECK — ходим на /health внутри контейнера
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Команда запуска FastAPI-приложения через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
