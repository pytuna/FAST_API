import uvicorn
from typing import Union
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel
app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Union[Item, None] = None, user: Union[User, None] = None):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

@app.put("/items3/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0, description="HAHA"),
    q: Union[str, None] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

@app.put("/items4/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
if __name__ == '__main__':
    uvicorn.run(app, debug = True)