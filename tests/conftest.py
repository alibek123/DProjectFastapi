from app.config import settings
from app.database import get_db, Base
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.oauth2 import create_access_token
from app import models, schema

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"username": "Alibek",
                 "email": "zhumash6@gmail.com",
                 "first_name": "Alibek",
                 "last_name": "Zhumash",
                 "phone": "7752131533",
                 "password": "admin",
                 "is_staff": "true"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.is_staff = True
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client


@pytest.fixture
def test_meals(test_user, session):
    new_category = models.Category(**{"name": "Гарниры",
                                      "slug": "garniri"})
    session.add(new_category)
    session.commit()
    posts_data = [
        {
            "name": "Чай с молоком",
            "slug": "tea with milk",
            "price": 50,
            "protein": 38,
            "fats": 29,
            "carbs": 43,
            "description": "Чай с молоком",
            "available_inventory": 40,
            "category_id": 1
        },
        {
            "name": "Чай с молоком",
            "slug": "tea with milk",
            "price": 50,
            "protein": 38,
            "fats": 29,
            "carbs": 43,
            "description": "Чай с молоком",
            "available_inventory": 40,
            "category_id": 1
        },
        {
            "name": "Чай с молоком",
            "slug": "tea with milk",
            "price": 50,
            "protein": 38,
            "fats": 29,
            "carbs": 43,
            "description": "Чай с молоком",
            "available_inventory": 40,
            "category_id": 1
        }
    ]

    def create_meal(meal):
        return models.Meal(**meal)

    meal_map = map(create_meal, posts_data)
    meals = list(meal_map)
    session.add_all(meals)
    session.commit()
    meals = session.query(models.Meal).all()
    return meals
