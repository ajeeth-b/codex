import threading
import requests
import time

def make_Req(id=-1):
	url = 'http://13.234.21.143:8081/'
	# data = {'code':'''for i in range(100000): print(i)'''}
	data = {'code':'''from time import sleep\nsleep(1)'''}
	start = time.time()
	res = requests.post(url+'python3', json=data)
	end = time.time()-start
	print(id,'###', end)
	print(res.text)

# if __name__ == "__main__":
# 	n=5
# 	process = []
# 	for i in range(1,n+1):
# 		process += [threading.Thread(target=make_Req, args=(i,))]

# 	for i in range(n):
# 		process[i].start()
# 		process[i].join()


start = time.time()
make_Req()
end = time.time()-start
print('local', end)
