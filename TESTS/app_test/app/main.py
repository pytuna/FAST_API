from unicodedata import name
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import List, Union
from mysql.connector.connection_cext import CMySQLConnection
import uvicorn
from fastapi import FastAPI, Path, Query,Request
from fastapi.responses import RedirectResponse
app = FastAPI()

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                        database='cardinfo',
                                        user='root',
                                        password='TrungNam@1611') 
    print(type(connection))
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        # cursor.execute("SELECT * FROM cardinfo.card_status;")
        # myresult = cursor.fetchall()
        # print(myresult)
        
        # cursor.execute("SHOW COLUMNS FROM card_status;")
        # myresult = cursor.fetchall()
        # for i in myresult:
        #     print(i[0])

except Error as e:
    print("Error while connecting to MySQL", e)

class Card(BaseModel):
    id: int
    sub01: bool
    sub02: bool
    sub03: bool
    sub04: bool
    sub05: bool
    sub06: bool
    sub07: bool
    sub08: bool
    sub09: bool
    sub10: bool
    sub11: bool
    sub11: bool
    sub12: bool
    sub13: bool
    sub14: bool
    def __init__(__pydantic_self__, **data) -> None:
        super().__init__(**data)

def get_database(connection:CMySQLConnection, id):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM cardinfo.card_status where idcard_status={id};")
    try:
        myresult = cursor.fetchall()[0] 
        print(myresult)
        return Card(id=myresult[0],
        sub01=myresult[1], sub02=myresult[2], 
        sub03=myresult[3], sub04=myresult[4], 
        sub05=myresult[5], sub06=myresult[6], 
        sub07=myresult[7], sub08=myresult[8],
        sub09=myresult[9], sub10=myresult[10], 
        sub11=myresult[11], sub12=myresult[12], 
        sub13=myresult[13], sub14=myresult[14])
    except:
        return {"message": "No found card"}

    


@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return RedirectResponse(url="/card")

@app.get("/card")
async def get_card():
    return {"message": "hehe"}

@app.get("/card/id")
async def get_card_id(
    id_card: int = Query(default=...)):
    return get_database(connection=connection, id=id_card)

@app.get("/items/")
async def read_items(
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

if __name__=="__main__":
    uvicorn.run(app,debug = True)
    