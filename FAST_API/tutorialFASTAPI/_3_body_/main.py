import uvicorn
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Yêu cầu thông số nội dung + đường dẫn
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Yêu cầu nội dung + đường dẫn + tham số truy vấn
@app.put("/items2/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    print
    if q:
        result.update({"q": q})
    return result


if __name__ == '__main__':
    uvicorn.run(app, debug = True)