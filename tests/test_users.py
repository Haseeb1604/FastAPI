import pytest
from app import schema


def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get("data") == "Hello World"
    assert res.status_code == 200



@pytest.mark.parametrize("email, password", 
    [
        ("mhaseeb1@gmail.com", "1234"),
    ]
)
def test_user(client, email, password):
    res = client.post(
        "/users/", 
        json={"email": email, "password": password}
            )
    new_user = schema.UserOut(**res.json())
    print(new_user.email)
    assert new_user.email == email
    assert res.status_code == 201