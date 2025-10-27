from http import HTTPStatus

def test_create_and_get_user(client):
    payload = {"email": "qa@example.com", "full_name": "QA Engineer"}
    r = client.post("/users", json=payload)
    assert r.status_code == HTTPStatus.CREATED
    user = r.json()

    r2 = client.get(f"/users/{user['id']}")
    assert r2.status_code == HTTPStatus.OK
    assert r2.json()["email"] == payload["email"]

def test_unique_email_constraint(client):
    payload = {"email": "unique@example.com", "full_name": "Unique"}
    assert client.post("/users", json=payload).status_code == HTTPStatus.CREATED
    r = client.post("/users", json=payload)
    assert r.status_code == HTTPStatus.CONFLICT
    assert r.json()["detail"] == "email already exists"