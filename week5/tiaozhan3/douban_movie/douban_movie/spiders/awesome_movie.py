# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from douban_movie.items import MovieItem

class AwesomeMovieSpider(scrapy.spiders.CrawlSpider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
        Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/?from=subject-page',)),
        callback = "parse_page",
        follow = True),        
    )


    def parse_movie_item(self, response):
        item = MovieItem()
        item['url'] = reponse.url
        item['name'] = response.css('#content > h1 > span:nth-child(1)').extract()
        item['summary'] = response.css('#link-report > span:nth-child(1)').extract()
        item['score'] = response.css('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong').extract()
        return item

    def parse_start_url(self, response):
        yield self.parse_movie_item(response)

    def parse_page(self, response):
        yield self.parse_movie_item(response)

