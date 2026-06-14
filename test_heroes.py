import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from main import app
from routers.heroes import get_session

@pytest.fixture
def client():
    # テスト用にインメモリDBを使う
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_read_heroes(client):
    response = client.get("/heroes/")
    assert response.status_code == 200
    assert response.json() == []  # テスト用DBは空なので空リスト

def test_create_hero(client):
    response = client.post("/heroes/", json={"name": "テスト太郎", "age": 20})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "テスト太郎"
    assert data["age"] == 20
    assert "id" in data

