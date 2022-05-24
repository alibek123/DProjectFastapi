def test_unauthorized_user_add_to_cart(client, test_user, test_meals):
    res = client.get(f"/cart/")
    assert res.status_code == 401


def test_authorized_user_add_to_cart(authorized_client, test_user, test_meals):
    res = authorized_client.get(f"/cart/")
    assert res.status_code == 404
