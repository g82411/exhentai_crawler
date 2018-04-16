# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.spiders import Spider
import re
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy import log
import os
from shutil import move
class ExhentaiPipeline(object):
    
    def process_item(self, item, spider):
        return item
class ExhentaiDownloadPipeline(ImagesPipeline):
    cookies = {
            "igneous":"942c9e50d",
            "ipb_member_id":"2950929",
            "ipb_pass_hash":"a8f176f10adc6fd2273d1f6a40804aba",
            "lv":"1522650532-1523844928",
            "s":"7a35705f2",
            "sk":"nfirszmhxpxzezi6t522ahv6n76t"
        }
    def get_media_requests(self, item, info):
        image_url = item['image_urls']
        yield Request(image_url, cookies=self.cookies)

    def item_completed(self, results, item, info):
        old_image_paths = os.path.join("exhentai","media",[x['path'] for ok, x in results if ok][0])
        new_image_paths = item['image_paths']
        if not os.path.isdir(item["image_title"]):
            os.mkdir(item["image_title"])
        move(os.path.abspath(old_image_paths), new_image_paths)
        return item
