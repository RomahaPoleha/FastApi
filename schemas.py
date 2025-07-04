#Реализация модели для API
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    quantity: int
    service: int
    ready: int
    reserve: int

class ItemCreate(ItemBase):
    pass
class ItemResponse(ItemBase):
    id:int
    for_shipment:int

    class Config:
        orm_mode=True