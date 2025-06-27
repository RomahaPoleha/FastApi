from fastapi import FastAPI
from models import ItemCreate,ItemResponse
import uvicorn

app = FastAPI()
items = [] # Место где хранится вся информация о добавленых еденицах оборудования
current_id = 1 # Уникальный ID  считается автоматически

# добавить оборудование
@app.post("/items/",response_model=ItemResponse)
def create_items(item:ItemCreate):
    global current_id
    new_item = ItemResponse(id=current_id, **item.dict())
    items.append(new_item)
    current_id += 1
    return new_item

# Вывести всё оборудование
@app.get("/items/",response_model=list[ItemResponse])
def get_items():
    return items

# Вывести оборудование по ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_items(item_id: int):
    for item in items:
        if item.id == item_id:
            return item



# Внести изменения количество( минус)
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_items_сalculation(item_id: int, updated_item: ItemCreate):
    for item in items:
        if item.id == item_id:

            # item.name = updated_item.name - #вносит изменение в имя(в данном случае в этом нет необходимости)
            item.quantity =  item.quantity - updated_item.quantity #Вносит изменения в количесвто
            return item

# Внести изменения количество(плюс)
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_items_addition(item_id: int, updated_item: ItemCreate):
    for item in items:
        if item.id == item_id:

            # item.name = updated_item.name - #вносит изменение в имя(в данном случае в этом нет необходимости)
            item.quantity =  item.quantity + updated_item.quantity #Вносит изменения в количесвто
            return item

# Удаление позиции
@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    for i ,item in enumerate(items):
        if item.id==item_id:
            del items[i]
            return {"message": f"Объект {item} успешно удалён "}






if __name__=="__main__":
    uvicorn.run("main:app", reload=True)