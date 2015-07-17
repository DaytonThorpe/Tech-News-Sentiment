# -*- coding: utf-8 -*-
import scrapy

from techcrunch.items import TechcrunchItem
from bs4 import BeautifulSoup

class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]

    def start_requests(self):
        # for debugging, crawl just 1 page
        # yield self.make_requests_from_url("http://techcrunch.com/page/2/")
        for num in range(1,6923):
            yield self.make_requests_from_url("http://techcrunch.com/page/%d/" % num)
    
    def parse(self, response):
        links = response.selector.xpath("//a[starts-with(@data-omni-sm, 'gbl_river_headline')]/@href")
        for link in links:
            yield scrapy.Request(link.extract(), callback=self.parse_article)
        return

    def parse_article(self, response):
        item = TechcrunchItem()
        item['title'] = response.selector.xpath("//h1[@class='alpha tweet-title']/text()").extract()[0]
        item['date'] = response.selector.xpath("//meta[@name='sailthru.date']").extract()[0][36:-1]
        item['author'] = response.selector.xpath("//*[contains(@rel, 'author')]/text()").extract()[0]
        rawBody = response.selector.xpath("//*[@class='article-entry text']").extract()[0]
        soup = BeautifulSoup(rawBody)
        [s.extract() for s in soup('script')]
        item['body'] = soup.get_text()
        item['url'] = str(response.request.url)
        yield item
