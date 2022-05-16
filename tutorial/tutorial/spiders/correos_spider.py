import scrapy


class CorreosSpider(scrapy.Spider):
    name = 'correos'
    start_urls = [
        'https://www.correosdemexico.gob.mx/SSLServicios/ConsultaCP/Descarga.aspx',
    ]
    
    def parse(self, response):
        with open('correos.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
       
        
        