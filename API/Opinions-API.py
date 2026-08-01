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

def postingEmail(email,password,username,name):
    try:
        connect=sqlite3.connect("signup.db")
        cursor=connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS sign_up(
                       email text,
                       password text,
                       username text,
                       name text)""")
        cursor.execute("INSERT INTO sign_up VALUES (?,?,?,?)",[email,password,username,name])
        connect.commit()
        return "Done"
    except Exception as e:
        return e

app=FastAPI()

class SigningUp(BaseModel):
    email:str
    password:str
    username:str
    name:str

@app.get("/get/bool/{email}")
def get_email_bool(email:str):
    statement=lookForsignup(email)
    return {"Result":f"{statement}"}

@app.post("/post/signup/account")
def post_email(data:SigningUp):
    information=postingEmail(data.email,data.password,data.username,data.name)
    return {"Result":information}

#soon...it will be completed soon
