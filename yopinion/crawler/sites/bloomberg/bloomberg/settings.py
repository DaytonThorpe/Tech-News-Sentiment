# -*- coding: utf-8 -*-

# Scrapy settings for bloomberg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bloomberg'

SPIDER_MODULES = ['bloomberg.spiders']
NEWSPIDER_MODULE = 'bloomberg.spiders'

ITEM_PIPELINES = {
    'bloomberg.pipelines.BloombergPipeline': 1000,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bloomberg (+http://www.yourdomain.com)'
