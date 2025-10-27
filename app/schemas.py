from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    owner_id: int

class ItemOut(BaseModel):
    id: int
    name: str
    price: float
    owner_id: int
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    item_id: int
    quantity: int = Field(ge=1)

class OrderOut(BaseModel):
    id: int
    user_id: int
    item_id: int
    quantity: int
    class Config:
        from_attributes = True