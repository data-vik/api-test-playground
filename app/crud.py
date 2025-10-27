from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

# Users
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    obj = models.User(email=user.email, full_name=user.full_name)
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="email already exists")
    db.refresh(obj)
    return obj

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def list_users(db: Session, q: str | None = None):
    qry = db.query(models.User)
    if q:
        qry = qry.filter(models.User.full_name.ilike(f"%{q}%"))
    return qry.order_by(models.User.id.asc()).all()

# Items
def create_item(db: Session, item: schemas.ItemCreate):
    # ensure owner exists
    if not get_user(db, item.owner_id):
        raise HTTPException(status_code=400, detail="owner not found")
    obj = models.Item(name=item.name, price=item.price, owner_id=item.owner_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def list_items(db: Session, owner_id: int | None = None):
    qry = db.query(models.Item)
    if owner_id:
        qry = qry.filter(models.Item.owner_id == owner_id)
    return qry.order_by(models.Item.id.asc()).all()

# Orders
def create_order(db: Session, order: schemas.OrderCreate):
    if not get_user(db, order.user_id):
        raise HTTPException(status_code=400, detail="user not found")
    if not get_item(db, order.item_id):
        raise HTTPException(status_code=400, detail="item not found")
    obj = models.Order(user_id=order.user_id, item_id=order.item_id, quantity=order.quantity)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def list_orders(db: Session, user_id: int | None = None):
    qry = db.query(models.Order)
    if user_id:
        qry = qry.filter(models.Order.user_id == user_id)
    return qry.order_by(models.Order.id.asc()).all()