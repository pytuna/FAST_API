from unittest import result
from fastapi import FastAPI, Query
import uvicorn
from enum import Enum
from typing import Union
from pydantic import BaseModel
import platform
import cpuinfo
import psutil
app = FastAPI()
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# async def read_user_item(
#     item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
# ):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/items/")
async def read_items(q: Union[list[str], None] = Query(default=None,min_length=2, max_length=5)): #... bat buoc
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    results.update({"cpu": platform.processor()+" "+cpuinfo.get_cpu_info()['brand_raw']})
    if q:
        results.update({"q": q})
    return results

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}



@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/test/")
async def read_test(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None




@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.get("/cpu/{user}")
async def get_cpu(user: str):
    results = dict()
    if user == "admin":
        results.update({"cpu": platform.processor()+" "+cpuinfo.get_cpu_info()['brand_raw']+" "+str(psutil.cpu_percent())})
        results.update({"RAM": psutil.virtual_memory()[2]})
    return results

if __name__ == '__main__':
    uvicorn.run(app,debug = True)