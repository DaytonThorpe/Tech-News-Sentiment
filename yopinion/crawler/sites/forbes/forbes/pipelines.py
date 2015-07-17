# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
import hashlib
from elasticsearch import Elasticsearch

class ForbesPipeline(object):
    def __init__(self):
        self.es = Elasticsearch()

    def process_item(self, item, spider):
        itemDict = dict(item)
        title = ''.join([i if ord(i) < 128 else ' ' for i in itemDict['title']])
        author = ''.join([i if ord(i) < 128 else ' ' for i in itemDict['author']])
        date = ''.join([i if ord(i) < 128 else ' ' for i in itemDict['date']])
        hashKey = str(title) + str(author) + str(date)
        docId = hashlib.sha224(hashKey).hexdigest()
        try:
            itemDict['timestamp'] = datetime.strptime(date, "%m/%d/%Y @ %I:%M%p")
        except ValueError:
            itemDict['timestamp'] = datetime.utcfromtimestamp(0)
        # self.es.index(index=item['author'].replace(' ', '-').replace('.', '').lower(), doc_type="article", body=dict(item))
        self.es.index(index="forbes", doc_type="article", id=docId, body=itemDict)
        return item
