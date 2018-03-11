# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import json
from scrapy.exceptions import DropItem

class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        item['score'] = float(item['score'])
        item['summary'] = item['summary'].strip()
        #if item['score'] >= 8.0:
           #raise DropItem('movie score more than 8.0')
        #else:
        data = json.dumps(dict(item))
        self.redis.lpush('douban_movie:items', data)
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    #def close_spider(self, spider):
        #self.redis.close()
