from sqlalchemy.orm import Session
from . import models

SAMPLE_USERS = [
    {"email": "alice@example.com", "full_name": "Alice Johnson"},
    {"email": "bob@example.com", "full_name": "Bob Smith"},
]

SAMPLE_ITEMS = [
    {"name": "Widget", "price": 19.99, "owner_email": "alice@example.com"},
    {"name": "Gadget", "price": 29.5, "owner_email": "bob@example.com"},
]

def seed(db: Session):
    email_to_id = {}
    for u in SAMPLE_USERS:
        user = db.query(models.User).filter_by(email=u["email"]).first()
        if not user:
            user = models.User(**u)
            db.add(user)
            db.commit(); db.refresh(user)
        email_to_id[u["email"]] = user.id
    for it in SAMPLE_ITEMS:
        owner_id = email_to_id[it.pop("owner_email")]
        exists = db.query(models.Item).filter_by(name=it["name"], owner_id=owner_id).first()
        if not exists:
            item = models.Item(owner_id=owner_id, **it)
            db.add(item)
            db.commit()