import scrapy

# todo: //a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href

## >> titulo solo //h1[@class="documentFirstHeading"]/text()
## >  paragraph : //div[contains(@class, "field-item")]/p[not(child::strong and child::i) and not(@class)]/text()

class CiaSpider(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections',
    ]
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 30,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFIFY_MAIL': ['robert.rivera@outlook.com'],
        'ROBOTSTXT_OBE': True,
        'USER_AGENT': 'RobertoUR',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    
    
    def parse(self, response):
        links_declassified = response.xpath('//a[starts-with(@href, "collection") and (parent::p|parent::h2)]/@href').getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})
            
            
    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath('//div[contains(@class, "field-item")]/p[not(child::strong and child::i) and not(@class)]/text()').getall()
        #img =  response.xpath('//div[@class="field-item even"]//img[not(@class)]/@src').get()
        yield {
            'url': link,
            'title': title,
            'body': paragraph,
         #   'imagenes': img,
        }