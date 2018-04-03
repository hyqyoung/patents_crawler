from mongoengine import connect, Document, StringField, IntField, FloatField, \
    EmbeddedDocument, ListField
from mongoengine.queryset.visitor import Q
from HtmlParser import HtmlParser
import threadpool
import pymongo

connect('Structure_Patents_info', host='mongodb://localhost/Structure_Patents_info')

class Patents(Document):
	'''要查询的数据类型'''
	patent_name = StringField(max_length=32, required=True)
	patent_num = IntField(max_length=16, required=True)
	patent_url = StringField(max_length=128, required=True)

	meta = {
		'collection': 'patents_infos'
	}
class Patent_infos(Document):
	'''要插入的数据类型'''
	Patent_name = StringField(max_length=256, required=True)
	Patent_num = IntField(max_length=16, required=True)
	Patent_description = StringField(required=True)
	Patent_url = StringField(required=True)
	meta = {
		'collection': 'patents_texts'
	}

class Use_MongoEngine(object):
	def __init__(self):
		self.parser = HtmlParser()

	def add_one(self,url_cont):
		'''新增数据'''
		pat_obj = Patent_infos(
			Patent_name = self.parser.get_all_patents_info(url_cont)['Patent_name'],
			Patent_num = self.parser.get_all_patents_info(url_cont)['Patent_num'],
			Patent_description = self.parser.get_all_patents_info(url_cont)['Patent_description'],
			Patent_url = self.parser.get_all_patents_info(url_cont)['Patent_url'],
		)
		pat_obj.save()
		return pat_obj

	def get_one(self):
		'''查询一条数据'''
		return Patents.objects.first()

	def get_more_infos(self):
		'''查询patents_infos的多条数据'''
		return Patents.objects(Q(patent_num__lt=20180000000) & Q(patent_num__gt=20170000000))

	def get_more_texts(self):
		'''查询patents_texts的多条数据'''
		return Patent_infos.objects()

	def delete(self):
		''' 删除数据 '''
		# # 删除一条数据
		# rest = Student.objects.filter(sex='male').first().delete()
		# # 删除多条数据
		# rest = Student.objects.filter(sex='male').delete()
		rest = Patent_infos.objects().delete()
		return rest

	def count(self):
		rest = len(Patent_infos.objects)
		#rest = len(Patent_infos.objects(Q(patent_num__lt=20180000000) & Q(patent_num__gt=20170000000)))
		return rest

		# #运算查询
		# ne – 不等于≠
		# lt – 小于<
		# lte – 小于等于≤
		# gt – 大于>
		# gte – 大于等于 ≥
		# not – 否定一个标准的检查，需要用在其他操作符之前(e.g. Q(age__not__mod=5))
		# in – 值在 list 中
		# nin – 值不在 list 中
		# mod – value % x == y, 其中 x 和 y 为给定的值
		# all – list 里面所有的值
		# size – 数组的大小
		# exists – 存在这个值
		#
		# #字符串查询
		# exact – 字符串型字段完全匹配这个值
		# iexact – 字符串型字段完全匹配这个值（大小写敏感）
		# contains – 字符串字段包含这个值
		# icontains – 字符串字段包含这个值（大小写敏感）
		# startswith – 字符串字段由这个值开头
		# istartswith – 字符串字段由这个值开头（大小写敏感）
		# endswith – 字符串字段由这个值结尾
		# iendswith – 字符串字段由这个值结尾（大小写敏感）
		# match – 执行 $elemMatch 操作，所以你可以使用一个数组中的 document 实例


class DataOutput(object):

	def __init__(self):
		self.obj = Use_MongoEngine()

	def output_html(self):
		'''设置set去重'''
		rest_infos = self.obj.get_more_infos()
		rest_texts = self.obj.get_more_texts()
		rest_urls = set()
		'''根据查询条件获得的列表页专利信息，包括url和专利号'''
		patents_infos_urls = [item.patent_url for item in rest_infos]#详情页URL
		patents_infos_nums = [item.patent_num for item in rest_infos]#详情页专利号
		dict_infos = dict(map(lambda x,y:[x,y],patents_infos_nums,patents_infos_urls))
		'''专利详情页文档下的所有专利信息，包括url和专利号'''
		patents_texts_urls = [item.Patent_url for item in rest_texts]
		patents_texts_nums = [item.Patent_num for item in rest_texts]
		dict_texts = dict(map(lambda x,y:[x,y],patents_texts_nums, patents_texts_urls))
		# print(len(dict_infos))
		# print(len(dict_texts))
		# print(len(set(dict_infos)-set(patents_texts_nums)))
		for item in (set(dict_infos)-set(patents_texts_nums)):
			for k,v in dict_infos.items():
				if item == k:
					rest_urls.add(v)
		# print(len(rest_urls))
		'''开启线程'''#8个线程32.47分钟,16个25.59分钟
		pool = threadpool.ThreadPool(8)
		tasks = threadpool.makeRequests(self.obj.add_one, rest_urls)
		[pool.putRequest(task) for task in tasks]
		pool.wait()


'''
#实例化测试
a = DataOutput()
a.output_html()


#删除文档
a = Use_MongoEngine()
rest = a.delete()
print(rest)

#检索文档数量
a = Use_MongoEngine()
rest = a.count()
print(rest)
'''