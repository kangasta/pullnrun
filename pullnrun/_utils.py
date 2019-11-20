from time import time

def timestamp():
	return int(time() * 1000)

def asList(a):
	if isinstance(a, list):
		return a
	if not a:
		return []
	return [a]