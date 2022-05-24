def test_unauthorized_user_add_to_cart(client, test_user, test_meals):
    res = client.put(f"/meals/{test_meals[0].id}")
    assert res.status_code == 401
