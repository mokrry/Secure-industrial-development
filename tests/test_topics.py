import os, tempfile, time
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db

def setup_test_app():
    fd, path = tempfile.mkstemp(suffix=".db"); os.close(fd)
    url = f"sqlite:///{path}"

    engine = create_engine(url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()  # закрываем сессию

    # подменяем зависимость БД
    app.dependency_overrides[get_db] = override_get_db

    return app, path, engine

def safe_unlink(db_path: str, engine):
    """Гарантированно закрываем коннекты и удаляем файл на Windows."""
    try:
        # снимаем все соединения/файловые дескрипторы
        engine.dispose()
    except Exception:
        pass
    # иногда Windows держит дескриптор ещё долю секунды
    for _ in range(10):
        try:
            os.remove(db_path)
            break
        except PermissionError:
            time.sleep(0.2)

def test_topics_flow():
    app_test, db_path, engine = setup_test_app()

    # гарантированно закрыть клиент и фоновые таски FastAPI
    with TestClient(app_test) as client:
        # POST /topics
        r = client.post("/api/v1/topics", json={"title":"Crypto","description":"Basics","status":"planned"})
        assert r.status_code == 201
        tid = r.json()["id"]

        # GET /topics/{id}
        g = client.get(f"/api/v1/topics/{tid}")
        assert g.status_code == 200
        assert g.json()["title"] == "Crypto"

        # PUT /topics/{id}
        u = client.put(f"/api/v1/topics/{tid}", json={"status":"in_progress"})
        assert u.status_code == 200
        assert u.json()["status"] == "in_progress"

        # GET /topics?status=in_progress
        flt = client.get("/api/v1/topics", params={"status":"in_progress"})
        assert flt.status_code == 200
        assert any(t["id"] == tid for t in flt.json())

        # GET /topics (all)
        allr = client.get("/api/v1/topics")
        assert allr.status_code == 200
        assert any(t["id"] == tid for t in allr.json())

    # снимаем override (на будущее) и удаляем временную БД
    app.dependency_overrides.clear()
    safe_unlink(db_path, engine)
