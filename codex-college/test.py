import requests
import time

url = 'http://13.234.21.143:8081/'


data = {'code':'''for i in range(100000): print(i)'''}
a = time.time()
res = requests.post(url+'python3', json=data)
# for i in range(100000): print(i)
print(time.time()-a)
# print(res.text)