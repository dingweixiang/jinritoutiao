# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JinritoutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class toutiaoItem(scrapy.Item):
    title = scrapy.Field()
    info = scrapy.Field()
    def get_insert_sql(self):
        sql = "INSERT INTO toutiao(title,info) VALUES" \
              "(%s,%s)"
        data = (self["title"],self["info"])
        return (sql,data)