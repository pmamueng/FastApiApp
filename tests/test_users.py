import pytest

from app import schemas
from app.config import settings
from jose import jwt


# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == 'Welcome to my API'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json = {'email':'test_email@test.com','password':'test_password'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'test_email@test.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data = {'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'test_password', 403),
    ('test_email@test.com', 'wrongPassword', 403),
    ('wrongemail@test.com', 'wrongPassword', 403),
    (None, 'test_password', 422),
    ('test_email@test.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data = {'username': email, 'password': password})
    assert res.status_code == status_code
