from http import HTTPStatus

def test_create_order_flow(client):
    u = client.post("/users", json={"email": "buyer@example.com", "full_name": "Buyer"}).json()
    i = client.post("/items", json={"name": "Gizmo", "price": 5.0, "owner_id": u["id"]}).json()

    r = client.post("/orders", json={"user_id": u["id"], "item_id": i["id"], "quantity": 2})
    assert r.status_code == HTTPStatus.CREATED
    order = r.json()
    assert order["quantity"] == 2

    got = client.get(f"/orders/{order['id']}")
    assert got.status_code == HTTPStatus.OK