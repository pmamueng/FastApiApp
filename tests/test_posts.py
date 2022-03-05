import pytest

from app import schemas
from tests.conftest import authorized_client


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.ResponsePost(**post)
    map(validate, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.ResponsePostVotesCount(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("test_first_title_post", "test_first_content_post", True),
    ("test_second_title_post", "test_second_content_post", False),
    ("test_third_title_post", "test_third_content_post", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json = {"title": title, "content": content, "published": published})
    created_post = schemas.ResponsePost(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json = {"title": "test_title", "content": "test_content"})
    created_post = schemas.ResponsePost(**res.json())
    assert res.status_code == 201
    assert created_post.title == "test_title"
    assert created_post.content == "test_content"
    assert created_post.published == True
    assert created_post.user_id == test_user['id']


def test_unauthorized_user_post_post(client, test_posts):
    res = client.post("/posts/", json = {"title": "test_title", "content": "test_content"})
    assert res.status_code == 401
