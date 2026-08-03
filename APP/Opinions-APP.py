from tkinter import *
import json
import requests
import validators

root=Tk()

def LoginPage():
    login_page=Tk()
    root.destroy()
    root=login_page

def SignUpPage():
    sign_up_page=Tk()
    root.destroy()
    root=sign_up_page
    label1=Label(root,text="Email")
    e1=Entry(root)
    label2=Label(root,text="Password")
    e2=Entry(root)
    label3=Label(root,text="Name")
    e3=Entry(root)
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
        confirmationCode=Tk()
        root.destroy()
        root=confirmationCode
        code_entry=Label(root,text="Confirmation Code")
        entry=Entry(root)
        confirmingButton=Button(root,text="Enter Code")

def ConfirmationCode(code:str,entry:str):
    if code==entry:
        response=requests.post()

login_button=Button(root,text="Login")
label_or=Label(root,text="or")
signup_page=Button(root,text="Sign Up")


root.mainloop()
#we will be growing here as well soon! although this is not enough for now
