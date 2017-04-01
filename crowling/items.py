# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
ここに欲しい情報を定義する
例えば、
store_name = scrapy.Field()
area = scrapy.Field()
など
'''
class CrowlingItem(scrapy.Item):
    # define the fields for your item here like:
    coin_name = scrapy.Field()
    coin_price = scrapy.Field()
    coin_pic = scrapy.Field()
    fin_date = scrapy.Field()
    pay_count = scrapy.Field()
