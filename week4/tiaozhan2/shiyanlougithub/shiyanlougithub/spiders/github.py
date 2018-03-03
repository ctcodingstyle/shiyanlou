# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import GithubItem


class GithubSpider(scrapy.Spider):
    name = 'github'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for github in response.css('li.col-12'):
            item = GithubItem({
                'name': github.css('div[class="d-inline-block mb-1"] h3 a::text').re_first('(\w+)'),
                'update_time':github.css('div[class="f6 text-gray mt-2"] relative-time::attr(datetime)').extract_first()
            })
            yield item
