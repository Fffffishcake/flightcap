#!/usr/bin/env python3

import sys
if len(sys.argv) == 3:
	import eventlet
	import eventlet.wsgi
	eventlet.monkey_patch()

import mimetypes
import time

import httpx
from pigwig import PigWig, Response

def root(request, short=None):
	with open('index.html', 'rb') as f:
		return Response(f.read(), content_type='text/html; charset=UTF-8')

def static(request, path):
	content_type, _ = mimetypes.guess_type(path)
	try:
		with open('static/' + path, 'rb') as f:
			return Response(f.read(), content_type=content_type)
	except FileNotFoundError:
		return Response('', code=404)

def flight_capacity(request):
	date = request.query['date']

	client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0'})
	headers = {
		'Content-Type': 'application/json',
		'Origin': 'https://www.united.com',
		'X-Authorization-Api': 'bearer ' + _token(),
		'Accept-Language': 'en-US',
	}
	url = 'https://www.united.com/api/flight/upgradeListExtended?flightNumber=857&flightDate=%s&fromAirportCode=SFO' % date
	r = client.get(url, timeout=10, headers=headers)
	r.raise_for_status()
	pbts = r.json()['pbts']
	cabins = []
	for pbt in pbts:
		cabins.append({
			'name': pbt['cabin'],
			'booked': pbt['booked'],
			'capacity': pbt['capacity'],
		})
	return Response.json(cabins)

cached_token = None
cached_token_time = 0
def _token():
	global cached_token, cached_token_time
	now = time.time()
	if cached_token_time + 60 * 5 < now:
		r = httpx.get("https://www.united.com/api/token/anonymous", headers={'User-Agent': 'Mozilla/5.0'})
		r.raise_for_status()
		cached_token = r.json()['data']['token']['hash']
		cached_token_time = now
	return cached_token

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