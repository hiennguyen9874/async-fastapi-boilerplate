from typing import Optional

from pydantic import BaseModel

from app.schemas.user import User, UserInDB, UserInDBBase


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    class Config:
        orm_mode = True

    id: int
    title: str
    owner: UserInDBBase


# Properties to return to client
class Item(ItemInDBBase):
    class Config:
        orm_mode = True

    owner: User


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    class Config:
        orm_mode = True

    owner: UserInDB
