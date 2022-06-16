from fastapi import FastAPI
import uvicorn
from enum import Enum
app = FastAPI()

@app.get("/")
async def root():
    return "This is root"


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"





@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

if __name__ == '__main__':
    uvicorn.run(app,debug = True)