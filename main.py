from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import ItemModel
from schemas import ItemCreate, ItemResponse
import database
import uvicorn

app = FastAPI()


#Создание таблицы в БД при запуске
database.Base.metadata.create_all(bind=database.engine)


#Зависимость для получения сессии БД
def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



# добавить оборудование
@app.post("/items/",response_model=ItemResponse)
def create_items(item:ItemCreate, db: Session=Depends(get_db)):
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Вывести всё оборудование
@app.get("/items/",response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items=db.query(ItemModel).all()
    return items

# Вывести оборудование по ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_items(item_id: int,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first() #поиск через SQLAlchemy
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item

# Внести изменения количество(минус)
@app.put("/items/items_subtraction{item_id}", response_model=ItemResponse)
def update_items_subtraction(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    item.quantity =  item.quantity - updated_item.quantity # Выполняет математическое действие -
    db.commit() #Сохраняем изменения в БД
    return item

# Внести изменения количество(плюс)
@app.put("/items/items_addition/{item_id}", response_model=ItemResponse)
def update_items_addition(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    item.quantity = item.quantity + updated_item.quantity  # Выполняет математическое действие +
    db.commit()  # Сохраняем изменения в БД
    return item

# # Удаление позиции
# @app.delete("/items/{item_id}")
# def delete_item(item_id:int):
#     for i ,item in enumerate(items):
#         if item.id==item_id:
#             del items[i]
#             return {"message": f"Объект {item} успешно удалён "}






if __name__=="__main__":
    uvicorn.run("main:app", reload=True)