from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app=FastAPI()

def Emails():
    connect=sqlite3.connect("signup.db")
    cursor=connect.cursor()
    cursor.execute("SELECT * FROM signup")
    info=cursor.fetchall()
    l=[]
    for i in info:
        l.append(i[0])
    return l

@app.get("/api/signup/get/{email}")
def dataEmails(email:str):
    data=Emails()
    if email in data:
        return {"Already":"In The Database"}
    else:
        return {"Can":"Be Added"}

#we will build this slowly slowly, and i could think of this only for now
