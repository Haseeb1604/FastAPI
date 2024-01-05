from typing import List
from app import schema
import pytest

def test_get_all_posts(authorized_client,  test_posts):
    res = authorized_client.get("/posts/")
    def validation(post):
        return schema.Post(**post)
    
    post_map = map(validation, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unautherized_get_all_posts(client,  test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unautherized_get_one_posts(client,  test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

def test_posts_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/888888")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published",[
    ("title 1", "content 1", True),
    ("title 2", "Content 2", False),
    ("title 3", "Content 3", True),
])
def test_create_posts(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })
    assert res.status_code == 201

def test_create_posts_published_default(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={
        "title": "abc",
        "content": "content"})
    assert res.status_code == 201

def test_unautherized_create_posts(client, test_posts):
    res = client.post("/posts/", json={
        "title": "title",
        "content": "content",
        "published": "published"
    })
    assert res.status_code == 401

def test_unautherized_delete_posts(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_autherized_delete_posts(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_posts_not_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/9999999")
    assert res.status_code == 404

def test_delete_other_user_posts(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]

def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_update_post_unautherized(client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 401

def test_update_posts_not_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/99999", json=data)
    assert res.status_code == 404