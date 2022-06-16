import uvicorn
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Query

app = FastAPI()


# Tham số truy vấn và xác thực chuỗi


@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=2,max_length=16)): #, regex="^fixedquery$"
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Danh sách tham số truy vấn / nhiều giá trị

@app.get("/items2/")
async def read_items(q: Union[list[str], None] = Query(default=["Duc", "Ngu"])):
    query_items = {"q": q}
    return query_items

@app.get("/items3/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items4/")
async def read_items(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items5/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        #regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items6/")
async def read_items(
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
if __name__ == '__main__':
    uvicorn.run(app, debug = True)
    
# Tóm tắt lại¶
# Bạn có thể khai báo các xác thực và siêu dữ liệu bổ sung cho các tham số của mình.

# Xác thực chung và siêu dữ liệu:

# alias
# title
# description
# deprecated
# Xác thực cụ thể cho các chuỗi:

# min_length
# max_length
# regex
# Trong các ví dụ này, bạn đã thấy cách khai báo xác thực cho strcác giá trị.

# Xem các chương tiếp theo để biết cách khai báo xác thực cho các kiểu khác, chẳng hạn như số.
