#!/usr/bin/env python

from datetime import datetime
import hashlib
from elasticsearch import Elasticsearch
import urllib2
import json
import StringIO
import gzip

opener = urllib2.build_opener()

def getDecodedUrlContent(url):
	req = urllib2.Request(url)
	req.add_header('Origin', 'http://developer.pearson.com')
	req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
	req.add_header('Accept-Language', 'en-US,en;q=0.8')
	req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36')
	req.add_header('Accept', 'application/json')
	req.add_header('Referer', 'http://developer.pearson.com/apis/ft-education-api')
	req.add_header('Connection', 'keep-alive')
	f = opener.open(req)
	compresseddata = f.read()
	compressedstream = StringIO.StringIO(compresseddata)
	gzipper = gzip.GzipFile(fileobj=compressedstream) 
	data = gzipper.read()
	return json.loads(data)

def iterateIds():
	# for i in xrange(0, 34877, 25):
	for i in xrange(0, 50, 25):
		print 'downloading ' + str(i)
		listArticlesUrl = 'http://api.pearson.com:80/v2/ft/articles?offset=' + str(i) + '&limit=25'
		decodedJson = getDecodedUrlContent(listArticlesUrl)
		if 'status' not in decodedJson or decodedJson['status'] != 200:
			print str(i) + ' error!'
		articleList = decodedJson['results']
		if len(articleList) > 0:
			for x in articleList:
				if 'id' in x:
					curId = x['id']
					if len(curId) > 0:
						loadArticleById(curId)

def persistToElasticsearch(articleDict):
	print articleDict['headline']

def loadArticleById(articleId):
	getArticlesUrl = 'http://api.pearson.com/v2/ft/articles/' + articleId
	decodedJson = getDecodedUrlContent(getArticlesUrl)
	if decodedJson['status'] != 200 or not decodedJson['result']:
		print 'error downloading article ' + articleId
		return
	persistToElasticsearch(decodedJson['result'])

def main():
	iterateIds()
	
if __name__ == '__main__':
    main()

