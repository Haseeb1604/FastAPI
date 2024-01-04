from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("data") == "Hello World"
    assert res.status_code == 200

def test_user():
    res = client.post(
        "/users/", 
        json={"email": "haseeb@gmail.com", "password": "1234"}
            )
    print(res.json())
    assert res.status_code == 201