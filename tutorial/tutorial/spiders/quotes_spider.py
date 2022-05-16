import scrapy

#titulo = //h1/a/text()
#citas = //span[@class="text" and @itemprop="text"]/text()
#top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
#next link = //ul[@class="pager"]//li[@class="next"]/a/@href
#authors: //div[contains(@class, "col-md-8")]//div[@class="quote"]//small[@class="author"]/text()


class QuotesSpider(scrapy.Spider):
    """
    It's a spider that scrapes quotes from the quotes.toscrape.com website, and stores the scraped data
    in the quotes.json file
    """
    
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 30,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFIFY_MAIL': ['robert.rivera@outlook.com'],
        'ROBOTSTXT_OBE': True,
        'USER_AGENT': 'RobertoUR',
        'FEED_EXPORT_ENCODING': 'utf-8',
        
    }
    
    
    
    def parse_only_quotes(self, response, **kwargs):
        """
        We are using the cb_kwargs argument to pass the quotes and author_name lists to the next page
        
        :param response: The response object that was returned from the URL request
        """
       
        if kwargs:
            quotes = kwargs['quotes']
            author_name = kwargs['autores']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        author_name.extend(response.xpath('//div[contains(@class, "col-md-8")]//div[@class="quote"]//small[@class="author"]/text()').getall())
        get_next_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if get_next_link:
            yield response.follow(get_next_link, callback=self.parse_only_quotes, cb_kwargs= {'quotes': quotes, 'autores': author_name})
        else:
            yield {
                'quotes': quotes,
                'autores': author_name,
            }
            
            
            
    def parse(self, response):
        """
        We are getting the title, quotes, authors and top ten tags from the current page, and then we are
        getting the next page link and passing it to the parse function
        
        :param response: The response object that was returned from the URL request
        """
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        author_name = response.xpath('//div[contains(@class, "col-md-8")]//div[@class="quote"]//small[@class="author"]/text()').getall()
        
        # It's getting the top argument from the command line, and if it's passed, it's converting it
        # to an integer, and then it's slicing the top_tags list to the top argument
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]
        
        yield {
            'Titulo': title,
            'Autores': author_name,
            'Top 10 Citas':    top_tags,
        }
            
        get_next_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if get_next_link:
            yield response.follow(get_next_link, callback=self.parse_only_quotes, cb_kwargs= {'quotes': quotes, 'autores': author_name})