'''
{
  "status": 200,
  "offset": 0,
  "limit": 25,
  "count": 25,
  "total": 9657,
  "url": "/v2/ft/articles?article_date=2014-01-01+TO+2014-12-31&limit=10000",
  "results": [
    {
      "article_date": "2013-12-19T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/c91c4e66-6895-11e3-bb3e-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "Hong Kong IPOs: Mojo regained",
      "id": "cqwzPCdYEB",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzPCdYEB"
    },
    {
      "article_date": "2013-12-02T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/9fca5402-5b31-11e3-a2ba-00144feabdc0,s01=1.html",
      "contributors": [
        "Scheherazade Daneshkhu"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Rathbone CEO Andy Pomfret to step down",
      "id": "cqwzKVErpr",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzKVErpr"
    },
    {
      "article_date": "2013-12-01T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/fc58ce42-58ed-11e3-9798-00144feabdc0,s01=1.html",
      "contributors": [
        "Henry Foy"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Iveco head sees end of Europe truck pain",
      "id": "cqwzJyYkkC",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzJyYkkC"
    },
    {
      "article_date": "2013-12-13T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/ae84ca9a-63ec-11e3-b70d-00144feabdc0,s01=1.html",
      "contributors": [
        "Andy Sharman"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Brokers forecast profit uptick for UK housebuilder Bellway",
      "id": "cqwzNKn0fd",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzNKn0fd"
    },
    {
      "article_date": "2013-12-10T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/42f1d9be-6197-11e3-916e-00144feabdc0,s01=1.html",
      "contributors": [
        "Andrew Parker"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Airlines tap capital markets for aircraft financing",
      "id": "cqwzMkygYV",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzMkygYV"
    },
    {
      "article_date": "2013-12-06T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/5545dc5c-5ea7-11e3-8621-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "World Cup draw sets the field for football's big event",
      "id": "cqwzMJNs6v",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzMJNs6v"
    },
    {
      "article_date": "2013-12-18T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/b4cdd1be-6804-11e3-a905-00144feabdc0,s01=1.html",
      "contributors": [
        "Andrea Felsted"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Analysts slash M&S sales and earnings forecasts",
      "id": "cqwzP7KtVH",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzP7KtVH"
    },
    {
      "article_date": "2013-09-10T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/72e502ec-1a28-11e3-b3da-00144feab7de,s01=1.html",
      "contributors": [
        "Mark Wembridge"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Fenner calls bottom of mining trough",
      "id": "cqDYcTAdHb",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqDYcTAdHb"
    },
    {
      "article_date": "2013-12-05T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/aba11bfc-5dda-11e3-8fca-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "Slow progress for Brazil's World Cup",
      "id": "cqwzM7M2dN",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzM7M2dN"
    },
    {
      "article_date": "2013-12-04T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/e760b144-5d0c-11e3-81bd-00144feabdc0,s01=1.html",
      "contributors": [
        "Daniel Thomas"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Three trims US roaming fee to lure custom",
      "id": "cqwzKsCs0y",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzKsCs0y"
    },
    {
      "article_date": "2013-12-12T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/a60dddfc-634c-11e3-a87d-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "EADS chief calls for EU drone budget",
      "id": "cqwzNBkgfG",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzNBkgfG"
    },
    {
      "article_date": "2013-12-17T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/eaa9bd06-66a2-11e3-aa10-00144feabdc0,s01=1.html",
      "contributors": [
        "Henny Sender"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "KKR to buy KFN debt vehicle for $2.6bn",
      "id": "cqwzNpz7Pt",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzNpz7Pt"
    },
    {
      "article_date": "2013-12-04T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/fc45b5e0-5ce0-11e3-81bd-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "Osborne holds out prospect of budget surplus",
      "id": "cqwzKv2Sxm",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzKv2Sxm"
    },
    {
      "article_date": "2013-11-14T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/4918aed4-4d52-11e3-bf32-00144feabdc0,s01=1.html",
      "contributors": [
        "Andrea Felsted"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "BHS threatens move into sale of food at 150 stores",
      "id": "cqaJGGJQWq",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqaJGGJQWq"
    },
    {
      "article_date": "2013-10-25T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/c704aa3e-3c89-11e3-86ef-00144feab7de,s01=1.html",
      "contributors": [
        "Tom Robbins"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Short cuts: Heston Blumenthal in a food festival in Italy; Toronto's $130m indoor aquarium",
      "id": "cqaJCXgyCZ",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqaJCXgyCZ"
    },
    {
      "article_date": "2013-11-18T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/c6b12d8a-5022-11e3-befe-00144feabdc0,s01=1.html",
      "contributors": [
        "Andy Sharman"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Aberdeen plans to take on US asset managers",
      "id": "cqaJGhmbKM",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqaJGhmbKM"
    },
    {
      "article_date": "2013-09-01T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/688c596e-118e-11e3-a14c-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "UK manufacturing output and orders at highest in three years",
      "id": "cqDYZVjwdv",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqDYZVjwdv"
    },
    {
      "article_date": "2013-11-15T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/8a16c848-4e25-11e3-8fa5-00144feabdc0,s01=1.html",
      "contributors": [
        "Bryce Elder"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Small-cap week, November 16",
      "id": "cqaJGXfQzw",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqaJGXfQzw"
    },
    {
      "article_date": "2013-11-04T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/a0add572-453a-11e3-997c-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "Q&A: What next for Co-op Bank retail bondholders?",
      "id": "cqaJE39HS4",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqaJE39HS4"
    },
    {
      "article_date": "2013-12-16T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/ea350fc6-662d-11e3-aa10-00144feabdc0,s01=1.html",
      "contributors": [
        "Jamie Chisholm"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Don't bet on rising food prices in 2014",
      "id": "cqwzNfrKcj",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzNfrKcj"
    },
    {
      "article_date": "2013-11-07T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/2db31af8-4771-11e3-9398-00144feabdc0,s01=1.html",
      "contributors": [
        "Chris Bryant"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "Siemens launches €4bn share buyback",
      "id": "cqaJEewJtS",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqaJEewJtS"
    },
    {
      "article_date": "2013-12-10T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/82510850-616a-11e3-916e-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "Mandela memorial: Thousands pay tribute at Soweto service",
      "id": "cqwzMjhy09",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzMjhy09"
    },
    {
      "article_date": "2013-12-15T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/e6cf1678-6548-11e3-a27d-00144feabdc0,s01=1.html",
      "contributors": [
        "James Crabtree"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "BofA unit chief predicts Indian IPO market to reopen next year",
      "id": "cqwzNW2D0j",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzNW2D0j"
    },
    {
      "article_date": "2013-12-10T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/82510850-616a-11e3-916e-00144feabdc0,s01=1.html",
      "datasets": [
        "articles"
      ],
      "headline": "Mandela memorial: Thousands pay tribute at Soweto service",
      "id": "cqwzMhe4kW",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzMhe4kW"
    },
    {
      "article_date": "2013-12-11T00:00:00Z",
      "article_url": "http://www.ft.com/cms/s/01d6e628-6227-11e3-bba5-00144feabdc0,s01=1.html",
      "contributors": [
        "James Politi"
      ],
      "datasets": [
        "articles"
      ],
      "headline": "US budget deal: What does it add up to?",
      "id": "cqwzMw1znp",
      "source": "FT.com site",
      "url": "/v2/ft/articles/cqwzMw1znp"
    }
  ]
}





title = ''.join([i if ord(i) < 128 else ' ' for i in itemDict['title']])
        author = ''.join([i if ord(i) < 128 else ' ' for i in itemDict['author']])
        date = ''.join([i if ord(i) < 128 else ' ' for i in itemDict['date']])
        hashKey = str(title) + str(author) + str(date)
        docId = hashlib.sha224(hashKey).hexdigest()
        try:
            itemDict['timestamp'] = datetime.strptime(date, "%Y-%m-%d %H:%M:%S\"")
        except ValueError:
            itemDict['timestamp'] = datetime.utcfromtimestamp(0)
        # self.es.index(index=item['author'].replace(' ', '-').replace('.', '').lower(), doc_type="article", body=dict(item))
        self.es.index(index="techcrunch", doc_type="article", id=docId, body=itemDict)


'''