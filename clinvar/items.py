# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClinvarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    vid = scrapy.Field()
    significance = scrapy.Field()
    status = scrapy.Field()
    title = scrapy.Field()
    rs = scrapy.Field()
    variant_type = scrapy.Field()
    location = scrapy.Field()

