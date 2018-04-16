# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from ..items import ExhentaiItem
class HentaiSpiderSpider(scrapy.Spider):
    name = 'hentai_spider'
    allowed_domains = ['exhentai.org']
    start_urls = ['http://exhentai.org/']
    def parse_img_url(self, response):
        selector = Selector(response=response)
        image_link = selector.css("#img::attr(src)").extract()[0]
        item = ExhentaiItem()
        filename = image_link.strip().split("/")[-1]
        item['image_urls'] = image_link
        item["image_paths"] = os.path.join(self.title, filename)
        item["image_title"] = self.title
        yield item
    def parse_img_link(self, response):
        selector = Selector(response=response)
        homepage_id = self.homepage_id
        page_urls = filter(lambda x: "/s/" in x, selector.css("a::attr(href)").extract())
        for url in set(page_urls):
            yield scrapy.Request(
                url=url,
                cookies=self.cookies,
                callback=self.parse_img_url
            )
    def parse_index_page(self, response):
        selector = Selector(response=response)
        title = selector.css("title::text").extract()[0]
        # os.mkdir(title.get())
        self.title = title
        homepage_id = self.homepage_id
        contain_url = "/g/"
        page_urls = filter(lambda x: contain_url in x and not "select" in x, selector.css("a::attr(href)").extract())
        for url in set(page_urls):
            yield scrapy.Request(
                url=url,
                cookies=self.cookies,
                callback=self.parse_img_link
            )
        
    def start_requests(self):
        self.cookies = {
            "igneous":"942c9e50d",
            "ipb_member_id":"2950929",
            "ipb_pass_hash":"a8f176f10adc6fd2273d1f6a40804aba",
            "lv":"1522650532-1523844928",
            "s":"7a35705f2",
            "sk":"nfirszmhxpxzezi6t522ahv6n76t"
        }

        url = "https://exhentai.org/g/1203157/19862e6383/"
        homepage_id = url.strip().split("/")[4]
        self.homepage_id = homepage_id
        yield scrapy.Request(url=url,
                            cookies=self.cookies,
                            callback=self.parse_index_page
                            )
    
