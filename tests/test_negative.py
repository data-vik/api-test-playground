from http import HTTPStatus

def test_get_user_404(client):
    r = client.get("/users/424242")
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert r.json()["detail"] == "user not found"

def test_validation_errors(client):
    # invalid email
    r = client.post("/users", json={"email": "not-an-email", "full_name": "X"})
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # invalid price
    # owner must exist first
    u = client.post("/users", json={"email": "p@test.com", "full_name": "P"}).json()
    r2 = client.post("/items", json={"name": "A", "price": -1, "owner_id": u["id"]})
    assert r2.status_code == HTTPStatus.UNPROCESSABLE_ENTITY