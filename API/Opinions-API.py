from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

def lookForsignup(email:str):
    connect=sqlite3.connect("signup.db")
    cursor=connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS sign_up(
                      email text,
                      password text,
                      username text,
                      name text)""")
    cursor.execute("SELECT * FROM sign_up")
    info=cursor.fetchall()
    for i in info:
        if i[0]==email:
            return True
        else:
            pass
    return False

app=FastAPI()

@app.get("/get/bool/{email}")
def get_email_bool(email:str):
    statement=lookForsignup(email)
    return {"Result":f"{statement}"}

#soon...it will be completed soon
