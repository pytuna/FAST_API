import uvicorn
from typing import Union

from fastapi import FastAPI
# Khi khai báo các tham số hàm khác không phải là một phần của tham số đường dẫn, 
# chúng sẽ tự động được hiểu là tham số "truy vấn".



app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# Truy vấn là tập hợp các cặp khóa-giá trị đi sau ? trong URL,
# được phân tách bằng &ký tự.

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return str(fake_items_db[skip : skip + limit])

@app.get("/items/{item_id}") #tham số "truy vấn" q: Union[str, None] = None, short: bool = False)
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# một số có giá trị mặc định và một số hoàn toàn tùy chọn:
@app.get("/items2/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

if __name__ == '__main__':
    uvicorn.run(app, debug = True)