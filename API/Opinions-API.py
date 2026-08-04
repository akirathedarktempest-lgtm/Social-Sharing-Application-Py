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

def returnCode():
    code=""
    for _ in range(6):
        code+=random.choice("0123456789")
    return code

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

@app.get("/get/code/{email}")
def confirmationCode(email:str):
    global dictionary
    information=lookForsignup(email)
    if information is True:
        return {"You are...":"...already there"}
    else:
        code=returnCode()
        dictionary[email]=code
        sender = "EMAIL"
        password = "APP PASSWORD"
        reciever=email
        message=EmailMessage()
        message["From"]=sender
        message["To"]=reciever
        message["Subject"]="Your verification code"
        message.set_content(f"""
Your verification code: {code}

If you didn't request this, you can safely ignore this""")
        server=smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login(sender,password)
        server.send_message(message)
        return {"It's out!":"The email is send!"}

@app.get("/check/confirmation/{email}/{code}")
def confirm(email:str,code:str):
    global dictionary
    if email in dictionary:
        if code==dictionary[email]:
            return {"Confirmed":True}
        else:
            return {"Wrong":False}
    else:
        return {"Not present":"No email code went!"}

#soon...it will be completed soon
