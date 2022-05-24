def test_unauthorized_user_make_order(client, test_user, test_meals):
    res = client.put(f"/meals/{test_meals[0].id}")
    assert res.status_code == 401
