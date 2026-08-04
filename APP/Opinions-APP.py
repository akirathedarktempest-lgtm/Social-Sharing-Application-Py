from tkinter import *
import json
import requests
import validators
import tokenGenerator

root=Tk()

def SignUpPage():
    global root
    sign_up_page=Tk()
    root.destroy()
    root=sign_up_page
    label1=Label(root,text="Email")
    label1.pack()
    e1=Entry(root)
    e1.pack()
    label2=Label(root,text="Password")
    label2.pack()
    e2=Entry(root)
    e2.pack()
    label3=Label(root,text="Name")
    label3.pack()
    e3=Entry(root)
    e3.pack()
    signup=Button(root,text="Sign-Up!",command=lambda:SignUp(e1,e2,e3,root))
    signup.pack()

def SignUp(e1:Entry,e2:Entry,e3:Entry,root:Tk):
    if str(e1.get())=="" or str(e2.get())=="" or " " in str(e1.get()) or " " in str(e2.get()):
        wrongSignUp=Tk()
        root.destroy()
        labelWrong=Label(wrongSignUp,text="You have given invalid email or password :(")
        labelWrong.pack()
        return
    if validators.email(str(e1.get())) is False:
        wrongSignUp=Tk()
        root.destroy()
        labelWrong=Label(wrongSignUp,text="Invalid email :(")
        labelWrong.pack()
        return
    if validators.email(str(e1.get())) is True:
        data=requests.get(f"http://127.0.0.1:8000/get/bool/{str(e1.get())}")
        data=data.content
        data=data.decode("utf-8")
        data=json.loads(data)
        if data["Result"] is True:
            wrong=Tk()
            root.destroy()
            root=wrong
            label=Label(root,text="The email is already there!")
            label.pack()
            return
        response=requests.get(f"http://127.0.0.1:8000/get/code/{str(e1.get())}")
        print(response.status_code)
        confirmationCode=Tk()
        entry1=str(e1.get())
        entry2=str(e2.get())
        entry3=str(e3.get())
        root.destroy()
        root=confirmationCode
        code_entry=Label(root,text="Confirmation Code\nCheck your email")
        code_entry.pack()
        entry=Entry(root)
        entry.pack()
        username=entry3
        if " " in username:
            username=username.replace(" ","")
        if ""==username:
            username=entry1.split("@")
            username=username[0]
        confirmingButton=Button(root,text="Enter Code",command=lambda:ConfirmationCode(root=root,email=entry1,password=entry2,username=tokenGenerator.Username(username),name=entry3,entry=str(entry.get())))
        confirmingButton.pack()

def ConfirmationCode(root:Tk,email:str,password:str,username:str,name:str,entry:str):
    response=requests.get(f"http://127.0.0.1:8000/check/confirmation/{email}/{entry}")
    response=response.content
    response=response.decode("utf-8")
    response=json.loads(response)
    if "Confirmed" in response:
        TOKEN=requests.get(f"http://127.0.0.1:8000/get/token/{email}")
        TOKEN=TOKEN.content
        TOKEN=TOKEN.decode("utf-8")
        TOKEN=json.loads(TOKEN)
        new_window=Tk()
        root.destroy()
        root=new_window
        data={"email":email,"password":password,"username":username,"name":name,"TOKEN":TOKEN["TOKEN"]}
        send_data=requests.post("http://127.0.0.1:8000/post/signup/account",json=data)
        print(send_data.status_code)
        label=Label(root,text="Welcome!")
        label.pack()
    else:
        new_window=Tk()
        root.destroy()
        root=new_window
        label=Label(root,text="Wrong code!")
        label.pack()
    return

signup_page=Button(root,text="Sign Up",command=SignUpPage)
signup_page.pack()

root.mainloop()
#we will be growing here as well soon! although this is not enough for now
