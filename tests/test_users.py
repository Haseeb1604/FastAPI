import pytest
from jose import jwt
from app import schema
from app.config import settings


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

@pytest.mark.parametrize("email, password, status_code",[
    ("abc@gmail.com", "wrongpass", 403),
    (None, "abc", 422),
    ("abc@gmail.com", None, 422)
]
)
def test_invalid_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password}
    )

    # assert res.json().get("detail") == "Invalid Credentails"
    assert res.status_code == status_code

