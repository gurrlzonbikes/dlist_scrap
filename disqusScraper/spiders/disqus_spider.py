__author__ = 'Tual'
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup
import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.item import Item, Field
import re

class disqusItem(Item):
    title = Field()
    name = Field()
    message = Field()

class DisqusSpider(CrawlSpider):
    name = "disqus"
    allowed_domains = ["dlisted.com"]
    start_urls = [
        "http://dlisted.com/2015/"
    ]
    rules = (Rule(SgmlLinkExtractor(allow="[0-9]+\/[0-9]+"), callback='parse_url', follow=True), )

    def parse_url(self, response):
        disqus_url = self.build_disqus_url(response)
        #pdb.set_trace()
        yield scrapy.http.Request(disqus_url, self.parse_final_object, method='GET', encoding='utf-8', priority=0, dont_filter=False)



    def build_disqus_url(self, response):
        #Complete url example:
        #http://disqus.com/embed/comments/?base=default&version=866b57a6cbb5f3ab2a4b4f4578d489f6&f=dlisted1&t_i=177027 http://dlisted.com/?p=177027&t_u=http://dlisted.com/2015/05/07/blake-lively-is-the-latest-mumbly-actress-to-join-woody-allens-next-film/
        base_url = "http://disqus.com/embed/comments/?"
        base_default = "base=default"
        disqus_version = "&version=866b57a6cbb5f3ab2a4b4f4578d489f6"
        forum = "&f=dlisted1"
        disqus_identifier = str(self.get_disqus_identifier(response))
        t_i = "&t_i=" + disqus_identifier + " http://dlisted.com/?p=" + disqus_identifier
        t_u = "&t_u=" + str(response.url)
        return str(base_url + base_default + disqus_version + forum + disqus_identifier + t_i + t_u).replace("'", "")


    def get_disqus_identifier(self, response):
        cdata_script = response.selector.xpath("/html/body/div[1]/div[1]/div/div[2]/script[1]").extract()
        try:
            cleaned = [s.split("=") for s in cdata_script[0].split(";") if "var disqus_identifier" in s]
        #eeeeew... dirty
        #exceptions.IndexError: list index out of range
            return cleaned[0][2]
        #pdb.set_trace()
        except:
            print response.url

    def parse_final_object(self, response):
        #Looking for <script type="text/json" id="disqus-threadData">
        json_data = response.selector.xpath("//script[@id='disqus-threadData']").extract()
        item = disqusItem()
        item['message'] = json_data
        return item
        #plus qu'a remove les balises <script> ici















