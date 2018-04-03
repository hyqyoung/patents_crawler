from HtmlDownloader import HtmlDownloader
import requests
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient('localhost',27017)
Structure_Patents_info = client['Structure_Patents_info']
patents_infos = Structure_Patents_info['patents_infos']

class UrlManager(object):
	def __init__(self):
		self.downloader = HtmlDownloader()

	def get_all_item_info(self,url):
		'''
		获取任意一个列表页专利号、专利名称和专利URL
		:return:
		'''
		html = self.downloader.download(url)
		soup = BeautifulSoup(html, 'lxml')
		tds = soup.find_all('td')
		td_urls = [td for td in tds if td.find('a')]
		td_ = list(zip(td_urls[::2],td_urls[1::2]))
		td_urls_ = [list(i) for i in td_]
		for item in td_urls_:
			patents_info = {
					'patent_name':item[1].a.string.strip(),
					'patent_num':int(item[0].a.string),
					'patent_url':'http://appft.uspto.gov'+item[0].a.get('href')
			}
			if patents_infos.find_one({'patent_num':patents_info['patent_num']}):
				print('专利%s,%s已经在数据库中啦,不用插入了哦'%(patents_info['patent_num'],patents_info['patent_name']))
			else:
				patents_infos.insert_one(patents_info)
				print('已经把专利%s,%s插入数据库啦'%(patents_info['patent_num'],patents_info['patent_name']))


	def get_all_patents_num(self,initial_url):
		'''
		获取初始列表页上所有相关专利的数量
		:param initial_url:
		:return:
		'''
		html_first = self.downloader.download(initial_url)
		soup = BeautifulSoup(html_first, 'lxml')
		all_patents_num = int(soup.select('body > i > strong:nth-of-type(3)')[0].text)
		patents_divisor = all_patents_num//50
		patents_remainder = all_patents_num%50
		#print([patents_divisor,patents_remainder])
		return [patents_divisor, patents_remainder]

'''
initial_url = "http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2" \
			   "Fsearch-bool.html&r=0&f=S&l=50&TERM1=seal structure&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01"

a = UrlManager()
a.get_all_patents_num(initial_url)
'''
