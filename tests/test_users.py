import pytest
from app import schema
from app.config import settings
from jose import jwt


def test_create_user(client):
    res = client.post("/users/", json={"username": "Aruzhan",
                                       "email": "ashimovazhaan@gmail.com",
                                       "first_name": "Aruzhan",
                                       "last_name": "Ashimova",
                                       "phone": "7752131533",
                                       "password": "admin",
                                       "balance": "100000"})
    new_user = schema.User(**res.json())
    assert new_user.email == "ashimovazhaan@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", json={"email": test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "admin", 403),
    ("wrong", "admin", 422),
    (None, "admin", 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", json={"email": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Неправильные данные"
