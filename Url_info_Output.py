from URLManager import UrlManager,patents_infos
import pymongo
import threadpool
#initial_url = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=seal structure&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01'


class Url_info_Output(object):
	def __init__(self):
		self.urlmanager = UrlManager()

	def output_url_info(self,initial_url):
		patents_divisor = self.urlmanager.get_all_patents_num(initial_url)[0]
		patents_remainder = self.urlmanager.get_all_patents_num(initial_url)[1]
		items = [str(i) for i in range(1,patents_divisor+2)]
		htt = 'http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p='
		laa = '&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=seal structure&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01'
		urls = [htt + items[i] + laa for i in range(patents_divisor+1)]
		pool = threadpool.ThreadPool(8)
		tasks = threadpool.makeRequests(self.urlmanager.get_all_item_info,urls)
		[pool.putRequest(task) for task in tasks]
		pool.wait()



'''
#测试这个模块
initial_url = "http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2" \
			   "Fsearch-bool.html&r=0&f=S&l=50&TERM1=seal structure&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PG01"
a = Url_info_Output()
a.output_url_info(initial_url)
'''