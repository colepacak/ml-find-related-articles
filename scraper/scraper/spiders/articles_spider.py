# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector


class ArticlesSpiderSpider(scrapy.Spider):
    name = 'articles_spider'

    def start_requests(self):
        urls = [
            'https://www.zerohedge.com/news/2018-06-05/bridgewater-we-are-bearish-almost-all-financial-assets',
            'https://www.zerohedge.com/news/2018-06-05/job-openings-soar-all-time-high-67-million'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('.page-title .field--name-title::text').extract()
        date = response.css('.submitted-datetime .field--name-created').xpath('@content').extract()
        body = response.css('.node--view-mode-full .field--name-body *::text').extract()

        bodyStr = ' '.join(body).replace('\n', '')

        for item in zip(title, date, body):
            scraped_info = {
                'title': item[0],
                'date': item[1],
                'body': bodyStr,
            }

            yield scraped_info
