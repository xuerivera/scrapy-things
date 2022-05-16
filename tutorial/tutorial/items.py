import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    python_listing = scrapy.Field()
    python_tags = scrapy.Field()


# class CiaItem(scrapy.Item):
#     name = scrapy.Field()
#     titulo_completo_mio = scrapy.Field()
#     titulo_completo = scrapy.Field()


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
