import pytest
from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app import schema
from app.config import settings
from app.database import get_db

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db()

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("data") == "Hello World"
    assert res.status_code == 200

@pytest.mark.parametrize(
    "email, password",
    [
        ("mhaseeb@gmail.com", "1234")
    ]
    )
def test_user(email, password):
    res = client.post(
        "/users/", 
        json={"email": email, "password": password}
            )
    print(res.json())
    assert res.json().get("email") == email
    assert res.status_code == 201