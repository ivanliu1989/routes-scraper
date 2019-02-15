# -*- coding: utf-8 -*-
import scrapy


class WechatSpiderSpider(scrapy.Spider):
    name = 'wechat_spider'
    allowed_domains = ['mp.qq.com']
    start_urls = ['http://mp.qq.com/']

    def parse(self, response):
        pass
