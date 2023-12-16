import scrapy


class PepParseItem(scrapy.Item):
    number = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
