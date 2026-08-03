import requests
import json

data=requests.get("link/of/the/api")
data=data.content
data=data.decode("utf-8")
data=json.loads(data)
print(data)
data=requests.get("link/of/the/api")
data=data.content
data=data.decode("utf-8")
data=json.loads(data)
print(data)
information={"email":"gmail@gmail.com","password":"password","username":"username","name":"name","TOKEN":"token"}
response=requests.post("link/of/the/api/post/signup/account",json=information)
print(response.status_code)
#this literally cooked me...but done
