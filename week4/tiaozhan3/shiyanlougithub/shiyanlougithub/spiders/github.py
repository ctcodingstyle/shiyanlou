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
                'name': github.css('div[class="d-inline-block mb-1"] h3 a::text').re_first('(\S+)'),
                'update_time':github.css('div[class="f6 text-gray mt-2"] relative-time::attr(datetime)').extract_first()
            })
            #github_url = 'https://github.com' + github.css('div[class="d-inline-block mb-1"] h3 a::attr(href)').extract_first()
            github_url = 'https://github.com/shiyanlou/' + github.css('div[class="d-inline-block mb-1"] h3 a::text').re_first('(\S+)')
            request = scrapy.Request(github_url,callback=self.parse_other)
            request.meta['item'] = item
            yield request

    def parse_other(self, response):
        item = response.meta['item']
        item['commits'] = response.css('li.commits a span::text').re_first('[^\d]*(.*)[$\d]*')
        item['branches'] = response.css('ul.numbers-summary li:nth-child(2) a span::text').re_first('[^\d]*(.*)[$\d]*')
        item['releases'] = response.css('ul.numbers-summary li:nth-child(3) a span::text').re_first('[^\d]*(.*)[$\d]*')
        yield item
