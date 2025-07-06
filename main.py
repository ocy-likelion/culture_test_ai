from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"안녕하십니까, 기업 컬쳐핏 ai 성향 테스트 c팀의 AI쪽을 담당하는 서버입니다"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}
    

@app.get("/hi")
def add():
    return {"helloooooo"}
    