from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from mercadolibre.items import MercadolibreItem
from time import time
import csv
import re
import string
import sys

class MercadolibreSpider(CrawlSpider):
	name = 'ml_crawler'
	allowed_domains = ["inmuebles.mercadolibre.com.mx","casa.mercadolibre.com.mx","departamento.mercadolibre.com.mx","terreno.mercadolibre.com.mx","inmueble.mercadolibre.com.mx"]
	start_urls =['http://inmuebles.mercadolibre.com.mx/*']
	rules = [
			Rule(LinkExtractor(allow=[r'.*_JM']), callback='parse_inmuebles'),
			Rule(LinkExtractor(allow=[r'.*_Desde_[0-9]+$']), callback='parse_paginacion',follow=True),
		]
	def parse_paginacion(self,response):
		item = MercadolibreItem()
		item['paginacion'] = response.url
		#yield item

	def parse_inmuebles(self, response):
		item = MercadolibreItem()
		item['titulo'] = response.xpath('//title/text()').extract()[0].encode('utf-8')
		item['url'] = response.url
		item['name'] = ' '.join([x.encode('utf-8') for x in response.xpath('//h1[@itemprop="name"]/text()').extract()]).strip()

		#Forma alterna de obtener el precio
		#response.xpath('//div[@class="product-info"]/fieldset/article[@class="price ch-price price-without-cents"]/strong/text()').extract()
		item['price'] = ' '.join([x.encode('utf-8') for x in response.xpath('//article[@class="vip-price ch-price"]/strong/text()').extract() ]).strip()
		item['main_details'] = response.xpath('//div[@class="card-section"]').extract()[0].encode('utf-8')
		try:
			item['data_holder'] = response.xpath('//div[@class="card-section"]').extract()[1].encode('utf-8')
		except:
			item['data_holder'] = ''

		try:
			item['google_map'] = response.xpath('//div[@id="sectionDynamicMap"]/noscript/img/@src').extract()
		except:
			item['google_map'] = ''
		yield item
