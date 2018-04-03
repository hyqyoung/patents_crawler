from DataOutput import DataOutput,Use_MongoEngine
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from URLManager import UrlManager
from Url_info_Output import Url_info_Output
import datetime

class SpiderMan(object):
	def __init__(self):
		self.manager = UrlManager()
		self.downloader = HtmlDownloader()
		self.parser = HtmlParser()
		self.dataoutput = DataOutput()
		self.mongoengine = Use_MongoEngine()
		self.urloutput = Url_info_Output()

	def crawl(self,initial_url):
		#添加入口url
		self.urloutput.output_url_info(initial_url)
		self.dataoutput.output_html()
		self.mongoengine.count()
		print("一共抓了%s篇专利"%self.mongoengine.count())

		'''
		while(self.manager.has_new_url() and self.manager.old_url_size() < 5):
			try:

			except Exception as e:
				print("crawl failed")
		self.output.output_html()
		print(self.manager.old_urls)
		print(self.manager.new_urls)
		'''

if __name__ == "__main__":
	start = datetime.datetime.now()
	spider_man = SpiderMan()
	initial_url = "http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2" \
			   "Fsearch-bool.html&r=0&f=S&l=50&TERM1=seal structure&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01"
	spider_man.crawl(initial_url)
	end = datetime.datetime.now()
	print('程序运行时间是：', end - start)


