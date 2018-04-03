from bs4 import BeautifulSoup
import regex as re
from pyquery import PyQuery as pq
from HtmlDownloader import HtmlDownloader



class HtmlParser(object):
	def __init__(self):
		self.downloader = HtmlDownloader()

	def get_all_patents_info(self,url_cont):
		html = self.downloader.download(url_cont)
		text = pq(html).text()
		soup = BeautifulSoup(html, 'html5lib')
		Patent_name = soup.find('font', size="+1").text.strip().lower()
		Patent_num = int(soup.select('body > table:nth-of-type(1) > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > b')[
			0].text.strip())
		Description = soup.find_all('i', text="Description")[0].text
		Patent_description = re.findall(r"(?<=%s)[\w\W]*?(?=\* \* \* \* \*)" % Description, text)[0]
		# Patent_abstract = soup.select('body > p:nth-of-type(2)')[0].text.strip()
		# Patent_claim = re.findall(r"(?<=Claims)[\w\W]*?(?=Description)", text)[0].replace("\n", "").replace('  ', '')
		pat_dict = {
			'Patent_name': Patent_name,
			'Patent_num': Patent_num,
			# 'Patent_text':text,
			# 'Patent_claim':Patent_claim,
			'Patent_description': Patent_description,
			'Patent_url':url_cont,
		}
		print(pat_dict)
		return pat_dict
		#patents_texts.insert_one(dict)

'''
initial_url = "http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool." \
              "html&r=1&f=G&l=50&co1=AND&d=PG01&s1=%22seal+structure%22&OS=%22seal+structure%22&RS=%22seal+structure%22"

a = HtmlParser()
a.get_all_patents_info(initial_url)
'''







