from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import tokenGenerator
import smtplib
import random
from email.message import EmailMessage
import bcrypt

token=tokenGenerator.generate()

dictionary={}

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

def hashCode(password:str):
    password=password.encode("utf-8")
    salt=bcrypt.gensalt()
    return bcrypt.hashpw(password,salt)

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
        password=hashCode(data.password)
        password=password.decode("utf-8")
        information=postingEmail(data.email,password,data.username,data.name)
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
        password = "APP_ PASS WORD"
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

class LoggingIn(BaseModel):
    email:str
    password:str

def EmailPasswords(email:str,password:str):
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
            verify=verifyPassword(password,i[1].encode("utf-8"))
            if verify is True:
                return True
            else:
                return False
    return False

def verifyPassword(password:str,hashPassword:bytes):
    password=password.encode("utf-8")
    return bcrypt.checkpw(password,hashPassword)

@app.post("/check/email/password")
def logging(user:LoggingIn):
    information=EmailPasswords(user.email,user.password)
    return {"Result":information}

class CreateOpinion(BaseModel):
    email:str
    password:str
    username:str
    name:str
    content:str

def createPost(username:str,name:str,date:str,postid:int,content:str):
    connect=sqlite3.connect("Opinions-DB.db")
    cursor=connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS opinions(
                        content text,
                        username text,
                        name text,
                        date str,
                        postid int)""")
    cursor.execute("INSERT INTO opinions VALUES (?,?,?,?,?)",[content,username,name,date,postid])
    connect.commit()

def length():
    connect=sqlite3.connect("Opinions-DB.db")
    cursor=connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS opinions(
                            content text,
                            username text,
                            name text,
                            date str,
                            postid int)""")
    cursor.execute("SELECT * FROM opinions")
    info=cursor.fetchall()
    n=len(info)
    return -(n+1)

@app.post("/post/opinion")
def postOpinion(user:CreateOpinion):
    result=EmailPasswords(user.email,user.password)
    if result is True:
        time=f"\"{datetime.now()}\" GMT +05:30"
        createPost(user.username,user.name,time,length(),user.content)
        return {"Result":True}
    else:
        return {"Failed":False}

def userName(email:str):
    connect=sqlite3.connect("signup.db")
    cursor=connect.cursor()
    cursor.execute("SELECT * FROM sign_up WHERE email=?",[email])
    data=cursor.fetchone()
    return {"username":data[2],"name":data[3]}

@app.get("/username/name/{email}")
def getUsername(email:str):
    return userName(email)

#soon...it will be completed soon
