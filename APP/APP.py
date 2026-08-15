from tkinter import *
import json
import requests
import validators
import tokenGenerator

root=Tk()

email_address__=""
password__=""
username__=""
name__=""

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
    global email_address__
    global password__
    global name__
    global username__
    if "Confirmed" in response:
        TOKEN=requests.get(f"http://127.0.0.1:8000/get/token/{email}")
        TOKEN=TOKEN.content
        TOKEN=TOKEN.decode("utf-8")
        TOKEN=json.loads(TOKEN)
        email_address__=email_address__.replace(email_address__,email)
        password__=password__.replace(password__,password)
        username__=username__.replace(username__,username)
        name__=name__.replace(name__,name)
        new_window=Tk()
        root.destroy()
        root=new_window
        data={"email":email,"password":password,"username":username,"name":name,"TOKEN":TOKEN["TOKEN"]}
        send_data=requests.post("http://127.0.0.1:8000/post/signup/account",json=data)
        print(send_data.status_code)
        label=Label(root,text="Welcome!")
        label.pack()
        button=Button(root,text="Wanna write something :)?",command=lambda:CreateOpinion(root))
        button.pack()
    else:
        new_window=Tk()
        root.destroy()
        root=new_window
        label=Label(root,text="Wrong code!")
        label.pack()
    return

def LogInPage(root:Tk):
    new_window=Tk()
    root.destroy()
    root=new_window
    emailLabel=Label(root,text="Email")
    emailEntry=Entry(root)
    passwordLabel=Label(root,text="Password")
    passwordEntry=Entry(root)
    loginButton=Button(root,text="Log In!",command=lambda:LogIn(str(emailEntry.get()),str(passwordEntry.get()),root))
    emailLabel.pack()
    emailEntry.pack()
    passwordLabel.pack()
    passwordEntry.pack()
    loginButton.pack()

def LogIn(emailEntry:str,passwordEntry:str,root:Tk):
    global email_address__
    global password__
    global username__
    global name__
    information={"email":emailEntry,"password":passwordEntry}
    response=requests.post("http://127.0.0.1:8000/check/email/password",json=information)
    data=response.content
    data=data.decode("utf-8")
    data=json.loads(data)
    if data["Result"] is False:
        new_window=Tk()
        root.destroy()
        root=new_window
        labelWrong=Label(root,text="Invalid email or password")
        labelWrong.pack()
        return
    elif data["Result"] is True:
        global number
        data=requests.get(f"http://127.0.0.1:8000/username/name/{emailEntry}")
        data=data.content
        data=data.decode("utf-8")
        data=json.loads(data)
        email_address__=email_address__.replace(email_address__,emailEntry)
        password__=password__.replace(password__,passwordEntry)
        username__=username__.replace(username__,data["username"])
        name__=name__.replace(name__,data["name"])
        new_window=Tk()
        root.destroy()
        root=new_window
        label=Label(root,text="Welcome back!")
        label.pack()
        post_button=Button(root,text="Wanna write something :)?",command=lambda:CreateOpinion(root))
        post_button.pack()
        watch=Button(root,text="See content!",command=lambda:show(root,length()))
        watch.pack()
    else:
        print("Something's wrong!")

login_page=Button(root,text="Log In",command=lambda:LogInPage(root))
login_page.pack()

label=Label(root,text="or")
label.pack()

signup_page=Button(root,text="Sign Up",command=SignUpPage)
signup_page.pack()

def CreateOpinion(root:Tk):
    new_window=Tk()
    root.destroy()
    root=new_window
    text=Text(root)
    button=Button(root,text="Post!",command=lambda:postContent(root,str(text.get("1.0","end-1c"))))
    button.pack()
    text.pack()

def postContent(root:Tk,content:str):
    global email_address__
    global password__
    global username__
    global name__
    new_window=Tk()
    root.destroy()
    root=new_window
    if content=="":
        label1=Label(root,text="The content had nothing :(")
        label1.pack()
        return
    if " " in content and content.replace(" ","")=="":
        label1=Label(root,text="This content has nothing :(")
        label1.pack()
        return
    opinion={"email":email_address__,"password":password__,"username":username__,"name":name__,"content":content}
    response=requests.post("http://127.0.0.1:8000/post/opinion",json=opinion)
    data=response.content
    data=data.decode("utf-8")
    data=json.loads(data)
    if "Result" in data:
        rightLabel=Label(root,text="Sent successfully :)!")
        rightLabel.pack()
        return
    elif "Failed" in data:
        wrongLabel=Label(root,text=f"Failed :(\nYour content: {content}")
        wrongLabel.pack()
        return
    else:
        print("Something's wrong here, line 200...bro")
        return

def length():
    response=requests.get("http://127.0.0.1:8000/length/content")
    response=response.content
    response=response.decode("utf-8")
    response=json.loads(response)
    return response["Number"]

def show(root:Tk,number):
    try:
        number=int(number)
    except Exception as e:
        print("Error of numbers :(")
    if type(number) is not int:
        wrong=Tk()
        root.destroy()
        root=wrong
        label=Label(root,text=f"You can only give integer number :(\nThere's only content of from 1 to {length()}")
        label.pack()
        entry=Entry(root)
        button=Button(root,text="Find",command=lambda:show(root,entry.get()))
        entry.pack()
        button.pack()
        return
    number=int(number)
    if number>length():
        wrong=Tk()
        root.destroy()
        root=wrong
        label=Label(root,text=f"There's not so much of data there there :(\nThere's only content of from 1 to {length()}")
        label.pack()
        entry=Entry(root)
        button=Button(root,text="Find",command=lambda:show(root,entry.get()))
        entry.pack()
        button.pack()
        return
    if number<=0:
        wrong=Tk()
        root.destroy()
        root=wrong
        label=Label(root,text=f"There's not so much of data there there :(\nThere's only content of from 1 to {length()}")
        label.pack()
        entry=Entry(root)
        button=Button(root,text="Find",command=lambda:show(root,entry.get()))
        entry.pack()
        button.pack()
        return
    right=Tk()
    root.destroy()
    root=right
    response=requests.get(f"http://127.0.0.1:8000/find/content/number/{number}")
    response=response.content
    response=response.decode("utf-8")
    response=json.loads(response)
    if response["Result"]["state"] is False:
        label=Label(root,text=f"There's something wrong :(\nThere's only content of from 1 to {length()}")
        label.pack()
        entry=Entry(root)
        button=Button(root,text="Find",command=lambda:show(root,entry.get()))
        entry.pack()
        button.pack()
        return
    elif response["Result"]["state"] is True:
        response=response["Result"]
        labelFrame=Label(root,text=f"{response["name"]}\n{response["username"]}\n{response["date"]}")
        contentFrame=Label(root,text=f"\n{response["content"]}")
        entry=Entry(root)
        button=Button(root,text="Find",command=lambda:show(root,entry.get()))
        labelFrame.pack()
        contentFrame.pack()
        entry.pack()
        button.pack()
        return
    else:
        print("still something's wrong there :(")

root.mainloop()
