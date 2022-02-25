from app import schemas
from tests.database import client, session


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Welcome to my API'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json = {'email':'test_email@test.com','password':'test_password'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'test_email@test.com'
    assert res.status_code == 201


def test_login_user(client):
    res = client.post("/login", data = {'username':'test_email@test.com','password':'test_password'})
    assert res.status_code == 200