from typing import List
import pytest
from app import schema


def test_get_all_meals(authorized_client, test_meals):
    res = authorized_client.get('/meals/')

    def validate(meal):
        return schema.Meal(**meal)

    meal_map = map(validate, res.json())
    assert res.status_code == 200
    assert len(res.json()) == len(test_meals)


def test_get_one_meal(authorized_client, test_meals):
    res = authorized_client.get(f'/meals/{test_meals[0].id}')
    meal = schema.Meal(**res.json())
    assert meal.id == test_meals[0].id
    assert meal.name == test_meals[0].name


@pytest.mark.parametrize("name,slug,price,protein,fats,carbs,description,available_inventory,category_id", [
    ("Pelmeni", "borsch", '890', '15', '35', '50', "Pelmeni", '50', '1')
])
def test_create_meal(authorized_client, test_user, test_meals, name, slug, price, protein, fats, carbs, description,
                     available_inventory, category_id):
    res = authorized_client.post("/meals/", json={"name": name,
                                                  "slug": slug,
                                                  "price": price,
                                                  "protein": protein,
                                                  "fats": fats,
                                                  "carbs": carbs,
                                                  "description": description,
                                                  "available_inventory": available_inventory,
                                                  "category_id": category_id
                                                  })

    created_meal = schema.Meal(**res.json())
    assert res.status_code == 201
    assert created_meal.name == name
    assert created_meal.category_id == int(category_id)
    assert created_meal.slug == slug
    assert created_meal.description == description


@pytest.mark.parametrize("name,slug,price,protein,fats,carbs,description,available_inventory,category_id", [
    ("Tea with milk", "tea with milk", '590', '5', '55', '40', "Tea milk", '50', '1')
])
def test_unauthorized_user_create_meal(client, test_user, test_meals, name, slug, price, protein, fats,
                                       carbs, description,
                                       available_inventory, category_id):
    res = client.post("/meals", json={"name": name,
                                      "slug": slug,
                                      "price": price,
                                      "protein": protein,
                                      "fats": fats,
                                      "carbs": carbs,
                                      "description": description,
                                      "available_inventory": available_inventory,
                                      "category_id": category_id
                                      })
    assert res.status_code == 307


def test_unauthorized_user_delete_meal(client, test_user, test_meals):
    res = client.delete(f"/meals/{test_meals[0].id}")
    assert res.status_code == 401


def test_delete_meal(authorized_client, test_user, test_meals):
    res = authorized_client.delete(f"/meals/{test_meals[0].id}")
    assert res.status_code == 204


def test_delete_meal_non_exist(authorized_client, test_user, test_meals):
    res = authorized_client.delete(f"/meals/897465")
    assert res.status_code == 404


def test_update_meal(authorized_client, test_user, test_meals):
    data = {
        "name": "Чай с молоком updated",
        "slug": "tea with milk",
        "price": 50,
        "protein": 38,
        "fats": 29,
        "carbs": 43,
        "description": "Чай с молоком updated",
        "available_inventory": 40,
        "category_id": 1
    }
    res = authorized_client.put(f"/meals/{test_meals[0].id}", json=data)
    updated_meal = schema.Meal(**res.json())
    assert res.status_code == 200
    assert updated_meal.name == data['name']
    assert updated_meal.description == data['description']


def test_unauthorized_user_update_meal(client, test_user, test_meals):
    res = client.put(f"/meals/{test_meals[0].id}")
    assert res.status_code == 401


def test_update_meal_non_exist(authorized_client, test_user, test_meals):
    data = {
        "name": "Чай с молоком updated",
        "slug": "tea with milk",
        "price": 50,
        "protein": 38,
        "fats": 29,
        "carbs": 43,
        "description": "Чай с молоком updated",
        "available_inventory": 40,
        "category_id": 1
    }
    res = authorized_client.put(f"/meals/897465", json=data)
    assert res.status_code == 404
