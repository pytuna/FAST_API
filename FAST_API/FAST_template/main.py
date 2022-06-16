from typing import Union
import uvicorn
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates/")
def mySQLgetname(name):
    test = tuple()
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='classicmodels',
                                            user='root',
                                            password='TrungNam@1611') 
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute("SELECT * FROM customers")
            myresult = cursor.fetchall()
            for x in myresult:
                if name in x:
                    test = x
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return test

@app.get('/')
def read_form():
    return 'hello world sss'


@app.get("/form")
def form_post(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/form")
def form_post(request: Request, num: int = Form(...), num2: int = Form(...)):
    result = num+num2
    return templates.TemplateResponse('form.html', context={'request': request, 'result': 12})


@app.get("/mysql")
def form_post(request: Request):
    return templates.TemplateResponse('sql.html', context={'request': request})

@app.post("/mysql")
def form_sql_post(request: Request, name: str = Form(...)):
    result = mySQLgetname(name)
    return templates.TemplateResponse('sql.html', context={'request': request, 'result': result})
    

if __name__ == '__main__':
    uvicorn.run(app,debug = True)
    