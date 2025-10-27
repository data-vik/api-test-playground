from http import HTTPStatus

def test_create_item_requires_owner(client):
    r = client.post("/items", json={"name": "Thing", "price": 10.0, "owner_id": 999})
    assert r.status_code == HTTPStatus.BAD_REQUEST
    assert r.json()["detail"] == "owner not found"

def test_create_item_happy_path(client):
    u = client.post("/users", json={"email": "iowner@example.com", "full_name": "Owner"}).json()
    r = client.post("/items", json={"name": "Widget", "price": 12.5, "owner_id": u["id"]})
    assert r.status_code == HTTPStatus.CREATED
    data = r.json()
    assert data["owner_id"] == u["id"]
    assert data["price"] == 12.5