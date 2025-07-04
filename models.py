#Реализация моделей для БД
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column,Integer,String
from database import Base

class ItemModel(Base):
    __tablename__="items"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String) #имя устройства
    quantity=Column(Integer)# Количество всего
    service=Column(Integer) #В сервисе
    ready=Column(Integer) #Прошло предпродажку
    reserve=Column(Integer)# Резерв

    @hybrid_property
    def for_shipment(self):
        return self.quantity - self.service - self.reserve