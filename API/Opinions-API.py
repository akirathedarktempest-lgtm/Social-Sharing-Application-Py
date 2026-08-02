from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import tokenGenerator

token=tokenGenerator.generate()

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
    TOKEN:str

@app.get("/get/bool/{email}")
def get_email_bool(email:str):
    statement=lookForsignup(email)
    return {"Result":statement}

@app.post("/post/signup/account")
def post_email(data:SigningUp):
    global token
    if token==data.TOKEN:
        information=postingEmail(data.email,data.password,data.username,data.name)
        token=token.replace(token,tokenGenerator.generate())
        return {"Result":information}
    else:
        return {"Wrong Token":"Not valid!"}

@app.get("/get/token/{email}")
def tokenAccess(email:str):
    global token
    information=lookForsignup(email)
    if information is True:
        return {"You can't access":"Refuses"}
    else:
        return {"TOKEN":token}

#soon...it will be completed soon
