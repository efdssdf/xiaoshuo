# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    book_id = scrapy.Field() #id
    chapte_id = scrapy.Field() #章节id
    chapte_name = scrapy.Field() #章节名称
    content = scrapy.Field() #章节内容
