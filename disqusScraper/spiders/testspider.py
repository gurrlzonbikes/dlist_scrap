import scrapy
from scrapy import signals
from scrapy.http import TextResponse 
from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()


class TestSpider(scrapy.Spider):
    name = "testspider"
    allowed_domains = ["dlisted.com"]
    start_urls = [
        "http://dlisted.com/2014/"
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse(self, response):
        # selenium part of the job
        self.driver.get('http://www.italki.com/entries/korean')
        while True:
            more_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "a_show_more"))
            )

            more_btn.click()


        # now scrapy should do the job
        response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        for post in response.xpath('//ul[@id="content"]/li'):
            item = ItalkiItem()
            item['title'] = post.xpath('.//a[@class="title_txt"]/text()').extract()[0]
            item['url'] = post.xpath('.//a[@class="title_txt"]/@href').extract()[0]

            yield scrapy.Request(item['url'], meta={'item': item}, callback=self.parse_post)

    def parse_post(self, response):
        item = response.meta['item']
        item["text"] = response.xpath('//div[@id="a_NMContent"]/text()').extract()
        return item