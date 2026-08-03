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
#this literally cooked me...but done
