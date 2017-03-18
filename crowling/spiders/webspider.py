# -*- coding: utf-8 -*-
import scrapy
import re
from crowling.items import CrowlingItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

'''
まずは検索結果一覧から該当するurl（個別ページ）を取得する
次ページがあれば次ページに遷移させる
'''
class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    allowed_domains = ["onsen.nifty.com"] #ドメイン指定
    start_urls = ['https://onsen.nifty.com/search/?text=&srt=n1&kkavg=0&c6=33554432'] #検索結果から行く時

    def parse(self,response):
        soup = BeautifulSoup(response.body)

        #各温泉施設のurlを取得する
        top_page = "https://onsen.nifty.com" #メインページのurl指定
        posts = soup.find_all('a', {'class':'spotOverlay'}) #いじる必要あり（クラス名を適宜変更）
        for post in posts:
            post_url = top_page + post['href']
            spider = WebspiderOnsen(post_url)
            req = scrapy.Request(url=post_url, callback=spider.parse)
            yield req
        #--ここまでで1ページのurlを取得
        #--ここから次ページがある場合にページ遷移する
        next_page = soup.find('a',{"class":"next"}) #いじる必要あり（次へボタンの情報入力）
        if 'href' not in next_page.attrs:
            yield
        #次のページがある場合
        path = top_page + next_page['href']
        next_crawl_page = scrapy.Request(path)
        yield next_crawl_page



class WebspiderOnsen(scrapy.Spider):
    name = "onsenspider"
    allowed_domains = ["onsen.nifty.com"]

    def __init__(self,post_url,*args,**kwargs):
        super(WebspiderOnsen,self).__init__(*args,**kwargs)
        self.post_url = post_url
        self.start_ulrs = ['https://onsen.nifty.com'+self.post_url]

    #辿ったサイトのどの情報を取るかを指定して、items.pyに定義した情報に入れる
    # （注意）tdタグ内の要素はtbodyタグを除いてxpathを指定する必要がある。（そのままxpathコピーすると何も取れない）
    def parse(self, response):
        i = CrowlingItem()
        i["store_name"] = response.xpath('//*[@id="data"]/div[1]/div[1]/div[1]/div/div/table//tr[1]/td/text()').extract()
        i["area"] = response.xpath('//*[@id="data"]/div[1]/div[1]/div[1]/div/div/table/tr[3]/td/text()').extract()
        i["tel_num"] = response.xpath('//*[@id="data"]/div[1]/div[1]/div[1]/div/div/table/tr[4]/td/text()').extract()
        i["hp_url"] = response.xpath('//*[@id="data"]/div[1]/div[1]/div[1]/div/div/table/tr[7]/td/a/@href').extract()
        #今回、目で確認した限り2つのHTMLパターンがあったから下記追加⇨（ワンパターンなら下記はいらない）
        if i["store_name"] == []:
            i["store_name"] = response.xpath('/html/body/section/div/div/div[1]/h1/text()').extract()
            i["area"] = response.xpath('//*[@id="secBasicInfo"]/div/ul[2]/li[1]/p[2]/text()').extract()
            i["tel_num"] = response.xpath('//*[@id="secBasicInfo"]/div/ul[2]/li[2]/p[2]/text()').extract()
            i["hp_url"] = response.xpath('//*[@id="secBasicInfo"]/div/ul[2]/li[3]/p[2]/a/@href').extract()
        return i
