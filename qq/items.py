# -*- coding: utf-8 -*-
import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QQItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    hire_num = scrapy.Field()
    pos = scrapy.Field()
    date = scrapy.Field()
    duty = scrapy.Field()
    condition = scrapy.Field()
    link = scrapy.Field()

