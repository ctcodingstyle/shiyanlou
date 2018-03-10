# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import json

class FlaskDocPipeline(object):
    #def __init__:
        #self.file = open('/home/shiyanlou/flask_doc/flask_doc/ceshi.jl', 'wb')

    def process_item(self, item, spider):
        #self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        item['text'] = re.sub('\n|\r|\t|\f|\v|[ ]{2,}', "", item['text'][0])
        item['text'] = re.sub('\<.*?\>', "", item['text'])
        data = json.dumps(dict(item))
        #self.file.write(data)
        self.redis.lpush('flask_doc:items', data)
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
