import requests

url = 'http://127.0.0.1:8000/unforge/python3/testcase'

data = {'code':'''print("Hello World")''', 'testcase_id':3, 's_testcase_id':2}
res = requests.post(url, json=data)
print(res)
print(res.text)