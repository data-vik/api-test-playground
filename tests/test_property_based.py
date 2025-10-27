from hypothesis import given, strategies as st
from http import HTTPStatus

@given(name=st.text(min_size=1, max_size=20), price=st.floats(min_value=0.01, max_value=9999))
def test_item_property_based_happy(client, name, price):
    # ensure email is simple/valid-esque; replace non-alnum for local-part
    safe = ''.join(ch if ch.isalnum() else 'x' for ch in name)
    u = client.post("/users", json={"email": f"{safe}@ex.com", "full_name": name}).json()
    r = client.post("/items", json={"name": name, "price": float(price), "owner_id": u["id"]})
    assert r.status_code == HTTPStatus.CREATED