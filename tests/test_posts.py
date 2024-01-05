from typing import List
from app import schema

def test_get_all_posts(authorized_client, test_user, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200