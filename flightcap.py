#!/usr/bin/env python3

import sys
if len(sys.argv) == 3:
	import eventlet
	import eventlet.wsgi
	eventlet.monkey_patch()

import httpx
from pigwig import PigWig, Response

def root(request, short=None):
	with open('index.html', 'rb') as f:
		return Response(f.read(), content_type='text/html; charset=UTF-8')

def static(request, path):
	content_type, _ = mimetypes.guess_type(path)
	with open('static/' + path, 'rb') as f:
		return Response(f.read(), content_type=content_type)

def flight_capacity(request):
	return Response.json(3)

routes = [
	('GET', '/', root),
	('GET', '/static/<path:path>', static),
	('GET', '/flight_capacity', flight_capacity),
]

app = PigWig(routes)

def main():
	if len(sys.argv) == 3:
		addr = sys.argv[1]
		port = int(sys.argv[2])
		eventlet.wsgi.server(eventlet.listen((addr, port)), app)
	else:
		app.main()

if __name__ == '__main__':
	main()