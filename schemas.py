#Реализация модели для API
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    quantity: int

class ItemCreate(ItemBase):
    pass
class ItemResponse(ItemBase):
    id:int

    class Config:
        orm_mode=True