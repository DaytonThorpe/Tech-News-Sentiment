# -*- coding: utf-8 -*-
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bloomberg.items import BloombergItem
from bs4 import BeautifulSoup

class BloombergSpider(CrawlSpider):
    name = "bloomberg"
    allowed_domains = ["www.bloomberg.com"]
    start_urls = ["http://www.bloomberg.com/"]

    rules = (
        Rule(LinkExtractor(allow=(r'.*/news/articles/[1-2][0-9][0-9]{2}(-[0-3][0-9]){2}/.*', ), ), callback='parse_article', follow=True),
        Rule(LinkExtractor(allow=(r'authors/.*', ), ), follow=True),
    )

    def parse_article(self, response):
        print('----------- parsing : ',response.url)
        try:
            item = BloombergItem()
            item['title'] = response.selector.xpath("//title/text()").extract()[0]
            item['date'] = response.selector.xpath("//time[@itemprop='datePublished']/@datetime").extract()[0]
            author = response.selector.xpath("//a[@itemprop='author']/text()").extract()
            if not author:
                author = response.selector.xpath("//a[starts-with(@href, 'mailto:')]/text()").extract()
            if not author:
                author = 'Bloomberg News'
            item['author'] = author
            rawBody = response.selector.xpath("//section[@itemprop='articleBody']").extract()[0]
            soup = BeautifulSoup(rawBody)
            item['body'] = soup.get_text()
            item['url'] = str(response.request.url)
            yield item
        except:
            print 'except'
