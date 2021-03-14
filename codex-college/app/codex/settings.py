from os import getcwd, path, mkdir

BASE_MOUNTPOINT = path.join(getcwd(), 'docker_volumes')

try:
	mkdir(BASE_MOUNTPOINT)
except Exception as e:
	# print(e)
	pass


CONTAINER_TIMEOUT = 'sleep ' + str(60*2) +'s'