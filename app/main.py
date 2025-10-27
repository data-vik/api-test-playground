from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from . import crud, schemas
from .settings import settings
from .seed import seed as seed_data

app = FastAPI(title=settings.app_name)

# init DB
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup():
    if settings.seed:
        with next(get_db()) as db:
            seed_data(db)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

# Users
@app.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=list[schemas.UserOut])
def list_users(q: str | None = Query(default=None, description="Search by name"), db: Session = Depends(get_db)):
    return crud.list_users(db, q)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    obj = crud.get_user(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="user not found")
    return obj

# Items
@app.post("/items", response_model=schemas.ItemOut, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/items", response_model=list[schemas.ItemOut])
def list_items(owner_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_items(db, owner_id)

@app.get("/items/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = crud.get_item(db, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="item not found")
    return obj

# Orders
@app.post("/orders", response_model=schemas.OrderOut, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.get("/orders", response_model=list[schemas.OrderOut])
def list_orders(user_id: int | None = None, db: Session = Depends(get_db)):
    return crud.list_orders(db, user_id)

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    obj = crud.get_order(db, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="order not found")
    return obj