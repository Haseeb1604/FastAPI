import pytest
from jose import jwt
from app import schema
from .database import client, session
from app.config import settings

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "abc@gmail.com",
        "password": "1234"
    }

    res = client.post("/users/", json=user_data)
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert res.status_code == 201
    return new_user

# def test_root(client):
#     res = client.get("/")
#     print(res.json())
#     assert res.json().get("data") == "Hello World"
#     assert res.status_code == 200

def test_user_create(client):
    res = client.post(
        "/users/", 
        json={"email": "abc@gmail.com", "password": "1234"}
            )
    new_user = schema.UserOut(**res.json())
    print(new_user.email)
    assert new_user.email == "abc@gmail.com"
    assert res.status_code == 201

def test_user_login(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, settings.ALGORITHM)
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200