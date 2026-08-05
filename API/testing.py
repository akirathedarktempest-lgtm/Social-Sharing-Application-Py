import requests
import json

data=requests.get("http://127.0.0.1:8000/get/bool/EMAIL")
data=data.content
data=data.decode("utf-8")
data=json.loads(data)
print(data)
data=requests.get("http://127.0.0.1:8000/get/token/EMAIL")
data=data.content
data=data.decode("utf-8")
data=json.loads(data)
print(data)
information={"email":"EMAIL","password":"PASSWORD","username":"USERNAME","name":"NAME","TOKEN":data["TOKEN"]}
response=requests.post("http://127.0.0.1:8000/post/signup/account",json=information)
print(response.content)#i didn't know that the dictionary will also be GET by POST, but it actually works
print(response.status_code)
