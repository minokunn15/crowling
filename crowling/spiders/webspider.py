# -*- coding: utf-8 -*-
import scrapy
import re
from crowling.items import CrowlingItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from selenium import webdriver

'''
まずは検索結果一覧から該当するurl（個別ページ）を取得する
次ページがあれば次ページに遷移させる
'''
class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    allowed_domains = ["aucfan.com"] #ドメイン指定
    start_urls = ['http://aucfan.com/search1/q-~b8c5c1ac/s-mix/?o=t1'] #検索結果から行く時

    def parse(self,response):
        soup = BeautifulSoup(response.body)

        #各温泉施設のurlを取得する
        top_page = "http://aucfan.com" #メインページのurl指定
        posts = soup.find_all('a', {'class':'item_title'}) #いじる必要あり（クラス名を適宜変更）
        for post in posts:
            post_url = post['href']
            spider = WebspiderOnsen(post_url)
            req = scrapy.Request(url=post_url, callback=spider.parse)
            yield req
        #--ここまでで1ページのurlを取得
        #--ここから次ページがある場合にページ遷移する
        next = soup.findAll('span',class_='next')
        next_page = next[0].find('a')
        if 'href' not in next_page.attrs:
            yield
        #次のページがある場合
        path = top_page + next_page['href']
        next_crawl_page = scrapy.Request(path)
        yield next_crawl_page



class WebspiderOnsen(scrapy.Spider):
    name = "onsenspider"
    allowed_domains = ["aucfan.com"]

    def __init__(self,post_url,*args,**kwargs):
        super(WebspiderOnsen,self).__init__(*args,**kwargs)
        self.post_url = post_url
        self.start_ulrs = ['http://aucfan.com'+self.post_url]
        self.driver = webdriver.PhantomJS()        

    #辿ったサイトのどの情報を取るかを指定して、items.pyに定義した情報に入れる
    # （注意）tdタグ内の要素はtbodyタグを除いてxpathを指定する必要がある。（そのままxpathコピーすると何も取れない）
    def parse(self, response):
        self.driver.get(response.url)
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        img_tags = soup.find('ul',class_='sliderNav').find_all('li')
        if img_tags == []:
            img_tags = soup.find_all('div',class_='sliderBlock')
        coin_name = soup.h1.text
        coin_price = soup.find('em',class_='amount').text
        fin_date = soup.find_all('dl',class_='tabContDl')[7].dd.text
        pay_count = soup.find('section',class_='marketPlaceInfoBlock').p.text[0] 
        for img in img_tags:
            i = CrowlingItem()
            i["coin_pic"] = img.img['src']
            i["coin_name"] = coin_name
            i["coin_price"] = coin_price
            i["fin_date"] = fin_date
            i["pay_count"] = pay_count
            yield i

