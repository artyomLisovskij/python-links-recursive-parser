import requests
from bs4 import BeautifulSoup
import redis
POOL = redis.ConnectionPool(host='myredis', port=6379, db=0)
import json


r = redis.Redis(connection_pool=POOL)

START_URL = os.getenv('START_URL', '')

r.set(START_URL, json.dumps({'status': 0, 'from': '/'}))


def recursiveUrl(url):
	new_url = ''
	if url.startswith(START_URL):
		# absolute url
		new_url = url
	else:
		# relative url?
		if url.startswith('/'):
			new_url = START_URL + url
		else:
			if url != '#' and 'vk.com' not in url and 'facebook.com' not in url and 'twitter.com' not in url and 'instagram.com' not in url:
				print('NONE - ' + url + ' at ' + json.loads(r.get(new_url).decode("utf-8"))['from'])
	if new_url != '':
		page = requests.get(new_url)
		soup = BeautifulSoup(page.text, 'html.parser')
		links = soup.find_all('a', href=True)

		temp = json.loads(r.get(new_url).decode("utf-8"))
		temp['status'] = 1
		r.set(new_url, json.dumps(temp))

		print('DONE - ' + new_url)
		for link in links:
			new_ = ''
			if link['href'].startswith(START_URL):
				# absolute url
				new_ = link['href']
			else:
				# relative url?
				if link['href'].startswith('/'):
					new_ = START_URL + link['href']
				else:
					if link['href'] != '#' and 'vk.com' not in link['href'] and 'instagram.com' not in link['href'] and 'facebook.com' not in link['href'] and 'twitter.com' not in link['href']:
						print('NONE - ' + link['href'] + ' at ' + new_url)
					continue
			if new_ != '' and not r.get(new_):
				r.set(new_, json.dumps({'status': 0, 'from': new_url}))
	for item in r.keys():
		item = item.decode("utf-8")
		temp = json.loads(r.get(item).decode("utf-8"))
		if temp['status'] == 0:
			print('NEXT - ' + item)
			recursiveUrl(item)
		else: 
			continue

recursiveUrl(START_URL)
print(r.keys())
