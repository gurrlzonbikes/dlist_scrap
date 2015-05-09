__author__ = 'Tual'
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pdb
import time
import json
from scrapy.item import Item, Field

class disqusItem(Item):
    title = Field()
    name = Field()
    message = Field()

class DisqusSpider(CrawlSpider):
    name = "disqus"
    allowed_domains = ["dlisted.com", "disqus.com"]
    start_urls = [
        "http://dlisted.com/2015/"
    ]
    #restrict regex : [a-z0-9.-_]+\/[0-9]+\/[0-9]+\/[0-9]+\/[a-z-_]+\/$
    rules = (Rule(LxmlLinkExtractor(allow="[a-z0-9.-_]+\/[0-9]+\/[0-9]+\/[0-9]+\/[a-z-_]+\/$"), callback='parse_url', follow=True), )

    def parse_url(self, response):
        try:
            disqus_url = self.build_disqus_url(response)
            yield scrapy.http.Request(disqus_url, self.parse_final_object, method='GET', encoding='utf-8', priority=0, dont_filter=False)
        except IndexError:
            pass

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
        t_e = "&t_e=" + str(response.selector.xpath("//h1/a/text()").extract()[0].encode("utf-8", "xmlcharrefreplace"))
        return str(base_url + base_default + disqus_version + forum + t_i + t_u + t_e)


    def get_disqus_identifier(self, response):
        cdata_script = response.selector.xpath("/html/body/div[1]/div[1]/div/div[2]/script[1]").extract()
        try:
            cleaned = [s.split("=") for s in cdata_script[0].split(";") if "var disqus_identifier" in s]
        #eeeeew... dirty
        #exceptions.IndexError: list index out of range
            return cleaned[0][2]
        except:
            print response.url

    def parse_final_object(self, response):
        #Looking for <script type="text/json" id="disqus-threadData">
        soup = self.open_with_selenium(response.url)
        pdb.set_trace()
        #json_data = response.selector.xpath("//script[@id='disqus-threadData']/text()").extract()
        item = disqusItem()
        #item['message'] = json.loads(json_data[0])
        item['message'] = response.url
        return item

    def open_with_selenium(self, url):
        driver = webdriver.PhantomJS("/Users/Tual/PycharmProjects/disqusScraper/phantomjs-2.0.0-macosx/bin/phantomjs")
        driver.get(url)
        test = self.click_load_more(driver)
        pdb.set_trace()
        return driver.page_source

        #//*[@id="posts"]/div[3]/a

    def click_load_more(self, driver):
        click_me_button= driver.find_element_by_xpath('//div[@class="load-more"]/a[@class="btn"]')
        actions = ActionChains(driver)
        actions.click(click_me_button)
        actions.perform()
        time.sleep(8)
        while driver.find_element_by_xpath('//div[@class="load-more"]/a[@class="btn"]').size() > 0: #while div "load more" exists
            self.click_load_more(driver)
        return driver.page_source


##Using xpath with scrapy implementation

#>>> body = '<html><body><span>good</span></body></html>'
#>>> Selector(text=body).xpath('//span/text()').extract()