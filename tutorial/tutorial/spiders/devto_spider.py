import scrapy

from scrapy.loader import ItemLoader
from tutorial.items import Product
#pyhon listing: //main[@class="articles-list"]//h2[@class="crayons-story__title"]/a/@href
#tags python: //main[@class="articles-list"]//div[@class="substories"]//a[contains(@class, "crayons-tag")]/text()'

class DevtoSpider(scrapy.Spider):
    name = 'devto'
    allowed_domains = ['https://dev.to/']
    start_urls = [
        'https://dev.to/t/python/top/infinity'
    ]
    custom_settings = {
        'FEED_URI': 'python_listing.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 30,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFIFY_MAIL': ['robert.rivera@outlook.com'],
        'ROBOTSTXT_OBE': True,
        'USER_AGENT': 'RobertoUR',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    
    
    
    
    def parse(self, response):
        
        # item = Product()
        # item['name'] = response.url
        # item['python_listing'] = response.xpath('//main[@class="articles-list"]//h2[@class="crayons-story__title"]/a/text()').getall()
        # item['python_tags'] = response.xpath('//main[@class="articles-list"]//div[@class="substories"]//a[contains(@class, "crayons-tag")]/text()').extract()
        
        
        # yield {
        #     'Python Listing': item['python_listing'],
        #     'Todas las Tags': item['python_tags']
        #     }
        
        l = ItemLoader(item=Product(), response=response)
        l.add_xpath('python_listing', '//main[@class="articles-list"]//h2[@class="crayons-story__title"]/a/text()')
        l.add_xpath('python_tags', '//main[@class="articles-list"]//div[@class="substories"]//a[contains(@class, "crayons-tag")]/text()')
        yield l.load_item()