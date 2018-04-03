import requests

class HtmlDownloader(object):
	def download(self,url):
		if url is None:
			return None
		user_agent = 'Your user_agent'
		try:
			headers = {'User-Agent': user_agent}
			r = requests.get(url, headers=headers,timeout=30)
			html = r.text
			if r.status_code == 200:
				r.encoding = 'utf-8'
				r.close
				return html
			return None
		except requests.exceptions.RequestException as e:
			print('timeout')
