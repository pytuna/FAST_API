import mysql.connector
from mysql.connector import Error

def connect_database(*, host="localhost", database='sys_info', user='root', password='TrungNam@1611'):
    connection = mysql.connector.connect(host=host,
                                            database=database,
                                            user=user,
                                            password=password)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        return cursor
    return None

def insert_info_ram(cursor=None, *args, **kwagrs):
    cursor.execute("select database();")


if __name__=="__main__":
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='sys_info',
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
            cursor.execute("SELECT * FROM sys_info.new_table;")
            myresult = cursor.fetchall()
            print(myresult)
        
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")