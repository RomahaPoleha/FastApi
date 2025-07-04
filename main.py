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

@app.post("/items/",response_model=ItemResponse,summary="Создать запись о товаре",tags=["Items"])
def create_items(item:ItemCreate, db: Session=Depends(get_db)):
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/",response_model=list[ItemResponse],summary="Получить список товаров",tags=["Items"])
def get_items(db: Session = Depends(get_db)):
    items=db.query(ItemModel).all()
    return items

def read_items(item_id: int,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first() #поиск через SQLAlchemy
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return item

@app.put("/items/items_subtraction/{item_id}", response_model=ItemResponse,summary="Уменьшить общее количество товара",tags=["Items"])
def update_items_subtraction(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    item.quantity =  item.quantity - updated_item.quantity # Выполняет математическое действие -
    db.commit() #Сохраняем изменения в БД
    return item

@app.put("/items/items_addition/{item_id}", response_model=ItemResponse,summary="Увеличить общее количество товара",tags=["Items"])
def update_items_addition(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    item.quantity = item.quantity + updated_item.quantity  # Выполняет математическое действие +
    db.commit()  # Сохраняем изменения в БД
    return item

@app.delete("/items/{item_id}",summary="Удалить товар по ID",tags=["Items"])
def delete_item(item_id:int,db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id==item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(db_item)
    db.commit()
    return {"message": f"Объект успешно удалён "}




@app.put("/items/decrease_from_service/{item_id}", response_model=ItemResponse,summary="Уменьшить количество в сервисе",tags=["Service"])
def update_items_subtraction(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if item.service<=0:
        raise HTTPException(status_code=404, detail="Количество не достаточно")
    else:
        item.service = item.service - updated_item.service # Выполняет математическое действие -
        db.commit() #Сохраняем изменения в БД
    return item


@app.put("/items/adding_to_service/{item_id}", response_model=ItemResponse,summary="Увеличить количество в сервисе",tags=["Service"])
def update_items_subtraction(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    item.service =  item.service + updated_item.service # Выполняет математическое действие +
    db.commit() #Сохраняем изменения в БД
    return item

@app.put("/items/items_ready_decrease/{item_id}", response_model=ItemResponse,summary="Уменьшить предпродаженное количество товара",tags=["Ready"])
def update_items_subtraction(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if item.ready<=0:
        raise HTTPException(status_code=404, detail="Количество недостаточно")
    else:
        item.ready =  item.ready - updated_item.ready # Выполняет математическое действие -
        db.commit() #Сохраняем изменения в БД
    return item

@app.put("/items/items_ready_adding/{item_id}", response_model=ItemResponse,summary="Увеличить предпродаженное количество товара",tags=["Ready"])
def update_items_subtraction(item_id: int, updated_item: ItemCreate,db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    item.ready =  item.ready + updated_item.ready # Выполняет математическое действие +
    db.commit() #Сохраняем изменения в БД
    return item

if __name__=="__main__":
    uvicorn.run("main:app", reload=True)