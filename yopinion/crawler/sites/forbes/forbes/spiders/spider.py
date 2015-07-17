# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from forbes.items import ForbesItem
from bs4 import BeautifulSoup

class ForbesSpider(CrawlSpider):
    name = "forbes"
    allowed_domains = ["www.forbes.com"]
    start_urls = ["http://www.forbes.com/"]

    rules = (
        # Rule(LinkExtractor(allow=('http://www.forbes.com/$', )), follow=True),
        Rule(LinkExtractor(allow=(r'sites/.*/[0-9]', ), deny=(r'\?commentId='), ), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=(r'sites/.*/$', ), deny=(r'\?commentId='),), follow=True),
    )

    def parse_article(self, response):
        print('----------- parsing : ',response.url)
        try:
            item = ForbesItem()
            item['title'] = response.selector.xpath("//h1[@itemprop='headline']/text()").extract()[0]
            item['date'] = response.selector.xpath("//time[@itemprop='datePublished']/text()").extract()[0]
            item['author'] = response.selector.xpath("//span[@itemprop='author']/text()").extract()[0]
            rawBody = response.selector.xpath("//*[@class='body_inner']").extract()[0]
            soup = BeautifulSoup(rawBody)
            item['body'] = soup.get_text()
            item['url'] = str(response.request.url)
            yield item
        except:
            print 'except'
